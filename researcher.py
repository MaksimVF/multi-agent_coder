






import os
from typing import Dict, Any, List, Optional
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup

# Import LiteLLM for LLM integration
try:
    import litellm
    from litellm import completion
except ImportError:
    print("Warning: litellm not installed. Please install with 'pip install litellm'")

# Import base agent class
try:
    from base_llm_agent import BaseLLMAgent
except ImportError:
    print("Warning: base_llm_agent not found. Please check the file exists.")
    class BaseLLMAgent:
        pass

class Researcher(BaseLLMAgent):
    """
    Researcher Agent for web research and documentation with Weaviate integration.

    Features:
    - Web research using LLM and web scraping
    - Documentation generation
    - Information extraction
    - Source citation
    - Weaviate knowledge base population
    - Research result storage
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        memory_manager: Optional["MemoryManager"] = None,
    ):
        """
        Initialize the LLM-powered Researcher.

        Args:
            model: LLM model to use
            temperature: Creativity level for LLM
            memory_manager: Memory manager for Weaviate integration
        """
        super().__init__(model=model, temperature=temperature, memory_manager=memory_manager)

    async def research_topic(self, topic: str, depth: int = 2) -> Dict:
        """
        Research a topic using LLM and web scraping, with Weaviate integration.

        Args:
            topic: Topic to research
            depth: Research depth (1-3)

        Returns:
            Research results
        """
        # Check Weaviate for existing research
        existing_research = []
        if self.memory_manager:
            existing_research = self.memory_manager.retrieve_long_term(
                topic,
                limit=3,
                agent="researcher",
            )

        if existing_research:
            # Use existing research as context
            context = "\n\n".join(r["content"] for r in existing_research)
        else:
            context = ""

        # Generate search queries
        query_prompt = f"""Generate {depth} search queries for researching the topic: {topic}

{'Existing research context:' if context else ''}
{context}

Format: ["query1", "query2", ...]"""

        query_result = await self._call_llm(query_prompt)

        if not query_result.get("success", False):
            return {"topic": topic, "results": [], "error": query_result.get("error", "Unknown error")}

        # Extract queries
        try:
            queries = json.loads(query_result["response"].replace("'", '"'))
            if not isinstance(queries, list):
                queries = [queries]
        except json.JSONDecodeError:
            queries = [query_result["response"].strip('[]"\'')]

        # Perform web research
        research_results = []
        for query in queries[:depth]:
            search_results = await self._web_search(query)
            research_results.extend(search_results)

        # Summarize findings
        summary_prompt = f"""Summarize the following research findings about {topic}:

{json.dumps(research_results, indent=2)}

{'Existing research context:' if context else ''}
{context}

Provide a comprehensive summary with key points and insights."""

        summary_result = await self._call_llm(summary_prompt)

        research_data = {
            "topic": topic,
            "queries": queries,
            "raw_results": research_results,
            "summary": summary_result["response"] if summary_result.get("success", False) else "Could not generate summary",
            "sources": [r.get("url", "unknown") for r in research_results],
            "existing_research": [r["content"] for r in existing_research],
        }

        # Store research results in Weaviate
        if self.memory_manager:
            self.memory_manager.store_long_term(
                research_data["summary"],
                metadata={
                    "topic": topic,
                    "queries": queries,
                    "sources": research_data["sources"],
                    "type": "research",
                    "existing_research": research_data["existing_research"],
                },
                agent="researcher",
                task_id=f"research_{topic.replace(' ', '_')}",
                importance=0.9,
            )

            # Store individual sources
            for i, source in enumerate(research_results):
                self.memory_manager.store_long_term(
                    source.get("text", ""),
                    metadata={
                        "topic": topic,
                        "url": source.get("url", ""),
                        "title": source.get("title", ""),
                        "source_type": source.get("source", "web"),
                        "type": "research_source",
                        "index": i,
                    },
                    agent="researcher",
                    task_id=f"research_{topic.replace(' ', '_')}",
                    importance=0.7,
                )

        return research_data

    async def _web_search(self, query: str) -> List[Dict]:
        """Perform a web search using DuckDuckGo API."""
        try:
            # Use DuckDuckGo API for web search
            url = f"https://api.duckduckgo.com/?q={query}&format=json"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = []

                        # Extract relevant information
                        if data.get("Abstract"):
                            results.append({
                                "title": data.get("Heading", query),
                                "url": data.get("AbstractURL", ""),
                                "text": data.get("Abstract", ""),
                                "source": data.get("AbstractSource", "web"),
                            })

                        # Add related topics
                        for topic in data.get("RelatedTopics", [])[:3]:
                            if topic.get("Text"):
                                results.append({
                                    "title": topic.get("FirstURL", topic.get("Text", "")),
                                    "url": topic.get("FirstURL", ""),
                                    "text": topic.get("Text", ""),
                                    "source": "related",
                                })

                        return results
                    else:
                        return [{"error": f"Search failed with status {response.status}"}]
        except Exception as e:
            return [{"error": str(e)}]

    async def generate_documentation(self, code_data: Dict) -> Dict:
        """
        Generate documentation for code and store in Weaviate.

        Args:
            code_data: Code data to document

        Returns:
            Generated documentation
        """
        # Check Weaviate for existing documentation
        existing_docs = []
        if self.memory_manager:
            existing_docs = self.memory_manager.retrieve_long_term(
                f"documentation for {code_data.get('description', 'code')}",
                limit=2,
                agent="researcher",
            )

        context = "\n\n".join(doc["content"] for doc in existing_docs) if existing_docs else ""

        prompt = f"""Generate comprehensive documentation for the following code:

Code:
{code_data.get('code', '')}

Description:
{code_data.get('description', 'No description provided')}

{'Existing documentation context:' if context else ''}
{context}

Include:
1. Function/Class descriptions
2. Parameter explanations
3. Return value descriptions
4. Usage examples
5. Best practices"""

        result = await self._call_llm(prompt)

        doc_data = {
            "code": code_data.get("code", ""),
            "documentation": result["response"] if result.get("success", False) else "Could not generate documentation",
            "description": code_data.get("description", ""),
            "existing_docs": [doc["content"] for doc in existing_docs],
        }

        # Store documentation in Weaviate
        if self.memory_manager:
            self.memory_manager.store_long_term(
                doc_data["documentation"],
                metadata={
                    "code": code_data.get("code", ""),
                    "description": code_data.get("description", ""),
                    "type": "documentation",
                    "existing_docs": doc_data["existing_docs"],
                },
                agent="researcher",
                task_id=f"docs_{code_data.get('description', 'code').replace(' ', '_')}",
                importance=0.8,
            )

        return doc_data

    async def extract_information(self, text: str, info_type: str = "key_points") -> Dict:
        """
        Extract specific information from text and store in Weaviate.

        Args:
            text: Input text
            info_type: Type of information to extract

        Returns:
            Extracted information
        """
        # Check Weaviate for similar extractions
        similar_extractions = []
        if self.memory_manager:
            similar_extractions = self.memory_manager.retrieve_long_term(
                f"{info_type} extraction",
                limit=2,
                agent="researcher",
            )

        context = "\n\n".join(ext["content"] for ext in similar_extractions) if similar_extractions else ""

        prompt = f"""Extract {info_type} from the following text:

Text:
{text}

{'Similar extractions:' if context else ''}
{context}

Provide the information in a structured format."""

        result = await self._call_llm(prompt)

        extraction_data = {
            "text": text,
            "info_type": info_type,
            "extracted": result["response"] if result.get("success", False) else "Could not extract information",
            "similar_extractions": [ext["content"] for ext in similar_extractions],
        }

        # Store extraction in Weaviate
        if self.memory_manager:
            self.memory_manager.store_long_term(
                extraction_data["extracted"],
                metadata={
                    "original_text": text,
                    "info_type": info_type,
                    "type": "information_extraction",
                    "similar_extractions": extraction_data["similar_extractions"],
                },
                agent="researcher",
                task_id=f"extraction_{info_type.replace(' ', '_')}",
                importance=0.7,
            )

        return extraction_data

    async def generate_bibliography(self, sources: List[str]) -> Dict:
        """
        Generate a bibliography from sources and store in Weaviate.

        Args:
            sources: List of source URLs or citations

        Returns:
            Formatted bibliography
        """
        # Check Weaviate for existing bibliographies
        existing_bibs = []
        if self.memory_manager:
            existing_bibs = self.memory_manager.retrieve_long_term(
                "bibliography",
                limit=2,
                agent="researcher",
            )

        context = "\n\n".join(bib["content"] for bib in existing_bibs) if existing_bibs else ""

        sources_text = "\n".join(f"- {source}" for source in sources)
        prompt = f"""Generate a properly formatted bibliography from these sources:

{sources_text}

{'Existing bibliography examples:' if context else ''}
{context}

Format: APA style"""

        result = await self._call_llm(prompt)

        bib_data = {
            "sources": sources,
            "bibliography": result["response"] if result.get("success", False) else "Could not generate bibliography",
            "existing_examples": [bib["content"] for bib in existing_bibs],
        }

        # Store bibliography in Weaviate
        if self.memory_manager:
            self.memory_manager.store_long_term(
                bib_data["bibliography"],
                metadata={
                    "sources": sources,
                    "type": "bibliography",
                    "existing_examples": bib_data["existing_examples"],
                },
                agent="researcher",
                task_id="bibliography",
                importance=0.6,
            )

        return bib_data

    async def populate_knowledge_base(self, topics: List[str]) -> Dict:
        """
        Populate the Weaviate knowledge base with research on multiple topics.

        Args:
            topics: List of topics to research

        Returns:
            Knowledge base population results
        """
        if not self.memory_manager:
            return {"error": "Memory manager not available", "topics": topics}

        results = {}
        for topic in topics:
            research_result = await self.research_topic(topic, depth=2)
            results[topic] = research_result

            # Store topic overview in Weaviate
            self.memory_manager.store_long_term(
                research_result["summary"],
                metadata={
                    "topic": topic,
                    "queries": research_result["queries"],
                    "sources": research_result["sources"],
                    "type": "knowledge_base_topic",
                },
                agent="researcher",
                task_id=f"kb_{topic.replace(' ', '_')}",
                importance=0.9,
            )

        return {
            "topics_researched": len(topics),
            "results": results,
            "status": "completed",
        }





