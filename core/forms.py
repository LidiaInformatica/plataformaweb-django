# core/forms.py
from django import forms
from estudiantes.models import Apoderado

class NotificacionManualForm(forms.Form):
    apoderado = forms.ModelChoiceField(queryset=Apoderado.objects.all(), label="Apoderado")
    asunto = forms.CharField(max_length=100, label="Asunto")
    mensaje = forms.CharField(widget=forms.Textarea, label="Mensaje")
