#Utilizar formularios
from django import forms

#Formulario para el reiew se debe llenar para enviar
class ReviewF(forms.Form):
    rating = forms.ChoiceField(label="Calificación",
                                choices=[(i, str(i)) for i in range(1, 11)],  # Genera opciones del 1 al 10
                                error_messages={"required": "La calificación es obligatoria"},
                                widget=forms.Select(attrs={"class":"text-gray-400"}))
    review = forms.CharField(label="Reseña", widget=forms.Textarea(attrs={"class":"text-gray-400", "rows": 3, "cols": 60}))