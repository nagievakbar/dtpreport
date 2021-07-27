from django import forms
from .models import *
import re
import datetime


class CustomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("DATA")
        # print(self.fields['total_report_cost'].initial)
        # if self.fields['total_report_cost'] != None:
        #     self.fields['total_report_cost'] = re.sub(r"\B(?=(\d{3})+(?!\d))", " ", self.fields['total_report_cost'])


class ReportForm(CustomForm):
    """docstring for ReportForm."""

    report_date = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Дата отчёта', 'class': 'input_in'}))
    report_number = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'placeholder': 'Номер отчёта', 'class': 'input_in'}))
    total_report_cost = forms.CharField(required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'invisible_class all_sum divide-integer'}))

    def custom_integer_validation(self):
        print('asdsasad')
        print(self['total_report_cost'].value())
        self.fields['total_report_cost'].initial = 123

    class Meta:
        model = Report
        fields = ['report_date', 'report_number', 'total_report_cost']


BRANDS = (
    ('Выберите Марку', "Выберите Марку"),
    ('Кобальт', 'Кобальт'),
    ('Спарк', 'Спарк'),
    ('Нексия3', 'Нексия3'),
    ('Малибу', 'Малибу'),
    ('Нексия Sonc', 'Нексия Sonc'),
    ('Дамас', 'Дамас'),
    ('Тико', 'Тико'),
    ('Тико', 'Тико'),
    ('Матиз', 'Матиз'),
    ('Матиз Бест', 'Матиз Бест'),
    ('Нексия Donc', 'Нексия Donc'),
    ('Ласетти', 'Ласетти'),
    ('Каптива', 'Каптива'),
    ('Такума', 'Такума'),
    ('Эпика', 'Эпика')
)

TYPE_CAR = (
    ('Выберите тип машины', 'Выберите тип машины'),
    ('Грузовой', 'Грузовой'),
    ('Легковой', 'Легковой')
)


class CarForm(forms.ModelForm):
    """docstring for CarForm."""
    brand_text = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Марка', 'class': 'input_in'}))
    brand = forms.ChoiceField(choices=BRANDS, required=False,
                              widget=forms.Select(attrs={'class': 'form-control select-block drop-down-list'}))
    car_number = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Номер машины', 'class': 'input_in'}))
    registration = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'placeholder': 'Тех. паспорт', 'class': 'input_in'}))
    engine_number = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'placeholder': 'Двигатель', 'class': 'input_in'}))
    body_number = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Кузов', 'class': 'input_in'}))
    chassis = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Шасси', 'class': 'input_in'}))
    car_color = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Цвет окраски', 'class': 'input_in'}))
    mileage = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Пробег', 'class': 'input_in'}))
    release_date = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Год и месяц выпуска', 'class': 'input_in'}))

    car_owner = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Владелец', 'class': 'input_in'}))
    owner_address = forms.CharField(required=False,
                                    widget=forms.Textarea(
                                        attrs={'placeholder': 'Адрес владельца', 'class': 'input_in',
                                               'onkeyup': 'textAreaAdjust(this)'}))
    type_of_car = forms.ChoiceField(
        required=False,
        choices=TYPE_CAR,
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Car
        fields = ['brand_text',
                  'brand',
                  'car_number',
                  'registration',
                  'engine_number',
                  'body_number',
                  'chassis',
                  'car_color',
                  'mileage',
                  'release_date',
                  'car_owner',
                  'owner_address',
                  'type_of_car']


class CalculationForm(forms.ModelForm):
    total = forms.CharField(required=False,
                            widget=forms.TextInput(
                                attrs={'class': 'input2 work-price-input2 price_all total divide-integer',
                                       'readonly': True}))
    departure = forms.CharField(required=False,
                                widget=forms.TextInput(
                                    attrs={'class': 'input2 work-price-input2 price_3 total divide-integer'}))
    opr_ust = forms.CharField(required=False,
                              widget=forms.TextInput(
                                  attrs={'class': 'input2 work-price-input2 price_2 total divide-integer'}))
    opr_damage = forms.CharField(required=False,
                                 widget=forms.TextInput(
                                     attrs={'class': 'input2 work-price-input2 price_1 total divide-integer'}))

    class Meta:
        model = Calculation
        fields = [
            'total',
            'departure',
            'opr_ust',
            'opr_damage',
        ]


# class ContractFormEdit(forms.ModelForm):
#     """docstring for ContractForm."""
#     contract_date = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={'placeholder': 'Дата договора', 'class': 'input_in'}))
#     contract_number = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={'placeholder': 'Номер договора', 'class': 'input_in'}))
#
#     class Meta:
#         model = Contract
#         fields = ['contract_date', 'contract_number']


class CustomerForm(forms.ModelForm):
    """docstring for CustomerForm."""

    name = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Заказчик', 'class': 'input_in'}))
    address = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Адрес заказчика', 'class': 'input_in'}))
    passport_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Паспорт', 'class': 'input_in'}))
    when_passport_issued = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Когда выдан', 'class': 'input_in'}))
    whom_passport_issued = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Кем выдан', 'class': 'input_in'}))
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Телефон', 'class': 'input_in'}))
    gnu_or_gje = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Г-ну', 'class': 'input_in'}))
    uvajaemaya = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Уважаемый', 'class': 'input_in'}))

    mesto_osmotra = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Акт осмотра Место', 'class': 'input_in'}))

    class Meta:
        model = Customer
        fields = ['name', 'address', 'passport_number', 'when_passport_issued',
                  'whom_passport_issued', 'phone_number', 'gnu_or_gje', 'uvajaemaya', 'mesto_osmotra']


class CustomerFormEdit(forms.ModelForm):
    name = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Заказчик', 'class': 'input_in'}))
    address = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Адрес заказчика', 'class': 'input_in'}))
    gnu_or_gje = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Г-ну', 'class': 'input_in'}))
    uvajaemaya = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Уважаемый', 'class': 'input_in'}))

    mesto_osmotra = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Акт осмотра Место', 'class': 'input_in'}))

    class Meta:
        model = Customer
        fields = ['name', 'address', 'gnu_or_gje', 'uvajaemaya', 'mesto_osmotra']


class EnumerationForms(forms.ModelForm):
    p_c = forms.CharField(required=False,
                          widget=forms.TextInput(attrs={'placeholder': ' Р/c №', 'class': 'input_in'}))
    bank = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Банк', 'class': 'input_in'}))
    MFO = forms.CharField(required=False,
                          widget=forms.TextInput(attrs={'placeholder': 'МФО', 'class': 'input_in'}))
    INN = forms.CharField(required=False,
                          widget=forms.TextInput(attrs={'placeholder': 'ИНН', 'class': 'input_in'}))
    OKED = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'ОKED', 'class': 'input_in'}))

    class Meta:
        model = Enumeration
        fields = [
            'p_c',
            'bank',
            'MFO',
            'INN',
            'OKED'
        ]


class ServiceForm(forms.Form):
    service_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input2 work-price-input2 first2'}))
    name = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'input2 work-price-input2 name2', 'onkeyup': 'textAreaAdjust(this)'}))
    norm_per_hour = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'input2 work-price-input2 time2 commaToPoint'}))
    premium = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input2 work-price-input2 allowance2 commaToPoint'}))  # 'value': '0'
    price = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input2 work-price-input2 price2 divide-integer commaToPoint'}))
    service_cost = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input2 work-price-input2 sum2 divide-integer', 'readonly': ''}))
    # 'readonly': ''


# user = User.objects.get(id=u.__getitem__(0).myuser.user_id)
class ProductForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'input3 work-price-input3 name3', 'onkeyup': 'textAreaAdjust(this)'}))
    quantity = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input3 work-price-input3 time3 commaToPoint', }))  # 'value': '0'
    price = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input3 work-price-input3 price3 divide-integer commaToPoint', }))
    product_cost = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input3 work-price-input3 sum3 divide-integer ', 'readonly': ''}))


class ConsumableForm(forms.Form):
    consumable_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 first4'}))
    name = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'input4 work-price-input4 name4', 'onkeyup': 'textAreaAdjust(this)'}))
    unit = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 time4 commaToPoint', }))
    quantity = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 allowance4 commaToPoint', }))  # 'value': '0'
    price = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input4 work-price-input4 price4 divide-integer commaToPoint', }))
    consumable_cost = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'input4 work-price-input4 sum4 divide-integer commaToPoint', 'readonly': ''}))


class ImageForm(forms.ModelForm):
    image = forms.CharField(
        required=False,
        widget=forms.FileInput(
            attrs={'id': 'imageinput', 'type': 'file', 'name': 'input', 'multiple': True, 'required': False}))

    class Meta:
        model = Images
        fields = ['image']


class PPhotoForm(forms.ModelForm):
    photo = forms.CharField(
        required=False,
        widget=forms.FileInput(
            attrs={'id': 'pphotoinput', 'type': 'file', 'name': 'input', 'multiple': True}))

    class Meta:
        model = PassportPhotos
        fields = ['photo']


class OPhotoForm(forms.ModelForm):
    photos = forms.CharField(
        required=False,
        widget=forms.FileInput(
            attrs={'id': 'ophotoinput', 'type': 'file', 'name': 'input', 'multiple': True}))

    class Meta:
        model = OtherPhotos
        fields = ['photos']


class DisposableForm(forms.ModelForm):
    pdf_report = forms.CharField(
        required=False,
        widget=forms.FileInput(
            attrs={'id': 'disposable_pdf', 'type': 'file', 'name': 'input', 'multiple': False}))

    class Meta:
        model = Report
        fields = ['pdf_report']


class ChecksForm(forms.ModelForm):
    checks = forms.CharField(
        required=False,
        widget=forms.FileInput(
            attrs={'id': 'checksinput', 'type': 'file', 'name': 'input', 'multiple': True}))

    class Meta:
        model = Checks
        fields = ['checks']


class WearForm(forms.Form):
    point = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input work-price-input point-input commaToPoint'}))
    weight = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input work-price-input weight-input commaToPoint'}))
    wear = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input work-price-input prehnite-input', 'readonly': ""}))
    accept_wear = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input work-price-input prehnite-input commaToPoint'}))


class ClosingDescForm(forms.ModelForm):
    movable_property_desc = forms.CharField(required=False,
                                            widget=forms.TextInput(
                                                attrs={'class': 'input_in'}), )
    movable_property = forms.CharField(required=False,
                                       widget=forms.Textarea(
                                           attrs={'placeholder': 'Движимое имущество', 'class': 'input_in',
                                                  'onkeyup': 'textAreaAdjust(this)', 'style': 'height:60px',}),
                                       )
    place_registration_desc = forms.CharField(required=False,
                                              widget=forms.TextInput(
                                                  attrs={'class': 'input_in'}),
                                              )
    damage_auto_desc = forms.CharField(required=False,
                                       widget=forms.Textarea(
                                           attrs={'class': 'input_in',
                                                  'style': 'height:50px',
                                                  'onkeyup': 'textAreaAdjust(this)'}))
    damage_auto = forms.CharField(required=False,
                                  widget=forms.TextInput(
                                      attrs={'placeholder': 'Ущерб автотранспортного средства по состоянию',
                                             'class': 'input_in'}))
    owner_desc = forms.CharField(required=False,
                                 widget=forms.TextInput(
                                     attrs={'class': 'input_in'}),
                                 )
    customer_desc = forms.CharField(required=False,
                                    widget=forms.TextInput(
                                        attrs={'class': 'input_in'}),
                                    )
    customer_address_desc = forms.CharField(required=False,
                                            widget=forms.TextInput(
                                                attrs={'class': 'input_in'}),
                                            )
    customer_props_desc = forms.CharField(required=False,
                                          widget=forms.TextInput(
                                              attrs={'class': 'input_in'}),
                                          )

    class Meta:
        model = Closing
        exclude = ('report',)
        fields = '__all__'


#
# class ClosingForm(forms.ModelForm):
#     report_number = forms.CharField(required=False,
#                                     widget=forms.TextInput(
#                                         attrs={'placeholder': 'Номер отчета', 'class': 'input_in'}))
#     movable_property = forms.CharField(required=False,
#                                        widget=forms.TextInput(
#                                            attrs={'placeholder': 'Движимое имущество', 'class': 'input_in'}))
#     place_registration = forms.CharField(required=False,
#                                          widget=forms.TextInput(
#                                              attrs={'placeholder': 'Место регистрации объекта оценки',
#                                                     'class': 'input_in'}))
#     damage_auto = forms.CharField(required=False,
#                                   widget=forms.TextInput(
#                                       attrs={'placeholder': 'Ущерб автотранспортного средства по состоянию',
#                                              'class': 'input_in'}))
#     report_date = forms.CharField(required=False,
#                                   widget=forms.TextInput(
#                                       attrs={'placeholder': 'Дата отчета',
#                                              'class': 'input_in'}))
#     owner = forms.CharField(required=False,
#                             widget=forms.TextInput(attrs={'placeholder': 'Владелец', 'class': 'input_in'}))
#     customer = forms.CharField(required=False,
#                                widget=forms.TextInput(attrs={'placeholder': 'Заказчик', 'class': 'input_in'}))
#     address_customer = forms.CharField(required=False,
#                                        widget=forms.TextInput(
#                                            attrs={'placeholder': 'Адрес Заказчика', 'class': 'input_in'}))
#     passport_data = forms.CharField(required=False,
#                                     widget=forms.TextInput(
#                                         attrs={'placeholder': 'Паспортные данные', 'class': 'input_in'}))
#     # executor = forms.CharField(required=False,
#     #                            widget=forms.TextInput(attrs={'placeholder': 'Исполнитель', 'class': 'input_in'}))
#     # requisite_executor = forms.CharField(required=False,
#     #                                      widget=forms.TextInput(
#     #                                          attrs={'placeholder': 'Реквизиты исполнителя', 'class': 'input_in'}))
#     # aim_mark = forms.CharField(required=False,
#     #                            widget=forms.TextInput(
#     #                                attrs={'placeholder': 'Цель и назначение оценки', 'class': 'input_in'}))
#     # appearance_cost = forms.CharField(required=False,
#     #                                   widget=forms.TextInput(
#     #                                       attrs={'placeholder': 'Вид определяемой стоимости', 'class': 'input_in'}))
#     # form_report = forms.CharField(required=False,
#     #                               widget=forms.TextInput(attrs={'placeholder': 'Электронная', 'class': 'input_in'}))
#     # license_executor = forms.CharField(required=False,
#     #                                    widget=forms.TextInput(
#     #                                        attrs={'placeholder': 'П Сведения о Лицензии и Страховом полисе Исполнителя',
#     #                                               'class': 'input_in'}))
#     # legislative_contractual_limitations = forms.CharField(required=False,
#     #                                                       widget=forms.TextInput(
#     #                                                           attrs={
#     #                                                               'placeholder': 'Законодательные или договорные ограничения',
#     #                                                               'class': 'input_in'}))
#     main_mark = forms.CharField(required=False,
#                                 widget=forms.TextInput(
#                                     attrs={'placeholder': 'Основание для проведения оценки', 'class': 'input_in'}))
#     data_mark = forms.CharField(required=False,
#                                 widget=forms.TextInput(attrs={'placeholder': 'Дата оценки', 'class': 'input_in'}))
#     data_creation_mark = forms.CharField(required=False,
#                                          widget=forms.TextInput(
#                                              attrs={'placeholder': 'Дата составления отчета об оценки',
#                                                     'class': 'input_in'}))
#
#     class Meta:
#         model = Closing
#         exclude = ('sign',)
#         fields = '__all__'


class CarClosingForm(forms.ModelForm):
    """docstring for CarForm."""
    # brand_text = forms.CharField(required=False,
    #                              widget=forms.TextInput(attrs={'placeholder': 'Марка', 'class': 'input_in'}))
    # car_number = forms.CharField(required=False,
    #                              widget=forms.TextInput(attrs={'placeholder': 'Номер машины', 'class': 'input_in'}))
    # release_date = forms.CharField(required=False, widget=forms.TextInput(
    #     attrs={'placeholder': 'Год и месяц выпуска', 'class': 'input_in'}))

    car_owner = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Владелец', 'class': 'input_in'}))
    owner_address = forms.CharField(required=False,
                                    widget=forms.Textarea(
                                        attrs={'placeholder': 'Адрес владельца', 'class': 'input_in',
                                               'onkeyup': 'textAreaAdjust(this)'}))

    class Meta:
        model = Car
        fields = ['brand_text', 'car_number', 'release_date', 'car_owner', 'owner_address']


REPORT_TYPE = (
    (0, 'Физ. лицо'),
    (1, 'Юр. лицо')

)


class ReportClosingForm(CustomForm):
    """docstring for ReportForm."""

    report_date = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Дата отчёта', 'class': 'input_in'}))
    report_number = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'placeholder': 'Номер отчёта', 'class': 'input_in'}))
    total_report_cost = forms.CharField(required=False,
                                        widget=forms.NumberInput(
                                            attrs={'placeholder': 'Ущерб автотранспортного средства(цена)',
                                                   'class': 'input_in'}))

    class Meta:
        model = Report
        fields = ['report_date', 'report_number', 'total_report_cost']


class CustomerClosingForm(forms.ModelForm):
    name = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Заказчик', 'class': 'input_in'}))
    address = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Адрес заказчика', 'class': 'input_in'}))
    passport_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Паспорт', 'class': 'input_in'}))
    when_passport_issued = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Когда выдан', 'class': 'input_in'}))
    whom_passport_issued = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Кем выдан', 'class': 'input_in'}))
    type_customer = forms.ChoiceField(
        required=False,
        choices=REPORT_TYPE,
        widget=forms.Select(attrs={'class': 'form-control type_customer', 'id': 'id_type_of_car'}))

    class Meta:
        model = Customer
        fields = ['name', 'address', 'passport_number', 'when_passport_issued',
                  'whom_passport_issued', 'type_customer']


class ContractForm(forms.ModelForm):
    """docstring for ContractForm."""

    contract_date = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'placeholder': 'Дата договора', 'class': 'input_in'}))
    contract_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Номер договора', 'class': 'input_in'}))

    class Meta:
        model = Contract
        fields = ['contract_date', 'contract_number']
