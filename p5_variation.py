import difflib

def group_variations(tokens, candidates):
    """
    Pipeline 5: Structural Pattern Analysis & Similarity Matching
    Groups structurally similar tokens into distinct clusters (e.g., {"WhatsApp", "whatsapp", "whats app"}).
    """
    all_unique_forms = set([t["original"] for t in tokens])
    clusters = []
    clustered = set()
    
    for candidate in candidates:
        if candidate in clustered:
            continue
            
        group = {candidate}
        normalized_cand = candidate.lower().replace(" ", "").replace("-", "")
        
        # Compare against single tokens
        for word in all_unique_forms:
            if word == candidate or word in clustered:
                continue
            normalized_word = word.lower().replace(" ", "").replace("-", "")
            
            # Exact letter match (ignoring case and basic punctuation)
            if normalized_cand == normalized_word:
                # FAILURE CASE 1 PREVENTION: Avoid grouping very short ambiguous forms (e.g., US vs us, AM vs am)
                if len(normalized_cand) <= 2 and candidate.isupper() and word.islower():
                    # We classify it as structurally ambiguous and delay correction to avoid overriding pronouns/adverbs
                    continue 
                group.add(word)
                continue
            if len(normalized_cand) > 4 and len(normalized_word) > 4:
                ratio = difflib.SequenceMatcher(None, normalized_cand, normalized_word).ratio()
                if ratio >= 0.85:
                    group.add(word)
        
        # Check for multi-token splits (e.g. "Whats App" vs "WhatsApp")
        for i in range(len(tokens) - 1):
            combined = tokens[i]["original"] + tokens[i+1]["original"]
            norm_combined = combined.lower().replace("-", "")
            if norm_combined == normalized_cand:
                split_form = f'{tokens[i]["original"]} {tokens[i+1]["original"]}'
                group.add(split_form)
                
        clusters.append(group)
        clustered.update(group)
        
    # Return clusters with more than one variation (inconsistencies found)
    return [c for c in clusters if len(c) > 1]
