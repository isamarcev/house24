from django.core.management import BaseCommand

from content.models import About, Block, Main, Seo


class Command(BaseCommand):
    help = "Create instance of Main -ansd-> SEO, Block and About models"

    def handle(self, *args, **options):
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
