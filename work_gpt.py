import time
from selenium import webdriver
import random
from selenium.webdriver.common.by import By
import PyPDF2
import pyperclip
import os
import openai

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
    global personalize_resume
    global personalize_CL
    url = url_entry
    try:
        time.sleep(random.uniform(0.0, 0.3))
        op = webdriver.EdgeOptions()
        op.add_argument('headless')
        op.add_argument("--incognito")
        driver = webdriver.Edge(options=op)
        driver.get(url)
        titel = driver.find_elements(By.XPATH,
                                     "//h1[@class='top-card-layout__title font-sans text-lg papabear:text-xl font-bold "
                                     "leading-open text-color-text mb-0 topcard__title']")[0].text
        time.sleep(random.uniform(0.0, 0.2))
        compeny = driver.find_elements(By.XPATH, "//a[@class='topcard__org-name-link topcard__flavor--black-link']")[0].text
        time.sleep(random.uniform(0.0, 0.1))
        button = driver.find_elements(By.XPATH, '//button[text()="\n        Show more\n\n        "]')
        button[0].click()
        time.sleep(random.uniform(0.0, 0.4))
        dis = driver.find_elements(By.XPATH, "//div[@class='description__text description__text--rich']")[0].text[:-9]
        driver.quit()
    except:
        print("There is problem in using selenium")
        return
    file_path = 'C:\\Users\\DanielV\\Documents\\CV\\Daniel Vishna CV.pdf'  # Replace with the actual path to your CV file
    CV = read_pdf(file_path)
    personalize_resume = f"Please personalize my resume for this {titel} role at {compeny}.\n" \
                         f"Here is the job description: \n{dis} \n" \
                         f"And here is my resume: \n {CV}"
    personalize_CL = f"Please write a personalized cover letter for this {titel} role at {compeny}.\n" \
                     f"Here is the job description: \n{dis} \n" \
                     f"And here is my resume: \n {CV}"



def copy_resume():

    pyperclip.copy(personalize_resume)
    print("Content copied to clipboard!")


def copy_cover_letter():
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "system", "content": "You are a recruitment "
                                                                                           "consultant who helps "
                                                                                           "candidates write cover "
                                                                                           "letters for jobs. Help "
                                                                                           "them stand out for the "
                                                                                           "job even if they don't "
                                                                                           "meet all the job "
                                                                                           "requirements."},
                                                             {"role": "user", "content": personalize_CL}])
    answer = chat_completion['choices'][0]['message']['content']
    pyperclip.copy(answer)
    print("Content copied to clipboard!")


if __name__ == '__main__':
    personalize_resume = ""
    personalize_CL = ""
    openai.api_key = os.environ["OPENAI_API_KEY"]
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "user", "content": "Hello world"}])



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

