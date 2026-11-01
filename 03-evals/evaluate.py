import json
from pathlib import Path

from extractor import extract_job

FIELDS = ["title", "company", "location", "skills", "experience_years", "remote"]


def normalize(field, value):
    """Make values comparable: ignore uppercase/lowercase, extra spaces and skill order."""
    if value is None:
        return None
    if field == "skills":
        return sorted(skill.strip().lower() for skill in value)
    if isinstance(value, str):
        return value.strip().lower()
    return value


def main():
    cases_file = Path(__file__).parent / "test_cases.json"
    cases = json.loads(cases_file.read_text(encoding="utf-8"))

    total = 0
    correct = 0

    for case in cases:
        print(f"\n[{case['id']}]")
        result = extract_job(case["input"])

        if result is None:
            print("  Extraction FAILED completely")
            total += len(FIELDS)
            continue

        actual = result.model_dump()
        case_errors = 0

        for field in FIELDS:
            expected = case["expected"][field]
            got = actual[field]
            total += 1

            if normalize(field, expected) == normalize(field, got):
                correct += 1
            else:
                case_errors += 1
                print(f"  WRONG {field}: expected {expected!r}, got {got!r}")

        if case_errors == 0:
            print("  All fields correct")

    print("\n" + "=" * 40)
    print(f"SCORE: {correct}/{total} fields correct ({correct / total:.0%})")
    print("=" * 40)


if __name__ == "__main__":
    main()