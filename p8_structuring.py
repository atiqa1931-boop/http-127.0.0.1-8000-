def structure_results(corrections_made):
    """
    Pipeline 8: Result Structuring Pipeline
    Converts raw correction logs into aggregated statistics structure for the frontend UI.
    """
    report = []
    summary = {}
    
    for c in corrections_made:
        canon = c["canonical"]
        orig = c["original"]
        
        if canon not in summary:
            summary[canon] = {"total_replacements": 0, "replaced_variants": set()}
            
        summary[canon]["total_replacements"] += 1
        summary[canon]["replaced_variants"].add(orig)
        
    for canon, data in summary.items():
        report.append({
            "canonical_form": canon,
            "replacements_count": data["total_replacements"],
            "variants_found": list(data["replaced_variants"])
        })
        
    # Sort report by highest replacement count
    report.sort(key=lambda x: x["replacements_count"], reverse=True)
        
    return {
        "total_corrections": len(corrections_made),
        "details": report
    }
