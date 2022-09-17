from django.db import models


class Main(models.Model):
    header = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    slide1 = models.ImageField(upload_to='content/main', null=True, blank=True)
    slide2 = models.ImageField(upload_to='content/main', null=True, blank=True)
    slide3 = models.ImageField(upload_to='content/main', null=True, blank=True)
    apps_links = models.BooleanField(null=True)
    # block = models.ForeignKey('Block', on_delete=models.PROTECT, null=True)
    seo = models.OneToOneField('Seo', on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name_plural = "Главные"
        verbose_name = "Главная"

    def __str__(self):
        return self.header


class Block(models.Model):
    header = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to='content/block', null=True, blank=True)
    main = models.ForeignKey(Main, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.header

    class Meta:
        verbose_name_plural = "Блоки"
        verbose_name = "Блок"


class Seo(models.Model):
    title = models.CharField(max_length=100)
    desctiption = models.TextField(max_length=1000, null=True, blank=True)
    key_words = models.TextField(max_length=100, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Сео блоки"
        verbose_name = "Сео блок"


class Document(models.Model):
    page = models.ForeignKey('About', on_delete=models.CASCADE, null=True)
    document = models.FileField(upload_to='content/document/', null=True, blank=True)
    title = models.CharField(max_length=30, default="Название документа",null=True, blank=True)

    class Meta:
        verbose_name_plural = "Документы"
        verbose_name = "Документ"

    def __str__(self):
        return f"{self.title}"


# def get_page():
#     x = About.objects.get(pk=1).id
#     return x

class About(models.Model):
    header = models.CharField(max_length=100)
    text = models.TextField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to='content/about/', null=True, blank=True)
    additional_text = models.TextField(max_length=1000, null=True, blank=True)
    additional_header = models.CharField(max_length=100, null=True, blank=True)
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.header

    class Meta:
        verbose_name_plural = "Страницы О нас"
        verbose_name = "Страница о нас"


class AdditionalGallery(models.Model):
    image = models.ImageField(upload_to='content/additional-gallery/', null=True, blank=True)
    page = models.ForeignKey('About', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Доплонительные Галереи"
        verbose_name = "Дополнительная Галерея"


class Gallery(models.Model):
    page = models.ForeignKey('About', on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='content/gallery/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Галереи"
        verbose_name = "Галерея"


class AboutService(models.Model):
    title = models.CharField(max_length=100, null=True)
    text = models.TextField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to='content/about_service/', null=True, blank=True)
    service_page = models.ForeignKey('ServicePage', on_delete=models.CASCADE, null=True)
    # seo = models.OneToOneField(Seo, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Страницы о сервисе"
        verbose_name = "Страница о сервисе"


class ServicePage(models.Model):
    # service = models.ForeignKey(AboutService, on_delete=models.PROTECT, null=True, blank=True)
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT, null=True, blank=True)


    class Meta:
        verbose_name_plural = "Услуги"
        verbose_name = "Услуга"


class Contacts(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000, null=True, blank=True)
    link_comm_site = models.URLField(null=True, blank=True)
    map = models.CharField(max_length=1000, null=True, blank=True)
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT)
    FIO = models.CharField(max_length=130, null=True)
    location = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True, blank=True)


