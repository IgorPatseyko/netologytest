from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 0


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        i = 0
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            if form.cleaned_data['is_main']:
                i += 1
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
        if i == 0:
            raise ValidationError('Укажите основной отдел')
        if i > 1:
            raise ValidationError('Основной раздел может быть только один')
        return super().clean()  # вызываем базовый код переопределяемого метода


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at']
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass



