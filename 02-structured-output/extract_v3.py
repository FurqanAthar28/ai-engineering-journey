import ollama
from pydantic import BaseModel, Field, ValidationError


# 1. Define exactly what a valid result looks like
class JobPosting(BaseModel):
    title: str
    company: str | None = Field(description="Company name, or null if not mentioned")
    location: str | None = Field(description="City name only, or null if not mentioned")
    skills: list[str]
    experience_years: int = Field(ge=0, le=20, description="Minimum years required; 0 if freshers are welcome")
    remote: bool


# 2. Some different job posts to test with
job_posts = [
    """We're hiring!! Backend dev needed at TechNova Solutions, Lahore office (no remote sorry).
    Must know Python + Django, PostgreSQL is a plus, Docker experience preferred.
    Freshers welcome but 1 year exp is better. Apply fast!!""",

    """Remote React + Node.js developer wanted. 3+ years of experience required.
    Must know TypeScript and AWS. We're a startup based in Karachi but the role is fully remote.
    Company: CloudPeak Labs.""",

    """Internship opportunity: Python/Django intern at a Faisalabad software house.
    Fresh graduates only. Knowledge of Git and REST APIs required.""",
]


# 3. Extract and validate
def extract_job(job_post: str) -> JobPosting | None:
    prompt = f"""
Extract information from the job post below.
Write the job title in full. Include every technology mentioned in skills.
If something is not mentioned, use null.
without words like “Wanted” or “Remote,” location as city only with no extra words,
Job post:
{job_post}
"""
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
        format=JobPosting.model_json_schema(),
        options={"temperature": 0},
    )
    raw = response["message"]["content"]

    try:
        return JobPosting.model_validate_json(raw)
    except ValidationError as e:
        print("Validation FAILED:")
        print(e)
        return None


# 4. Run it on every post
for i, post in enumerate(job_posts, start=1):
    job = extract_job(post)
    if job:
        print(f"\nJob {i}: {job.title} at {job.company}")
        print(f"  Location:   {job.location} | Remote: {job.remote}")
        print(f"  Skills:     {', '.join(job.skills)}")
        print(f"  Experience: {job.experience_years}+ years")