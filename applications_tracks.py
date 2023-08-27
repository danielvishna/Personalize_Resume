import os

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side
from datetime import date


from job import scraping_job_data, Job


def style(sheet, job):
    # Add hyperlink to the "Link for the job ad" cell
    sheet.cell(row=sheet.max_row, column=6).hyperlink = job.url
    sheet.cell(row=sheet.max_row, column=6).font = Font(color="000000FF", underline="single")

    sheet.cell(row=sheet.max_row, column=3).hyperlink = job.get_company_link()
    sheet.cell(row=sheet.max_row, column=3).font = Font(color="000000FF", underline="single")

    # Apply border styling to the cells in the new row
    new_row = sheet[sheet.max_row]
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'),
                    bottom=Side(style='thin'))
    for cell in new_row:
        cell.border = border


def create_or_append_excel(file, job):
    headers = ["No", "Title", "Company", "Location", "Date of send", "Link for the ad job"]
    # Check if the file exists
    try:
        workbook = openpyxl.load_workbook(file)
        sheet = workbook.active
    except FileNotFoundError:
        # Create a new workbook and add headers
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(headers)
        border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'),
                        bottom=Side(style='thin'))
        font = Font(bold=True)
        for cell in sheet["1:1"]:
            cell.font = font
            cell.border = border
        #todo: add exception for open file
    data = [sheet.max_row, job.get_title(), job.get_company_name(), job.get_location(),
            (date.today()).strftime("%d/%m/%Y"), job.get_title() + " " + job.get_company_name()]
    # Add data to the sheet
    sheet.append(data)

    # # Add hyperlink to the "Link for the job ad" cell
    # sheet.cell(row=sheet.max_row, column=5).hyperlink = job.url
    # sheet.cell(row=sheet.max_row, column=5).font = Font(color="000000FF", underline="single")
    style(sheet, job)

    # Save the workbook
    workbook.save(file)

# def create_excel(file_path, headers):
#     workbook = Workbook()
#     sheet = workbook.active
#     sheet.append(headers)
#     for cell in sheet["1:1"]:
#         cell.font = Font(bold=True)
#     workbook.save(file_path)
#
#
# def get_number_of_rows(file_path):
#     try:
#         my_file = Path(file_path)
#         if not my_file.is_file():
#             return 1
#
#         workbook = openpyxl.load_workbook(file_path)
#         sheet = workbook.active
#         return sheet.max_row
#     except FileNotFoundError:
#         return 0  # File doesn't exist, so there are 0 rows


# def prepare_row_data(file_path, url):
#     job_data = scraping_job_data(url)
#     row_number = get_number_of_rows(file_path)
#     if row_number == 0:
#         row_number = 1
#     formatted_date = (date.today()).strftime("%d/%m/%Y")
#
#     row_data = [
#         str(row_number),
#         job_data.title,
#         job_data.company,
#         formatted_date,
#         job_data.url
#     ]
#
#     return row_data



if __name__ == '__main__':
    file_directory = 'C:/Users/DanielV/Documents/CV'
    file_name = 'Applications Tracks.xlsx'
    file_path = os.path.join(file_directory, file_name)
    # my_file = Path(file_path)

    # if not my_file.is_file():
    #     create_excel(file_path, headers)

    url = "https://www.linkedin.com/jobs/view/3651370729/?refId=b1f0bebf-cbd0-473a-b2b8-5a074d8588a2&trackingId=fPeyjCpxRzGwQoUqkW5Kbw%3D%3D"
    job_data = Job("d", 'Fortinet', 'Backend Developer', 'https://www.linkedin.com/jobs/view/3651370729/?refId=b1f0bebf-cbd0-473a-b2b8-5a074d8588a2&trackingId=fPeyjCpxRzGwQoUqkW5Kbw%3D%3D') #scraping_job_data(url)

    create_or_append_excel(file_path, job_data)