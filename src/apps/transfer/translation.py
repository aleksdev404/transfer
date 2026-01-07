from modeltranslation.translator import translator, TranslationOptions
from . import models


class ExcursionTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'excerpt',
        'description',
    )


class ExcursionTagTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


class ExcursionCategoryTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


class WeekDayTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


class FAQTranslationOptions(TranslationOptions):
    fields = (
        'question',
        'answer'
    )


class PlaceTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


translator.register(models.Excursion, ExcursionTranslationOptions)
translator.register(models.ExcursionTag, ExcursionTagTranslationOptions)
translator.register(models.ExcursionCategory, ExcursionCategoryTranslationOptions) # noqa
translator.register(models.WeekDay, WeekDayTranslationOptions)
translator.register(models.FAQ, FAQTranslationOptions)
translator.register(models.Place, PlaceTranslationOptions)
