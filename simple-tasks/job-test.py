"""
============================================================
🎯 AI ENGINEER JOB ASSESSMENT TEST - Complete Python Tutorial
============================================================
Covers: Python Fundamentals, OOP, Data Structures, APIs,
        NLP/ML Basics, LangChain, RAG, Prompt Engineering,
        Vector DBs, Error Handling, and Real-World Scenarios.
============================================================
"""

# ============================================================
# SECTION 1: PYTHON FUNDAMENTALS
# ============================================================

print("=" * 60)
print("SECTION 1: PYTHON FUNDAMENTALS")
print("=" * 60)

# --- 1.1 Variables, Data Types & Type Hints ---
from typing import List, Dict, Optional, Tuple, Union

def demonstrate_types():
    """Basic Python types used heavily in AI engineering."""
    name: str = "GPT-4"
    version: float = 4.0
    is_multimodal: bool = True
    capabilities: List[str] = ["text", "image", "code"]
    config: Dict[str, Union[str, int]] = {"model": "gpt-4", "max_tokens": 1024}
    embedding: Optional[List[float]] = None

    print(f"Model: {name} v{version}")
    print(f"Multimodal: {is_multimodal}")
    print(f"Capabilities: {capabilities}")
    print(f"Config: {config}")
    print(f"Embedding: {embedding}")

demonstrate_types()


# --- 1.2 List/Dict Comprehensions ---
def comprehension_examples():
    """Comprehensions are common in data preprocessing."""
    words = ["Hello", "WORLD", "AI", "engineer", "Test"]

    # Lowercase all words
    lower_words = [w.lower() for w in words]
    print(f"\nLowered: {lower_words}")

    # Filter words longer than 3 chars
    long_words = [w for w in words if len(w) > 3]
    print(f"Long words: {long_words}")

    # Word -> length mapping
    word_lengths = {w: len(w) for w in words}
    print(f"Word lengths: {word_lengths}")

    # Nested: flatten a list of lists
    chunks = [["hello", "world"], ["AI", "test"]]
    flat = [word for chunk in chunks for word in chunk]
    print(f"Flattened: {flat}")

comprehension_examples()


# --- 1.3 Lambda, Map, Filter ---
def functional_examples():
    """Functional programming patterns for data pipelines."""
    scores = [0.95, 0.42, 0.78, 0.31, 0.88, 0.67]

    # Filter high-confidence scores
    high_conf = list(filter(lambda x: x > 0.7, scores))
    print(f"\nHigh confidence (>0.7): {high_conf}")

    # Normalize scores to percentages
    percentages = list(map(lambda x: round(x * 100, 1), scores))
    print(f"Percentages: {percentages}")

    # Sort documents by relevance score
    docs = [("doc1", 0.9), ("doc2", 0.3), ("doc3", 0.7)]
    sorted_docs = sorted(docs, key=lambda d: d[1], reverse=True)
    print(f"Sorted by relevance: {sorted_docs}")

functional_examples()


# --- 1.4 String Manipulation (Critical for Prompt Engineering) ---
def string_operations():
    """String ops used in prompt building and text processing."""
    template = "You are a {role}. Answer the question: {question}"
    prompt = template.format(role="helpful assistant", question="What is AI?")
    print(f"\nFormatted prompt: {prompt}")

    # f-string with expressions
    model, temp = "gpt-4", 0.7
    config_str = f"Model={model}, Temperature={temp}, Top-P={1 - temp:.1f}"
    print(f"Config: {config_str}")

    # Multiline prompt (common in AI apps)
    system_prompt = """You are an AI assistant.
Rules:
- Be concise
- Be accurate
- Cite sources""".strip()
    print(f"System prompt:\n{system_prompt}")

    # Text cleaning for preprocessing
    raw_text = "  Hello,   World!  This   has   extra   spaces.  "
    clean = " ".join(raw_text.split())
    print(f"\nCleaned text: '{clean}'")

string_operations()


# ============================================================
# SECTION 2: OBJECT-ORIENTED PROGRAMMING (OOP)
# ============================================================

print("\n" + "=" * 60)
print("SECTION 2: OBJECT-ORIENTED PROGRAMMING")
print("=" * 60)

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


# --- 2.1 Abstract Base Class for AI Models ---
class BaseLLM(ABC):
    """Abstract base class representing any LLM provider."""

    def __init__(self, model_name: str, api_key: str = "sk-test"):
        self.model_name = model_name
        self.api_key = api_key
        self._call_count = 0

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from the model."""
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in given text."""
        pass

    def get_stats(self) -> Dict[str, any]:
        return {"model": self.model_name, "calls": self._call_count}


class OpenAIModel(BaseLLM):
    """Simulated OpenAI model implementation."""

    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.7):
        super().__init__(model_name)
        self.temperature = temperature

    def generate(self, prompt: str, **kwargs) -> str:
        self._call_count += 1
        max_tokens = kwargs.get("max_tokens", 100)
        # Simulated response
        return f"[{self.model_name}] Response to: '{prompt[:30]}...' (temp={self.temperature})"

    def count_tokens(self, text: str) -> int:
        # Rough estimation: ~4 chars per token
        return len(text) // 4


class AnthropicModel(BaseLLM):
    """Simulated Anthropic Claude model."""

    def generate(self, prompt: str, **kwargs) -> str:
        self._call_count += 1
        return f"[Claude] Response to: '{prompt[:30]}...'"

    def count_tokens(self, text: str) -> int:
        return len(text) // 3


# --- 2.2 Dataclasses (Modern Python Pattern) ---
@dataclass
class ChatMessage:
    """Represents a single chat message."""
    role: str              # "system", "user", "assistant"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {"role": self.role, "content": self.content}


@dataclass
class ChatSession:
    """Manages a conversation session."""
    session_id: str
    messages: List[ChatMessage] = field(default_factory=list)
    model: Optional[BaseLLM] = None

    def add_message(self, role: str, content: str):
        self.messages.append(ChatMessage(role=role, content=content))

    def get_history(self) -> List[Dict]:
        return [msg.to_dict() for msg in self.messages]

    def get_last_n(self, n: int = 5) -> List[Dict]:
        return [msg.to_dict() for msg in self.messages[-n:]]


# Demo OOP
def demo_oop():
    print("\n--- OOP Demo ---")
    gpt = OpenAIModel("gpt-4", temperature=0.5)
    claude = AnthropicModel("claude-3")

    # Polymorphism - same interface, different implementations
    for model in [gpt, claude]:
        response = model.generate("Explain machine learning in simple terms")
        tokens = model.count_tokens("Hello world, this is a test")
        print(f"{response} | Tokens: {tokens}")

    # Chat session management
    session = ChatSession(session_id="sess-001", model=gpt)
    session.add_message("system", "You are a helpful AI assistant.")
    session.add_message("user", "What is RAG?")
    session.add_message("assistant", "RAG stands for Retrieval-Augmented Generation...")
    print(f"\nChat history: {session.get_history()}")
    print(f"Model stats: {gpt.get_stats()}")

demo_oop()


# ============================================================
# SECTION 3: ERROR HANDLING & RESILIENCE
# ============================================================

print("\n" + "=" * 60)
print("SECTION 3: ERROR HANDLING & RESILIENCE")
print("=" * 60)

import time
import random


# --- 3.1 Custom Exceptions ---
class AIEngineError(Exception):
    """Base exception for AI engine errors."""
    pass

class RateLimitError(AIEngineError):
    """Raised when API rate limit is hit."""
    def __init__(self, retry_after: float = 1.0):
        self.retry_after = retry_after
        super().__init__(f"Rate limited. Retry after {retry_after}s")

class TokenLimitError(AIEngineError):
    """Raised when token limit is exceeded."""
    def __init__(self, used: int, limit: int):
        self.used = used
        self.limit = limit
        super().__init__(f"Token limit exceeded: {used}/{limit}")

class ModelNotFoundError(AIEngineError):
    """Raised when requested model doesn't exist."""
    pass


# --- 3.2 Retry Decorator with Exponential Backoff ---
def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
    """Decorator for retrying API calls with exponential backoff."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except RateLimitError as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    print(f"  ⚠️ Rate limited (attempt {attempt + 1}/{max_retries}). "
                          f"Retrying in {delay}s...")
                    # time.sleep(delay)  # Commented out for demo speed
                except Exception as e:
                    print(f"  ❌ Unexpected error: {e}")
                    raise
            return None
        return wrapper
    return decorator


# --- 3.3 Practical Error Handling Scenario ---
@retry_with_backoff(max_retries=3, base_delay=0.5)
def call_llm_api(prompt: str, simulate_error: bool = False) -> str:
    """Simulates calling an LLM API with error handling."""
    if simulate_error and random.random() < 0.7:
        raise RateLimitError(retry_after=1.0)
    return f"Response to: {prompt}"


def demo_error_handling():
    print("\n--- Error Handling Demo ---")

    # Scenario 1: Token limit check
    def validate_prompt(prompt: str, max_tokens: int = 4096):
        estimated_tokens = len(prompt) // 4
        if estimated_tokens > max_tokens:
            raise TokenLimitError(used=estimated_tokens, limit=max_tokens)
        return True

    try:
        short_prompt = "What is AI?"
        validate_prompt(short_prompt)
        print(f"✅ Prompt '{short_prompt}' is within token limits")

        long_prompt = "x" * 20000
        validate_prompt(long_prompt)
    except TokenLimitError as e:
        print(f"⚠️ {e}")

    # Scenario 2: Retry on rate limit
    try:
        result = call_llm_api("Tell me about Python", simulate_error=True)
        print(f"✅ API call succeeded: {result}")
    except RateLimitError:
        print("❌ All retries exhausted")

    # Scenario 3: Graceful fallback
    def get_response_with_fallback(prompt: str) -> str:
        models = ["gpt-4", "gpt-3.5-turbo", "fallback-local"]
        for model in models:
            try:
                if model == "gpt-4":
                    raise ModelNotFoundError(f"Model {model} unavailable")
                return f"[{model}] Response generated"
            except ModelNotFoundError:
                print(f"  ⚠️ {model} unavailable, trying next...")
                continue
        return "Default fallback response"

    result = get_response_with_fallback("Hello")
    print(f"✅ Final response: {result}")

demo_error_handling()


# ============================================================
# SECTION 4: DATA STRUCTURES FOR AI ENGINEERING
# ============================================================

print("\n" + "=" * 60)
print("SECTION 4: DATA STRUCTURES FOR AI ENGINEERING")
print("=" * 60)

import json
import hashlib
from collections import defaultdict, Counter


# --- 4.1 Document Processing Pipeline ---
@dataclass
class Document:
    """Represents a document in a RAG system."""
    doc_id: str
    content: str
    metadata: Dict = field(default_factory=dict)
    chunks: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None

    def chunk_text(self, chunk_size: int = 200, overlap: int = 50) -> List[str]:
        """Split document into overlapping chunks."""
        self.chunks = []
        start = 0
        while start < len(self.content):
            end = start + chunk_size
            self.chunks.append(self.content[start:end])
            start += chunk_size - overlap
        return self.chunks

    def generate_id(self) -> str:
        """Generate unique ID from content hash."""
        return hashlib.md5(self.content.encode()).hexdigest()[:12]


# --- 4.2 Simple In-Memory Vector Store ---
class SimpleVectorStore:
    """
    Simulated vector store for understanding RAG concepts.
    In production, use Pinecone, Weaviate, ChromaDB, etc.
    """

    def __init__(self):
        self.documents: Dict[str, Document] = {}
        self.index: Dict[str, List[str]] = defaultdict(list)  # inverted index

    def add_document(self, doc: Document):
        self.documents[doc.doc_id] = doc
        # Build simple inverted index (keyword-based)
        words = doc.content.lower().split()
        for word in set(words):
            clean_word = word.strip(".,!?;:")
            self.index[clean_word].append(doc.doc_id)

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Simple keyword-based search (simulates vector similarity)."""
        query_words = set(query.lower().split())
        scores = Counter()

        for word in query_words:
            clean_word = word.strip(".,!?;:")
            for doc_id in self.index.get(clean_word, []):
                scores[doc_id] += 1

        # Normalize scores
        results = []
        for doc_id, count in scores.most_common(top_k):
            score = count / len(query_words) if query_words else 0
            results.append((doc_id, round(score, 3)))
        return results

    def get_document(self, doc_id: str) -> Optional[Document]:
        return self.documents.get(doc_id)


def demo_data_structures():
    print("\n--- Data Structures Demo ---")

    # Create documents
    docs = [
        Document("doc1", "Machine learning is a subset of artificial intelligence "
                         "that enables systems to learn from data automatically."),
        Document("doc2", "Natural language processing helps computers understand "
                         "human language using deep learning techniques."),
        Document("doc3", "RAG combines retrieval and generation to provide "
                         "accurate answers grounded in real documents."),
        Document("doc4", "Python is a popular programming language for AI "
                         "and machine learning development."),
    ]

    # Chunk a document
    docs[0].chunk_text(chunk_size=50, overlap=10)
    print(f"Document chunks: {docs[0].chunks}")

    # Build vector store
    store = SimpleVectorStore()
    for doc in docs:
        store.add_document(doc)

    # Search
    query = "machine learning artificial intelligence"
    results = store.search(query, top_k=3)
    print(f"\nSearch query: '{query}'")
    for doc_id, score in results:
        doc = store.get_document(doc_id)
        print(f"  📄 {doc_id} (score: {score}): {doc.content[:60]}...")

demo_data_structures()


# ============================================================
# SECTION 5: API INTERACTION PATTERNS
# ============================================================

print("\n" + "=" * 60)
print("SECTION 5: API INTERACTION PATTERNS")
print("=" * 60)

import os


# --- 5.1 Simulated OpenAI API Client ---
class MockOpenAIClient:
    """
    Simulates OpenAI API interaction patterns.
    In real code, use: from openai import OpenAI
    """

    def __init__(self, api_key: str = "sk-test-key"):
        self.api_key = api_key
        self.usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_cost": 0.0}

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> Dict:
        """Simulates chat completion API call."""

        # Token counting simulation
        prompt_tokens = sum(len(m["content"]) // 4 for m in messages)
        completion_tokens = max_tokens // 2  # Simulated

        self.usage["prompt_tokens"] += prompt_tokens
        self.usage["completion_tokens"] += completion_tokens

        # Cost estimation (GPT-4 pricing simulation)
        cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000
        self.usage["total_cost"] += cost

        user_msg = messages[-1]["content"] if messages else ""
        return {
            "id": f"chatcmpl-{hashlib.md5(user_msg.encode()).hexdigest()[:8]}",
            "model": model,
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": f"Simulated response to: {user_msg[:50]}"
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens
            }
        }

    def create_embedding(self, text: str, model: str = "text-embedding-3-small") -> List[float]:
        """Simulates embedding generation."""
        # Returns a fake 8-dimensional embedding for demo purposes
        random.seed(hash(text) % (2**32))
        return [round(random.uniform(-1, 1), 4) for _ in range(8)]


def demo_api_patterns():
    print("\n--- API Patterns Demo ---")

    client = MockOpenAIClient()

    # Build conversation messages (the standard pattern)
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant specialized in Python."},
        {"role": "user", "content": "What is the difference between a list and a tuple?"},
    ]

    response = client.chat_completion(messages, model="gpt-4", temperature=0.3)
    assistant_reply = response["choices"][0]["message"]["content"]
    print(f"Response: {assistant_reply}")
    print(f"Tokens used: {response['usage']}")

    # Multi-turn conversation
    messages.append({"role": "assistant", "content": assistant_reply})
    messages.append({"role": "user", "content": "Can you give me an example?"})
    response2 = client.chat_completion(messages)
    print(f"\nMulti-turn response: {response2['choices'][0]['message']['content']}")
    print(f"Cumulative usage: {client.usage}")

    # Embeddings
    emb = client.create_embedding("What is machine learning?")
    print(f"\nEmbedding (8-dim): {emb}")

demo_api_patterns()


# ============================================================
# SECTION 6: PROMPT ENGINEERING PATTERNS
# ============================================================

print("\n" + "=" * 60)
print("SECTION 6: PROMPT ENGINEERING")
print("=" * 60)


class PromptTemplate:
    """Reusable prompt template with variable substitution."""

    def __init__(self, template: str, required_vars: List[str] = None):
        self.template = template
        self.required_vars = required_vars or []

    def format(self, **kwargs) -> str:
        # Validate all required variables are provided
        missing = [v for v in self.required_vars if v not in kwargs]
        if missing:
            raise ValueError(f"Missing required variables: {missing}")
        return self.template.format(**kwargs)


# --- 6.1 Common Prompt Patterns ---
def demo_prompt_engineering():
    print("\n--- Prompt Engineering Demo ---")

    # Pattern 1: Zero-Shot
    zero_shot = PromptTemplate(
        "Classify the following text as POSITIVE, NEGATIVE, or NEUTRAL.\n"
        "Text: {text}\n"
        "Classification:",
        required_vars=["text"]
    )
    print("Zero-Shot Prompt:")
    print(zero_shot.format(text="I love this product! It works great."))

    # Pattern 2: Few-Shot
    few_shot = PromptTemplate(
        "Classify the sentiment of each text.\n\n"
        "Text: 'I love this!' -> POSITIVE\n"
        "Text: 'This is terrible.' -> NEGATIVE\n"
        "Text: 'It is okay.' -> NEUTRAL\n\n"
        "Text: '{text}' ->",
        required_vars=["text"]
    )
    print(f"\nFew-Shot Prompt:")
    print(few_shot.format(text="The weather is nice today"))

    # Pattern 3: Chain of Thought (CoT)
    cot_prompt = PromptTemplate(
        "Question: {question}\n\n"
        "Let's think step by step:\n"
        "1. First, identify the key concepts.\n"
        "2. Then, analyze the relationships.\n"
        "3. Finally, provide the answer.\n\n"
        "Answer:",
        required_vars=["question"]
    )
    print(f"\nChain-of-Thought Prompt:")
    print(cot_prompt.format(question="How does RAG improve LLM responses?"))

    # Pattern 4: System + User with Context (RAG Pattern)
    rag_prompt = PromptTemplate(
        "SYSTEM: You are a helpful assistant. Use ONLY the provided context "
        "to answer. If the answer is not in the context, say 'I don't know'.\n\n"
        "CONTEXT:\n{context}\n\n"
        "USER QUESTION: {question}\n\n"
        "ANSWER:",
        required_vars=["context", "question"]
    )
    print(f"\nRAG Prompt:")
    print(rag_prompt.format(
        context="Python was created by Guido van Rossum in 1991. "
                "It emphasizes code readability.",
        question="Who created Python?"
    ))

demo_prompt_engineering()


# ============================================================
# SECTION 7: RAG (RETRIEVAL-AUGMENTED GENERATION) PIPELINE
# ============================================================

print("\n" + "=" * 60)
print("SECTION 7: RAG PIPELINE SIMULATION")
print("=" * 60)


class SimpleRAGPipeline:
    """
    Complete RAG pipeline demonstration.
    Shows: Ingest -> Chunk -> Index -> Retrieve -> Generate
    """

    def __init__(self, llm_client: MockOpenAIClient):
        self.vector_store = SimpleVectorStore()
        self.llm = llm_client
        self.chunk_size = 200
        self.chunk_overlap = 50

    def ingest(self, documents: List[Dict[str, str]]):
        """Step 1: Ingest and index documents."""
        print("\n📥 Ingesting documents...")
        for i, doc_data in enumerate(documents):
            doc = Document(
                doc_id=f"doc_{i}",
                content=doc_data["content"],
                metadata={"source": doc_data.get("source", "unknown")}
            )
            doc.chunk_text(self.chunk_size, self.chunk_overlap)
            self.vector_store.add_document(doc)
            print(f"  ✅ Indexed: {doc.doc_id} ({len(doc.chunks)} chunks)")

    def retrieve(self, query: str, top_k: int = 2) -> List[str]:
        """Step 2: Retrieve relevant documents."""
        print(f"\n🔍 Retrieving for: '{query}'")
        results = self.vector_store.search(query, top_k=top_k)
        contexts = []
        for doc_id, score in results:
            doc = self.vector_store.get_document(doc_id)
            if doc:
                contexts.append(doc.content)
                print(f"  📄 {doc_id} (score: {score})")
        return contexts

    def generate(self, query: str, contexts: List[str]) -> str:
        """Step 3: Generate answer using retrieved context."""
        context_text = "\n---\n".join(contexts)
        messages = [
            {"role": "system", "content": "Answer based only on the provided context."},
            {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
        ]
        response = self.llm.chat_completion(messages, temperature=0.3)
        return response["choices"][0]["message"]["content"]

    def query(self, question: str) -> str:
        """Full RAG pipeline: Retrieve -> Generate."""
        contexts = self.retrieve(question)
        if not contexts:
            return "I couldn't find relevant information to answer your question."
        answer = self.generate(question, contexts)
        return answer


def demo_rag_pipeline():
    print("\n--- RAG Pipeline Demo ---")

    client = MockOpenAIClient()
    rag = SimpleRAGPipeline(client)

    # Ingest knowledge base
    knowledge_base = [
        {"content": "Python is a high-level programming language created by "
                    "Guido van Rossum. It supports multiple programming paradigms "
                    "including procedural, object-oriented, and functional programming.",
         "source": "python_docs"},
        {"content": "LangChain is a framework for developing applications powered "
                    "by language models. It provides tools for chains, agents, "
                    "and retrieval-augmented generation.",
         "source": "langchain_docs"},
        {"content": "Vector databases store data as high-dimensional vectors. "
                    "Popular options include Pinecone, Weaviate, ChromaDB, and "
                    "Qdrant for similarity search.",
         "source": "vector_db_guide"},
    ]

    rag.ingest(knowledge_base)

    # Query the RAG system
    questions = [
        "What is Python programming language?",
        "What is LangChain used for?",
        "Which vector databases are available?",
    ]

    for q in questions:
        answer = rag.query(q)
        print(f"\n💬 Q: {q}")
        print(f"🤖 A: {answer}\n")

demo_rag_pipeline()


# ============================================================
# SECTION 8: ASYNC PATTERNS & BATCH PROCESSING
# ============================================================

print("\n" + "=" * 60)
print("SECTION 8: ASYNC & BATCH PROCESSING")
print("=" * 60)

import asyncio
from concurrent.futures import ThreadPoolExecutor


def process_batch_sync(items: List[str], batch_size: int = 3) -> List[str]:
    """Process items in batches (synchronous version)."""
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        print(f"  Processing batch {i // batch_size + 1}: {batch}")
        # Simulate API calls
        batch_results = [f"Result for '{item}'" for item in batch]
        results.extend(batch_results)
    return results


def demo_batch_processing():
    print("\n--- Batch Processing Demo ---")
    items = ["query1", "query2", "query3", "query4", "query5", "query6", "query7"]
    results = process_batch_sync(items, batch_size=3)
    print(f"Results: {results[:3]}...")  # Show first 3

demo_batch_processing()


# ============================================================
# SECTION 9: TESTING PATTERNS FOR AI ENGINEERS
# ============================================================

print("\n" + "=" * 60)
print("SECTION 9: TESTING PATTERNS")
print("=" * 60)


def test_prompt_template():
    """Test prompt template formatting."""
    template = PromptTemplate(
        "Hello {name}, you asked: {question}",
        required_vars=["name", "question"]
    )

    # Test 1: Valid formatting
    result = template.format(name="Alice", question="What is AI?")
    assert "Alice" in result, "Name should be in prompt"
    assert "What is AI?" in result, "Question should be in prompt"
    print("✅ Test 1 passed: Prompt template formatting works")

    # Test 2: Missing variable raises error
    try:
        template.format(name="Alice")  # Missing 'question'
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "question" in str(e)
        print("✅ Test 2 passed: Missing variable raises ValueError")

    # Test 3: Token limit validation
    def validate_tokens(text: str, limit: int = 4096) -> bool:
        return len(text) // 4 <= limit

    assert validate_tokens("Hello") == True
    assert validate_tokens("x" * 20000) == False
    print("✅ Test 3 passed: Token validation works")


def test_document_chunking():
    """Test document chunking logic."""
    doc = Document("test", "A" * 500)
    chunks = doc.chunk_text(chunk_size=200, overlap=50)

    # Verify chunks were created
    assert len(chunks) > 1, "Should create multiple chunks"
    print(f"✅ Test 4 passed: Created {len(chunks)} chunks from 500 chars")

    # Verify chunk sizes
    for i, chunk in enumerate(chunks[:-1]):  # All but last
        assert len(chunk) == 200, f"Chunk {i} should be 200 chars"
    print("✅ Test 5 passed: Chunk sizes are correct")

    # Verify overlap
    if len(chunks) >= 2:
        overlap_region = chunks[0][-50:]
        assert chunks[1].startswith(overlap_region), "Chunks should overlap"
        print("✅ Test 6 passed: Chunk overlap works correctly")


def test_vector_store():
    """Test vector store search functionality."""
    store = SimpleVectorStore()
    store.add_document(Document("d1", "python programming language"))
    store.add_document(Document("d2", "javascript web development"))
    store.add_document(Document("d3", "python machine learning AI"))

    results = store.search("python", top_k=2)
    assert len(results) > 0, "Should find results"
    doc_ids = [r[0] for r in results]
    assert "d1" in doc_ids or "d3" in doc_ids, "Should find python docs"
    print("✅ Test 7 passed: Vector store search returns relevant results")


def demo_testing():
    print("\n--- Testing Demo ---")
    test_prompt_template()
    test_document_chunking()
    test_vector_store()
    print("\n🎉 All tests passed!")

demo_testing()


# ============================================================
# SECTION 10: REAL-WORLD SCENARIO QUESTIONS
# ============================================================

print("\n" + "=" * 60)
print("SECTION 10: SCENARIO-BASED QUESTIONS & ANSWERS")
print("=" * 60)

scenarios = """

📋 SCENARIO 1: Rate Limiting & API Management
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Q: Your chatbot is hitting OpenAI's rate limit during peak hours.
   How would you handle this?

A: Implement a multi-layered approach:
   1. Retry with exponential backoff (shown in Section 3)
   2. Request queuing with priority levels
   3. Response caching for repeated queries
   4. Fallback to a secondary model (e.g., GPT-3.5 if GPT-4 fails)
   5. Token budget management per user/session


📋 SCENARIO 2: RAG Quality Improvement
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Q: Your RAG system returns irrelevant documents. How do you fix it?

A: Systematic improvement approach:
   1. Improve chunking strategy (smaller chunks, semantic splitting)
   2. Use hybrid search (keyword + semantic/vector)
   3. Add metadata filtering (date, source, category)
   4. Implement re-ranking (cross-encoder models)
   5. Tune embedding model or use domain-specific embeddings
   6. Add query expansion / reformulation
   7. Evaluate with metrics: MRR, Recall@K, NDCG


📋 SCENARIO 3: Hallucination Prevention
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Q: Your LLM produces hallucinated/incorrect answers.
   What strategies would you implement?

A: Multi-layer defense:
   1. Use RAG to ground responses in real data
   2. Lower temperature (0.1-0.3) for factual tasks
   3. Add "If unsure, say I don't know" in system prompt
   4. Implement fact-checking against knowledge base
   5. Use structured output (JSON mode) for predictable formats
   6. Add citation requirements to prompts
   7. Human-in-the-loop for critical decisions


📋 SCENARIO 4: Conversation Memory Management
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Q: Your chatbot loses context in long conversations.
   How do you maintain conversation history efficiently?

A: Implement smart memory management:
   1. Sliding window: Keep last N messages
   2. Summarization: Summarize older messages periodically
   3. Token budget: Trim history to fit context window
   4. Important message pinning: Never trim system prompts
   5. Session storage: Use Redis/DB for persistence
   6. Hybrid: Recent messages verbatim + older summarized


📋 SCENARIO 5: Production Deployment Checklist
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Q: What do you check before deploying an AI chatbot to production?

A: Key checklist:
   1. API key security (env vars, secrets manager)
   2. Input validation & sanitization (prompt injection defense)
   3. Rate limiting & cost controls
   4. Logging & monitoring (latency, errors, token usage)
   5. Fallback responses for API failures
   6. Content moderation / safety filters
   7. Load testing with realistic traffic
   8. Data privacy compliance (PII handling)
   9. A/B testing framework for prompt improvements
   10. Automated evaluation pipeline

"""

print(scenarios)


# ============================================================
# SECTION 11: LANGCHAIN-STYLE CHAIN PATTERN
# ============================================================

print("=" * 60)
print("SECTION 11: CHAIN PATTERN (LangChain-Style)")
print("=" * 60)


class Chain:
    """Simulates a LangChain-style processing chain."""

    def __init__(self, steps: List):
        self.steps = steps

    def run(self, input_data: Dict) -> Dict:
        """Execute all steps in sequence."""
        data = input_data.copy()
        for i, step in enumerate(self.steps):
            print(f"  Step {i + 1}: {step.__name__}")
            data = step(data)
        return data


def preprocess_query(data: Dict) -> Dict:
    """Clean and normalize the user query."""
    data["processed_query"] = data["query"].lower().strip()
    data["query_tokens"] = data["processed_query"].split()
    return data


def classify_intent(data: Dict) -> Dict:
    """Classify the intent of the query."""
    query = data["processed_query"]
    if any(w in query for w in ["how", "what", "why", "explain"]):
        data["intent"] = "question"
    elif any(w in query for w in ["write", "create", "generate", "build"]):
        data["intent"] = "generation"
    elif any(w in query for w in ["fix", "debug", "error", "issue"]):
        data["intent"] = "debugging"
    else:
        data["intent"] = "general"
    return data


def select_prompt(data: Dict) -> Dict:
    """Select appropriate prompt template based on intent."""
    prompts = {
        "question": "Answer this question clearly: {query}",
        "generation": "Generate the following: {query}",
        "debugging": "Help debug this issue: {query}",
        "general": "Respond to: {query}",
    }
    data["prompt"] = prompts[data["intent"]].format(query=data["query"])
    return data


def generate_response(data: Dict) -> Dict:
    """Generate the final response."""
    data["response"] = f"[Generated] Intent={data['intent']}: {data['prompt']}"
    return data


def demo_chain():
    print("\n--- Chain Pattern Demo ---")

    pipeline = Chain(steps=[
        preprocess_query,
        classify_intent,
        select_prompt,
        generate_response,
    ])

    queries = [
        "What is machine learning?",
        "Write a Python function to sort a list",
        "Fix this error: IndexError in my code",
        "Hello there!",
    ]

    for q in queries:
        result = pipeline.run({"query": q})
        print(f"  📝 Query: '{q}'")
        print(f"     Intent: {result['intent']}")
        print(f"     Response: {result['response']}\n")

demo_chain()


# ============================================================
# SECTION 12: CONFIGURATION MANAGEMENT
# ============================================================

print("=" * 60)
print("SECTION 12: CONFIGURATION MANAGEMENT")
print("=" * 60)


@dataclass
class AIConfig:
    """Centralized configuration for AI applications."""
    # Model settings
    model_name: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float = 0.95

    # RAG settings
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k_results: int = 5

    # API settings
    api_timeout: int = 30
    max_retries: int = 3
    rate_limit_rpm: int = 60

    # Safety
    max_input_length: int = 10000
    blocked_topics: List[str] = field(default_factory=lambda: ["harmful", "illegal"])

    def to_dict(self) -> Dict:
        return {
            "model": {"name": self.model_name, "temperature": self.temperature,
                      "max_tokens": self.max_tokens, "top_p": self.top_p},
            "rag": {"chunk_size": self.chunk_size, "overlap": self.chunk_overlap,
                    "top_k": self.top_k_results},
            "api": {"timeout": self.api_timeout, "retries": self.max_retries,
                    "rpm_limit": self.rate_limit_rpm},
        }

    def validate(self) -> List[str]:
        errors = []
        if self.temperature < 0 or self.temperature > 2:
            errors.append("Temperature must be between 0 and 2")
        if self.max_tokens < 1:
            errors.append("Max tokens must be positive")
        if self.chunk_overlap >= self.chunk_size:
            errors.append("Chunk overlap must be less than chunk size")
        return errors


def demo_config():
    print("\n--- Config Demo ---")
    config = AIConfig(model_name="gpt-4", temperature=0.3)
    errors = config.validate()
    if errors:
        print(f"❌ Config errors: {errors}")
    else:
        print(f"✅ Config valid: {json.dumps(config.to_dict(), indent=2)}")

demo_config()


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("🎓 AI ENGINEER ASSESSMENT - TOPICS COVERED")
print("=" * 60)

summary = """
 ✅  1. Python Fundamentals (types, comprehensions, lambdas, strings)
 ✅  2. OOP (abstract classes, inheritance, polymorphism, dataclasses)
 ✅  3. Error Handling (custom exceptions, retry, backoff, fallback)
 ✅  4. Data Structures (documents, chunking, vector stores)
 ✅  5. API Interaction (chat completions, embeddings, token tracking)
 ✅  6. Prompt Engineering (zero-shot, few-shot, CoT, RAG prompts)
 ✅  7. RAG Pipeline (ingest, chunk, index, retrieve, generate)
 ✅  8. Batch Processing (sync batching patterns)
 ✅  9. Testing (unit tests, assertions, edge cases)
 ✅ 10. Scenario Questions (rate limits, hallucination, deployment)
 ✅ 11. Chain Patterns (LangChain-style sequential pipelines)
 ✅ 12. Configuration Management (dataclass configs, validation)

💡 Key Libraries to Know:
   - openai, langchain, llama-index
   - chromadb, pinecone, weaviate
   - transformers, sentence-transformers
   - fastapi, pydantic, httpx
   - pytest, unittest

🚀 Good luck with your AI Engineer assessment!
"""
print(summary)
