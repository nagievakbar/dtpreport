import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from django.utils.decorators import method_decorator

from django.views.generic import View
from django.db.models import Q, Subquery
from .forms import *
from .utils import *

from pdf_report.views import create_base64, create_base64_closing
from DTPreport import settings as s
from pdf_report.tasks import reduce_image, delete_empty_report, make_pdf, make_pdf_additional, make_pdf_enumeration, \
    concatenate_pdf_disposable


class ImageDelete(View):
    def post(self, request):
        image = Images.objects.get(image_id=request.POST['key'])
        image.delete()
        return JsonResponse({'errors': True})


class ImageView(View):
    def post(self, request):
        hold_image = HoldsImages.objects.get(id=request.POST['id'])
        image = Images.objects.create(
            image=request.FILES['image'],
        )
        hold_image.image.add(image)
        hold_image.save()
        image.save()
        reduce_image.delay(image.image.path)
        link_img = "{}{}".format(s.URL_FILES, image.image.url)
        print(link_img)
        link_delete = "{}/report/image/delete/".format(s.URL_FILES)
        return JsonResponse(
            response_file(link_file=link_img, link_delete=link_delete, file=image.image, id=image.image_id))


class PDFDisposableDelete(View):
    def post(self, request):
        disposable = Report.objects.get(report_id=request.POST['key'])
        disposable.clear_pdf()
        return JsonResponse({'errors': True})


# create method
class PDFDisposableView(View):
    def post(self, request):
        disposable = Report.objects.get(report_id=request.POST['id'])
        pdf = request.FILES['pdf_report']
        disposable.save_disposable_pdf(pdf)
        link_img = "{}{}".format(s.URL_FILES, disposable.pdf_report.url)
        print(link_img)
        link_delete = "{}/report/pdf/delete/".format(s.URL_FILES)
        return JsonResponse(
            response_file(link_file=link_img, link_delete=link_delete, file=disposable.pdf_report,
                          id=disposable.report_id, type='pdf'))


class PPhotoDelete(View):
    def post(self, request):
        image = PassportPhotos.objects.get(p_photo_id=request.POST['key'])
        image.delete()
        return JsonResponse({'errors': True})


class PPhotoView(View):
    def post(self, request):
        hold_image = HoldsImages.objects.get(id=request.POST['id'])
        image = PassportPhotos.objects.create(
            photo=request.FILES['photo'],
        )
        hold_image.pp_photo.add(image)
        hold_image.save()
        image.save()
        reduce_image.delay(image.photo.path)
        link_img = "{}{}".format(s.URL_FILES, image.photo.url)
        print(link_img)
        link_delete = "{}/report/pphoto/delete/".format(s.URL_FILES)
        return JsonResponse(
            response_file(link_file=link_img, link_delete=link_delete, file=image.photo, id=image.p_photo_id))


class OPhotoDelete(View):
    def post(self, request):
        image = OtherPhotos.objects.get(o_photo_id=request.POST['key'])
        image.delete()
        return JsonResponse({'errors': True})


class OPhotoView(View):
    def post(self, request, id=None):
        hold_image = HoldsImages.objects.get(id=request.POST['id'])
        image = OtherPhotos.objects.create(
            photos=request.FILES['photos'],
        )
        hold_image.o_images.add(image)
        hold_image.save()
        image.save()
        reduce_image.delay(image.photos.path)
        link_img = "{}{}".format(s.URL_FILES, image.photos.url)
        print(link_img)
        link_delete = "{}/report/ophoto/delete/".format(s.URL_FILES)
        return JsonResponse(
            response_file(link_file=link_img, link_delete=link_delete, file=image.photos, id=image.o_photo_id))


class ChecksDelete(View):
    def post(self, request):
        image = Checks.objects.get(checks_id=request.POST['key'])
        image.delete()
        return JsonResponse({'errors': True})


class ChecksView(View):
    def post(self, request, id=None):
        hold_image = HoldsImages.objects.get(id=request.POST['id'])
        image = Checks.objects.create(
            checks=request.FILES['checks'],
        )
        hold_image.checks.add(image)
        hold_image.save()
        image.save()
        reduce_image.delay(image.checks.path)
        link_img = "{}{}".format(s.URL_FILES, image.checks.url)
        print(link_img)
        link_delete = "{}/report/checks/delete/".format(s.URL_FILES)
        return JsonResponse(
            response_file(link_file=link_img, link_delete=link_delete, file=image.checks, id=image.checks_id))


def hold_image():
    last_hold = HoldsImages.objects.last()
    if last_hold is None or last_hold.report is not None:
        holds_image = HoldsImages.objects.create()
        print("CREATED NEW ONE ")
        holds_image.save()
        return holds_image
    for image in last_hold.image.all():
        image.delete()
    for pphotos in last_hold.pp_photo.all():
        pphotos.delete()
    for o_images in last_hold.o_images.all():
        o_images.delete()
    for checks in last_hold.checks.all():
        checks.delete()
    return last_hold


# Additional thingsss
class ReportEditView(View):
    decorators = [login_required]

    @method_decorator(decorators)
    def get(self, request, id=None):
        calculation = Calculation.objects.get(report_id=id)
        calculation_form = CalculationForm(instance=calculation)
        holds_image = HoldsImages.objects.get(report_id=id)
        new_hold_images = HoldsImages.objects.create()
        new_hold_images.set_new(holds_image)
        new_report = create_report_additional(request)
        new_hold_images.report = new_report
        new_hold_images.save()
        images = new_hold_images.image_previous.all()
        pphotos = new_hold_images.pp_photo_previous.all()
        ophotos = new_hold_images.o_images_previous.all()
        checks = new_hold_images.checks_previous.all()
        image_form = ImageForm(instance=Images(), use_required_attribute=False)
        passphoto_form = PPhotoForm(instance=PassportPhotos(), use_required_attribute=False)
        otherphoto_form = OPhotoForm(instance=OtherPhotos(), use_required_attribute=False)
        checks_form = ChecksForm(instance=Checks(), use_required_attribute=False)
        report = Report.objects.get(report_id=id)
        report.consumable_cost = 0
        report.product_cost = 0
        report.service_cost = 0
        contract = Contract.objects.get(contract_id=report.contract_id)
        contract_form = ContractForm(instance=contract)
        report_form = ReportForm(instance=Report())
        car = Car.objects.get(car_id=report.car_id)
        car.release_date = car.release_date
        car_form = CarForm(instance=car)
        customer = Customer.objects.get(customer_id=contract.customer_id)
        customer_form = CustomerForm(instance=customer)
        service_form = formset_factory(ServiceForm, extra=1)
        service_formset = service_form(prefix='service')
        product_form = formset_factory(ProductForm, extra=1)
        product_formset = product_form(prefix='product')
        consumable_form = formset_factory(ConsumableForm, extra=1)
        consumable_formset = consumable_form(prefix='consumable')
        wear_form = WearForm(initial=report.wear_data)
        total_price_report = report.total_report_cost

        template = 'makereport/add_repor.html'
        context = {
            'base': False,
            'id_image': new_hold_images.id,
            'calculation_form': calculation_form,
            'contract_form': contract_form,
            'report_form': report_form,
            'id': new_report.report_id,
            'prices': get_prices(),
            'car_form': car_form,
            'customer_form': customer_form,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'wear_form': wear_form,
            'report': new_report or None,
            'total_price_report': total_price_report,
            'image_form': image_form or None,
            'passphoto_form': passphoto_form or None,
            'otherphoto_form': otherphoto_form or None,
            'checks_form': checks_form or None,
            'images': images or None,
            'pphotos': pphotos or None,
            'ophotos': ophotos or None,
            'checks': checks or None,
        }
        return render(request, template, context)

    @method_decorator(decorators)
    def post(self, request, id=None):
        holds_images = HoldsImages.objects.get(id=request.POST['id_image'])
        images = holds_images.image_concatinate()
        pphotos = holds_images.pp_photo_concatinate()
        ophotos = holds_images.o_photo_concatinate()
        checks = holds_images.check_concatinate()
        report_id = int(request.POST['id_report'])
        if report_id == 0:
            calculation_form = CalculationForm(request.POST, instance=Calculation())
            contract_form = ContractForm(request.POST, instance=Contract())
            report_form = ReportForm(request.POST, instance=Report())
            car_form = CarForm(request.POST, instance=Car())
            customer_form = CustomerForm(request.POST, instance=Customer())
        else:
            report = Report.objects.get(report_id=report_id)
            calculation = Calculation.objects.get(report_id=report_id)
            calculation_form = CalculationForm(request.POST, instance=calculation)
            contract_form = ContractForm(request.POST, instance=report.contract)
            report_form = ReportForm(request.POST, instance=report)
            car_form = CarForm(request.POST, instance=report.car)
            customer_form = CustomerForm(request.POST, instance=report.contract.customer)

        image_form = ImageForm(request.POST, request.FILES)
        passphoto_form = PPhotoForm(request.POST, request.FILES)
        otherphoto_form = OPhotoForm(request.POST, request.FILES)
        checks_form = ChecksForm(request.POST, request.FILES)

        service_formset = self.init_service_formset(request)
        product_formset = self.init_product_formset(request)
        consumable_formset = self.init_consumable_formset(request)
        wear_form = WearForm(request.POST)

        print("VALIDATION {}{}{} {}".format(report_form.is_valid(), car_form.is_valid(), customer_form.is_valid(),
                                            calculation_form.is_valid()))
        print(car_form.errors)
        context = {
            'base': False,
            'id_image': holds_images.id,
            'calculation_form': calculation_form,
            'contract_form': contract_form,
            'report_form': report_form,
            'id': report_id,
            'prices': get_prices(),
            'car_form': car_form,
            'customer_form': customer_form,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'report': None,
            'wear_form': wear_form,
            'image_form': image_form,
            'passphoto_form': passphoto_form,
            'otherphoto_form': otherphoto_form,
            'checks_form': checks_form,
            'images': images or None,
            'pphotos': pphotos or None,
            'ophotos': ophotos or None,
            'checks': checks or None,
        }
        if report_form.is_valid() \
                and car_form.is_valid() \
                and customer_form.is_valid() \
                and contract_form.is_valid() \
                and calculation_form.is_valid():
            new_contract = contract_form.save()
            new_customer = customer_form.save(commit=False)
            new_customer.save()
            new_contract.customer = new_customer
            new_contract.save()
            new_report = report_form.save(commit=False)
            new_report.contract = new_contract
            new_car = car_form.save()
            new_car.save()
            new_report.car = new_car
            new_report.created_by = request.user
            new_report.save()
            holds_images.report = new_report
            holds_images.store_add()
            new_calculation = calculation_form.save()
            new_calculation.report = new_report
            new_calculation.save()
            new_report.clean_incoming_data()
            for form in service_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    sd = get_data_from_service_form(form)
                    if sd.__getitem__('service_cost') is not None:
                        add_service_to_report(new_report, sd.__getitem__('service_id'), sd.__getitem__('service_cost'))
                        new_report.service_data.append(sd)
            for form in product_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    pd = get_data_from_product_form(form)
                    if pd.__getitem__('product_cost') is not None:
                        add_product_to_report(new_report, pd.__getitem__('product_cost'))
                        new_report.product_data.append(pd)
            for form in consumable_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    cd = get_data_from_consum_form(form)
                    if cd.__getitem__('consumable_cost') is not None:
                        add_consumable_to_report(new_report, cd.__getitem__('consumable_id'),
                                                 cd.__getitem__('consumable_cost'))
                        new_report.consumable_data.append(cd)
            if wear_form.is_valid():
                wd = get_data_from_wear_form(wear_form)
                new_report.wear_data.update(wd)
                new_report.get_total_report_price()
            else:
                print("ERRROS WEAR FORMSSS")
                print(wear_form.errors)
            new_report.set_private_key()
            new_report.save()
            total_price_report = new_report.total_report_cost
            context['id'] = new_report.report_id
            context['total_price_report'] = total_price_report
            context['report'] = new_report
            try:
                create_base64(new_report)
            except KeyError:
                pass
            make_pdf_additional.delay(new_report.report_id)

        return render(request, 'makereport/add_repor.html', context)

    def init_service_formset(self, request):
        service_form = formset_factory(ServiceForm, extra=2)
        service_formset = service_form(request.POST, prefix='service')
        return service_formset

    def init_product_formset(self, request):
        product_form = formset_factory(ProductForm, extra=2)
        product_formset = product_form(request.POST, prefix='product')
        return product_formset

    def init_consumable_formset(self, request):
        consumable_form = formset_factory(ConsumableForm, extra=2)
        consumable_formset = consumable_form(request.POST, prefix='consumable')
        return consumable_formset


class ReportView(View):
    decorators = [login_required]
    template_name = 'makereport/add_repor.html'

    @method_decorator(decorators)
    def get(self, request, id=None, extend=0):
        if id is None:
            report = create_report(request)
        else:
            report = Report.objects.get(report_id=id)
        context = self.prepare_get_request(request, id, report, customer_form=CustomerForm)
        return render(request, self.template_name, context)

    def prepare_get_request(self, request, id, report: Report, customer_form=forms.ModelForm):
        images = None
        pphotos = None
        ophotos = None
        checks = None
        if id:
            report_id = id
            holds_image = HoldsImages.objects.get(report_id=id)
            images = holds_image.image.all()
            pphotos = holds_image.pp_photo.all()
            ophotos = holds_image.o_images.all()
            checks = holds_image.checks.all()
            calculation = Calculation.objects.get(report_id=id)
            calculation_form = CalculationForm(instance=calculation)
            image_form = ImageForm(instance=Images(), use_required_attribute=False)
            passphoto_form = PPhotoForm(instance=PassportPhotos(), use_required_attribute=False)
            otherphoto_form = OPhotoForm(instance=OtherPhotos(), use_required_attribute=False)
            checks_form = ChecksForm(instance=Checks(), use_required_attribute=False)
            report = Report.objects.get(report_id=id)
            contract = Contract.objects.get(contract_id=report.contract_id)
            contract_form = ContractForm(instance=contract)
            report_form = ReportForm(instance=report)
            report_form.custom_integer_validation()
            car = Car.objects.get(car_id=report.car_id)
            car.release_date = car.release_date
            car_form = CarForm(instance=car)
            customer = Customer.objects.get(customer_id=contract.customer_id)
            customer_form = customer_form(instance=customer)
            service_form = formset_factory(ServiceForm, extra=1)
            service_formset = service_form(initial=report.service_data, prefix='service')
            product_form = formset_factory(ProductForm, extra=1)
            product_formset = product_form(initial=report.product_data, prefix='product')
            consumable_form = formset_factory(ConsumableForm, extra=1)
            consumable_formset = consumable_form(initial=report.consumable_data, prefix='consumable')
            wear_form = WearForm(initial=report.wear_data)
            total_price_report = report.total_report_cost
        else:
            report_id = report.report_id
            calculation_form = CalculationForm(instance=Calculation())
            image_form = ImageForm(instance=Images())
            contract_form = ContractForm(instance=Contract())
            passphoto_form = PPhotoForm(instance=PassportPhotos())
            otherphoto_form = OPhotoForm(instance=OtherPhotos())
            checks_form = ChecksForm(instance=Checks())
            report_form = ReportForm(instance=Report())
            car_form = CarForm(instance=Car())
            customer_form = customer_form(instance=Customer())
            service_form = formset_factory(ServiceForm, extra=2)
            service_formset = service_form(prefix='service')
            product_form = formset_factory(ProductForm, extra=2)
            product_formset = product_form(prefix='product')
            consumable_form = formset_factory(ConsumableForm, extra=2)
            consumable_formset = consumable_form(prefix='consumable')
            wear_form = WearForm()
            total_price_report = 0
            holds_image = HoldsImages.objects.create()
            holds_image.report = report
            holds_image.save()
        context = {
            'base': True,
            'id_image': holds_image.id,
            'id': report_id,
            'calculation_form': calculation_form,
            'contract_form': contract_form,
            'report_form': report_form,
            'car_form': car_form,
            'prices': get_prices(),
            'customer_form': customer_form,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'wear_form': wear_form,
            'report': report or None,
            'total_price_report': total_price_report,
            'image_form': image_form or None,
            'passphoto_form': passphoto_form or None,
            'otherphoto_form': otherphoto_form or None,
            'checks_form': checks_form or None,
            'images': images or None,
            'pphotos': pphotos or None,
            'ophotos': ophotos or None,
            'checks': checks or None,
        }
        return context

    @method_decorator(decorators)
    def post(self, request, id=None, extend=0):
        total_report_price = 0
        print("ID REPORT")

        if int(request.POST['id_report']) != 0:
            id = int(request.POST['id_report'])
        if id:
            return self.put(request, id)
        print("THIS IS HERE")
        holds_images = HoldsImages.objects.get(id=request.POST['id_image'])
        images = holds_images.image.all()
        pphotos = holds_images.pp_photo.all()
        ophotos = holds_images.o_images.all()
        checks = holds_images.checks.all()
        calculation_form = CalculationForm(request.POST, instance=Calculation())
        contract_form = ContractForm(request.POST, instance=Contract())
        report_form = ReportForm(request.POST, instance=Report())
        car_form = CarForm(request.POST, instance=Car())
        customer_form = CustomerForm(request.POST, instance=Customer())
        image_form = ImageForm(instance=Images(), use_required_attribute=False)
        passphoto_form = PPhotoForm(instance=PassportPhotos(), use_required_attribute=False)
        otherphoto_form = OPhotoForm(instance=OtherPhotos(), use_required_attribute=False)
        checks_form = ChecksForm(instance=Checks(), use_required_attribute=False)
        service_formset = self.init_service_formset(request)
        product_formset = self.init_product_formset(request)
        consumable_formset = self.init_consumable_formset(request)
        wear_form = WearForm(request.POST)
        context = {
            'base': True,
            'id_image': holds_images.id,
            'id': 0,
            'calculation_form': calculation_form,
            'contract_form': contract_form,
            'report_form': report_form,
            'car_form': car_form,
            'prices': get_prices(),
            'customer_form': customer_form,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'wear_form': wear_form,
            'report': None,
            'image_form': image_form or None,
            'passphoto_form': passphoto_form or None,
            'otherphoto_form': otherphoto_form or None,
            'checks_form': checks_form or None,
            'images': images or None,
            'pphotos': pphotos or None,
            'ophotos': ophotos or None,
            'checks': checks or None,
        }
        print(
            "VALIDATION {}{} {} {} {}".format(report_form.is_valid(), car_form.is_valid(), customer_form.is_valid(),
                                              contract_form.is_valid(), calculation_form.is_valid()))
        if report_form.is_valid() and car_form.is_valid() \
                and customer_form.is_valid() and \
                contract_form.is_valid() and calculation_form.is_valid():
            new_contract = contract_form.save()
            new_customer = customer_form.save(commit=False)
            new_customer.save()
            new_contract.customer = new_customer
            new_contract.save()
            new_report = report_form.save(commit=False)
            new_report.contract = new_contract
            new_car = car_form.save()
            new_car.save()
            new_report.car = new_car
            new_report.created_by = request.user
            new_report.save()
            holds_images.report = new_report
            holds_images.save()
            new_calculation = calculation_form.save()
            new_calculation.report = new_report
            new_calculation.save()
            new_report.clean_incoming_data()
            for form in service_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    sd = get_data_from_service_form(form)
                    print(sd)
                    add_service_to_report(new_report, sd.__getitem__('service_id'), sd.__getitem__('service_cost'))
                    new_report.service_data.append(sd)
                else:
                    print(form.errors)
            for form in product_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    pd = get_data_from_product_form(form)
                    add_product_to_report(new_report, pd.__getitem__('product_cost'))
                    new_report.product_data.append(pd)
                else:
                    print(form.errors)
            for form in consumable_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    cd = get_data_from_consum_form(form)
                    add_consumable_to_report(new_report, cd.__getitem__('consumable_id'),
                                             cd.__getitem__('consumable_cost'))
                    new_report.consumable_data.append(cd)
                else:
                    print(form.errors)
            if wear_form.is_valid():
                wd = get_data_from_wear_form(wear_form)
                new_report.wear_data.update(wd)
                new_report.get_total_report_price()
            else:
                print("ERRROS WEAR FORMSSS")
                print(wear_form.errors)

            new_report.set_private_key()
            new_report.save()
            total_price_report = new_report.total_report_cost
            context['id'] = new_report.report_id
            context['total_price_report'] = total_price_report
            context['report'] = new_report
            try:
                create_base64(new_report)
            except KeyError:
                pass
            make_pdf.delay(new_report.report_id)
            # make_pdf_additional.delay(new_report.report_id)
        return render(request, self.template_name, context)

    @method_decorator(decorators)
    def put(self, request, id=None):
        holds_images = HoldsImages.objects.get(id=request.POST['id_image'])
        images = holds_images.image.all()
        pphotos = holds_images.pp_photo.all()
        ophotos = holds_images.o_images.all()
        checks = holds_images.checks.all()
        calculation = Calculation.objects.get(report_id=id)
        report = Report.objects.get(report_id=id)
        car = Car.objects.get(car_id=report.car_id)
        contract = report.contract
        customer = contract.customer
        contract_form = ContractForm(request.POST, instance=contract)
        car_form = CarForm(request.POST, instance=car)
        calculation_form = CalculationForm(request.POST, instance=calculation)
        report_form = ReportForm(request.POST, instance=report)
        customer_form = CustomerForm(request.POST, instance=customer)
        image_form = ImageForm(instance=Images(), use_required_attribute=False)
        passphoto_form = PPhotoForm(instance=PassportPhotos(), use_required_attribute=False)
        otherphoto_form = OPhotoForm(instance=OtherPhotos(), use_required_attribute=False)
        checks_form = ChecksForm(instance=Checks(), use_required_attribute=False)
        service_formset = self.init_service_formset(request)
        product_formset = self.init_product_formset(request)
        consumable_formset = self.init_consumable_formset(request)
        wear_form = WearForm(request.POST)
        print(
            "VALIDATION {}{} {} {} {}".format(report_form.is_valid(), car_form.is_valid(), customer_form.is_valid(),
                                              contract_form.is_valid(), calculation_form.is_valid()))

        context = {
            'base': True,
            'id_image': holds_images.id,
            'id': id,
            'calculation_form': calculation_form,
            'contract_form': contract_form,
            'report_form': report_form,
            'car_form': car_form,
            'prices': get_prices(),
            'customer_form': customer_form,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'wear_form': wear_form,
            'report': report or None,
            'image_form': image_form or None,
            'passphoto_form': passphoto_form or None,
            'otherphoto_form': otherphoto_form or None,
            'checks_form': checks_form or None,
            'images': images or None,
            'pphotos': pphotos or None,
            'ophotos': ophotos or None,
            'checks': checks or None,
        }

        # report_form.is_valid() and
        if report_form.is_valid() and car_form.is_valid() \
                and customer_form.is_valid() and \
                contract_form.is_valid() and calculation_form.is_valid():
            new_contract = contract_form.save()
            new_customer = customer_form.save(commit=False)
            new_customer.save()
            new_contract.customer = new_customer
            new_contract.save()
            new_report = report_form.save(commit=False)
            new_report.contract = new_contract
            new_car = car_form.save()
            new_car.save()
            new_report.car = new_car
            new_report.created_by = request.user
            new_report.save()
            holds_images.report = new_report
            holds_images.save()
            new_calculation = calculation_form.save()
            new_calculation.report = new_report
            new_calculation.save()
            new_report.clean_incoming_data()
            for form in service_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    sd = get_data_from_service_form(form)
                    add_service_to_report(new_report, sd.__getitem__('service_id'), sd.__getitem__('service_cost'))
                    new_report.service_data.append(sd)
                else:
                    print(form.errors)
            for form in product_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    pd = get_data_from_product_form(form)
                    print(pd.__getitem__('product_cost'))
                    add_product_to_report(new_report, pd.__getitem__('product_cost'))
                    new_report.product_data.append(pd)
                else:
                    print(form.errors)
            for form in consumable_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    cd = get_data_from_consum_form(form)
                    add_consumable_to_report(new_report, cd.__getitem__('consumable_id'),
                                             cd.__getitem__('consumable_cost'))
                    new_report.consumable_data.append(cd)
                else:
                    print(form.errors)
            if wear_form.is_valid():
                wd = get_data_from_wear_form(wear_form)
                new_report.wear_data.update(wd)
                new_report.get_total_report_price()
            else:
                print("ERRROS WEAR FORMSSS")
                print(wear_form.errors)

            new_report.set_private_key()
            new_report.save()

            context['report'] = new_report
            total_price_report = new_report.total_report_cost
            context['total_price_report'] = total_price_report
            try:
                create_base64(new_report)
            except KeyError:
                pass

            finally:
                if new_report.type_report == 0:
                    make_pdf.delay(new_report.report_id)
                elif new_report.type_report == 1:
                    make_pdf_additional.delay(new_report.report_id)
                context = {
                    'base': True,
                    'id_image': holds_images.id,
                    'id': id,
                    'calculation_form': calculation_form,
                    'contract_form': contract_form,
                    'report_form': report_form,
                    'car_form': car_form,
                    'prices': get_prices(),
                    'customer_form': customer_form,
                    'service_formset': service_formset,
                    'product_formset': product_formset,
                    'consumable_formset': consumable_formset,
                    'wear_form': wear_form,
                    'report': new_report,
                    'total_price_report': total_price_report,
                    'image_form': image_form or None,
                    'passphoto_form': passphoto_form or None,
                    'otherphoto_form': otherphoto_form or None,
                    'checks_form': checks_form or None,
                    'images': images or None,
                    'pphotos': pphotos or None,
                    'ophotos': ophotos or None,
                    'checks': checks or None,
                }

        return render(request, self.template_name, context)

    def init_service_formset(self, request):

        service_form = formset_factory(ServiceForm, extra=2)
        service_formset = service_form(request.POST, prefix='service')
        return service_formset

    def init_product_formset(self, request):
        product_form = formset_factory(ProductForm, extra=2)
        product_formset = product_form(request.POST, prefix='product')
        return product_formset

    def init_consumable_formset(self, request):
        consumable_form = formset_factory(ConsumableForm, extra=2)
        consumable_formset = consumable_form(request.POST, prefix='consumable')
        return consumable_formset


class EnumerationView(ReportView):
    decorators = [login_required]
    extend = False

    @method_decorator(decorators)
    def get(self, request, id=None):
        template = 'makereport/enumeration.html'
        if id is None:
            enumeration_form = EnumerationForms(instance=Enumeration())
            report = create_report_enumeration(request)
        else:
            enumeration = Enumeration.objects.get(report_id=id)
            enumeration_form = EnumerationForms(instance=enumeration)
            report = Report.objects.get(report_id=id)
        context = self.prepare_get_request(request, id, report, customer_form=CustomerFormEdit)
        context['enumeration_form'] = enumeration_form
        return render(request, self.template_name, context)

    @method_decorator(decorators)
    def post(self, request, id=None):
        holds_images = HoldsImages.objects.get(id=request.POST['id_image'])
        images = holds_images.image.all()
        pphotos = holds_images.pp_photo.all()
        ophotos = holds_images.o_images.all()
        checks = holds_images.checks.all()
        if id is not None:
            report_id = id
        else:
            report_id = int(request.POST['id_report'])
        if report_id == 0:
            calculation_form = CalculationForm(request.POST, instance=Calculation())
            contract_form = ContractForm(request.POST, instance=Contract())
            report_form = ReportForm(request.POST, instance=Report())
            car_form = CarForm(request.POST, instance=Car())
            customer_form = CustomerFormEdit(request.POST, instance=Customer())
            enumeration_form = EnumerationForms(instance=Enumeration())
        else:
            report = Report.objects.get(report_id=report_id)
            calculation = Calculation.objects.get(report_id=report_id)
            enumeration = Enumeration.objects.get(report_id=report_id)
            calculation_form = CalculationForm(request.POST, instance=calculation)
            contract_form = ContractForm(request.POST, instance=report.contract)
            report_form = ReportForm(request.POST, instance=report)
            car_form = CarForm(request.POST, instance=report.car)
            customer_form = CustomerFormEdit(request.POST, instance=report.contract.customer)
            enumeration_form = EnumerationForms(request.POST, instance=enumeration)

        image_form = ImageForm(request.POST, request.FILES)
        passphoto_form = PPhotoForm(request.POST, request.FILES)
        otherphoto_form = OPhotoForm(request.POST, request.FILES)
        checks_form = ChecksForm(request.POST, request.FILES)

        service_formset = self.init_service_formset(request)
        product_formset = self.init_product_formset(request)
        consumable_formset = self.init_consumable_formset(request)
        wear_form = WearForm(request.POST)

        print("VALIDATION {}{}{} {}  {}".format(report_form.is_valid(), car_form.is_valid(), customer_form.is_valid(),
                                                calculation_form.is_valid(), enumeration_form.is_valid()))
        print(car_form.errors)
        context = {
            'base': False,
            'id_image': holds_images.id,
            'calculation_form': calculation_form,
            'contract_form': contract_form,
            'report_form': report_form,
            'enumeration_form': enumeration_form,
            'id': report_id,
            'prices': get_prices(),
            'car_form': car_form,
            'customer_form': customer_form,
            'service_formset': service_formset,
            'product_formset': product_formset,
            'consumable_formset': consumable_formset,
            'report': None,
            'wear_form': wear_form,
            'image_form': image_form,
            'passphoto_form': passphoto_form,
            'otherphoto_form': otherphoto_form,
            'checks_form': checks_form,
            'images': images or None,
            'pphotos': pphotos or None,
            'ophotos': ophotos or None,
            'checks': checks or None,
        }
        if report_form.is_valid() \
                and car_form.is_valid() \
                and customer_form.is_valid() \
                and contract_form.is_valid() \
                and calculation_form.is_valid() \
                and enumeration_form.is_valid():
            new_contract = contract_form.save()
            new_customer = customer_form.save(commit=False)
            new_customer.save()
            new_contract.customer = new_customer
            new_contract.save()

            new_report = report_form.save(commit=False)
            new_report.contract = new_contract
            new_car = car_form.save()
            new_car.save()
            new_report.car = new_car
            new_report.created_by = request.user
            new_report.save()
            enumeration_form.save()
            holds_images.report = new_report

            ## I CHANGE TO SAVE ##
            holds_images.save()
            new_calculation = calculation_form.save()
            new_calculation.report = new_report
            new_calculation.save()
            new_report.clean_incoming_data()
            for form in service_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    sd = get_data_from_service_form(form)
                    if sd.__getitem__('service_cost') is not None:
                        add_service_to_report(new_report, sd.__getitem__('service_id'), sd.__getitem__('service_cost'))
                        new_report.service_data.append(sd)
            for form in product_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    pd = get_data_from_product_form(form)
                    if pd.__getitem__('product_cost') is not None:
                        add_product_to_report(new_report, pd.__getitem__('product_cost'))
                        new_report.product_data.append(pd)
            for form in consumable_formset.forms:
                if form.is_valid() and form.cleaned_data:
                    cd = get_data_from_consum_form(form)
                    if cd.__getitem__('consumable_cost') is not None:
                        add_consumable_to_report(new_report, cd.__getitem__('consumable_id'),
                                                 cd.__getitem__('consumable_cost'))
                        new_report.consumable_data.append(cd)
            if wear_form.is_valid():
                wd = get_data_from_wear_form(wear_form)
                new_report.wear_data.update(wd)
                new_report.get_total_report_price()
            else:
                print("ERRROS WEAR FORMSSS")
                print(wear_form.errors)
            new_report.set_private_key()
            new_report.save()
            total_price_report = new_report.total_report_cost
            context['id'] = new_report.report_id
            context['total_price_report'] = total_price_report
            context['report'] = new_report
            try:
                create_base64(new_report)
            except KeyError:
                pass
            make_pdf_enumeration.delay(new_report.report_id)

        return render(request, self.template_name, context)


def delete(request):
    try:
        report = Report.objects.get(report_id=request.GET.get('id', 0))
        report.delete()
    finally:
        pass
    return JsonResponse({})


@login_required
def reports_list(request):
    return admin_list(request)


# do not forget to make extra validation in search
@login_required
def reports_edit_list(request):
    context = list(request, additional_filter=Q(type_report=0))
    return render(request, 'makereport/additional.html', context=context)


def list(request, additional_filter=Q()):
    page = pagination_update(request)
    params = ""
    if 'search' in request.GET:
        reports = Report.objects.filter(car__car_number__contains=request.GET['search']).exclude(
            (Q(key__isnull=True) | Q(key__exact='')))
    elif 'filter' in request.GET:
        params += "filter={}&".format(request.GET['filter'])
        reports = filter_update(request)
    elif 'date_from' in request.GET or 'date_to' in request.GET:
        data = date_update(request)
        params += data['params']
        reports = data['reports']
    else:
        reports = Report.objects

    paginator = CustomPaginator(
        reports.filter(additional_filter).exclude(
            (Q(key__isnull=True) | Q(key__exact=''))).order_by(
            '-report_id'), page)
    page_number = request.GET.get('page')
    reports = paginator.get_page(page_number)
    context = {'reports': reports, "page_obj": PaginationModels.objects.all().order_by('page'),
               'params': params}
    return context


def admin_list(request):
    context = list(request)
    return render(request, 'makereport/index.html', context=context)


def user_list_some(request):
    if 'search' in request.GET:
        reports = Report.objects.filter(car__car_number__contains=request.GET['search'], created_by=request.user)
    else:
        reports = Report.objects.filter(created_by=request.user)
    return render(request, 'makereport/index.html', context={'reports': reports})


@login_required
def users_list(request):
    users = User.objects.all()
    return render(request, 'makereport/users_list.html', context={'users': users})


@login_required
def get_template(request):
    print("COMMING")
    try:
        TemplateBase.objects.last().delete()
    finally:
        new_template = TemplateBase.objects.create()
        new_template.template = request.FILES['file']
        new_template.save()
        return JsonResponse({})


@login_required
def get_template_mixing(request):
    try:
        TemplateMixing.objects.last().delete()
    finally:
        new_template = TemplateMixing.objects.create()
        new_template.template = request.FILES['file']
        new_template.save()
        return JsonResponse({})


@login_required
def get_template_agreement(request):
    try:
        TemplateAgreement.objects.last().delete()
    finally:
        new_template = TemplateAgreement.objects.create()
        new_template.template = request.FILES['file']
        new_template.save()
        return JsonResponse({})


@login_required
def get_template_additional(request):
    try:
        TemplateAdditional.objects.last().delete()
    finally:
        new_template = TemplateAdditional.objects.create()
        new_template.template = request.FILES['file']
        new_template.save()
        return JsonResponse({})


def delete_old(template):
    if template is not None:
        template.delete()


class UserSettingsView(View):
    decorators = [login_required]

    @method_decorator(decorators)
    def get(self, request):
        return render(request, 'makereport/user_settings.html')


def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('reports_list'))
        else:
            context["error"] = True
            context["description"] = "Введен неправильный логин или пароль"
            return render(request, "makereport/auth/login_sea.html", context)
    else:
        if request.user.is_anonymous:
            return render(request, "makereport/auth/login_sea.html", context)
        else:
            return redirect('reports_list')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


def reduce_documents_size(request):
    document = Documents.objects.first()
    reduce_image.delay(document.license.path)
    reduce_image.delay(document.guvonhnoma.path)
    reduce_image.delay(document.certificate.path)
    reduce_image.delay(document.insurance.path)
    return JsonResponse({})


def search(request):
    errors = "Введите ключ"
    if 'key' in request.GET:
        try:
            key = request.GET['key'].replace(' ', '')
            report = Report.objects.get(key=key)
            if report.type_report == 0:
                return HttpResponseRedirect('pdf/{}/'.format(report.report_id))
            elif report.type_report == 1:
                return HttpResponseRedirect('pdf/additional/{}/'.format(report.report_id))
            elif report.type_report == 2:
                return HttpResponseRedirect('pdf/enumeration/{}/'.format(report.report_id))
            elif report.type_report == 3:
                return HttpResponseRedirect('pdf/disposable/{}/'.format(report.report_id))
        except Report.DoesNotExist:
            errors = 'Такого ключа не существует'
    context = {
        'errors': errors
    }
    return render(request, "makereport/auth/search.html", context=context)


class DisposableView(View):
    template_name = "makereport/disposable.html"

    def get(self, request, id=None):
        if id is None:
            return self.show_new_disposable(request)
        else:
            return self.show_existing_disposable(request, id)

    def post(self, request, id=0):
        id_report = int(request.POST.get('id_report', id))
        return self.store_disposable(request, id_report)

    def store_disposable(self, request, id):
        holds_image = HoldsImages.objects.get(report_id=id)
        report = Report.objects.get(report_id=id)
        enumeration = Enumeration.objects.get(report_id=id)
        closing = Closing.objects.get(report_id=id)
        car = Car.objects.get(car_id=report.car_id)
        contract = report.contract
        customer = contract.customer

        contract_form = ContractForm(request.POST, instance=contract)
        car_form = CarClosingForm(request.POST, instance=car)
        report_form = ReportClosingForm(request.POST, instance=report)
        customer_form = CustomerClosingForm(request.POST, instance=customer)
        enumeration_form = EnumerationForms(request.POST, instance=enumeration)
        closing_form = ClosingDescForm(request.POST, instance=closing)

        images = holds_image.image.all()
        pphotos = holds_image.pp_photo.all()
        ophotos = holds_image.o_images.all()
        checks = holds_image.checks.all()
        if contract_form.is_valid() \
                and car_form.is_valid() \
                and report_form.is_valid() \
                and customer_form.is_valid() \
                and enumeration_form.is_valid() \
                and closing_form.is_valid():
            contract_form.save()
            closing_form.save()
            car_form.save()
            report_form.save()
            customer_form.save()
            enumeration_form.save()
            report.set_private_key()
            create_base64_closing(report)
            report.save()
            concatenate_pdf_disposable.delay(report.id)

        else:
            dict = {
                1: contract_form.errors,
                2: car_form.errors,
                3: report_form.errors,
                4: customer_form.errors,
                5: enumeration_form.errors,
                6: closing_form.errors,
            }
            raise Exception(dict)

        context = {
            'id_image': holds_image.id,
            'id': report.report_id,
            'contract_form': contract_form,
            'car_form': car_form,
            'report_form': report_form,
            'customer_form': customer_form,
            'enumeration_form': enumeration_form,
            'closing_form': closing_form,
            'report': report,
            'images': images,
            'pphotos': pphotos,
            'ophotos': ophotos,
            'checks': checks,
        }

        context = self.get_context_forms(context)
        return render(request, self.template_name, context)

    def get_context_forms(self, context: dict) -> dict:
        disposable_from = DisposableForm(Report())
        image_form = ImageForm(Images())
        passphoto_form = PPhotoForm(PassportPhotos())
        otherphoto_form = OPhotoForm(OtherPhotos())
        checks_form = ChecksForm(Checks())
        context['image_form'] = image_form
        context['passphoto_form'] = passphoto_form
        context['disposable_from'] = disposable_from
        context['otherphoto_form'] = otherphoto_form
        context['checks_form'] = checks_form

        return context

    def get_context_forms_closing(self, context: dict) -> dict:
        context = self.get_context_forms(context)
        car_form = CarClosingForm(instance=Car(), initial={
            'owner_address': 'РУз г. Ташкент Чиланзарский р-н, Чиланзар- 1А, гараж там же',
            'car_owner': "Abduraxmonov Abdulla Suyunovich"})
        contract_form = ContractForm(instance=Contract())
        report_form = ReportClosingForm(instance=Report())
        customer_form = CustomerClosingForm(instance=Customer(), initial={
            'name': "Mukimov Mansur Jumakulovich",
            'address': "Qashqadaryo viloyati Shaxrisabz tumani",
            'passport_number': "AB 1892957",
            'when_passport_issued': "13.11.2015",
            "whom_passport_issued": "Qashqadaryo viloyati Shaxrisabz tumani IIB"
        })
        enumeration_form = EnumerationForms(instance=Enumeration(), initial={
            'p_c': "20208000298017089001",
            'bank': "в Чиланзар.ф-л АИКБ 'Ипак Йули' г. Ташкент",
            'MFO': "01067",
            "INN": " 302667624",
            "OKED": '68310'
        })
        closing_form = ClosingDescForm(instance=Closing())
        context['car_form'] = car_form
        context['contract_form'] = contract_form
        context['report_form'] = report_form
        context['customer_form'] = customer_form
        context['enumeration_form'] = enumeration_form
        context['closing_form'] = closing_form
        return context

    def show_new_disposable(self, request):
        report = create_report_disposable(request)
        holds_images = HoldsImages.objects.create(
            report_id=report.report_id
        )
        context = {
            'id_image': holds_images.id,
            'id': report.report_id,
            'report': report,
            'images': None,
            'pphotos': None,
            'ophotos': None,
            'checks': None,
        }
        context = self.get_context_forms_closing(context)
        return render(request, self.template_name, context)

    def show_existing_disposable(self, request, id):
        holds_image = HoldsImages.objects.get(report_id=id)
        report = Report.objects.get(report_id=id)
        enumeration = Enumeration.objects.get(report_id=id)
        closing = Closing.objects.get(report_id=id)
        car = Car.objects.get(car_id=report.car_id)
        contract = report.contract
        customer = contract.customer
        images = holds_image.image.all()
        pphotos = holds_image.pp_photo.all()
        ophotos = holds_image.o_images.all()
        contract_form = ContractForm(instance=contract)
        car_form = CarClosingForm(instance=car)
        report_form = ReportClosingForm(instance=report)
        customer_form = CustomerClosingForm(instance=customer)
        enumeration_form = EnumerationForms(instance=enumeration)
        closing_form = ClosingDescForm(instance=closing)
        checks = holds_image.checks.all()
        context = {
            'id_image': holds_image.id,
            'id': report.report_id,
            'contract_form': contract_form,
            'car_form': car_form,
            'report_form': report_form,
            'customer_form': customer_form,
            'enumeration_form': enumeration_form,
            'closing_form': closing_form,
            'report': report,
            'images': images,
            'pphotos': pphotos,
            'ophotos': ophotos,
            'checks': checks,
        }
        context = self.get_context_forms(context)
        return render(request, self.template_name, context)


# class ClosingView(View):
#     template_name = "makereport/closing.html"
#
#     def get(self, request, id=None):
#         if id is None:
#             return self.show_new_closing(request)
#         else:
#             return self.show_existing_closing(request, id)
#
#     def post(self, request, id=0):
#         closing_id = int(request.POST.get('id_closing', id))
#         print("CLOSING {}{}".format(closing_id, type(closing_id)))
#         if closing_id == 0:
#             return self.create_new_closing(request)
#         else:
#             return self.edit_closing(request, closing_id)
#
#     def create_new_closing(self, request):
#         closing_form = ClosingForm(request.POST, instance=Closing())
#         context = {
#             'closing_form': closing_form,
#         }
#         if closing_form.is_valid():
#             closing = closing_form.save()
#             create_base64_closing(closing)
#             context['id'] = closing.id
#             context['closing'] = closing
#         else:
#             context['id'] = 0
#             raise Exception(closing_form.errors)
#
#         return render(request, self.template_name, context)
#
#     def edit_closing(self, request, id):
#         closing = Closing.objects.get(id=id)
#         closing_form = ClosingForm(request.POST, instance=closing)
#         context = {
#             'closing_form': closing_form,
#             'closing': closing,
#             'id': closing.id
#         }
#         if closing_form.is_valid():
#             closing_form.save()
#             create_base64_closing(closing)
#         else:
#             raise Exception(closing_form.errors)
#         return render(request, self.template_name, context)
#
#     def show_new_closing(self, request):
#         closing_form = ClosingForm(instance=Closing())
#         context = {
#             'closing_form': closing_form,
#             'id': 0
#         }
#         return render(request, self.template_name, context)
#
#     def show_existing_closing(self, request, id: int):
#         closing = Closing.objects.get(id=id)
#         closing_form = ClosingForm(instance=closing)
#         context = {
#             'closing_form': closing_form,
#             'closing': closing,
#             'id': closing.id
#         }
#         return render(request, self.template_name, context)


# LIST OF CLOSING WHICH HAS TO BE SHOWN
class ListClosing(View):
    pass


# LIST OF DISPOSABLE WHICH HAS TO BE SHOWN
class ListDisposable(View):
    pass
