from django.urls import path
from .views import *
from .utils import *

urlpatterns = [
    path('list', reports_list, name='reports_list'),
    path('create/', ReportView.as_view(), name='new_report'),
    path('<str:extend>/<int:id>', ReportView.as_view(), name='extend_report'),
    path('<int:id>/edit/', ReportView.as_view(), name='edit_report'),
    path('report/delete/', delete, name='delete_report'),
    path('user_settings/', UserSettingsView.as_view(), name='user_settings'),
    path(r'ajax/get_service_ajax/', get_service_ajax, name='get_service_ajax'),
    path(r'ajax/get_service_cost/', get_service_cost, name='get_service_cost'),
    path(r'ajax/get_product_ajax/', get_product_ajax, name='get_product_ajax'),
    path(r'ajax/get_product_cost/', get_product_cost, name='get_product_cost'),
    path(r'ajax/get_consumable_cost/', get_consumable_cost, name='get_consumable_cost'),
    path(r'ajax/get_consumable_ajax/', get_consumable_ajax, name='get_consumable_ajax'),
    path(r'ajax/get_wear_ajax/', get_wear_ajax, name='get_wear_ajax'),
    path(r'ajax/get_car_card/', get_car_card, name='get_car_card'),
    path(r'ajax/get_btn_to_download/', get_btn_to_download, name='get_btn_to_download'),
    path(r'ajax/verifyPkcs7/', verifyPkcs7, name='verifyPkcs7'),
    # created new url for signing , though it is not implemented yet
    path(r'ajax/verifyPkcs7/closing', verifyPkcs7Closing, name='verifyPkcs7Closing'),
    path('user_settings/get_template/base', get_template, name='upload_template'),
    path('user_settings/get_template/mixing', get_template_mixing, name='upload_template_mixing'),
    path('user_settings/get_template/agreement', get_template_agreement, name='upload_template_agreement'),
    path('user_settings/get_template/additional', get_template_additional, name='upload_template_additional'),
    path('user_settings/get_template/mixing_pdf', get_template_additional, name='upload_template_additional'),

    path('list_edit', reports_edit_list, name='reports_edit_list'),
    path('<int:id>/add/', ReportEditView.as_view(), name='add_report'),
    path(r'image/display/', ImageView.as_view(), name='image_view'),
    path(r'image/delete/', ImageDelete.as_view(), name='image_delete'),
    path(r'pphoto/display/', PPhotoView.as_view(), name='pphoto_view'),
    path(r'pphoto/delete/', PPhotoDelete.as_view(), name='pphoto_delete'),
    path(r'ophoto/display/', OPhotoView.as_view(), name='ophoto_view'),
    path(r'ophoto/delete/', OPhotoDelete.as_view(), name='ophoto_delete'),
    path(r'checks/display/', ChecksView.as_view(), name='checks_view'),
    path(r'checks/delete/', ChecksDelete.as_view(), name='chekcs_delete'),
    path(r'pdf/display/', PDFDisposableView.as_view(), name='pdf_view'),
    path(r'pdf/delete/', PDFDisposableDelete.as_view(), name='pdf_delete'),
    path(r"reduce/documents", reduce_documents_size, name="reduce_documents_size"),
    path(r'enumeration/', EnumerationView.as_view(), name="enumeration_view"),
    path(r'enumeration/edit/<int:id>', EnumerationView.as_view(), name="enumeration_view_edit"),
    # implement this methods
    path(r'disposable/', DisposableView.as_view(), name="disposable_view"),
    path(r'disposable/edit/<int:id>', DisposableView.as_view(), name="disposable_view_edit"),


]
