def generate_output_text(raw_text: str, corrected_tokens: list) -> str:
    """
    Pipeline 9: Output Generation Pipeline
    Reconstructs the full string seamlessly.
    """
    if not corrected_tokens:
        return raw_text
        
    result = ""
    current_idx = 0
    
    for t in corrected_tokens:
        pos = t["position"]
        length = t.get("original_length", len(t["original"]))
        
        # Add any punctuation/spaces that occurred before this token
        if pos > current_idx:
            result += raw_text[current_idx:pos]
            
        # Add the corrected/original token
        result += t["original"]
        
        # Advance raw pointer
        current_idx = pos + length
        
    # Add trailing punctuation/spaces
    if current_idx < len(raw_text):
        result += raw_text[current_idx:]
        
    return result
