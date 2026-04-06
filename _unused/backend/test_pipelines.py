# test_pipelines.py
import sys
import os

# Add the backend directory to Python path so we can import pipelines
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipelines.p2_preprocessing import preprocess_text
from pipelines.p11_integration import run_analytical_pipelines

def test_system():
    # Complex test string covering repetition, variations, splits, ambiguity (us/US), and context (Apple vs phone)
    raw_input = "I use whatsapp daily. but I think Whats App is better than whatsapp. My US friend told us to use Apple phones to test it instead of eating an apple."
    
    print("--- STARTING SYSTEM VERIFICATION OVERRIDE ---")
    print(f"RAW INPUT: {raw_input}")
    
    preprocessed = preprocess_text(raw_input)
    print(f"PIPELINE 2 (PREPROCESSED): {preprocessed}")
    
    analytics = run_analytical_pipelines(preprocessed)
    
    print("\n--- FINAL OUTPUT ---")
    print(analytics["final_text"])
    
    print("\n--- ANALYTICS REPORT ---")
    for detail in analytics["report"]["details"]:
        print(f"Canonical: {detail['canonical_form']} | Replaced: {detail['variants_found']}")

if __name__ == "__main__":
    test_system()
