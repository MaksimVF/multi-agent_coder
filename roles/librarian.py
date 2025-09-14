
import os
from typing import Dict, Any, List, Optional
from .base_role import BaseRole
import json

class LibrarianAgent(BaseRole):
    """Librarian Agent - manages knowledge and provides contextual information to other agents"""

    def __init__(self, memory_manager=None):
        super().__init__(
            name="LibrarianAgent",
            description="Manages knowledge base and provides contextual information",
            tools=["knowledge_search", "context_analysis", "knowledge_organization"]
        )
        self.memory_manager = memory_manager

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute librarian functionality based on context"""
        query = context.get("query", "")
        task_id = context.get("task_id", "unknown")
        agent = context.get("agent", "unknown")

        results = {}

        # Search for relevant information
        if query:
            results["search_results"] = await self.search_knowledge(query, task_id, agent)

        # Analyze context if available
        if "contextual_knowledge" in context:
            results["context_analysis"] = await self.analyze_context(context["contextual_knowledge"])

        # Organize knowledge if requested
        if context.get("organize_knowledge", False):
            results["organization_results"] = await self.organize_knowledge()

        return {
            "librarian_results": results,
            "status": "completed"
        }

    async def search_knowledge(self, query: str, task_id: str = "unknown", agent: str = "unknown") -> List[Dict]:
        """Search knowledge base for relevant information"""
        results = []

        # Search in long-term memory (Weaviate)
        if self.memory_manager:
            weaviate_results = self.memory_manager.retrieve_long_term(
                query=query,
                limit=10,
                agent=agent if agent != "unknown" else None,
                task_id=task_id if task_id != "unknown" else None
            )

            for result in weaviate_results:
                results.append({
                    "source": "long_term_memory",
                    "content": result["content"],
                    "metadata": result["metadata"],
                    "timestamp": result["timestamp"],
                    "relevance": self._calculate_relevance(query, result["content"])
                })

        # Search in short-term memory (Redis)
        if self.memory_manager:
            pattern = f"{task_id}:{agent}:*" if task_id != "unknown" else "*"
            keys = self.memory_manager.redis_client.keys(pattern)

            for key in keys:
                data = self.memory_manager.retrieve_short_term(key)
                if data:
                    results.append({
                        "source": "short_term_memory",
                        "content": str(data["value"]),
                        "metadata": data["metadata"],
                        "timestamp": data["timestamp"],
                        "relevance": self._calculate_relevance(query, str(data["value"]))
                    })

        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results

    async def analyze_context(self, contextual_knowledge: Dict) -> Dict[str, Any]:
        """Analyze contextual knowledge to provide insights"""
        insights = []

        # Analyze microagent knowledge
        if "microagent_knowledge" in contextual_knowledge:
            for knowledge in contextual_knowledge["microagent_knowledge"]:
                insight = {
                    "type": "microagent_insight",
                    "name": knowledge["name"],
                    "trigger": knowledge["trigger"],
                    "analysis": f"Microagent {knowledge['name']} triggered by '{knowledge['trigger']}' " \
                               f"provides relevant knowledge: {knowledge['content'][:100]}..."
                }
                insights.append(insight)

        # Analyze repo instructions
        if "repo_instructions" in contextual_knowledge:
            for instruction in contextual_knowledge["repo_instructions"]:
                insight = {
                    "type": "repo_insight",
                    "name": instruction["name"],
                    "analysis": f"Repository instruction from {instruction['name']}: " \
                               f"{instruction['content'][:100]}..."
                }
                insights.append(insight)

        return {"insights": insights}

    async def organize_knowledge(self) -> Dict[str, Any]:
        """Organize and categorize knowledge in the system"""
        organization_results = {
            "categories_created": 0,
            "knowledge_items_organized": 0,
            "status": "completed"
        }

        # In a real implementation, this would organize knowledge in Weaviate
        # For now, we'll simulate the process
        if self.memory_manager and self.memory_manager.weaviate_client:
            try:
                # This is where we would implement actual organization logic
                # For example, creating categories, tagging knowledge items, etc.
                organization_results["categories_created"] = 2
                organization_results["knowledge_items_organized"] = 15
            except Exception as e:
                organization_results["status"] = "error"
                organization_results["error"] = str(e)

        return organization_results

    def _calculate_relevance(self, query: str, content: str) -> float:
        """Calculate relevance score between query and content"""
        # Simple relevance calculation based on word overlap
        query_words = set(query.lower().split())
        content_words = set(content.lower().split())

        intersection = query_words.intersection(content_words)
        union = query_words.union(content_words)

        if not union:
            return 0.0

        # Jaccard similarity
        return len(intersection) / len(union)

    async def store_knowledge(self, content: str, metadata: Dict, task_id: str, agent: str, importance: float = 0.5) -> bool:
        """Store new knowledge in the system"""
        if not self.memory_manager:
            return False

        # Store in long-term memory
        result = self.memory_manager.store_long_term(
            content=content,
            metadata=metadata,
            task_id=task_id,
            agent=agent,
            importance=importance
        )

        return result is not None

    async def learn_from_feedback(self, feedback: Dict) -> Dict[str, Any]:
        """Learn from feedback to improve future responses"""
        # In a real implementation, this would update the knowledge base
        # based on feedback about the quality of previous responses
        return {
            "status": "feedback_processed",
            "feedback": feedback
        }
