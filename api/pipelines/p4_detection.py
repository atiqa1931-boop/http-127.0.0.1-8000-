def detect_candidates(tokens):
    """
    Pipeline 4: Proper Noun Detection
    Identifies candidate words based on structural signals like:
    - Capitalization patterns (Upper, Mixed, Title)
    - Word position (ignoring Title case at sentence start)
    - Repetition and Uniqueness of word form (for lowercase entities)
    """
    candidates = set()
    
    # Track frequencies to find repeated unique forms
    word_freq = {}
    for t in tokens:
        word = t["original"]
        word_freq[word] = word_freq.get(word, 0) + 1
        
    for t in tokens:
        word = t["original"]
        ctype = t["case_type"]
        is_start = t["is_sentence_start"]
        
        # 1. Capitalization Patterns & Word Position
        # Mixed and Upper case are strong structural signals anywhere
        if ctype in ["upper", "mixed"] and len(word) > 1:
            candidates.add(word)
            
        # Title case is a structural signal if it is mid-sentence
        elif ctype == "title" and not is_start:
            candidates.add(word)
            
        # 2. Repetition across text (Lower case anomaly detection)
        # If a lowercase word is sufficiently long (unique form) and repeats frequently, 
        # it is held as a candidate for variation matching.
        elif ctype == "lower" and len(word) > 4:
            if word_freq[word] > 1:
                candidates.add(word)
                
    return candidates
