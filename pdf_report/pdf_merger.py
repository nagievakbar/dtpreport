import PyPDF2
from django.core.files.base import ContentFile
from fitz import Rect, fitz
from flask_qrcode import QRcode

from makereport.models import Documents, Report

from pdf_report.utils import check_qr_code


class PDFInputImage:
    def __init__(self, pdf_file_path: str, qr_code: str):
        if qr_code is None:
            raise ValueError('qr_code cannot be null')
        self._qr_code = QRcode.qrcode(qr_code, mode='raw')
        self._pdf_file = fitz.open(pdf_file_path)
        self._origin_path = pdf_file_path

    def insert_images(self):
        image_rectangle = Rect(530, 770, 590, 830)
        for i in range(0, self._pdf_file.pageCount):
            page = self._pdf_file[i]
            page.insertImage(image_rectangle, stream=self._qr_code)
            self._pdf_file.save(self._origin_path, encryption=False, incremental=True)


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

    # I will use pdf writer for creating merged pdf
    def write_first_pdf(self) -> int:
        pdf_file = self.report_model.pdf_report
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
