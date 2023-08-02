import sys
import time
from selenium import webdriver
import random
import re
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, InvalidArgumentException
from selenium.webdriver.common.by import By
import PyPDF2
import pyperclip
import os
import openai
from collections import namedtuple
import docx2txt
import urllib.parse

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
    """
      Reads a PDF file and extracts text from all pages.

      Args:
          file_path (str): The file path to the PDF file.

      Returns:
          str: The concatenated text extracted from all pages of the PDF, or None if there was an error.
      """
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            text = []
            for page_number in range(num_pages):
                page = pdf_reader.pages[page_number]
                text.append(page.extract_text().strip())
            return '\n'.join(text)
    except PyPDF2.utils.PdfReadError as e:
        print(f"Error while reading the PDF: {e}")
        return None
    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' does not exist.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading the PDF: {e}")
        return None


def read_word(file_path):
    """
    Reads a docx file and extracts text.

    Args:
        file_path (str): The file path to the docx file.

    Returns:
        str: The extracted text from the docx, or None if there was an error.
    """
    try:
        text = docx2txt.process(file_path)
        return text
    except docx2txt.exceptions.DocxInvalidFileError as e:
        print(f"Error while reading the docx: {e}")
        return None
    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' does not exist.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading the docx: {e}")
        return None


def read_file(file_path):
    if file_path[-5:] == ".docx" or file_path[-4:] == ".doc":
        return read_word(file_path)
    elif file_path[-4:] == ".pdf":
        return read_pdf(file_path)
    else:
        return None


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
        description = driver.find_elements(By.XPATH, description_tag)[0].text[:-9]  # Remove last 9 characters
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


def create_promt(job, cv, is_cove_letter=True):
    promt = f"{job.title} role at {job.company}.\nHere is the job description: \n{job.description}\n" \
            f"And here is my resume: \n {cv}".replace("  ", " ").replace("\n\n", "\n")
    if is_cove_letter:
        promt = "Please write a personalized cover letter for this " + promt
    else:
        promt = "Please personalize my resume for this " + promt
    return promt


def copy_resume(job, cv):
    """
    Copies a personalized resume and job description to the clipboard.

    Args:
        job (Job): A named tuple containing job information (title, company, description).
        cv (str): The content of the resume to be copied.
    """
    personalize_resume = create_promt(job, cv, False)
    pyperclip.copy(personalize_resume)
    print("Content copied to clipboard!")


def copy_cover_letter(job, cv):
    """
    Copies a personalized cover letter to the clipboard.

    Args:
        job (Job): A named tuple containing job information (title, company, description).
        cv (str): The content of the resume to be included in the cover letter.
    """
    personalize_CL = create_promt(job, cv)
    system_content = 'You are a recruitment consultant who helps candidates write cover letters for jobs.' \
                     'Help them stand out for the job even if they don\'t meet all the job requirements.'

    # Use OpenAI GPT-3.5 Turbo model to generate the cover letter content
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "system", "content": system_content},
                                                             {"role": "user", "content": personalize_CL}])
    answer = chat_completion['choices'][0]['message']['content']
    pyperclip.copy(answer)
    print("Content copied to clipboard!")


def is_valid_url(url):
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


if __name__ == '__main__':
    # Check if OpenAI API key is set
    if "OPENAI_API_KEY" not in os.environ:
        print("Error: OpenAI API key is not set.")
        print("Please set the environment variable 'OPENAI_API_KEY' with your OpenAI API key.")
        sys.exit(1)

    # Set your OpenAI API key
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # Replace with the actual path to your CV file
    file_path = 'C:\\Users\\DanielV\\Documents\\CV\\Daniel Vishna CV.docx'
    CV = read_file(file_path)
    if not CV:
        print("There is a problem with the resume file. Please check that you entered the correct file path.")
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
            print("Enter 1 to insert a new URL, 2 to copy the resume, 3 to get the cover letter, or 'exit' to quit the "
                  "program.")
            inputs = input()
            if inputs == "1":
                url_entry = input("Enter the URL:\n")
                job = scraping_job_data(url_entry)
            elif inputs == "2":
                copy_resume(job, CV)
            elif inputs == "3":
                copy_cover_letter(job, CV)
            elif inputs.lower() == "exit":
                break
