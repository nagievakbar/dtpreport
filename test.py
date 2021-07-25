from fitz import fitz, Rect
from flask_qrcode import QRcode

input_file = "mixing.pdf"
output_file = "example-with-barcode.pdf"
barcode_file = "asd.png"


# # define the position (upper-right corner)
# image_rectangle = Rect(500, 700, 600, 900)
# img = open('asd.png', 'rb').read()
# # retrieve the first page of the PDF
# file_handle = fitz.open(input_file)
# first_page = file_handle[0]
#
# # add the image
# first_page.insertImage(image_rectangle, stream=img)
#
# file_handle.save('mixing.pdf', incremental=True ,encryption=
import PyPDF2
from django.core.files.base import ContentFile
from fitz import Rect, fitz
from flask_qrcode import QRcode

from makereport.models import Documents, Report

from pdf_report.utils import check_qr_code


class PDFInputImage:
    def __init__(self, pdf_file_path: str, qr_code_user: str, qr_code_company: str):
        self._qr_code_user = qr_code_user
        self._qr_code_company = qr_code_company
        self._pdf_file = fitz.open(pdf_file_path)
        self._origin_path = pdf_file_path
        self.padding = 10
        self.width = 50
        self.height = 50

    def add_signs(self) -> bytes:
        # adds user sign
        self.insert_images(sign='sadsadasd asdsadas', number_pages=self._pdf_file.page_count,
                           location_sign=self.calculate_location_sign_user)
        # adds company sign
        self.insert_images(sign='ASdsadsasdsa asdsads', number_pages=1,
                           location_sign=self.calculate_location_sign_company)
        return self._pdf_file.write()

    # fix this error!!!
    def insert_images(self, sign, number_pages, location_sign):
        if sign is not None:
            sign = QRcode.qrcode(sign, mode='raw')
            for i in range(0, number_pages):
                page = self._pdf_file[i]
                size_page = page.rect
                image_rectangle = location_sign(size_page)
                page.insertImage(image_rectangle, stream=sign)

    # def insert_images(self):
    #     if qr_code_user is None:
    #         raise ValueError('qr_code cannot be null')
    #     if qr_code_company is None:
    #         raise ValueError('qr_code cannot be null')
    #     for i in range(0, self._pdf_file.page_count):
    #         page = self._pdf_file[i]
    #         size_page = page.rect
    #         image_rectangle = self.calculate_location_sign_user(size_page)
    #         page.insertImage(image_rectangle, stream=self._qr_code_user)
    #         if i == 0:
    #             image_sign_company = self.calculate_location_sign_company()
    #             page.insertImage(image_sign_company, stream=self._qr_code_company)
    #     return self._pdf_file.write()

    def calculate_location_sign_user(self, react: Rect):
        return Rect(react.width - self.width - self.padding,
                    react.height - self.width - self.padding,
                    react.width - self.padding,
                    react.height - self.padding)

    def calculate_location_sign_company(self, *args, **kwargs):
        return Rect(self.padding,
                    self.padding,
                    self.width + self.padding,
                    self.height + self.padding)


class PDFMerger:
    def __init__(self, id: int):
        self.report_model = Report.objects.get(report_id=id)
        self.pdf_writer = PyPDF2.PdfFileWriter()

    def concatenate_pdf(self):
        number_pages = self.write_first_pdf()
        self.create_and_write_second_pdf(number_pages)
        self.store_pdf()

    def create_and_write_second_pdf(self, number_pages: int):
        pdf_second = self.create_second_pdf(number_pages)
        self.write_second_pdf(pdf_second)

    # add images and returns bytes objects
    def return_prepared_first_pdf_adding_signs(self) -> bytes:
        sign_put = PDFInputImage(pdf_file_path=self.report_model.pdf_report.path,
                                 qr_code_user=self.report_model.pdf_qr_code_user,
                                 qr_code_company=self.report_model.pdf_qr_code_company)
        return sign_put.add_signs()

    # I will use pdf writer for creating merged pdf
    def write_first_pdf(self) -> int:
        pdf_file = open(self.return_prepared_first_pdf_adding_signs(), 'rb')
        pdf_first_reader = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = pdf_first_reader.numPages
        self._write(pdf_first_reader)
        return number_of_pages

    def _write(self, reader: PyPDF2.PdfFileReader):
        for page_num in range(reader.numPages):
            page_obj = reader.getPage(page_num)
            self.pdf_writer.addPage(page_obj)

    def create_second_pdf(self, number_pages: int) -> ContentFile:
        holds_images = self.report_model.holds_images
        images = holds_images.image.all()
        passport = holds_images.pp_photo.all()
        checks = holds_images.checks.first()
        other_photos = holds_images.o_images.all()
        document_photo = Documents.objects.first()
        from DTPreport import settings as s
        context = {
            'number_of_pages': number_pages,
            's': s.BASE_URL,
            'images': images,
            'document_photo': document_photo,
            'passport': passport,
            'checks': checks,
            'other_photos': other_photos,
        }
        from pdf_report.utils import generate_pdf
        pdf = generate_pdf(context=context, default_template="disposable.html",
                           css_name="report.css")
        return ContentFile(pdf)

    def write_second_pdf(self, pdf_second: ContentFile):
        pdf_second_reader = PyPDF2.PdfFileReader(pdf_second)
        self._write(pdf_second_reader)
        pdf_second.close()

    def store_pdf(self):
        pdf_output = ContentFile(bytes())
        self.pdf_writer.write(pdf_output)
        self.report_model.save_created_pdf(pdf_output)
