import time
from selenium import webdriver
import random
from selenium.webdriver.common.by import By
import PyPDF2
import pyperclip

personalized_resume = False
pr = ""


def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        text = []
        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            text.append(page.extract_text())
        return '\n'.join(text)


def generate_personalized_resume():
    global pr
    global personalized_resume
    global personalize_resume
    global personalize_CL
    url = url_entry
    try:
        time.sleep(random.uniform(0.0, 1.0))
        op = webdriver.EdgeOptions()
        op.add_argument('headless')
        driver = webdriver.Edge(options=op)
        driver.get(url)
        titel = driver.find_elements(By.XPATH,
                                     "//h1[@class='top-card-layout__title font-sans text-lg papabear:text-xl font-bold "
                                     "leading-open text-color-text mb-0 topcard__title']")[0].text
        time.sleep(random.uniform(0.0, 0.6))
        compeny = driver.find_elements(By.XPATH, "//a[@class='topcard__org-name-link topcard__flavor--black-link']")[0].text
        time.sleep(random.uniform(0.0, 0.3))
        button = driver.find_elements(By.XPATH, '//button[text()="\n        Show more\n\n        "]')
        button[0].click()
        time.sleep(random.uniform(0.0, 0.9))
        dis = driver.find_elements(By.XPATH, "//div[@class='description__text description__text--rich']")[0].text[:-9]
        time.sleep(random.uniform(0.0, 1.5))
        driver.quit()
    except:
        print("There is problem in using selenium")
    file_path = 'C:\\Users\\DanielV\\Documents\\CV\\Daniel Vishna CV.pdf'  # Replace with the actual path to your CV file
    CV = read_pdf(file_path)
    personalize_resume = f"Please personalize my resume for this {titel} role at {compeny}.\n" \
                         f"Here is the job description: \n{dis} \n" \
                         f"And here is my resume: \n {CV}"
    pr = personalize_resume
    # pyperclip.copy(personalize_resume)
    personalize_CL = f"Please write a personalized cover letter for this {titel} role at {compeny}.\n" \
                     f"Here is the job description: \n{dis} \n" \
                     f"And here is my resume: \n {CV}"

    personalized_resume = True


def copy_resume():
    pyperclip.copy(personalize_resume)
    print("Content copied to clipboard!")


def copy_cover_letter():
    pyperclip.copy(personalize_CL)
    print("Content copied to clipboard!")


if __name__ == '__main__':
    inputs = "1"
    personalize_resume = ""
    personalize_CL = ""

    while True:
        print("enter 1 for insert new url\nenter 2 for copy the resume\nand 3 for get the cover letter\nfor brake "
              "enter anything else")
        inputs = input()
        if inputs == "1":
            url_entry = input("enter the url\n")
            generate_personalized_resume()
        elif inputs == "2":
            copy_resume()
        elif inputs == "3":
            copy_cover_letter()
        else:
            break

