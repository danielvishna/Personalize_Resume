import time
from selenium import webdriver
import random
from selenium.webdriver.common.by import By
import PyPDF2
import pyperclip
import os
import openai
from collections import namedtuple

# Define a named tuple 'Job' to represent job information (title, company, description)
Job = namedtuple('Job', ['title', 'company', 'description'])


def read_pdf(file_path):
    """
    Reads a PDF file and extracts text from all pages.

    Args:
        file_path (str): The file path to the PDF file.

    Returns:
        str: The concatenated text extracted from all pages of the PDF.
    """
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        text = []
        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            text.append(page.extract_text())
        return '\n'.join(text)


def generate_personalized_resume():
    """
    Generates a personalized resume for a given URL.

    Returns:
        Job or None: A named tuple representing job information (title, company, description) if successful, otherwise None.
    """
    url = url_entry
    try:
        # XPaths for extracting job title, company, and job description from the LinkedIn job page.
        title_tag = "//h1[@class='top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open " \
                    "text-color-text mb-0 topcard__title']"
        company_tag = "//a[@class='topcard__org-name-link topcard__flavor--black-link']"
        button_tag = '//button[text()="\n        Show more\n\n        "]'
        description_tag = "//div[@class='description__text description__text--rich']"

        time.sleep(random.uniform(0.0, 0.3))
        # Set up the Edge web driver in headless mode
        op = webdriver.EdgeOptions()
        op.add_argument('headless')
        op.add_argument("--incognito")
        driver = webdriver.Edge(options=op)
        driver.get(url)

        # Extract job title, company, and description from the page
        title = driver.find_elements(By.XPATH, title_tag)[0].text
        time.sleep(random.uniform(0.0, 0.2))
        company = driver.find_elements(By.XPATH, company_tag)[0].text
        time.sleep(random.uniform(0.0, 0.1))
        button = driver.find_elements(By.XPATH, button_tag)
        button[0].click()
        time.sleep(random.uniform(0.0, 0.4))
        description = driver.find_elements(By.XPATH, description_tag)[0].text[:-9]  # Remove last 9 characters

        driver.quit()
    except:
        raise Exception("There is a problem using Selenium")

    return Job(title, company, description)


def copy_resume(job, cv):
    """
    Copies a personalized resume and job description to the clipboard.

    Args:
        job (Job): A named tuple containing job information (title, company, description).
        cv (str): The content of the resume to be copied.
    """
    personalize_resume = f"Please personalize my resume for this {job.title} role at {job.company}.\n" \
                         f"Here is the job description: \n{job.description} \n" \
                         f"And here is my resume: \n {cv}"
    pyperclip.copy(personalize_resume)
    print("Content copied to clipboard!")


def copy_cover_letter(job, cv):
    """
    Copies a personalized cover letter to the clipboard.

    Args:
        job (Job): A named tuple containing job information (title, company, description).
        cv (str): The content of the resume to be included in the cover letter.
    """
    personalize_CL = f"Please write a personalized cover letter for this {job.title} role at {job.company}.\n" \
                     f"Here is the job description: \n{job.description} \n" \
                     f"And here is my resume: \n {cv}"
    system_content = 'You are a recruitment consultant who helps candidates write cover letters for jobs.' \
                     'Help them stand out for the job even if they don\'t meet all the job requirements.'

    # Use OpenAI GPT-3.5 Turbo model to generate the cover letter content
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "system", "content": system_content},
                                                             {"role": "user", "content": personalize_CL}])
    answer = chat_completion['choices'][0]['message']['content']
    pyperclip.copy(answer)
    print("Content copied to clipboard!")


if __name__ == '__main__':
    # Set your OpenAI API key
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # Replace with the actual path to your CV file
    file_path = 'C:\\Users\\DanielV\\Documents\\CV\\Daniel Vishna CV.pdf'
    CV = read_pdf(file_path)

    job = None
    while True:
        print("Enter 1 to insert a new URL, 2 to copy the resume, 3 to get the cover letter, or any other key to exit.")
        inputs = input()
        if inputs == "1":
            url_entry = input("Enter the URL:\n")
            job = generate_personalized_resume()
        elif inputs == "2":
            copy_resume(job, CV)
        elif inputs == "3":
            copy_cover_letter(job, CV)
        else:
            break

