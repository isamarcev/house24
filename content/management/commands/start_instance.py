from django.core.management import BaseCommand

from content.models import About, Block, Main, Seo, ServicePage, AboutService, Contacts
from crm_home.models import Requisites
from users.models import Role


class Command(BaseCommand):
    help = "Create instance of Main -ansd-> SEO, Block and About models"

    def handle(self, *args, **options):
        """Main Page instances"""
        seo_main_page = Seo.objects.create(title='Home 24 MAIN', desctiption='Write your ...', key_words='Base, Management')
        seo_main_page.save()
        seo_about_page = Seo.objects.create(title='Home 24 ABOUT', desctiption='Write your ...', key_words='Base, Management')
        seo_about_page.save()
        main_page = Main.objects.create(
            header='Header', text='Text Page', seo=seo_main_page, slide1='url', slide2='url2', slide3='urld3'
        )
        blocks = Block.objects.bulk_create([
            Block(header='Block 1', description='Block 1 Block 1', main=main_page, image='asdfs'),
            Block(header='Block 2', description='Block 1 Block 1', main=main_page, image='asdfs' ),
            Block(header='Block 3', description='Block 1 Block 1', main=main_page, image='asdfs'),
            Block(header='Block 4', description='Block 1 Block 1', main=main_page, image='asdfs'),
            Block(header='Block 5', description='Block 1 Block 1', main=main_page, image='asdfs'),
            Block(header='Block 6', description='Block 1 Block 1', main=main_page, image='asdfs'),
        ])
        about_page = About.objects.create(header='About ABOUT', text='ABOTU ABOUT Abotu aboout',
                                          additional_text='Some additional text', additional_header='some add header',
                                          seo=seo_about_page, image='Photo Directora')
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

        seo_contacts = Seo.objects.create(title='Contacts', desctiption='contacts description', key_words='contacts')
        seo_contacts.save()
        contacts = Contacts.objects.create(title='Contacts', seo=seo_contacts, text='COntacts text')
        contacts.save()
        roles = Role.objects.bulk_create([
            Role(name='Директор'),
            Role(name='Управляющий'),
            Role(name='Бухгалтер'),
            Role(name='Сантехник'),
            Role(name='Электрик'),
        ])

        requisites = Requisites.objects.create(title='ABC oj', info='Hello world')
