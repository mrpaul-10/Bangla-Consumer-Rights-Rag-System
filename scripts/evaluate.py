"""
Runs the full pipeline against the evaluation question set and
reports whether the expected section appeared in the top retrieved results.
"""

import json
import time
from src.pipeline import answer_question

EVAL_FILE = "tests/eval_questions.json"


def load_eval_questions():
    with open(EVAL_FILE, encoding="utf-8") as f:
        return json.load(f)


def run_evaluation():
    questions = load_eval_questions()
    correct = 0
    results = []

    for item in questions:
        q = item["question"]
        expected = item["expected_section"]

        try:
            result = answer_question(q)
            found_sections = result["sources"]
            is_correct = expected in found_sections
        except Exception as e:
            print(f"[ERROR] {q}")
            print(f"   {e}")
            results.append({
                "question": q,
                "expected": expected,
                "retrieved": [],
                "correct": False,
                "error": str(e),
            })
            time.sleep(13)
            continue

        if is_correct:
            correct += 1

        results.append({
            "question": q,
            "expected": expected,
            "retrieved": found_sections,
            "correct": is_correct,
        })

        status = "[PASS]" if is_correct else "[FAIL]"
        print(f"{status} {q}")
        print(f"   Expected: {expected} | Retrieved: {found_sections}")

        time.sleep(13)  # Rate limit: max ~5 requests/minute on free tier

    total = len(questions)
    accuracy = (correct / total) * 100
    print(f"\n{'='*40}")
    print(f"Accuracy: {correct}/{total} ({accuracy:.1f}%)")

    with open("tests/eval_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    run_evaluation()