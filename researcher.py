

import asyncio
import aiohttp
import datetime
from bs4 import BeautifulSoup
import json
import os
from pathlib import Path

class Researcher:
    def __init__(self):
        self.cache_dir = Path("research_cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.current_date = datetime.datetime(2025, 7, 28, 13, 30)  # Fixed date as per requirements

    async def fetch_url(self, url, max_length=5000):
        """Fetch a URL with caching and respecting max length."""
        try:
            # Check cache first
            cache_file = self.cache_dir / f"{hash(url)}.cache"
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)

            # Fetch from web
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        content = await response.text()
                        # Cache the result
                        with open(cache_file, 'w', encoding='utf-8') as f:
                            json.dump({
                                'content': content[:max_length],
                                'timestamp': datetime.datetime.now().isoformat()
                            }, f)
                        return {
                            'content': content[:max_length],
                            'timestamp': datetime.datetime.now().isoformat()
                        }
                    else:
                        return {'error': f"HTTP {response.status}", 'url': url}
        except Exception as e:
            return {'error': str(e), 'url': url}

    async def search_web(self, query, max_results=3):
        """Search the web for relevant information."""
        try:
            # For this implementation, we'll use a simple approach
            # In a real scenario, we might use a search API
            search_results = []

            # Simulate some common search results based on the query
            if "python" in query.lower() and "argparse" in query.lower():
                search_results.append({
                    "title": "argparse — Parser for command-line options, arguments and sub-commands",
                    "url": "https://docs.python.org/3/library/argparse.html",
                    "snippet": "The argparse module makes it easy to write user-friendly command-line interfaces."
                })
            elif "javascript" in query.lower() and "promise" in query.lower():
                search_results.append({
                    "title": "Using Promises - JavaScript | MDN",
                    "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises",
                    "snippet": "A Promise is an object representing the eventual completion or failure of an asynchronous operation."
                })
            elif "java" in query.lower() and "stream" in query.lower():
                search_results.append({
                    "title": "Package java.util.stream - Java Platform SE 8",
                    "url": "https://docs.oracle.com/javase/8/docs/api/java/util/stream/package-summary.html",
                    "snippet": "Classes for supporting functional-style operations on streams of elements."
                })
            elif "c#" in query.lower() and "async" in query.lower():
                search_results.append({
                    "title": "Asynchronous programming with async and await - C# | Microsoft Learn",
                    "url": "https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/async/",
                    "snippet": "Learn how to use async and await to write asynchronous code in C#."
                })

            # Add some general programming resources
            if len(search_results) < max_results:
                general_resources = [
                    {
                        "title": "Stack Overflow - Where Developers Learn, Share, & Build Careers",
                        "url": "https://stackoverflow.com/",
                        "snippet": "Q&A platform for developers to ask questions and share knowledge."
                    },
                    {
                        "title": "GitHub: Where the world builds software",
                        "url": "https://github.com/",
                        "snippet": "Platform for version control and collaboration on software projects."
                    },
                    {
                        "title": "Python Documentation",
                        "url": "https://docs.python.org/3/",
                        "snippet": "Official documentation for the Python programming language."
                    }
                ]

                for resource in general_resources:
                    if len(search_results) >= max_results:
                        break
                    if query.lower() in resource['title'].lower() or query.lower() in resource['snippet'].lower():
                        search_results.append(resource)

            return search_results[:max_results]

        except Exception as e:
            return [{"error": str(e)}]

    async def fetch_documentation(self, query):
        """Fetch documentation for a specific topic."""
        try:
            # For now, we'll simulate documentation fetching
            # In a real implementation, we would fetch from official documentation sites
            docs = {}

            if "python" in query.lower() and "argparse" in query.lower():
                docs = {
                    "source": "python.org",
                    "title": "argparse Documentation",
                    "url": "https://docs.python.org/3/library/argparse.html",
                    "content": """
                    The argparse module makes it easy to write user-friendly command-line interfaces.
                    The program defines what arguments it requires, and argparse will figure out how
                    to parse those out of sys.argv. The argparse module also automatically generates
                    help and usage messages and issues errors when users give the program invalid arguments.

                    Example:
                    import argparse
                    parser = argparse.ArgumentParser(description='Process some integers.')
                    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                                       help='an integer for the accumulator')
                    parser.add_argument('--sum', dest='accumulate', action='store_const',
                                       const=sum, default=max,
                                       help='sum the integers (default: find the max)')
                    args = parser.parse_args()
                    print(args.accumulate(args.integers))
                    """
                }
            elif "javascript" in query.lower() and "promise" in query.lower():
                docs = {
                    "source": "developer.mozilla.org",
                    "title": "Using Promises - JavaScript | MDN",
                    "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises",
                    "content": """
                    A Promise is an object representing the eventual completion or failure of an asynchronous operation.
                    Since most modern asynchronous APIs are based on promises, it's a good idea to understand how they work.

                    A Promise is in one of these states:
                    - pending: initial state, neither fulfilled nor rejected.
                    - fulfilled: meaning that the operation was completed successfully.
                    - rejected: meaning that the operation failed.

                    Example:
                    let myPromise = new Promise(function(resolve, reject) {
                        // "Producing Code" (May take some time)
                        resolve(); // when successful
                        reject();  // when error
                    });

                    myPromise.then(
                        function(value) { /* code if successful */ },
                        function(error) { /* code if some error */ }
                    );
                    """
                }
            else:
                # Try to find something relevant
                results = await self.search_web(f"{query} documentation")
                if results and len(results) > 0:
                    docs = {
                        "source": "web search",
                        "title": results[0]['title'],
                        "url": results[0]['url'],
                        "content": f"Found documentation: {results[0]['snippet']}. Visit {results[0]['url']} for details."
                    }

            return docs

        except Exception as e:
            return {"error": str(e)}

    async def research_optimizations(self, language, topic):
        """Research code optimizations and best practices."""
        try:
            # Simulate optimization research
            optimizations = []

            if language.lower() == "python":
                if "performance" in topic.lower():
                    optimizations.append({
                        "title": "Python Performance Tips",
                        "content": """
                        1. Use list comprehensions instead of for loops when possible
                        2. Use built-in functions and libraries (they're implemented in C)
                        3. Avoid global variables
                        4. Use generators for large datasets
                        5. Profile your code to find bottlenecks
                        """
                    })
                elif "memory" in topic.lower():
                    optimizations.append({
                        "title": "Python Memory Optimization",
                        "content": """
                        1. Use __slots__ in classes to reduce memory usage
                        2. Delete variables when they're no longer needed
                        3. Use generators instead of lists for large data
                        4. Be careful with data structures - use appropriate ones
                        """
                    })
            elif language.lower() == "javascript":
                if "performance" in topic.lower():
                    optimizations.append({
                        "title": "JavaScript Performance Tips",
                        "content": """
                        1. Minimize DOM access and manipulation
                        2. Use requestAnimationFrame for animations
                        3. Debounce expensive operations
                        4. Use Web Workers for CPU-intensive tasks
                        5. Optimize images and other assets
                        """
                    })

            # Add some general optimizations
            optimizations.append({
                "title": "General Optimization Tips",
                "content": """
                1. Profile before optimizing - find the real bottlenecks
                2. Optimize algorithms before micro-optimizations
                3. Consider trade-offs between speed, memory, and maintainability
                4. Write clear code first, then optimize if needed
                """
            })

            return optimizations

        except Exception as e:
            return [{"error": str(e)}]

    async def research_problem(self, query):
        """Research solutions to specific programming problems."""
        try:
            # Simulate problem research
            solutions = []

            if "python" in query.lower() and "memory leak" in query.lower():
                solutions.append({
                    "title": "Python Memory Leak Solutions",
                    "content": """
                    1. Check for circular references
                    2. Use weakref for caching
                    3. Avoid global variables
                    4. Use context managers for file handling
                    5. Profile memory usage with tracemalloc
                    """
                })
            elif "javascript" in query.lower() and "memory leak" in query.lower():
                solutions.append({
                    "title": "JavaScript Memory Leak Solutions",
                    "content": """
                    1. Remove event listeners when not needed
                    2. Clean up DOM references
                    3. Avoid circular references
                    4. Use weak references (WeakMap, WeakSet)
                    5. Profile with Chrome DevTools
                    """
                })

            # Add general problem solving advice
            solutions.append({
                "title": "General Problem Solving",
                "content": """
                1. Clearly define the problem
                2. Break it down into smaller parts
                3. Research similar problems
                4. Try different approaches
                5. Test thoroughly
                """
            })

            return solutions

        except Exception as e:
            return [{"error": str(e)}]

    async def get_code_examples(self, language, topic):
        """Get code examples for specific topics."""
        try:
            examples = []

            if language.lower() == "python":
                if "argparse" in topic.lower():
                    examples.append({
                        "title": "Python argparse Example",
                        "code": """
                        import argparse

                        def main():
                            parser = argparse.ArgumentParser(description='Process some integers.')
                            parser.add_argument('integers', metavar='N', type=int, nargs='+',
                                               help='an integer for the accumulator')
                            parser.add_argument('--sum', dest='accumulate', action='store_const',
                                               const=sum, default=max,
                                               help='sum the integers (default: find the max)')

                            args = parser.parse_args()
                            result = args.accumulate(args.integers)
                            print(f"Result: {result}")

                        if __name__ == "__main__":
                            main()
                        """
                    })
            elif language.lower() == "javascript":
                if "promise" in topic.lower():
                    examples.append({
                        "title": "JavaScript Promise Example",
                        "code": """
                        function fetchData(url) {
                            return new Promise((resolve, reject) => {
                                fetch(url)
                                    .then(response => {
                                        if (!response.ok) {
                                            throw new Error('Network response was not ok');
                                        }
                                        return response.json();
                                    })
                                    .then(data => resolve(data))
                                    .catch(error => reject(error));
                            });
                        }

                        // Usage
                        fetchData('https://api.example.com/data')
                            .then(data => console.log('Data received:', data))
                            .catch(error => console.error('Error:', error));
                        """
                    })

            return examples

        except Exception as e:
            return [{"error": str(e)}]

    async def handle_request(self, request):
        """Handle research requests from other agents."""
        try:
            request_type = request.get("type", "general")
            query = request.get("query", "")
            language = request.get("language", "python")
            topic = request.get("topic", "")

            if request_type == "documentation":
                return await self.fetch_documentation(query)
            elif request_type == "optimization":
                return await self.research_optimizations(language, topic)
            elif request_type == "problem":
                return await self.research_problem(query)
            elif request_type == "examples":
                return await self.get_code_examples(language, topic)
            else:
                # General web search
                return await self.search_web(query)

        except Exception as e:
            return {"error": str(e)}

