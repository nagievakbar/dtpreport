from datetime import datetime

from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from .converters import num2text
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Contract(models.Model):
    contract_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    customer = models.ForeignKey('Customer', null=True, blank=True, on_delete=models.CASCADE, related_name='Customer',
                                 verbose_name='Клиент')
    pdf_contract = models.FileField(blank=True, null=True, verbose_name='Контракт в пдф')
    contract_date = models.CharField(max_length=20, null=True, blank=True, default="")
    contract_number = models.CharField(max_length=20, null=True, blank=True, default="")

    def __str__(self):
        return str(self.contract_id)

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'


BRANDS = (
    ('Выберите Марку', 'Выберите Марку'),
    ('Кобальт', 'Кобальт'),
    ('Спарк', 'Спарк'),
    ('Нексия3', 'Нексия3'),
    ('Малибу', 'Малибу'),
    ('Нексия Sonc', 'Нексия Sonc'),
    ('Дамас', 'Дамас'),
    ('Тико', 'Тико'),
    ('Матиз', 'Матиз'),
    ('Матиз Бест', 'Матиз Бест'),
    ('Нексия Donc', 'Нексия Donc'),
    ('Ласетти', 'Ласетти'),
    ('Каптива', 'Каптива'),
    ('Такума', 'Такума'),
    ('Эпика', 'Эпика')
)
TYPE_OF_CAR = (
    ('Выберите тип машины', 'Выберите тип машины'),
    ('Грузовой', 'Грузовой'),
    ('Легковой', 'Легковой'))


class Car(models.Model):
    car_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    brand_text = models.CharField(max_length=30, blank=True, null=True, )
    brand = models.CharField(max_length=30, choices=BRANDS, null=True, blank=True)
    car_number = models.CharField(max_length=20, blank=True, null=True, )
    registration = models.CharField(max_length=15, blank=True, null=True, )
    engine_number = models.CharField(max_length=30, blank=True, null=True, )
    body_number = models.CharField(max_length=30, blank=True, null=True, )
    chassis = models.CharField(max_length=30, blank=True, null=True, )
    car_color = models.CharField(max_length=20, blank=True, null=True, )
    mileage = models.CharField(max_length=20, blank=True, null=True, )
    release_date = models.CharField(max_length=20, blank=True, null=True, )
    car_type = models.CharField(max_length=20, blank=True, null=True, )
    car_owner = models.CharField(max_length=60, blank=True, null=True, )
    owner_address = models.CharField(max_length=100, blank=True, null=True, )
    type_of_car = models.CharField(max_length=50, choices=TYPE_OF_CAR)

    def __str__(self):
        return str(self.car_number) + ' ' + str(self.brand)

    class Meta:
        verbose_name = 'Машину'
        verbose_name_plural = 'Машины'


class Documents(models.Model):
    license = models.ImageField(blank=True, null=True, verbose_name='Лицензия')
    guvonhnoma = models.ImageField(blank=True, null=True, verbose_name='Гувохнома')
    certificate = models.ImageField(blank=True, null=True, verbose_name='Сертификат')
    insurance = models.ImageField(blank=True, null=True, verbose_name='Cтраховка')

    class Meta:
        verbose_name = 'Фотографии для документа'
        verbose_name_plural = 'Фотографии для документов'

    def __str__(self):
        return "Документ № {}".format(self.id)


class Customer(models.Model):
    customer_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, verbose_name='ФИО', blank=True, null=True, )
    address = models.CharField(max_length=100, blank=True, null=True, )
    passport_number = models.CharField(max_length=20, verbose_name='Паспорт', blank=True, null=True, )
    when_passport_issued = models.CharField(max_length=20)
    whom_passport_issued = models.CharField(max_length=50, blank=True, null=True, )
    phone_number = models.CharField(max_length=20, verbose_name='Тел. номер', blank=True, null=True, )
    gnu_or_gje = models.CharField(max_length=40, blank=True, null=True, )
    uvajaemaya = models.CharField(max_length=40, blank=True, null=True, )
    mesto_osmotra = models.CharField(max_length=200, blank=True, null=True, )

    def __str__(self):
        return str(self.name)

    def name_respect(self):
        try:
            name_new = self.name.split(' ')
            return "{first} {second}".format(first=name_new[1], second=name_new[2])
        except:
            return self.name

    class Meta:
        verbose_name = 'Клиента'
        verbose_name_plural = 'Клиенты'


class Product(models.Model):
    product_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, )
    unit = models.CharField(max_length=20, verbose_name='Ед.измер.')
    nexia3 = models.FloatField(blank=True, null=True, verbose_name='Нексия 3')
    cobalt = models.FloatField(blank=True, null=True, verbose_name='Кобальт')
    malibu = models.FloatField(blank=True, null=True, verbose_name='Малибу')
    nexia_sonc = models.FloatField(blank=True, null=True, verbose_name='Нексия Sonc')
    damas = models.FloatField(blank=True, null=True, verbose_name='Дамас')
    tiko = models.FloatField(blank=True, null=True, verbose_name='Тико')
    matiz = models.FloatField(blank=True, null=True, verbose_name='Матиз')
    matiz_best = models.FloatField(blank=True, null=True, verbose_name='Матиз Бест')
    spark = models.FloatField(blank=True, null=True, verbose_name='Спарк')
    nexia_dons = models.FloatField(blank=True, null=True, verbose_name='Нексия Донс')
    lacceti = models.FloatField(blank=True, null=True, verbose_name='Лассети')
    captiva = models.FloatField(blank=True, null=True, verbose_name='Каптива')
    takuma = models.FloatField(blank=True, null=True, verbose_name='Такума')
    epica = models.FloatField(blank=True, null=True, verbose_name='Эпика')

    price = models.IntegerField(blank=True, null=True, verbose_name='Цена')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'


class Service(models.Model):
    service_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')
    name = models.CharField(max_length=1000, blank=True, null=True)
    nexia3 = models.FloatField(blank=True, null=True, verbose_name='Нексия 3')
    cobalt = models.FloatField(blank=True, null=True, verbose_name='Кобальт')
    malibu = models.FloatField(blank=True, null=True, verbose_name='Малибу')
    nexia_sonc = models.FloatField(blank=True, null=True, verbose_name='Нексия Sonc')
    damas = models.FloatField(blank=True, null=True, verbose_name='Дамас')
    tiko = models.FloatField(blank=True, null=True, verbose_name='Тико')
    matiz = models.FloatField(blank=True, null=True, verbose_name='Матиз')
    matiz_best = models.FloatField(blank=True, null=True, verbose_name='Матиз Бест')
    spark = models.FloatField(blank=True, null=True, verbose_name='Спарк')
    nexia_dons = models.FloatField(blank=True, null=True, verbose_name='Нексия Донс')
    lacceti = models.FloatField(blank=True, null=True, verbose_name='Лассети')
    captiva = models.FloatField(blank=True, null=True, verbose_name='Каптива')
    takuma = models.FloatField(blank=True, null=True, verbose_name='Такума')
    epica = models.FloatField(blank=True, null=True, verbose_name='Эпика')

    price = models.IntegerField(blank=True, null=True, verbose_name='Цена')

    BRANDS = {
        'Кобальт': cobalt,
        'Спарк': spark,
        'Нексия3': nexia3,
        'Малибу': malibu,
        'Нексия Sonc': nexia_sonc,
        'Дамас': damas,
        'Тико': tiko,
        'Матиз': matiz,
        'Матиз Бест': matiz_best,
        'Нексия Donc': nexia_dons,
        'Ласетти': lacceti,
        'Каптива': captiva,
        'Такума': takuma,
        'Эпика': epica
    }

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Услугу'
        verbose_name_plural = 'Услуги'


class Consumable(models.Model):
    consumable_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, verbose_name='Ед.измер.')

    price = models.IntegerField(blank=True, null=True, verbose_name='Цена')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Расходник'
        verbose_name_plural = 'Расходники'


def handler_base(instance, filename):
    return "templates_html/report_custom.html"


def handler_base_mixing(instance, filename):
    return "templates_html/finish_custom.html"


def handler_base_agreement(instance, filename):
    return "templates_html/agreement_custom.html"


def handler_base_additional(instance, filename):
    return "templates_html/additional_custom.html"


class TemplateBase(models.Model):
    template = models.FileField(blank=True, null=True, upload_to=handler_base,
                                verbose_name='Шаблон для отчета')

    def delete(self, *args, **kwargs):
        try:
            default_storage.delete(self.template.path)
        finally:
            super(TemplateBase, self).delete(*args, **kwargs)


class TemplateMixing(models.Model):
    template = models.FileField(blank=True, null=True, upload_to=handler_base_mixing,
                                verbose_name='Шаблоны для заключения')

    def delete(self, *args, **kwargs):
        try:
            default_storage.delete(self.template.path)
        finally:
            super(TemplateMixing, self).delete(*args, **kwargs)


class TemplateAdditional(models.Model):
    template = models.FileField(blank=True, null=True, upload_to=handler_base_additional,
                                verbose_name='Шаблоны для дополнения')

    def delete(self, *args, **kwargs):
        try:
            default_storage.delete(self.template.path)
        finally:
            super(TemplateAdditional, self).delete(*args, **kwargs)


class TemplateAgreement(models.Model):
    template = models.FileField(blank=True, null=True, upload_to=handler_base_agreement,
                                verbose_name='Шаблоны для догвора')

    def delete(self, *args, **kwargs):
        try:
            default_storage.delete(self.template.path)
        finally:
            super(TemplateAgreement, self).delete(*args, **kwargs)


class HoldsImages(models.Model):
    # previous images are needed for additional report
    # Because we are considering to type of group images: new ones and old ones
    # So I , at first, store every old image to previous images and then transfer everything to usual place

    image = models.ManyToManyField('Images')
    image_previous = models.ManyToManyField('Images', related_name="image_previous")
    pp_photo = models.ManyToManyField('PassportPhotos')
    pp_photo_previous = models.ManyToManyField('PassportPhotos', related_name="pp_photo_previous")
    o_images = models.ManyToManyField('OtherPhotos')
    o_images_previous = models.ManyToManyField('OtherPhotos', related_name="o_photo_previous")
    checks = models.ManyToManyField('Checks')
    checks_previous = models.ManyToManyField('Checks', related_name="check_previous")
    report = models.ForeignKey('Report', blank=True, null=True, on_delete=models.CASCADE)

    def create_new(self, old):
        self.image.set(old.image.all())
        self.pp_photo.set(old.pp_photo.all())
        self.o_images.set(old.o_images.all())
        self.checks.set(old.checks.all())
        self.save()

    def set_new(self, old):
        self._clear()
        self.pp_photo_previous.set(old.pp_photo.all())
        self.o_images_previous.set(old.o_images.all())
        self.save()

    def store_add(self):
        self._store(self.image_previous.all(), self.image)
        self._store(self.pp_photo_previous.all(), self.pp_photo)
        self._store(self.o_images_previous.all(), self.o_images)
        self._store(self.checks_previous.all(), self.checks)
        self._clear()
        self.save()

    def _clear(self):
        self.image_previous.clear()
        self.pp_photo_previous.clear()
        self.o_images_previous.clear()
        self.checks_previous.clear()

    def image_concatinate(self):
        return list(self.image_previous.all()) + list(self.image.all())

    def pp_photo_concatinate(self):
        return list(self.pp_photo_previous.all()) + list(self.pp_photo.all())

    def check_concatinate(self):
        return list(self.checks_previous.all()) + list(self.checks.all())

    def o_photo_concatinate(self):
        return list(self.o_images.all()) + list(self.o_images_previous.all())

    def _store(self, from_model, to_model):
        for each in from_model:
            to_model.add(each)


class Images(models.Model):
    image_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    image = models.ImageField(blank=True, null=True, verbose_name='Фото')
    report = models.ForeignKey('Report', on_delete=models.CASCADE, blank=True, null=True, related_name='reportImages',
                               verbose_name='Отчёт')

    def delete(self, *args, **kwargs):
        default_storage.delete(self.image.path)
        super(Images, self).delete(*args, **kwargs)


class PassportPhotos(models.Model):
    p_photo_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    photo = models.ImageField(blank=True, null=True, verbose_name='Фото пасспорта')
    report = models.ForeignKey('Report', on_delete=models.CASCADE, blank=True, null=True, related_name='reportPPhotos',
                               verbose_name='Отчёт')

    def delete(self, *args, **kwargs):
        default_storage.delete(self.photo.path)
        super(PassportPhotos, self).delete(*args, **kwargs)


class OtherPhotos(models.Model):
    o_photo_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    photos = models.ImageField(blank=True, null=True, verbose_name='Фото чеков')
    report = models.ForeignKey('Report', on_delete=models.CASCADE, blank=True, null=True, related_name='reportOPhotos',
                               verbose_name='Отчёт')

    def delete(self, *args, **kwargs):
        default_storage.delete(self.photos.path)
        super(OtherPhotos, self).delete(*args, **kwargs)


class CustomSum(models.Model):
    sum = models.IntegerField(default=0, verbose_name="Введите сумму", blank=True, null=True, )

    class Meta:
        verbose_name = 'Сумма'
        verbose_name_plural = 'Сумма'

    def __str__(self):
        return str(self.sum)


class Checks(models.Model):
    checks_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    checks = models.ImageField(blank=True, null=True, verbose_name='Фото чеков')
    report = models.ForeignKey('Report', on_delete=models.CASCADE, blank=True, null=True, related_name='reportChecks',
                               verbose_name='Отчёт')

    def delete(self, *args, **kwargs):
        try:
            default_storage.delete(self.checks.path)
        except ValueError:
            pass
        except AssertionError:
            pass
        except:
            pass
        super(Checks, self).delete(*args, **kwargs)


class Enumeration(models.Model):
    report = models.ForeignKey('Report', on_delete=models.CASCADE, blank=True, null=True,
                               related_name='report_enumeration',
                               verbose_name='Отчёт')
    p_c = models.CharField(max_length=50, blank=True, null=True)
    bank = models.CharField(max_length=50, blank=True, null=True)
    MFO = models.CharField(max_length=50, blank=True, null=True)
    INN = models.CharField(max_length=50, blank=True, null=True)
    OKED = models.CharField(max_length=50, blank=True, null=True)
    pdf_report_enumeration = models.FileField(blank=True, null=True, upload_to='uploads_enumeration/%Y/%m/%d',
                                              verbose_name='Дополнительный отчет в пдф')

    def save_pdf_enumeration(self, filename, data):

        try:
            path = self.pdf_report_enumeration.path
        except ValueError:
            path = None

        self.pdf_report_enumeration.save(filename, ContentFile(data))
        self.save()
        try:
            default_storage.delete(path)
        except ValueError:
            pass
        except AssertionError:
            pass
        except:
            pass


TYPE_OF_REPORT = (
    (0, 0),
    (1, 1),
    (2, 2)
)


class Closing(models.Model):
    report_number = models.CharField(max_length=100, blank=True, null=True)
    movable_property = models.CharField(max_length=100, blank=True, null=True)
    place_registration = models.CharField(max_length=100, blank=True, null=True)
    damage_auto = models.CharField(max_length=100, blank=True, null=True)
    report_date = models.CharField(max_length=100, blank=True, null=True)
    owner = models.CharField(max_length=100, blank=True, null=True)
    customer = models.CharField(max_length=100, blank=True, null=True)
    address_customer = models.CharField(max_length=100, blank=True, null=True)
    passport_data = models.CharField(max_length=100, blank=True, null=True)
    # executor = models.CharField(max_length=100, blank=True, null=True)
    # requisite_executor = models.CharField(max_length=100, blank=True, null=True)
    # aim_mark = models.CharField(max_length=100, blank=True, null=True)
    # appearance_cost = models.CharField(max_length=100, blank=True, null=True)
    # form_report = models.CharField(max_length=100, blank=True, null=True)
    # license_executor = models.CharField(max_length=100, blank=True, null=True)
    # legislative_contractual_limitations = models.CharField(max_length=100, blank=True, null=True)
    main_mark = models.CharField(max_length=100, blank=True, null=True)
    data_mark = models.CharField(max_length=100, blank=True, null=True)
    data_creation_mark = models.CharField(max_length=100, blank=True, null=True)

    pdf_closing_base64 = models.CharField(max_length=1000000, blank=True, null=True)
    sign = models.CharField(max_length=400, blank=True, null=True)


def delete_pdf(path):
    try:
        default_storage.delete(path)
    except ValueError:
        pass
    except AssertionError:
        pass
    except:
        pass


def delete_pdf_path(obj):
    try:
        delete_pdf(obj.path)
    except:
        pass


# class Disposable(models.Model):
#     pdf_disposable = models.FileField(blank=True, null=True, upload_to='uploads_disposable/%Y/%m/%d',
#                                       verbose_name='Одноразовый пдф')
#     pdf_created = models.FileField(blank=True, null=True, upload_to='uploads_created/%Y/%m/%d',
#                                    verbose_name="Объединенный пдф")
#     report_id = models.ForeignKey('Report', null=True, blank=True, on_delete=models.CASCADE)
#
#     def clear_pdf(self):
#         delete_pdf_path(self.pdf_disposable)
#         self.pdf_disposable.delete()
#
#     def delete(self, *args, **kwargs):
#         self.clear_pdf()
#         delete_pdf_path(self.pdf_created)
#         super(Disposable, self).delete(*args, **kwargs)
#
#     @property
#     def url_pdf_disposable(self):
#         try:
#             url = self.pdf_disposable.url
#         except:
#             url = ""
#         return url
#
#     def save_disposable_pdf(self, data):
#         filename = "disposable_{}_{}.pdf".format(datetime.now().timestamp(), self.id)
#         try:
#             path = self.pdf_disposable.path
#         except ValueError:
#             path = None
#
#         self.pdf_disposable.save(filename, data)
#         self.save()
#
#         delete_pdf(path)
#
#     def save_created_pdf(self, data):
#         filename = "created_{}_{}.pdf".format(datetime.now().timestamp(), self.id)
#         try:
#             path = self.pdf_created.path
#         except ValueError:
#             path = None
#
#         self.pdf_created.save(filename, data)
#         self.save()
#
#         delete_pdf(path)


# 0 is usual report
# 1 is additional report
# 2 is enumeration report
# 3 is disposable report
class Report(models.Model):
    type_report = models.IntegerField(default=0, choices=TYPE_OF_REPORT)
    report_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    report_number = models.CharField(max_length=20, blank=True, null=True, )
    report_date = models.CharField(max_length=20, blank=True, null=True, )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by', verbose_name='Создан')
    created_at = models.DateField(blank=True, null=True, verbose_name='Время создания')

    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='Car', verbose_name='Машина')
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, related_name='Contract', verbose_name='Контракт')

    service = models.ManyToManyField(Service, related_name='Услуги', verbose_name='Услуги')
    product = models.ManyToManyField(Product, related_name='Детали', verbose_name='Детали')
    consumable = models.ManyToManyField(Consumable, related_name='Расходники', verbose_name='Расходники')

    service_cost = models.IntegerField(default=0, blank=True, null=True, )
    product_cost = models.IntegerField(default=0, blank=True, null=True, )
    product_acc_cost = models.IntegerField(default=0, blank=True, null=True, )
    consumable_cost = models.IntegerField(default=0, blank=True, null=True, )
    key = models.CharField(max_length=13, blank=True)

    total_report_cost = models.CharField(max_length=20, blank=True, null=True, )
    total_report_cost_txt = models.CharField(max_length=200, blank=True, null=True, )

    pdf_report_additional = models.FileField(blank=True, null=True, upload_to='uploads_additional/%Y/%m/%d',
                                             verbose_name='Дополнительный отчет в пдф')

    pdf_report = models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m/%d', verbose_name='Отчёт в пдф')
    pdf_report_base64 = models.CharField(max_length=1000000, blank=True, null=True)
    pdf_report_pkcs7 = models.JSONField(blank=True, null=True)
    pdf_report_qr = models.JSONField(blank=True, null=True)
    pdf_qr_code_user = models.CharField(max_length=500, blank=True, null=True)
    pdf_qr_code_company = models.CharField(max_length=500, blank=True, null=True)
    signed = models.BooleanField(default=False)
    signed_by_boss = models.BooleanField(default=False)

    passport_photo = models.FileField(blank=True, null=True, verbose_name='Фото пасспорта')
    registration_photo = models.FileField(blank=True, null=True, verbose_name='Фото тех.пасспорта')

    wear_data = models.JSONField(blank=True, null=True)
    service_data = models.JSONField(blank=True, null=True)
    product_data = models.JSONField(blank=True, null=True)
    consumable_data = models.JSONField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.report_id)

    def save_additional_pdf(self, filename, data):
        try:
            path = self.pdf_report_additional.path
        except ValueError:
            path = None
        self.pdf_report_additional.save(filename, ContentFile(data))
        self.save()

        delete_pdf(path)

    def save_pdf(self, filename, data):

        try:
            path = self.pdf_report.path
        except ValueError:
            path = None

        self.pdf_report.save(filename, ContentFile(data))
        self.save()

        delete_pdf(path)

    def delete(self, *args, **kwargs):

        delete_pdf_path(self.passport_photo)
        delete_pdf_path(self.registration_photo)
        delete_pdf_path(self.pdf_report)
        return super(Report, self).delete(*args, **kwargs)

    def precise_iznos_ki(self):
        try:
            return "{0:.0f}".format(self.product_cost - self.product_acc_cost)
        except:
            return 0

    def clean_incoming_data(self):
        self.product_cost = 0
        self.consumable_cost = 0
        self.service_cost = 0
        self.service_data = []
        self.product_data = []
        self.consumable_data = []
        self.wear_data = {}

    def precise_acc_cost(self):
        try:
            return "{0:.0f}".format(self.product_acc_cost)
        except:
            return 0

    def get_product_acc_cost(self):
        print('get_product_acc_cost')
        try:
            print(self.wear_data.__getitem__('accept_wear'))
            self.product_acc_cost = (self.product_cost * (1 - self.wear_data.__getitem__('accept_wear') / 100))
            return self.product_acc_cost
        except:
            return 0

    def wear_data_get(self, key: str):
        try:
            return self.wear_data.__getitem__(key)
        except:
            return 0

    def get_total_report_price(self):
        try:
            self.total_report_cost = ' '.join(
                '{:,}'.format(int(self.service_cost + self.get_product_acc_cost() + self.consumable_cost)).split(','))
        except:
            return 0

    def get_total_report_cost_txt(self):

        try:
            print("REPORT TYPE {}".format(self.type_report))
            if self.type_report == 3:
                print(int(self.total_report_cost))
                price = num2text(int(self.total_report_cost),
                                 main_units=((u'сум', u'сум', u'суммов'), 'f'))
                return price
            self.total_report_cost_txt = num2text(
                int(self.service_cost + self.get_product_acc_cost() + self.consumable_cost),
                main_units=((u'сум', u'сум', u'суммов'), 'f'))
            return self.total_report_cost_txt
        except:
            return num2text(0, main_units=((u'сум', u'сум', u'суммов'), 'f'))

    def set_private_key(self):
        while True:
            figure = uuid.uuid4().hex[:12].upper()
            if not Report.objects.filter(key=figure).exists():
                break
        self.key = figure

    def clear_pdf(self):
        delete_pdf_path(self.pdf_report)
        self.pdf_report.delete()

    @property
    def url_pdf_disposable(self):
        try:
            url = self.pdf_report.url
        except:
            url = ""
        return url

    def save_disposable_pdf(self, data):
        filename = "disposable_{}_{}.pdf".format(datetime.now().timestamp(), self.report_id)
        try:
            path = self.pdf_report.path
        except ValueError:
            path = None

        self.pdf_report.save(filename, data)
        self.save()

        delete_pdf(path)

    @property
    def id(self):
        return self.report_id

    @property
    def holds_images(self):
        return HoldsImages.objects.get(report_id=self.id)

    def save_created_pdf(self, data):
        filename = "created_{}_{}.pdf".format(datetime.now().timestamp(), self.report_id)
        try:
            path = self.pdf_report_additional.path
        except ValueError:
            path = None

        self.pdf_report_additional.save(filename, data)
        self.save()

        delete_pdf(path)

    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'


class Calculation(models.Model):
    total = models.CharField(max_length=20)
    departure = models.CharField(max_length=20)
    opr_ust = models.CharField(max_length=20)
    opr_damage = models.CharField(max_length=20)
    report = models.ForeignKey('Report', on_delete=models.CASCADE, related_name='report', verbose_name='Репорт',
                               null=True, blank=True)

    def get_total_report_cost_txt(self):
        if self.total == "":
            return num2text(0, main_units=((u'сумм', u'сумм', u'суммов'), 'f'))
        else:
            report_rate_price_txt = num2text(int(self.total.strip().replace(' ', "")),
                                             main_units=((u'сумм', u'сумм', u'суммов'), 'f'))
            return report_rate_price_txt


class PaginationModels(models.Model):
    page = models.IntegerField(default=10, verbose_name="Количество документов на одной странице")
    is_chosen = models.BooleanField(default=False, verbose_name="Активация для сайта")

    def save(self, *args, **kwargs):
        PaginationModels.objects.exclude(id=self.id).update(is_chosen=False)
        super(PaginationModels, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Документы на странице'
        verbose_name_plural = 'Документы на странице'

    def __str__(self):
        return str(self.page)
