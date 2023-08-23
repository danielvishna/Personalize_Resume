import sys
import time
from selenium import webdriver
import random
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, InvalidArgumentException
from selenium.webdriver.common.by import By
import pyperclip
import os
import openai
from collections import namedtuple
import urllib.parse
import logging

from files_works import Resume

# Define a named tuple 'Job' to represent job information (title, company, description)
Job = namedtuple('Job', ['title', 'company', 'description'])


def scraping_job_data(url):
    """
    Scrapes job information from a given URL.

    Returns:
        Job or None: A named tuple representing job information (title, company, description) if successful, otherwise None.
    """
    # Set up the Edge web driver in headless mode
    op = webdriver.EdgeOptions()
    op.add_argument('headless')
    op.add_argument("--incognito")
    driver = webdriver.Edge(options=op)
    try:
        # XPaths for extracting job title, company, and job description from the LinkedIn job page.
        title_tag = "//h1[@class='top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open " \
                    "text-color-text mb-0 topcard__title']"
        company_tag = "//a[@class='topcard__org-name-link topcard__flavor--black-link']"
        button_tag = '//button[text()="\n        Show more\n\n        "]'
        description_tag = "//div[@class='description__text description__text--rich']"

        driver.get(url)
        time.sleep(random.uniform(0.0, 0.3))

        # Extract job title, company, and description from the page
        title = driver.find_element(By.XPATH, title_tag).text
        time.sleep(random.uniform(0.0, 0.2))
        company = driver.find_element(By.XPATH, company_tag).text
        time.sleep(random.uniform(0.0, 0.1))
        button = driver.find_element(By.XPATH, button_tag)
        button.click()
        time.sleep(random.uniform(0.0, 0.4))
        description = driver.find_element(By.XPATH, description_tag).text[:-9]  # Remove last 9 characters
        return Job(title, company, description)
    except (NoSuchElementException, NoSuchAttributeException):
        # Handle the exception here
        print(
            "Error: Unable to find job elements on the page. Please recheck the URL, and contact the developer if the "
            "error still occurs for an update.")
        return
    except InvalidArgumentException:
        print("Please recheck the URL")
        return
    except Exception as e:
        print("There is a problem contact the developer")
    finally:
        driver.quit()


def create_prompt(job, cv, is_cove_letter=True):
    prompt = f'{job.title} role at {job.company}.\nHere is the job description: \n<job description>{job.description}' \
             f'<\\job description>\nAnd here is my resume: \n <resume>{cv}<\\resume>'.replace("  ", " "). \
        replace("\n\n", "\n")
    if is_cove_letter:
        prompt = "Please write a personalized cover letter for this " + prompt
    else:
        prompt = "Please personalize my resume for this " + prompt
    return prompt


def call_gpt(system_content, user_content):
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "system", "content": system_content},
                                                             {"role": "user", "content": user_content}])
    answer = chat_completion['choices'][0]['message']['content']
    pyperclip.copy(answer)


def copy_resume(job, cv, use_gpt):
    """
    Copies a personalized resume and job description to the clipboard.

    Args:
        job (Job): A named tuple containing job information (title, company, description).
        cv (str): The content of the resume to be copied.
    """
    system_content = "You are a skilled resume personalization expert. Your expertise lies in customizing candidate " \
                     "resumes to fit specific job roles, even when their qualifications may not perfectly match the " \
                     "requirements. You will receive candidate resumes and job descriptions marked up with XML " \
                     "tags.Your objective is to personalize and ensure candidates' resumes are tailored effectively," \
                     " showcasing their relevant skills and experiences for each job."
    personalize_resume = create_prompt(job, cv, False)
    if use_gpt:
        call_gpt(system_content, personalize_resume)
        print("Personalize resume copied to clipboard!")
    else:
        pyperclip.copy(system_content + "\n" + personalize_resume)
        print("Personalize resume prompt copied to clipboard!")


def copy_cover_letter(job, cv, use_gpt):
    """
    Copies a personalized cover letter to the clipboard.

    Args:
        job (Job): A named tuple containing job information (title, company, description).
        cv (str): The content of the resume to be included in the cover letter.
    """
    cover_letter = create_prompt(job, cv)

    system_content = "You are an expert recruitment consultant specializing in crafting compelling cover letters for " \
                     "job candidates. You excel at composing responses that help candidates shine, even when they " \
                     "don't fully meet the job requirements. You will receive job descriptions and the candidate's" \
                     " resume, marked up with XML tags.Your goal is to provide expert-level guidance that ensures " \
                     "candidates stand out and make a strong impression in their cover letters."
    if use_gpt:
        call_gpt(system_content, cover_letter)
        print("Cover letter copied to clipboard!")
    else:
        pyperclip.copy(system_content + "\n" + cover_letter)
        print("Cover letter prompt copied to clipboard!")


def is_valid_url(url):
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


if __name__ == '__main__':
    # Check if OpenAI API key is set
    logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')
    use_gpt = True
    while True:
        input_gpt = input("Do you want to use OpenAI automation (yes, no or exit)? If you write no, you will need to"
                          " enter manually the copied prompt (use chatgpt) \n")
        if input_gpt.lower() == "yes":

            if "OPENAI_API_KEY" not in os.environ:
                print("Error: OpenAI API key is not set.")
                print("Please set the environment variable 'OPENAI_API_KEY' with your OpenAI API key.")
                sys.exit()

            # Set your OpenAI API key
            openai.api_key = os.environ["OPENAI_API_KEY"]
            break
        elif input_gpt.lower() == "no":
            use_gpt = False
            break
        elif input_gpt.lower() == "exit":
            sys.exit()
        else:
            print("Pleas enter only yes, no or exit.")

    # Replace with the actual path to your CV file
    file_path = 'C:\\Users\\DanielV\\Documents\\CV\\Daniel Vishna CV.pdf'
    resume = Resume()
    CV = resume.read_file(file_path)
    if not CV:
        logging.error("There is a problem with the resume file. Please check that you entered the correct file path.")
        sys.exit()

    job = None
    url_entry = ""
    while True:
        if not job:
            while True:
                url_entry = input("Please enter the URL for the job ad from LinkedIn, or 'exit' to quit: \n")
                if url_entry.lower() == "exit":
                    break

                if is_valid_url(url_entry):
                    break
                else:
                    print("Invalid URL. Please enter a valid URL.")
            if url_entry.lower() == "exit":
                break
            job = scraping_job_data(url_entry)
        else:
            inputs = input("Enter 1 to insert a new URL, 2 to get personalize resume, 3 to get the cover letter,"
                           " or 'exit' to quit the program.\n")
            if inputs == "1":
                url_entry = input("Enter the URL:\n")
                job = scraping_job_data(url_entry)
            elif inputs == "2":
                copy_resume(job, CV, use_gpt)
            elif inputs == "3":
                copy_cover_letter(job, CV, use_gpt)
            elif inputs.lower() == "exit":
                break
