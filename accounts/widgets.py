from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

class ButtonWidget(forms.Widget):
    template_name = 'widgets\\auth_button_widget.html'
    class Media:
        js = (
            'js/admin_button_script.js',
        )
        css = {
            'all': (
                'css/admin_button_widget.css',
            )
        }
    def __init__(self, name, value, attrs=None):
        self.name=name
        self.value=value
    def render(self, name, value, attrs=None):
        context = {
            'url': '/',
            'name':self.name,
            'value':self.value
        }
        return mark_safe(render_to_string(self.template_name, context))
