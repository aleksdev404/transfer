import os
import uuid

from django_resized import ResizedImageField
from slugify import slugify

from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _


def upload_to(field_name: str = None, filename_attr: str = None):
    """
    Путь:
        <app>/<model>/<field(optional)>/<slugified_name>.<ext>

    Имя файла:
        1) slugify(instance.<filename_attr>)
        2) иначе slugify(<original filename>)
    """

    def _(instance, filename: str):
        app = instance._meta.app_label
        model = instance.__class__.__name__.lower()

        ext = os.path.splitext(filename)[1]
        original_base = os.path.splitext(filename)[0]

        # источник имени
        base = original_base
        if filename_attr:
            value = getattr(instance, filename_attr, None)
            if value:
                base = value

        # всегда slugify
        base = slugify(base)

        path = f"{app}/{model}"
        if field_name:
            path += f"/{field_name}"

        return f"{path}/{base}{ext}"

    return _


class WeekDay(models.Model):
    name = models.CharField('Adı', max_length=30)

    class Meta:
        verbose_name = 'Hafta günü'
        verbose_name_plural = 'Hafta günleri'
        ordering = ('-id', )

    def __repr__(self):
        return f'<WeekDay {self.name}>'

    def __str__(self):
        return f'{self.name}'


class Place(models.Model):
    name = models.CharField('Konum adı', max_length=100)
    link_map = models.URLField('Konum linki', blank=True, null=True)

    def __repr__(self):
        return f'<Place {self.name}>'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Konum'
        verbose_name_plural = 'Konumlar'
        ordering = ('name',)


class Transfer(models.Model):
    email = models.EmailField(_('E-mail'), blank=True, null=True)
    phone = models.CharField(_('Phone number'), max_length=20)

    pax = models.PositiveIntegerField(_('Passengers'))
    baggage = models.PositiveIntegerField(_('Baggage (kg)'))

    rfrom = models.ForeignKey(verbose_name=_('From where?'), to=Place, on_delete=models.SET_NULL, blank=True, null=True, related_name='transfer_from') # noqa ignore
    rto = models.ForeignKey(verbose_name=_('To where?'), to=Place, on_delete=models.SET_NULL, blank=True, null=True, related_name='transfer_to') # noqa ignore

    date = models.DateField(_('Meeting date'))
    time = models.TimeField(_('Meeting time'))

    proceed = models.BooleanField('İncelendi', default=False)
    created = models.DateTimeField('Oluşturma tarihi', auto_now_add=True)

    class Meta:
        verbose_name = 'Transfer'
        verbose_name_plural = 'Transferler'
        ordering = ('-date', '-time', 'proceed')

    def __repr__(self):
        return f'<Transfer {self.date} {self.time}>'

    def __str__(self):
        return f'{self.date} {self.time} / {self.rfrom} -> {self.rto}' # noqa ignore


class TransferExtended(Transfer, models.Model):
    price = models.PositiveIntegerField('Fiyat (USD)', blank=True, null=True)
    price_final = models.BooleanField('Fiyat sonmu?', default=True)

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    back = models.BooleanField('Ek geri dönüş')

    iata = models.CharField(_('Flight code (IATA)'), max_length=10, blank=True, null=True) # noqa
    iata_back = models.CharField(_('Flight code (IATA)'), max_length=10, blank=True, null=True) # noqa

    date_back = models.DateField(_('Meeting date'), blank=True, null=True)
    time_back = models.TimeField(_('Meeting time'), blank=True, null=True)

    pax_back = models.PositiveIntegerField(_('Passengers'), blank=True, null=True) # noqa
    baggage_back = models.PositiveIntegerField(_('Baggage (kg)'), blank=True, null=True) # noqa

    first_name = models.CharField(_('Name'), max_length=20)
    last_name = models.CharField(_('Surname'), max_length=20)
    comment = models.TextField(_('Description'), blank=True, null=True)

    done = models.BooleanField('Tamamlandı', default=False)
    paid = models.BooleanField('Ödeme yapıldı', default=False)

    rating = models.PositiveIntegerField(_('Rating'), blank=True, null=True) # noqa ignore

    class Meta:
        verbose_name = 'Transfer (Gelişmiş)'
        verbose_name_plural = 'Transferler (Gelişmiş)'
        ordering = ('-paid', '-date', '-time', 'price')

    def __repr__(self):
        return f'<TransferExtended {self.date} {self.time} {self.price}>'

    def __str__(self):
        return f'{self.date} {self.time} / {self.rfrom} -> {self.rto} / {self.price}' # noqa ignore

    def get_absolute_url(self):
        return reverse_lazy('transfer:transfer-extended-checkout', args=[self.uuid]) # noqa

    def pax_total(self):
        return f'{self.pax} - {self.pax_back}'

    def date_total(self):
        return f'{self.date} - {self.date_back}'

    def time_total(self):
        return f'{self.time} - {self.time_back}'

    def baggage_total(self):
        return f'{self.baggage} - {self.baggage_back}'

    def iata_total(self):
        return f'{self.iata} - {self.iata_back}'


class ExcursionCategory(models.Model):
    name = models.CharField('Kategori adı', max_length=25)

    class Meta:
        verbose_name = 'Tur kategorisi'
        verbose_name_plural = 'Tur kategorileri'
        ordering = ('name',)

    def __repr__(self):
        return f'<ExcursionCategory {self.name}>'

    def __str__(self):
        return f'{self.name}'


class ExcursionTag(models.Model):
    name = models.CharField('Kategori etiketi', max_length=25)

    class Meta:
        verbose_name = 'Tur etiketi'
        verbose_name_plural = 'Tur etiketleri'
        ordering = ('name',)

    def __repr__(self):
        return f'<ExcursionTag {self.name}>'

    def __str__(self):
        return f'{self.name}'


class Excursion(models.Model):
    name = models.CharField('Tur adı', max_length=55)
    excerpt = models.TextField('Kısa açıklama')
    description = models.TextField('Açıklama')
    duration_hours = models.PositiveIntegerField('Tur süresi', blank=True, null=True)  # noqa
    created = models.DateField(auto_now_add=True)
    image = ResizedImageField(
        size=[1024, 724],
        crop=['middle', 'center'],
        quality=75,
        upload_to=upload_to("image", "name")
    )
    image_head = ResizedImageField(
        size=[1920, 600],
        crop=['middle', 'center'],
        quality=90,
        upload_to=upload_to("image_head", "name")
    )
    category = models.ForeignKey(verbose_name='Kategori', to=ExcursionCategory, on_delete=models.SET_NULL, blank=True, null=True) # noqa ignore
    tags = models.ManyToManyField(to=ExcursionTag, blank=True)
    video_link = models.URLField('Video linki', blank=True, null=True)
    time_start = models.TimeField('Başlangıç saati', blank=True, null=True)
    time_end = models.TimeField('Bitiş saati', blank=True, null=True)
    weekdays = models.ManyToManyField(verbose_name='Hafta günleri', to=WeekDay, blank=True) # noqa

    class Meta:
        verbose_name = 'Tur'
        verbose_name_plural = 'Turlar'
        ordering = ('name', 'created')

    def __repr__(self):
        return f'<Excursion {self.name}>'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('transfer:tour-detail', args=[self.id])


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class CompanyData(SingletonModel, models.Model):
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_repr = models.CharField(max_length=25, blank=True, null=True)
    phone_whatsapp = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField('Kurumsal E-posta', blank=True, null=True)
    address = models.TextField('İş adresi', blank=True, null=True)
    address_link = models.TextField('İş adresi linki', blank=True, null=True)

    class Meta:
        verbose_name = 'Site ayarları'
        verbose_name_plural = 'Site ayarları'


class Media(models.Model):
    name = models.CharField('Medya adı', max_length=60)
    fa_icon = models.CharField('Ikon kodu (Font Awesome)', max_length=40)
    link = models.URLField('Link')

    class Meta:
        verbose_name = 'Medya hesabı'
        verbose_name_plural = "Medya hesapları"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Media {self.name}> {self.id}'


class Request(models.Model):
    full_name = models.CharField(_('Name surname'), max_length=55)
    email = models.EmailField(_('E-mail'))
    description = models.TextField(_('Your message'))
    created = models.DateTimeField('Tarih ve saat', auto_now=True)
    answered = models.BooleanField('Cevaplandı', default=False)

    class Meta:
        verbose_name = 'Talep, Şikayet'
        verbose_name_plural = 'Talepler ve Şikayetler'

    def __str__(self):
        return f'{self.full_name} {self.created}'

    def __repr__(self):
        return f'<Request {self.id} {self.full_name} {self.email}>'


class FAQ(models.Model):
    question = models.CharField('Soru', max_length=64)
    answer = models.TextField('Cevap')

    class Meta:
        verbose_name = 'Sıkça sorulan soru'
        verbose_name_plural = 'Sıkça sorulan sorular'

    def __str__(self):
        return f'{self.question}'

    def __repr__(self):
        return f'<FAQ {self.id} {self.question}>'
