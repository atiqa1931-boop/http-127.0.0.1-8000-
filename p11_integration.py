from pipelines.p3_tokenization import tokenize_text
from pipelines.p4_detection import detect_candidates
from pipelines.p5_variation import group_variations
from pipelines.p6_canonical import select_canonical_forms
from pipelines.p7_correction import apply_corrections
from pipelines.p8_structuring import structure_results
from pipelines.p9_output_generation import generate_output_text

def run_analytical_pipelines(preprocessed_text: str):
    """
    Pipeline 11: System Integration Pipeline
    Runs step 3 through 9 sequentially.
    """
    # Pipeline 3
    tokens = tokenize_text(preprocessed_text)
    
    # Pipeline 4
    candidates = detect_candidates(tokens)
    
    # Pipeline 5
    variant_clusters = group_variations(tokens, candidates)
    
    # Pipeline 6
    canonical_map = select_canonical_forms(variant_clusters, tokens)
    
    # Pipeline 7
    corrected_tokens, corrections_made = apply_corrections(tokens, canonical_map)
    
    # Pipeline 8
    structured_report = structure_results(corrections_made)
    
    # Pipeline 9
    final_text = generate_output_text(preprocessed_text, corrected_tokens)
    
    return {
        "final_text": final_text,
        "report": structured_report
    }
