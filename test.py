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
def check_qr_code(qrcode: str):
    return QRcode.qrcode(qrcode) if qrcode is not None else None


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


file = PDFInputImage(pdf_file_path='', qr_code="sda")
file.insert_images()
