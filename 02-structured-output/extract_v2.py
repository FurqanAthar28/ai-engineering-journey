import json
import ollama

job_post = """
We're hiring!! Backend dev needed at TechNova Solutions, Lahore office (no remote sorry).
Must know Python + Django, PostgreSQL is a plus, Docker experience preferred.
Freshers welcome but 1 year exp is better. Apply fast!!
"""

prompt = f"""
Extract information from the job post below.

Return ONLY a valid JSON object. No explanation, no notes, no markdown, no backticks.

Use exactly these fields:
- "title": string, the job title, written in full (e.g. "Backend Developer", not "Backend Dev")
- "company": string
- "location": string, city name only (e.g. "Lahore")
- "skills": list of strings, include EVERY technology mentioned
- "experience_years": number. If the post says freshers are welcome, this MUST be 0, even if more experience is preferred.
- "remote": true or false

Job post:
{job_post}
"""

example_post = """
Junior PHP developer needed at WebCraft, Islamabad. Laravel and MySQL required.
Freshers are welcome, although 2 years of experience is a plus. On-site only.
"""

example_answer = """{"title": "Junior PHP Developer", "company": "WebCraft", "location": "Islamabad", "skills": ["PHP", "Laravel", "MySQL"], "experience_years": 0, "remote": false}"""

response = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "system", "content": "You extract job post data as JSON. If freshers are welcome, experience_years is 0."},
        {"role": "user", "content": prompt.replace(job_post, example_post)},
        {"role": "assistant", "content": example_answer},
        {"role": "user", "content": prompt},
    ],
    format="json",
    options={"temperature": 0},
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