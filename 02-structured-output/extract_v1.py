import json
import ollama

job_post = """
We're hiring!! Backend dev needed at TechNova Solutions, Lahore office (no remote sorry).
Must know Python + Django, PostgreSQL is a plus, Docker experience preferred.
Freshers welcome but 1 year exp is better. Apply fast!!
"""

prompt = f"""
Extract information from this job post and return it as JSON with these fields:
title, company, location, skills (list), experience_years (number), remote (true/false).

Job post:
{job_post}
"""

response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": prompt}],
)

raw = response["message"]["content"]
print("----- RAW OUTPUT -----")
print(raw)

print("\n----- TRYING TO PARSE -----")
try:
    data = json.loads(raw)
    print("Success! Parsed data:")
    print(data)
except json.JSONDecodeError as e:
    print("FAILED to parse JSON:", e)