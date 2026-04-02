import re
from typing import List, Dict

def tokenize_text(text: str) -> List[Dict[str, any]]:
    """
    Pipeline 3: Tokenization Pipeline
    Tokenizes the preprocessed text into words, retaining positional and formatting information.
    This sets up the foundation for 'Step 1: Identifying Candidate Proper Nouns' 
    which requires checking word position and capitalization logic.
    """
    if not text:
        return []

    # Simple tokenization that preserves punctuation and whitespace as structural signals, 
    # but for analyzing proper nouns we'll isolate the words and track their starting index.
    
    tokens = []
    # Match words (including internal apostrophe/dash for things like 'Wi-Fi' or "O'Connor")
    # Output structure maps to the rules from the framework
    for match in re.finditer(r"[\w'-]+", text):
        word = match.group()
        start = match.start()
        
        # Analyze capitalization patterns (All Caps, Title Case, Lowercase, Mixed Case)
        case_type = "lower"
        if word.isupper():
            case_type = "upper"
        elif word.istitle():
            case_type = "title"
        elif any(c.isupper() for c in word):
            case_type = "mixed"
            
        tokens.append({
            "original": word,
            "case_type": case_type,
            "position": start,
            "original_length": len(word),
            "is_sentence_start": False # We will refine this
        })
        
    # Mark sentence boundaries accurately using the original text indices
    # We find sentence-ending punctuation followed by whitespace and a character
    for t in tokens:
        # The very first token is always a sentence start
        if t == tokens[0]:
            t["is_sentence_start"] = True
            continue
            
        pos = t["position"]
        # Look backwards to see if there's a sentence terminator before this word 
        # but after the previous word
        preceding_text = text[:pos].strip()
        if not preceding_text:
            t["is_sentence_start"] = True
        elif preceding_text[-1] in ".!?":
            t["is_sentence_start"] = True
        else:
            t["is_sentence_start"] = False

    return tokens
