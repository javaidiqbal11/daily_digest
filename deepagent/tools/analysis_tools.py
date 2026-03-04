"""
DeepAgent Analysis Tools
Tools for text analysis and source comparison.
"""

from collections import Counter
import re


def analyze_text(
    text: str,
    analysis_type: str = "summary_stats",
) -> str:
    """
    Analyze text content and provide statistics or insights.
    
    Use this to get a quick analysis of text content including word count,
    reading time, key phrases, and structure analysis.
    
    Args:
        text: The text content to analyze
        analysis_type: Type of analysis to perform.
                       Options: "summary_stats", "key_phrases", "structure"
    
    Returns:
        Analysis results as formatted text
    """
    results = []
    
    if analysis_type in ("summary_stats", "all"):
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        
        results.append("## 📊 Text Statistics")
        results.append(f"- **Words**: {len(words):,}")
        results.append(f"- **Characters**: {len(text):,}")
        results.append(f"- **Sentences**: {len(sentences):,}")
        results.append(f"- **Paragraphs**: {len(paragraphs):,}")
        results.append(f"- **Avg words/sentence**: {len(words) / max(len(sentences), 1):.1f}")
        results.append(f"- **Est. reading time**: {len(words) // 200} min {(len(words) % 200) // 3} sec")
    
    if analysis_type in ("key_phrases", "all"):
        # Simple key phrase extraction (word frequency)
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        # Filter common stop words
        stop_words = {
            "that", "this", "with", "from", "have", "been", "were", "they",
            "their", "what", "when", "where", "which", "there", "about",
            "would", "could", "should", "other", "than", "then", "into",
            "also", "more", "some", "such", "only", "over", "very",
        }
        filtered = [w for w in words if w not in stop_words]
        freq = Counter(filtered).most_common(15)
        
        results.append("\n## 🔑 Key Terms (by frequency)")
        for word, count in freq:
            bar = "█" * min(count, 20)
            results.append(f"- **{word}**: {count} {bar}")
    
    if analysis_type in ("structure", "all"):
        headers = re.findall(r'^#+\s+.+$', text, re.MULTILINE)
        links = re.findall(r'https?://[^\s\)]+', text)
        code_blocks = re.findall(r'```[\s\S]*?```', text)
        
        results.append("\n## 🏗️ Structure Analysis")
        results.append(f"- **Headers**: {len(headers)}")
        results.append(f"- **Links/URLs**: {len(links)}")
        results.append(f"- **Code blocks**: {len(code_blocks)}")
        
        if headers:
            results.append("\n### Document Outline:")
            for h in headers[:20]:
                level = len(h) - len(h.lstrip('#'))
                indent = "  " * (level - 1)
                results.append(f"{indent}- {h.strip('#').strip()}")

    return "\n".join(results) if results else "No analysis performed. Choose: summary_stats, key_phrases, or structure"


def compare_sources(
    source_1: str,
    source_2: str,
    source_1_name: str = "Source 1",
    source_2_name: str = "Source 2",
) -> str:
    """
    Compare two text sources and identify similarities and differences.
    
    Use this to cross-reference information from different sources and
    identify consensus, conflicts, or unique information.
    
    Args:
        source_1: First text source content
        source_2: Second text source content
        source_1_name: Label for the first source
        source_2_name: Label for the second source
    
    Returns:
        Comparison analysis as formatted text
    """
    # Extract key terms from each source
    def extract_terms(text):
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        stop_words = {
            "that", "this", "with", "from", "have", "been", "were", "they",
            "their", "what", "when", "where", "which", "there", "about",
        }
        return set(w for w in words if w not in stop_words)

    terms_1 = extract_terms(source_1)
    terms_2 = extract_terms(source_2)
    
    common = terms_1 & terms_2
    unique_1 = terms_1 - terms_2
    unique_2 = terms_2 - terms_1
    
    overlap = len(common) / max(len(terms_1 | terms_2), 1) * 100

    results = [
        "## 🔄 Source Comparison\n",
        f"### Overview",
        f"- **{source_1_name}**: {len(source_1.split())} words, {len(terms_1)} unique terms",
        f"- **{source_2_name}**: {len(source_2.split())} words, {len(terms_2)} unique terms",
        f"- **Topic overlap**: {overlap:.1f}%\n",
        f"### Common Topics ({len(common)} shared terms)",
        f"{', '.join(sorted(list(common))[:30])}\n",
        f"### Unique to {source_1_name} ({len(unique_1)} terms)",
        f"{', '.join(sorted(list(unique_1))[:20])}\n",
        f"### Unique to {source_2_name} ({len(unique_2)} terms)",
        f"{', '.join(sorted(list(unique_2))[:20])}",
    ]

    return "\n".join(results)
