import PyPDF2
import tkinter as tk
from tkinter import messagebox
import pyperclip
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        text = []
        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            text.append(page.extract_text())
        return '\n'.join(text)

def copy_resume():
    title = title_entry.get()
    company = company_entry.get()
    description = description_entry.get()
    personalize_resume = f"Please personalize my resume for this {title} role at {company}.\n" \
                         f"Here is the job description: \n{description} \n" \
                         f"And here is my resume: \n {CV}"
    pyperclip.copy(personalize_resume)
    messagebox.showinfo("Personalized Resume", "Content copied to clipboard!")

def copy_cover_letter():
    title = title_entry.get()
    company = company_entry.get()
    description = description_entry.get()
    personalize_CL = f"Please write a personalized cover letter for this {title} role at {company}.\n" \
                     f"Here is the job description: \n{description} \n" \
                     f"And here is my resume: \n {CV}"
    pyperclip.copy(personalize_CL)
    messagebox.showinfo("Personalized Cover Letter", "Content copied to clipboard!")


if __name__ == '__main__':
    file_path = 'C:\\Users\\DanielV\\Documents\\CV\\Daniel Vishna CV.pdf'  # Replace with the actual path to your CV file
    CV = read_pdf(file_path)
    window = tk.Tk()
    window.title("Personalized Resume Generator")
    text_generat_b = "Generate"
    title_label = tk.Label(window, text="Enter the title:")
    title_label.pack()
    title_entry = tk.Entry(window)
    title_entry.pack()
    company_label = tk.Label(window, text="Enter the company name:")
    company_label.pack()
    company_entry = tk.Entry(window)
    company_entry.pack()
    description_label = tk.Label(window, text="Enter the description:")
    description_label.pack()
    description_entry = tk.Entry(window)
    description_entry.pack()
    generate_CV = tk.Button(window, text="Copy Resume", command=copy_resume)
    generate_CV.pack()
    generate_CV = tk.Button(window, text="Copy Cover Letter", command=copy_cover_letter)
    generate_CV.pack()
    window.mainloop()

