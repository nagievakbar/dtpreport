from django.contrib import admin
from django.urls import path, include
from .views import *
from .tasks import get_base

urlpatterns = [
    path('<int:id>/', GeneratePDF.as_view(), name='get_response'),
    path('mixing/<int:id>', finish_view, name='get_mixing'),
    path('agreement/<int:id>', agreement_view, name='get_agreement'),
    path('additional/<int:id>/', GenerateAdditional.as_view(), name='get_additional'),
    path("download_xml/", get_base_template, name='download_xml'),
    path("make_pdf/", get_base, name='make_pdf'),
    path("make_pdf_additional/", get_base_additional_template, name='make_pdf_additional'),
    path("download_xml_mixing/", get_base_mixing_template, name='download_xml_mixing'),
    path("download_xml_agreement/", get_base_agreement_template, name='download_xml_agreement'),
    path("download_xml_additional/", get_base_additional_template, name="download_xml_additional"),
    path("test_finish/<int:id>", finish_view),
    path("test_agreement/<int:id>", agreement_view),
    path("test_report/<int:id>", test_report),
    # new methods which have to implemented
    path('enumeration/<int:id>/', ShowEnumerationPDF.as_view(), name='get_enumeration'),
    path('disposable/<int:id>/', ShowDisposablePDF.as_view(), name='get_disposable'),
    path('closing/<int:id>/', closing_pdf, name='get_closing'),

]
