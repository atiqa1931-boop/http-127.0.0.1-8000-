def select_canonical_forms(variant_clusters, tokens):
    """
    Pipeline 6: Canonical Form Selection
    Assigns the most structurally complete/accepted spelling per cluster.
    """
    text = " ".join([t["original"] for t in tokens]) 
    canonical_map = {}
    
    for cluster in variant_clusters:
        best_score_variants = []
        highest_score = -1
        
        # Simple context dictionary for Step 7: Exception Handling (apple vs Apple)
        tech_keywords = ["phone", "laptop", "software", "tech", "download", "app", "mac"]
        food_keywords = ["fruit", "eat", "juice", "bite", "pie"]
        
        for variant in cluster:
            score = text.count(variant)
            
            # Step 7 Exception Logic: Contextual boosting for known ambiguous nouns
            if variant.lower() == "apple":
                if any(kw in text.lower() for kw in tech_keywords) and variant == "Apple":
                    score += 10 # Heavily boost Title case if tech context
                elif any(kw in text.lower() for kw in food_keywords) and variant == "apple":
                    score += 10 # Heavily boost lowercase if food context
            
            if len(variant) > 1:
                # Favors mixed case (WhatsApp)
                if any(c.isupper() for c in variant[1:]) and variant[0].isupper():
                    score += 5
                # Favors title case (Apple)
                elif variant.istitle():
                    score += 3
                # Favors upper case (IBM)
                elif variant.isupper():
                    score += 2
                    
            if score > highest_score:
                highest_score = score
                best_score_variants = [variant]
            elif score == highest_score:
                best_score_variants.append(variant)
                
        # Step 7: Ambiguity Handling. If there's a tie, mark as uncertain and do NOT correct.
        if len(best_score_variants) > 1:
            best_form = "<UNCERTAIN>"
        elif len(best_score_variants) == 1:
            best_form = best_score_variants[0]
        else:
            best_form = list(cluster)[0]
            
        for variant in cluster:
            if variant != best_form and best_form != "<UNCERTAIN>": 
                canonical_map[variant] = best_form
            elif best_form == "<UNCERTAIN>":
                # We record it for the report but won't change the actual string
                canonical_map[variant] = variant 
            
    return canonical_map
