import unittest
from collections import namedtuple

import pytest
from work_gpt import scraping_job_data, create_prompt, is_valid_url
from job import *

# Test the scraping_job_data function
# Job = namedtuple('Job', ['title', 'company', 'description'])

def test_scraping_job_data():
    url = "https://www.linkedin.com/jobs/view/3682761081/?alternateChannel=search&refId=%2F%2F3VMv%2Be9jOGo4qRzrhd8w%3D%3D&trackingId=8RobfT9R2EqoKBzIAPQC6A%3D%3D"
    job = scraping_job_data(url)
    assert job is not None
    assert job.title != ""
    assert job.company_name != ""
    assert job.description != ""

def test_create_promt():
    # Test with job and CV content
    job = Job("Software Engineer", "Example Inc.", "Job description goes here."," " , " ", "Tel-Aviv")
    cv = "My resume content goes here."
    prompt = create_prompt(job, cv)
    expected_prompt = "Please write a personalized cover letter for this Software Engineer role at Example Inc." \
                     ".\nHere is the job description:\n<job description>Job description goes here.<\\job description>\nAnd here is my resume:\n<resume>" \
                     "My resume content goes here.<\\resume>"
    assert prompt == expected_prompt

    # Test with is_cove_letter set to False
    prompt = create_prompt(job, cv, is_cover_letter=False)
    expected_prompt = "Please personalize my resume for this Software Engineer role at Example Inc." \
                     ".\nHere is the job description:\n<job description>Job description goes here.<\\job description>" \
                      "\nAnd here is my resume:\n<resume>" \
                     "My resume content goes here.<\\resume>"
    assert prompt == expected_prompt

def test_is_valid_url():
    # Valid URL
    url1 = "https://www.example.com/job"
    assert is_valid_url(url1) == True

    # Invalid URL
    url2 = "example.com/job"
    assert is_valid_url(url2) == False

    # Invalid URL (No scheme)
    url3 = "www.example.com/job"
    assert is_valid_url(url3) == False

    # Invalid URL (No domain)
    url4 = "https://"
    assert is_valid_url(url4) == False

    # Invalid URL (Empty URL)
    url5 = ""
    assert is_valid_url(url5) == False

# Run the tests
if __name__ == '__main__':
    pytest.main()
