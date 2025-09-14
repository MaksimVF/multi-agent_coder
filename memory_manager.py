


import os
import json
import redis
import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

class MemoryManager:
    """
    Memory Manager for agents with Redis (short-term) and Weaviate (long-term) integration.

    Features:
    - Short-term memory in Redis (volatile, fast access)
    - Long-term memory in Weaviate (persistent, semantic search)
    - Knowledge base functionality
    - Memory consolidation and cleanup
    - Microagent knowledge integration
    - Contextual recall capabilities
    """

    def __init__(
        self,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        weaviate_url: str = "http://localhost:8080",
        weaviate_class: str = "AgentMemory",
    ):
        """
        Initialize the Memory Manager.

        Args:
            redis_host: Redis server host
            redis_port: Redis server port
            weaviate_url: Weaviate server URL
            weaviate_class: Weaviate class for memory storage
        """
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.weaviate_url = weaviate_url
        self.weaviate_class = weaviate_class

        # Initialize Redis connection
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True,
            retry_on_timeout=True,
            socket_timeout=10,
            socket_connect_timeout=10,
        )

        # Initialize Weaviate connection
        try:
            import weaviate
            self.weaviate_client = weaviate.Client(weaviate_url)
            self._setup_weaviate_schema()
        except Exception as e:
            print(f"Warning: Could not connect to Weaviate - {e}")
            self.weaviate_client = None

        # Load microagents
        self.repo_microagents = {}
        self.knowledge_microagents = {}
        self._load_microagents()

    def _setup_weaviate_schema(self) -> None:
        """Set up Weaviate schema for agent memory."""
        if not self.weaviate_client:
            return

        schema = {
            "class": self.weaviate_class,
            "properties": [
                {"name": "content", "dataType": ["text"]},
                {"name": "metadata", "dataType": ["text"]},
                {"name": "timestamp", "dataType": ["date"]},
                {"name": "agent", "dataType": ["string"]},
                {"name": "task_id", "dataType": ["string"]},
                {"name": "importance", "dataType": ["number"]},
            ],
            "vectorizer": "text2vec-transformers",
            "moduleConfig": {
                "text2vec-transformers": {
                    "poolingStrategy": "masked_mean",
                    "vectorizeClassName": False,
                }
            },
        }

        try:
            if not self.weaviate_client.schema.exists(self.weaviate_class):
                self.weaviate_client.schema.create_class(schema)
        except Exception as e:
            print(f"Warning: Could not set up Weaviate schema - {e}")

    def store_short_term(
        self,
        key: str,
        value: Any,
        expiration: int = 3600,
        metadata: Optional[Dict] = None,
    ) -> bool:
        """
        Store data in short-term memory (Redis).

        Args:
            key: Memory key
            value: Data to store
            expiration: Expiration time in seconds
            metadata: Additional metadata

        Returns:
            True if successful, False otherwise
        """
        try:
            data = {
                "value": value,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {},
            }
            self.redis_client.setex(key, expiration, json.dumps(data))
            return True
        except Exception as e:
            print(f"Error storing in Redis: {e}")
            return False

    def retrieve_short_term(self, key: str) -> Optional[Dict]:
        """
        Retrieve data from short-term memory (Redis).

        Args:
            key: Memory key

        Returns:
            Retrieved data or None if not found
        """
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            print(f"Error retrieving from Redis: {e}")
            return None

    def store_long_term(
        self,
        content: str,
        metadata: Optional[Dict] = None,
        agent: str = "unknown",
        task_id: str = "unknown",
        importance: float = 0.5,
    ) -> Optional[str]:
        """
        Store data in long-term memory (Weaviate).

        Args:
            content: Text content to store
            metadata: Additional metadata
            agent: Agent name
            task_id: Associated task ID
            importance: Importance score (0-1)

        Returns:
            Weaviate object ID or None if failed
        """
        if not self.weaviate_client:
            return None

        try:
            data = {
                "content": content,
                "metadata": json.dumps(metadata or {}),
                "timestamp": datetime.now().isoformat(),
                "agent": agent,
                "task_id": task_id,
                "importance": importance,
            }
            result = self.weaviate_client.data_object.create(
                data, self.weaviate_class
            )
            return result["id"]
        except Exception as e:
            print(f"Error storing in Weaviate: {e}")
            return None

    def retrieve_long_term(
        self,
        query: str,
        limit: int = 5,
        agent: Optional[str] = None,
        task_id: Optional[str] = None,
    ) -> List[Dict]:
        """
        Retrieve data from long-term memory (Weaviate) using semantic search.

        Args:
            query: Search query
            limit: Maximum results to return
            agent: Filter by agent name
            task_id: Filter by task ID

        Returns:
            List of retrieved memory objects
        """
        if not self.weaviate_client:
            return []

        try:
            where_filter = {}
            if agent:
                where_filter["path"] = ["agent"]
                where_filter["operator"] = "Equal"
                where_filter["valueString"] = agent

            if task_id:
                if where_filter:
                    where_filter = {"operator": "And", "operands": [where_filter]}
                task_filter = {
                    "path": ["task_id"],
                    "operator": "Equal",
                    "valueString": task_id,
                }
                where_filter["operands"].append(task_filter)

            query_result = self.weaviate_client.query.get(
                self.weaviate_class,
                ["content", "metadata", "timestamp", "agent", "task_id", "importance"],
            ).with_where(where_filter).with_near_text(
                {"concepts": [query]}
            ).with_limit(limit).do()

            return [
                {
                    "content": obj["content"],
                    "metadata": json.loads(obj["metadata"]),
                    "timestamp": obj["timestamp"],
                    "agent": obj["agent"],
                    "task_id": obj["task_id"],
                    "importance": obj["importance"],
                }
                for obj in query_result["data"]["Get"][self.weaviate_class]
            ]
        except Exception as e:
            print(f"Error retrieving from Weaviate: {e}")
            return []

    def consolidate_memory(self, task_id: str, agent: str = "unknown") -> None:
        """
        Consolidate short-term memory to long-term memory for a task.

        Args:
            task_id: Task ID to consolidate
            agent: Agent name
        """
        try:
            # Find all short-term memory keys for this task
            pattern = f"{task_id}:{agent}:*"
            keys = self.redis_client.keys(pattern)

            for key in keys:
                data = self.retrieve_short_term(key)
                if data:
                    # Store in long-term memory
                    self.store_long_term(
                        str(data["value"]),
                        metadata=data["metadata"],
                        agent=agent,
                        task_id=task_id,
                        importance=data["metadata"].get("importance", 0.5),
                    )
                    # Delete from short-term memory
                    self.redis_client.delete(key)
        except Exception as e:
            print(f"Error consolidating memory: {e}")

    def cleanup_short_term(self, max_age: int = 86400) -> int:
        """
        Clean up old short-term memory entries.

        Args:
            max_age: Maximum age in seconds

        Returns:
            Number of deleted entries
        """
        try:
            deleted = 0
            now = datetime.now()
            keys = self.redis_client.keys("*")

            for key in keys:
                data = self.retrieve_short_term(key)
                if data:
                    age = (now - datetime.fromisoformat(data["timestamp"])).total_seconds()
                    if age > max_age:
                        self.redis_client.delete(key)
                        deleted += 1
            return deleted
        except Exception as e:
            print(f"Error cleaning up Redis: {e}")
            return 0

    def get_recent_memory(
        self, agent: str, limit: int = 10, hours: int = 24
    ) -> List[Dict]:
        """
        Get recent memory entries for an agent.

        Args:
            agent: Agent name
            limit: Maximum results
            hours: Time window in hours

        Returns:
            List of recent memory entries
        """
        try:
            cutoff = datetime.now() - timedelta(hours=hours)
            pattern = f"*:{agent}:*"
            keys = self.redis_client.keys(pattern)

            results = []
            for key in keys:
                data = self.retrieve_short_term(key)
                if data:
                    timestamp = datetime.fromisoformat(data["timestamp"])
                    if timestamp >= cutoff:
                        results.append(data)
                        if len(results) >= limit:
                            break

            return results
        except Exception as e:
            print(f"Error getting recent memory: {e}")
            return []

    def _load_microagents(self) -> None:
        """Load microagents from the microagents directory."""
        try:
            # Debug: Check current working directory
            print(f"Current working directory: {os.getcwd()}")
            print(f"Microagents directory exists: {os.path.exists('microagents')}")

            # Import microagents module
            from microagents import load_microagents_from_dir, GLOBAL_MICROAGENTS_DIR, USER_MICROAGENTS_DIR

            print(f"GLOBAL_MICROAGENTS_DIR: {GLOBAL_MICROAGENTS_DIR}")
            print(f"GLOBAL_MICROAGENTS_DIR exists: {os.path.exists(GLOBAL_MICROAGENTS_DIR)}")

            # Load global microagents
            repo_agents, knowledge_agents = load_microagents_from_dir(GLOBAL_MICROAGENTS_DIR)
            print(f"Loaded {len(repo_agents)} repo agents and {len(knowledge_agents)} knowledge agents from global dir")

            self.repo_microagents.update(repo_agents)
            self.knowledge_microagents.update(knowledge_agents)

            # Load user microagents if directory exists
            if os.path.exists(USER_MICROAGENTS_DIR):
                repo_agents, knowledge_agents = load_microagents_from_dir(USER_MICROAGENTS_DIR)
                self.repo_microagents.update(repo_agents)
                self.knowledge_microagents.update(knowledge_agents)

        except Exception as e:
            print(f"Warning: Could not load microagents: {e}")
            import traceback
            traceback.print_exc()

    def find_microagent_knowledge(self, query: str) -> List[Dict]:
        """Find microagent knowledge based on a query.

        Args:
            query: The query to search for microagent triggers

        Returns:
            A list of matched microagent knowledge objects
        """
        recalled_content = []

        # Search for microagent triggers in the query
        for name, microagent in self.knowledge_microagents.items():
            trigger = microagent.match_trigger(query)
            if trigger:
                recalled_content.append({
                    "name": microagent.name,
                    "trigger": trigger,
                    "content": microagent.content,
                    "type": "knowledge"
                })

        return recalled_content

    def get_repo_instructions(self) -> List[Dict]:
        """Get repository instructions from all repo microagents.

        Returns:
            A list of repository instruction objects
        """
        instructions = []

        for name, microagent in self.repo_microagents.items():
            instructions.append({
                "name": microagent.name,
                "content": microagent.content,
                "type": "repo"
            })

        return instructions

    def recall_contextual_knowledge(self, query: str) -> Dict:
        """Recall contextual knowledge based on a query.

        Args:
            query: The query to search for relevant knowledge

        Returns:
            Dictionary with microagent knowledge and repo instructions
        """
        return {
            "microagent_knowledge": self.find_microagent_knowledge(query),
            "repo_instructions": self.get_repo_instructions()
        }

    def close(self) -> None:
        """Close all connections."""
        try:
            if hasattr(self, "redis_client"):
                self.redis_client.close()
        except Exception:
            pass

    def __del__(self):
        """Destructor to ensure connections are closed."""
        self.close()

