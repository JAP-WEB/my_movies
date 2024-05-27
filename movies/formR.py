from django import forms


class ReviewF(forms.Form):
    rating = forms.ChoiceField(
        label="⭐ Score:",
        choices=[(i, str(i)) for i in range(1, 11)],  # Genera opciones del 1 al 10
        error_messages={"required": "La calificación es obligatoria"},
        widget=forms.Select(attrs={"class": "text-black fixed-size w-full p-2 border border-gray-300 rounded-md"})
    )
    review = forms.CharField(
        label="💭 Review:",
        widget=forms.Textarea(attrs={"class": "text-black w-full p-2 border border-gray-300 rounded-md", "rows": 3})
    )