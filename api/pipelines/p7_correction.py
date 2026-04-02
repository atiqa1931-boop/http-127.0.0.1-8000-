def apply_corrections(tokens, canonical_map):
    """
    Pipeline 7: Consistency Correction Mechanism
    Applies the canonical spelling globally. Replaces variations in the structure.
    Also tracks statistics for the Structuring pipeline.
    """
    corrections_made = []
    corrected_tokens = []
    
    i = 0
    while i < len(tokens):
        # Multi-word check
        if i < len(tokens) - 1:
            combined = f'{tokens[i]["original"]} {tokens[i+1]["original"]}'
            if combined in canonical_map:
                canon = canonical_map[combined]
                # Combined total length + 1 (for the space separating them in raw text)
                omb_length = tokens[i]["original_length"] + 1 + tokens[i+1]["original_length"] 
                
                corrected_tokens.append({
                    "original": canon,
                    "position": tokens[i]["position"], 
                    "original_length": omb_length,
                    "is_sentence_start": tokens[i]["is_sentence_start"]
                })
                corrections_made.append({
                    "original": combined,
                    "canonical": canon,
                    "type": "multi_word_merge"
                })
                i += 2
                continue
                
        # Single token check
        word = tokens[i]["original"]
        if word in canonical_map:
            canon = canonical_map[word]
            corrected_tokens.append({
                "original": canon,
                "position": tokens[i]["position"],
                "original_length": tokens[i]["original_length"],
                "is_sentence_start": tokens[i]["is_sentence_start"]
            })
            corrections_made.append({
                "original": word,
                "canonical": canon,
                "type": "single_word"
            })
            i += 1
        else:
            corrected_tokens.append(tokens[i])
            i += 1
            
    return corrected_tokens, corrections_made
