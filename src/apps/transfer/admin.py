from django.contrib import admin

from . import models


@admin.register(models.Transfer)
class TransferAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = (
        'date',
        'time',
        'rfrom',
        'rto',
        'pax',
        'baggage',
        'phone',
        'email',
    )
    list_filter = (
        'proceed',
    )


@admin.register(models.TransferExtended)
class TransferExtendedAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = (
        'uuid',
        'date',
        'time',
        'rating',
        'rfrom',
        'rto',
        'iata_total',
        'pax_total',
        'baggage_total',
        'paid',
        'created',
        'phone',
        'email',
        'proceed',
    )
    list_filter = (
        'proceed',
        'paid',
        'back',
        'created'
    )
    fieldsets = (
        (
            'Şahsi',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'phone'
                )
            }
        ),
        (
            'Transfer',
            {
                'fields': (
                    'uuid',
                    'proceed',
                    'done',
                    'back',
                    'rto',
                    'rfrom',
                    'price',
                    'paid',
                )
            },
        ),
        (
            'Gidiş',
            {
                'fields': (
                    'date',
                    'time',
                    'pax',
                    'baggage',
                    'iata',
                )
            },
        ),
        (
            'Geliş',
            {
                'fields': (
                    'date_back',
                    'time_back',
                    'pax_back',
                    'baggage_back',
                    'iata_back'
                )
            }
        )
    )


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'link_map'
    )


@admin.register(models.Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created'
    )


@admin.register(models.ExcursionCategory)
class ExcursionCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(models.ExcursionTag)
class ExcursionTagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(models.CompanyData)
class CompanyDataAdmin(admin.ModelAdmin):
    list_display = (
        'phone',
        'phone_repr',
        'phone_whatsapp',
        'email',
        'address',
        'address_link'
    )


@admin.register(models.WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(models.Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(models.FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'answer',
        'question_en',
        'answer_en'
    )
    list_editable = (
        'question_en',
        'answer_en'
    )


@admin.register(models.Request)
class RequestAdmin(admin.ModelAdmin):
    list_filter = ('answered',)
    list_display = (
        'full_name',
        'email',
        'created',
        'answered'
    )
