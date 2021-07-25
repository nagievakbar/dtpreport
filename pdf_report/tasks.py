import datetime

from celery import shared_task
from django.core.files.base import ContentFile
from django.http import JsonResponse
from PIL import Image

from pdf_report.pdf_merger import PDFMerger, PDFInputImage
from pdf_report.views import generate_pdf_report, generate_pdf_enumeration
from django.db.models import Q
from makereport.models import TemplateBase, Report, TemplateAdditional, Enumeration


@shared_task(name="reduce_image")
def reduce_image(path):
    image_opened = Image.open(path)
    width, height = image_opened.size
    image_opened = image_opened.resize((int(width / 2), int(height / 2)), Image.ANTIALIAS)
    image_opened.save(path, quality=10)


def get_base(request):
    try:
        id = request.GET.get('id', 0)
        make_pdf.delay(id)
    except Report.DoesNotExist:
        pass
    return JsonResponse({})


def get_additional_pdf(request):
    try:
        id = request.GET.get('id', 0)
        make_pdf_additional.delay(id)
    except Report.DoesNotExist:
        pass
    return JsonResponse({})


@shared_task(name="delete_empty")
def delete_empty_report():
    report = Report.objects.filter((Q(key__isnull=True) | Q(key__exact='')))
    for rep in report.all():
        rep.delete()


@shared_task(name="make_pdf")
def make_pdf(id):
    obj = TemplateBase
    new_report_pdf = Report.objects.get(report_id=id)
    data = generate_pdf_report(id, obj=obj)
    filename = "main_{}.pdf".format(new_report_pdf.report_id)
    new_report_pdf.save_pdf(filename, data)


@shared_task(name="make_pdf_additional")
def make_pdf_additional(id):
    obj = TemplateAdditional
    new_report_pdf = Report.objects.get(report_id=id)
    data = generate_pdf_report(id, obj=obj)
    filename = "second_{}.pdf".format(new_report_pdf.report_id)
    new_report_pdf.save_additional_pdf(filename, data)


@shared_task(name="make_pdf_enumeration")
def make_pdf_enumeration(id):
    obj = TemplateBase
    new_report_pdf = Enumeration.objects.get(report_id=id)
    data = generate_pdf_enumeration(id, obj=obj)
    filename = "main_enumeration_{}.pdf".format(new_report_pdf.report_id)
    new_report_pdf.save_pdf_enumeration(filename, data)


@shared_task(name='concatenate_pdf_disposable')
def concatenate_pdf_disposable(id: int):
    manger = PDFMerger(id)
    manger.concatenate_pdf()


import PyPDF2

from io import BytesIO
