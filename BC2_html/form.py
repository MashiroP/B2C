from django import forms
from django.contrib import auth
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class Commodity_editor(forms.Form):
    # Commodity_name=
    # describe
    # Price
    # Stock
    # Sales_volumes
    # Commodity_category
    # Commodity_img
    # state
    describe = forms.CharField(label='', widget=CKEditorUploadingWidget())