import time
from selenium import webdriver
import random
from selenium.webdriver.common.by import By
# import docx
import PyPDF2
import tkinter as tk
from tkinter import messagebox
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


# def read_docx(file_path):
#     doc = docx.Document(file_path)
#     text = []
#     for paragraph in doc.paragraphs:
#         text.append(paragraph.text)
#     return '\n'.join(text)


def generate_personalized_resume():
    global pr
    global personalized_resume
    global text_generat_b
    global personalize_resume
    global personalize_CL
    url = url_entry.get()
    time.sleep(random.uniform(0.0, 1.0))
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Edge(options=op)
    driver.get(url)
    titel = driver.find_elements(By.XPATH,
                                 "//h1[@class='top-card-layout__title font-sans text-lg papabear:text-xl font-bold "
                                 "leading-open text-color-text mb-0 topcard__title']")[0].text
    time.sleep(random.uniform(0.0, 0.6))
    compeny = driver.find_elements(By.XPATH, "//a[@class='topcard__org-name-link topcard__flavor--black-link']")[0].text
    time.sleep(random.uniform(0.0, 0.3))
    button = driver.find_elements(By.XPATH,
                                  "//button[@class='show-more-less-html__button show-more-less-html__button--more']")
    button[0].click()
    time.sleep(random.uniform(0.0, 0.9))
    dis = driver.find_elements(By.XPATH, "//div[@class='description__text description__text--rich']")[0].text[:-9]
    time.sleep(random.uniform(0.0, 1.5))
    driver.quit()
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
    generate_CV = tk.Button(window, text="Copy Resume", command=copy_resume)
    generate_CV.pack()
    generate_CV = tk.Button(window, text="Copy Cover Letter", command=copy_cover_letter)
    generate_CV.pack()
    text_generat_b = "New Generate"


def copy_resume():
    pyperclip.copy(personalize_resume)
    messagebox.showinfo("Personalized Resume", "Content copied to clipboard!")

def copy_cover_letter():
    pyperclip.copy(personalize_CL)
    messagebox.showinfo("Personalized Cover Letter", "Content copied to clipboard!")


if __name__ == '__main__':
    # Create the GUI window
    personalize_resume = ""
    personalize_CL = ""
    window = tk.Tk()
    window.title("Personalized Resume Generator")
    text_generat_b = "Generate"

    # Create URL input label and entry field
    url_label = tk.Label(window, text="Enter the URL:")
    url_label.pack()
    url_entry = tk.Entry(window)
    url_entry.pack()

    # Create generate button
    generate_button = tk.Button(window, text=text_generat_b, command=generate_personalized_resume)
    generate_button.pack()

    # Run the GUI event loop
    window.mainloop()

