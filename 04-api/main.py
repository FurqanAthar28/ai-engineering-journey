from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from extractor import JobPosting, extract_job

app = FastAPI(title="Job Post Extractor")


# What the customer sends us
class JobPostRequest(BaseModel):
    text: str


# A simple page to check that the API is running
@app.get("/")
def home():
    return {"message": "Job Post Extractor is running"}


# The main counter: send a job post, get clean data back
@app.post("/extract", response_model=JobPosting)
def extract(request: JobPostRequest):
    try:
        job = extract_job(request.text)
    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="The AI model is not available right now. Please try again later.",
        )

    if job is None:
        raise HTTPException(status_code=422, detail="Could not extract job data")
    return job