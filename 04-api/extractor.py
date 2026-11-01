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



# 2. The few-shot example: a fake job ad + its perfect answer
example_post = """Urgently hiring: Junior Python Developer at a Lahore-based agency.
Python and FastAPI required. Freshers welcome, but 2 years of experience is a plus.
Office-based role."""

example_answer = """{"title": "Junior Python Developer", "company": null, "location": "Lahore",
 "skills": ["Python", "FastAPI"], "experience_years": 0, "remote": false}"""

rules = """You extract data from job posts. Follow these rules:
- title: the job title only. Remove extra words like "Urgently hiring", "Wanted", "Remote".
- company: the company's actual name. If no name is given, use null.
- location: the city name only, with no extra words. If a city is mentioned anywhere, use it.
- skills: every technology mentioned.
- experience_years: the minimum required. If freshers are welcome, use 0.
- remote: true only if the role can be done remotely."""


# . Extract and validate
def extract_job(job_post: str) -> JobPosting | None:
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": rules},
            {"role": "user", "content": example_post},
            {"role": "assistant", "content": example_answer},
            {"role": "user", "content": job_post},
        ],
        format=JobPosting.model_json_schema(),
        options={"temperature": 0},
    )
    raw = response["message"]["content"]

    try:
        job = JobPosting.model_validate_json(raw)

        # Rules that must always be right: handle them in code, not with the AI
        text = job_post.lower()
        if "fresher" in text or "fresh graduate" in text:
            job.experience_years = 0

        job.title = job.title.removeprefix("Remote ").strip()

        return job
    except ValidationError as e:
        print("Validation FAILED:")
        print(e)
        return None
