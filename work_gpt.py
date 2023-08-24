import os
import sys
import time
import random
import logging
import pyperclip
import urllib.parse
from collections import namedtuple
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, InvalidArgumentException
from selenium.webdriver.common.by import By
import openai

# Importing the Resume class from the files_works module
from files_works import Resume

# Define a named tuple 'Job' to represent job information (title, company, description)
Job = namedtuple('Job', ['title', 'company', 'description'])


# Define custom exceptions

class ScrapingError(Exception):
    """Custom exception for scraping errors."""


class InvalidURLException(ScrapingError):
    """Exception raised for invalid URL."""


class PageElementNotFoundError(ScrapingError):
    """Exception raised when a required page element is not found."""


class PageLoadError(ScrapingError):
    """Exception raised when there is an issue loading the page."""


def scraping_job_data(url):
    """
    Scrapes job information from a given URL.

    Args:
        url (str): The URL of the job posting on LinkedIn.

    Returns:
        Job or None: A named tuple representing job information (title, company, description) if successful, otherwise None.
    """
    # Set up the Edge web driver in headless mode
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument('headless')
    edge_options.add_argument("--incognito")
    driver = webdriver.Edge(options=edge_options)
    try:
        if not is_valid_url(url):
            raise InvalidURLException("Invalid URL")
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

        logging.debug("Extracted title: %s", title)
        logging.debug("Extracted company: %s", company)
        logging.debug("Extracted description: %s", description)

        return Job(title, company, description)
    except InvalidURLException:
        # Handle InvalidURLException
        logging.error("Invalid URL format.")
        raise InvalidURLException("Invalid URL format.")
    except (NoSuchElementException, NoSuchAttributeException) as e:
        # Handle PageElementNotFoundError
        logging.error("Unable to find required job elements on the page: %s", e)
        raise PageElementNotFoundError("Unable to find required job elements on the page.")
    except InvalidArgumentException as e:
        # Handle PageLoadError
        logging.error("Failed to load the page: %s", e)
        raise PageLoadError("Failed to load the page.")
    except Exception as e:
        # Handle other ScrapingError
        logging.error("An unexpected error occurred: %s", e)
        raise ScrapingError("An unexpected error occurred.")
    finally:
        driver.quit()


def create_prompt(job, content_cv, is_cover_letter=True):
    """
    Creates a prompt for generating personalized content.

    Args:
        job (Job): A named tuple containing job information (title, company, description).
        content_cv (str): The content of the resume to be copied.
        is_cover_letter (bool): Whether the prompt is for a cover letter (True) or resume (False).

    Returns:
        str: A formatted prompt for generating content.
    """
    prompt = (
        f"{job.title} role at {job.company}.\n"
        "Here is the job description:\n"
        f"<job description>{job.description}<\\job description>\n"
        "And here is my resume:\n"
        f"<resume>{content_cv}<\\resume>"
    )

    # Clean up the prompt
    prompt = prompt.replace("  ", " ").replace("\n\n", "\n")
    if is_cover_letter:
        prompt = "Please write a personalized cover letter for this " + prompt
    else:
        prompt = "Please personalize my resume for this " + prompt
    return prompt


def call_gpt(system_content, user_content):
    """
    Calls the GPT model to generate content.

    Args:
        system_content (str): The system instruction for GPT.
        user_content (str): The user's input content.

    Returns:
        None
    """
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "system", "content": system_content},
                                                             {"role": "user", "content": user_content}])
    answer = chat_completion['choices'][0]['message']['content']
    pyperclip.copy(answer)


def copy_resume(job, content_cv, use_gpt):
    """
    Copies a personalized resume or prompt to the clipboard.

    Args:
        job (Job): A named tuple containing job information (title, company, description).
        content_cv (str): The content of the resume to be copied.
        use_gpt (bool): Whether to use GPT model for content generation.
    """
    system_content = "You are a skilled resume personalization expert. Your expertise lies in customizing candidate " \
                     "resumes to fit specific job roles, even when their qualifications may not perfectly match the " \
                     "requirements. You will receive candidate resumes and job descriptions marked up with XML " \
                     "tags.Your objective is to personalize and ensure candidates' resumes are tailored effectively," \
                     " showcasing their relevant skills and experiences for each job."
    personalize_resume = create_prompt(job, content_cv, False)
    if use_gpt:
        call_gpt(system_content, personalize_resume)
        print("Personalized resume copied to clipboard!")
    else:
        pyperclip.copy(system_content + "\n" + personalize_resume)
        print("Personalized resume prompt copied to clipboard!")


def copy_cover_letter(job, content_cv, use_gpt):
    """
    Copies a personalized cover letter or prompt to the clipboard.

    Args:
        job (Job): A named tuple containing job information (title, company, description).
        content_cv (str): The content of the resume to be included in the cover letter.
        use_gpt (bool): Whether to use GPT model for content generation.
    """
    cover_letter = create_prompt(job, content_cv)

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
    """
    Checks if a URL is valid.

    Args:
        url (str): The URL to be validated.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def to_use_gpt():
    """
    Asks the user whether to use OpenAI GPT for automation.

    Returns:
        bool: True if GPT is to be used, False otherwise.
    """
    while True:
        input_gpt = input("Enter 'yes' to use OpenAI automation, 'no' to manually enter prompts, or 'exit' to quit: ")

        if input_gpt.lower() == "yes":
            check_openai_api_key()
            return True
        elif input_gpt.lower() == "no":
            return False
        elif input_gpt.lower() == "exit":
            sys.exit()
        else:
            print("Invalid input. Please enter only 'yes', 'no', or 'exit'.")


def check_openai_api_key():
    """
    Checks if the OpenAI API key is set in the environment variables.
    Exits if the key is not set.
    """
    if "OPENAI_API_KEY" not in os.environ:
        logging.error("Error: OpenAI API key is not set.")
        logging.error("Please set the environment variable 'OPENAI_API_KEY' with your OpenAI API key.")
        sys.exit()
    # Set your OpenAI API key
    openai.api_key = os.environ["OPENAI_API_KEY"]


def get_job(url):
    """
    Retrieves job information by scraping a given URL.

    Args:
        url (str): The URL of the job posting.

    Returns:
        Job or None: A named tuple representing job information if successful, otherwise None.
    """
    try:
        return scraping_job_data(url)
    except InvalidURLException as e:
        logging.error(f"Invalid URL: {e}")
    except PageElementNotFoundError as e:
        logging.error(f"Page element not found: {e}")
    except PageLoadError as e:
        logging.error(f"Page load error: {e}")
    except ScrapingError as e:
        logging.error(f"Scraping error: {e}")


def get_resume_content(file_path):
    """
    Reads and retrieves content from a resume file.

    Args:
        file_path (str): The path to the resume file.

    Returns:
        str: The content of the resume.
    """
    resume = Resume()
    cv_content = resume.read_file(file_path)
    if not cv_content or len(cv_content) == 0:
        logging.error("There is a problem with the resume file. Please check that you entered the correct file path.")
        sys.exit()
    return cv_content


def main():
    """
    Main program loop.
    """
    # Check if OpenAI API key is set
    logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

    # Check if the OPENAI_API_KEY environment variable is set
    use_gpt = to_use_gpt()

    # Replace with the appropriate directory and file name
    file_directory = 'C:/Users/DanielV/Documents/CV'
    file_name = 'Daniel Vishna CV.pdf'

    # Use os.path.join() to construct the file path
    file_path = os.path.join(file_directory, file_name)

    cv_content = get_resume_content(file_path)
    job = None
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
            job = get_job(url_entry)
        else:
            user_input = input("Enter 1 to insert a new URL, 2 to get personalize resume, 3 to get the cover letter,"
                               " or 'exit' to quit the program.\n")
            if user_input == "1":
                url_entry = input("Enter the URL:\n")
                job = get_job(url_entry)
            elif user_input == "2":
                copy_resume(job, cv_content, use_gpt)
            elif user_input == "3":
                copy_cover_letter(job, cv_content, use_gpt)
            elif user_input.lower() == "exit":
                break


if __name__ == '__main__':
    main()
