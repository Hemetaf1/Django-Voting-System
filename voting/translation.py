from modeltranslation.translator import register, TranslationOptions
from .models import Section, Project

@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'synopsis') 