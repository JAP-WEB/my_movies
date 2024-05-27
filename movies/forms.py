#se utilizó para las pruebas de caja de texto en clase
from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label="Nombre", max_length=100, help_text="100 characters max.", 
                                error_messages={"required": "El nombre es obligatorio"},
                                widget=forms.Textarea(attrs={"class":"text-gray-400", "rows": 3, "cols": 60}))