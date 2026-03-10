"""
============================================================
🎯 AI ENGINEER JOB ASSESSMENT - COMPLETE SOLUTION
============================================================
This file contains a realistic technical assessment for an 
AI Engineer role, along with the complete solutions.

The assessment covers 5 practical scenarios:
1. API Resilience (Retries & Backoff)
2. RAG Document Chunking
3. Conversation Memory Management
4. Asynchronous Tool Execution / Batching
5. Basic Information Retrieval (Jaccard Similarity)
============================================================
"""

import time
import asyncio
import random
from typing import List, Dict, Optional


# ============================================================
# PROBLEM 1: API RESILIENCE (RETRIES & BACKOFF)
# ============================================================
"""
Scenario: 
You are querying an LLM API that randomly fails with a RateLimitError. 
Write a decorator `retry_api_call` that retries the target function up 
to `max_retries` times. It should use exponential backoff: on attempt `i`, 
it waits `base_delay * (2 ** i)` seconds before retrying. 
If it fails after all retries, raise the final exception.
"""

class RateLimitError(Exception):
    pass

# ---- SOLUTION 1 ----
def retry_api_call(max_retries: int = 3, base_delay: float = 0.5):
    """Decorator for exponential backoff retries."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except RateLimitError as e:
                    if attempt == max_retries - 1:
                        print(f"❌ Failed after {max_retries} attempts.")
                        raise e
                    
                    delay = base_delay * (2 ** attempt)
                    print(f"⚠️ Rate limited. Retrying in {delay}s (Attempt {attempt+1}/{max_retries})...")
                    time.sleep(delay)
        return wrapper
    return decorator

# Test Problem 1
@retry_api_call(max_retries=3, base_delay=0.1)
def mock_llm_call(prompt: str) -> str:
    # Fails 60% of the time
    if random.random() < 0.6:
        raise RateLimitError("API rate limit exceeded")
    return f"Response to: {prompt}"


# ============================================================
# PROBLEM 2: RAG DOCUMENT CHUNKING
# ============================================================
"""
Scenario:
Before feeding a large document to an embedding model, it must be chunked.
Write a function `chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> List[str]`
that splits the text into chunks of `chunk_size` characters, with `chunk_overlap`
characters overlapping between consecutive chunks.
"""

# ---- SOLUTION 2 ----
def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """Splits a document into overlapping text chunks."""
    if chunk_size <= 0 or chunk_overlap >= chunk_size:
        raise ValueError("Invalid chunk parameters.")
    
    if not text:
        return []
        
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunks.append(text[start:end])
        
        # If we've reached the end of the text, stop.
        if end >= text_length:
            break
            
        start += (chunk_size - chunk_overlap)
        
    return chunks


# ============================================================
# PROBLEM 3: CONVERSATION MEMORY MANAGEMENT
# ============================================================
"""
Scenario:
LLMs have a context window limit. Create a `ChatHistory` class that manages 
a conversation buffer. It should keep a maximum of `max_messages`. 
When adding a new message exceeds this limit, the oldest message shouldn't 
just be deleted if it's the 'system' prompt; the system prompt must ALWAYS 
remain at index 0. Omit the oldest user/assistant message instead.
"""

# ---- SOLUTION 3 ----
class ChatHistory:
    def __init__(self, max_messages: int = 5):
        self.max_messages = max_messages
        self.messages: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        """Adds a message and enforces the sliding window, preserving the system prompt."""
        self.messages.append({"role": role, "content": content})
        self._trim_history()

    def _trim_history(self):
        """Trims history if it exceeds max_messages."""
        while len(self.messages) > self.max_messages:
            # Check if index 0 is a system prompt
            if self.messages[0]["role"] == "system":
                # Remove the oldest non-system message (index 1)
                if len(self.messages) > 1:
                    self.messages.pop(1)
                else:
                    break # Only system prompt remains
            else:
                # Safe to remove the oldest message at index 0
                self.messages.pop(0)

    def get_history(self) -> List[Dict[str, str]]:
        return self.messages


# ============================================================
# PROBLEM 4: ASYNCHRONOUS BATCHING
# ============================================================
"""
Scenario:
You need to process a list of user queries concurrently using the `asyncio`
framework. Write an async function `process_queries_concurrently(queries: List[str]) -> List[str]`
that passes each query to the async `mock_async_llm` and returns all the 
responses in the same order as the queries.
"""

async def mock_async_llm(query: str) -> str:
    """Mock async LLM call that takes variable time."""
    delay = random.uniform(0.1, 0.4)
    await asyncio.sleep(delay)
    return f"Processed: {query}"

# ---- SOLUTION 4 ----
async def process_queries_concurrently(queries: List[str]) -> List[str]:
    """Processes multiple queries simultaneously using asyncio.gather."""
    # Create a list of asynchronous tasks
    tasks = [mock_async_llm(query) for query in queries]
    
    # Run all tasks concurrently and wait for them to finish
    results = await asyncio.gather(*tasks)
    return results


# ============================================================
# PROBLEM 5: BASIC INFORMATION RETRIEVAL
# ============================================================
"""
Scenario:
Implement a fallback basic retrieval function without using vector embeddings.
Write a function `retrieve_relevant_doc(query: str, documents: List[str]) -> str`
that returns the single document with the highest Jaccard similarity score.
Jaccard Similarity = (Intersection of unique words) / (Union of unique words).
"""

# ---- SOLUTION 5 ----
def calculate_jaccard(str1: str, str2: str) -> float:
    """Calculates Jaccard similarity between two strings."""
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())
    
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    if union == 0:
        return 0.0
    return intersection / union

def retrieve_relevant_doc(query: str, documents: List[str]) -> Optional[str]:
    """Returns the document with the highest word overlap to the query."""
    if not documents:
        return None
        
    best_doc = None
    best_score = -1.0
    
    for doc in documents:
        score = calculate_jaccard(query, doc)
        if score > best_score:
            best_score = score
            best_doc = doc
            
    # Return best matching document (if score > 0), else a default
    if best_score > 0:
        return best_doc
    return documents[0]


# ============================================================
# RUN TESTS TO VALIDATE SOLUTIONS
# ============================================================

def run_tests():
    print("=" * 60)
    print("🚀 RUNNING ASSESSMENT SOLUTIONS TESTS")
    print("=" * 60)

    # Test 1
    print("\n--- Testing Problem 1: API Resilience ---")
    try:
        response = mock_llm_call("How does self-attention work?")
        print(f"✅ Auto-retry success: {response}")
    except RateLimitError:
        print("✅ Gracefully failed after all retries (Expected Behavior).")

    # Test 2
    print("\n--- Testing Problem 2: Document Chunking ---")
    doc_text = "ABCDEFGHIJ"
    chunks = chunk_text(doc_text, chunk_size=4, chunk_overlap=2)
    print(f"Original Text: {doc_text}")
    print(f"Chunks: {chunks}")
    assert chunks == ["ABCD", "CDEF", "EFGH", "GHIJ"], "Chunking logic failed!"
    print("✅ Document chunking is correct.")

    # Test 3
    print("\n--- Testing Problem 3: Conversation Memory ---")
    chat = ChatHistory(max_messages=3)
    chat.add_message("system", "You are an AI.")
    chat.add_message("user", "Q1")
    chat.add_message("assistant", "A1")
    chat.add_message("user", "Q2")  # This should eject Q1 to keep System
    
    history_roles = [msg["role"] for msg in chat.get_history()]
    assert history_roles == ["system", "assistant", "user"], f"Memory failed: {history_roles}"
    print(f"Current Memory Buffer: {history_roles}")
    print("✅ System prompt preservation & sliding window works.")

    # Test 4
    print("\n--- Testing Problem 4: Async Batching ---")
    queries = ["What is RAG?", "Explain LoRA", "Define Agentic Workflow"]
    results = asyncio.run(process_queries_concurrently(queries))
    for r in results:
        print(f"  {r}")
    print(f"✅ Processed {len(results)} asynchronous queries concurrently.")

    # Test 5
    print("\n--- Testing Problem 5: Search & Retrieval ---")
    docs = [
        "Python is a versatile programming language.",
        "Generative AI relies heavily on large language models.",
        "Data scientists use pandas for data analysis."
    ]
    query = "Language models define modern AI."
    best_match = retrieve_relevant_doc(query, docs)
    print(f"Query: '{query}'")
    print(f"Best Match Document: '{best_match}'")
    assert "large language models" in best_match, "Retrieval targeting failed!"
    print("✅ Semantic retrieval successfully matched the correct document.")
    
    print("\n" + "=" * 60)
    print("🎉 ALL ASSESSMENT SOLUTIONS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    # Ensure a consistent random state for deterministic tests where possible
    random.seed(42)
    run_tests()
