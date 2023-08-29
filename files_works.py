# import PyPDF2
import docx2txt
import logging
import fitz  # PyMuPDF



class Resume:
    def __read_pdf(self, file_path):
        """
        Reads a PDF file and extracts text from all pages.

        Args:
            file_path (str): The file path to the PDF file.

        Returns:
            str: The concatenated text extracted from all pages of the PDF,
                 or None if there was an error.
        """
        try:
            pdf_document = fitz.open(file_path)
            num_pages = pdf_document.page_count
            text = []
            for page_number in range(num_pages):
                page = pdf_document[page_number]
                text.append(page.get_text("text").strip())
            pdf_document.close()
            return '\n'.join(text)
        except FileNotFoundError as e:
            logging.error(f"Error: The file '{file_path}' does not exist.")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred while reading the PDF: {e}")
            return None

    def __read_docx(self, file_path):
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
        except FileNotFoundError as e:
            logging.error(f"Error: The file '{file_path}' does not exist.")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred while reading the docx: {e}")
            return None

    def __read_txt(self, file_path):
        """
        Reads a text file and extracts text.

        Args:
            file_path (str): The file path to the text file.

        Returns:
            str: The extracted text from the text file, or None if there was an error.
        """
        try:
            with open(file_path, "r") as f:
                text = f.read()
                return text
        except FileNotFoundError as e:
            logging.error(f"Error: The file '{file_path}' does not exist.")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred while reading the text file: {e}")
            return None

    def read_file(self, file_path):
        """
        Reads a file and extracts text content based on the file format.

        Args:
            file_path (str): The file path to the input file.

        Returns:
            str: The extracted text content, or None if there was an error.
        """
        if file_path.endswith(".docx"):
            return self.__read_docx(file_path)
        elif file_path.endswith(".pdf"):
            return self.__read_pdf(file_path)
        elif file_path.endswith(".txt"):
            return self.__read_txt(file_path)
        else:
            logging.error(f"Unsupported file format: '{file_path}' the system support only pdf, docx and txt files.")
            return None
