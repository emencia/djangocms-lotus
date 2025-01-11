from django import forms

from ..models.article import ArticleFlux


class ArticleFluxForm(forms.ModelForm):
    """
    TODO: Categories should be listed with their language in '[..]'
    """
    class Meta:
        model = ArticleFlux
        exclude = []
        fields = [
            "title",
            "template",
            "length",
            "featured_only",
            "from_categories",
            "from_tags",
        ]
