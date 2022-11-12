from django.core.management import BaseCommand

from content.models import About, Block, Main, Seo, ServicePage, AboutService, Contacts
from crm_home.models import Requisites, Tariff, Unit, Service
from houses.models import House
from users.models import Role


slideurl = 'shortenerua.herokuapp.com/ZXQAA/'
imageurl = 'shortenerua.herokuapp.com/ky1q8/'
class Command(BaseCommand):
    help = "Create instance of Main -ansd-> SEO, Block and About models"

    def handle(self, *args, **options):
        """Main Page instances"""
        seo_main_page = Seo.objects.create(title='Home 24 MAIN',
                                           desctiption='Write your ...',
                                           key_words='Base, Management')
        seo_main_page.save()
        seo_about_page = Seo.objects.create(title='Home 24 ABOUT',
                                            desctiption='Write your ...',
                                            key_words='Base, Management')
        seo_about_page.save()
        main_page = Main.objects.create(
            header='О управляющей компании',
            text='Жилой комплекс «NORD» расположен  на берегу Черного моря в '
                 'живописном районе Одессы. Оригинальная архитектура комплекса'
                 ' делает его уникальным объектом не только для Одессы, '
                 'но и для всей Украины – дом прекрасно вписывается в '
                 'архитектуру берега и открывает свои жильцам и гостям '
                 'прекрасный вид на бескрайнее море. Ярким преимуществом '
                 'жилого комплекса является его месторасположения – удобная'
                 ' транспортная развязка, социальная инфраструктура, парк и '
                 'прекрасный морской воздух создают все условия для '
                 'комфортного проживания.', seo=seo_main_page,
            slide1=slideurl,
            slide2=slideurl, slide3=slideurl
        )
        blocks = Block.objects.bulk_create([
            Block(header='Рестораны и Кафе',
                  description='В непосредственной близости от жилого '
                              'комплекса  расположены рыбный ресторан  и '
                              'итальянская пиццерия. Кроме того, всего в '
                              'десяти минутах ходьбы от комплекса находятся '
                              'рестораны испанской, итальянской, американской,'
                              ' украинской и русской кухни, пиццерии, кафе '
                              'и лаунж-бары на любой вкус.',
                  main=main_page, image=imageurl),
            Block(header='Рестораны и Кафе',
                  description='В непосредственной близости от жилого '
                              'комплекса  расположены рыбный ресторан  и '
                              'итальянская пиццерия. Кроме того, всего в '
                              'десяти минутах ходьбы от комплекса находятся '
                              'рестораны испанской, итальянской, американской,'
                              ' украинской и русской кухни, пиццерии, кафе '
                              'и лаунж-бары на любой вкус.',
                  main=main_page, image=imageurl),
            Block(header='Рестораны и Кафе',
                  description='В непосредственной близости от жилого '
                              'комплекса  расположены рыбный ресторан  и '
                              'итальянская пиццерия. Кроме того, всего в '
                              'десяти минутах ходьбы от комплекса находятся '
                              'рестораны испанской, итальянской, американской,'
                              ' украинской и русской кухни, пиццерии, кафе '
                              'и лаунж-бары на любой вкус.',
                  main=main_page, image=imageurl),
            Block(header='Рестораны и Кафе',
                  description='В непосредственной близости от жилого '
                              'комплекса  расположены рыбный ресторан  и '
                              'итальянская пиццерия. Кроме того, всего в '
                              'десяти минутах ходьбы от комплекса находятся '
                              'рестораны испанской, итальянской, американской,'
                              ' украинской и русской кухни, пиццерии, кафе '
                              'и лаунж-бары на любой вкус.',
                  main=main_page, image=imageurl),
            Block(header='Рестораны и Кафе',
                  description='В непосредственной близости от жилого '
                              'комплекса  расположены рыбный ресторан  и '
                              'итальянская пиццерия. Кроме того, всего в '
                              'десяти минутах ходьбы от комплекса находятся '
                              'рестораны испанской, итальянской, американской,'
                              ' украинской и русской кухни, пиццерии, кафе '
                              'и лаунж-бары на любой вкус.',
                  main=main_page, image=imageurl),
            Block(header='Рестораны и Кафе',
                  description='В непосредственной близости от жилого '
                              'комплекса  расположены рыбный ресторан  и '
                              'итальянская пиццерия. Кроме того, всего в '
                              'десяти минутах ходьбы от комплекса находятся '
                              'рестораны испанской, итальянской, американской,'
                              ' украинской и русской кухни, пиццерии, кафе '
                              'и лаунж-бары на любой вкус.',
                  main=main_page, image=imageurl),
        ])
        about_page = About.objects.create(header='О управляющей компании',
                                          text='ABOTU ABOUT Abotu aboout',
                                          additional_text='Some additional text',
                                          additional_header='some add header',
                                          seo=seo_about_page,
                                          image=imageurl)
        about_page.save()

        # about service instances
        service_page_seo = Seo.objects.create(
            title='About Service page', desctiption='Все возможности системы для ОСМД или управляющей компании ЖКХ: \n учет квартир, жильцов, показаний счетчиков, выставление счетов. \n Мобильные приложения для оплаты коммунальных услуг для жильцов \n многоквартиных домов.',
            key_words='KEy word section')
        service_page = ServicePage.objects.create(seo=service_page_seo)
        services = AboutService.objects.bulk_create([
            AboutService(title='First page service', text='First page service text',
                         image='url', service_page=service_page),
            AboutService(title='second page service', text='First page service text',
                         image='url', service_page=service_page),
            AboutService(title='Third page service', text='Third page service text',
                         image='url', service_page=service_page)
        ])

        seo_contacts = Seo.objects.create(title='Contacts',
                                          desctiption='contacts description',
                                          key_words='contacts')
        seo_contacts.save()
        contacts = Contacts.objects.create(title='Contacts', seo=seo_contacts,
                                           text='COntacts text')
        contacts.save()
        roles = Role.objects.bulk_create([
            Role(name='Директор', statistics=True, cashbox=True, invoice=True,
                 personal_account=True, flat=True, owner=True, house=True,
                 message=True, application=True, meter=True,
                 site_management=True, service=True, tariff=True, role=True,
                 users=True, requisites=True),
            Role(name='Управляющий'),
            Role(name='Бухгалтер'),
            Role(name='Сантехник'),
            Role(name='Электрик'),
        ])

        requisites = Requisites.objects.create(title='ABC oj',
                                               info='Hello world')
        tariffs = Tariff.objects.bulk_create([
            Tariff(name='Successful', describe='Goodlucker'),
            Tariff(name='SecondFull', describe='Yes yes yes')
        ])
        units = Unit.objects.bulk_create([
            Unit(title='m2'),
            Unit(title='String')
        ])
        services_units = Service.objects.bulk_create([
            Service(name='Coding'),
            Service(name='Cooking')
        ])

        houses = House.objects.bulk_create([
            House(title='ЖК Килограмм счастья', address='Бульвар Шевченка 78'),
            House(title='ЖК Килограмм ванили', address='Бульвар Шевченка 76'),
        ])

