import unittest
from files_works import Resume

class TestResume(unittest.TestCase):
    def setUp(self):
        # Create an instance of the Resume class for testing
        self.resume = Resume()

    def test_read_pdf(self):
        # Test reading a valid PDF file
        pdf_path = "test_files/Daniel Vishna CV.pdf"
        text = self.resume.read_file(pdf_path)
        self.assertIsNotNone(text)
        self.assertTrue(isinstance(text, str))

        # Test reading a non-existing PDF file
        invalid_pdf_path = "test_files/non_existing.pdf"
        text = self.resume.read_file(invalid_pdf_path)
        self.assertIsNone(text)

    def test_read_docx(self):
        # Test reading a valid DOCX file
        docx_path = "test_files/Daniel Vishna CV.docx"
        text = self.resume.read_file(docx_path)
        self.assertIsNotNone(text)
        self.assertTrue(isinstance(text, str))

        # Test reading a non-existing DOCX file
        invalid_docx_path = "test_files/non_existing.docx"
        text = self.resume.read_file(invalid_docx_path)
        self.assertIsNone(text)

    def test_read_txt(self):
        # Test reading a valid TXT file
        txt_path = "test_files/Daniel Vishna CV.txt"
        text = self.resume.read_file(txt_path)
        self.assertIsNotNone(text)
        self.assertTrue(isinstance(text, str))

        # Test reading a non-existing TXT file
        invalid_txt_path = "test_files/non_existing.txt"
        text = self.resume.read_file(invalid_txt_path)
        self.assertIsNone(text)

    def test_read_file(self):
        # Test reading a valid file
        pdf_path = "test_files/Daniel Vishna CV.txt"
        text = self.resume.read_file(pdf_path)
        self.assertIsNotNone(text)
        self.assertTrue(isinstance(text, str))


        # Test reading a non-existing file
        invalid_file_fourmt = "Daniel Vishna CV.tx"
        text = self.resume.read_file(invalid_file_fourmt)
        self.assertIsNone(text)

if __name__ == '__main__':
    unittest.main()
