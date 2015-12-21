from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms.formsets import formset_factory

from .models import ConversionTask


class TaskForm(forms.ModelForm):
    file_name = ""

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = "converter_form"
        self.helper.form_method = "post"
        self.helper.add_input(Submit("upload", "Upload"))
        self.helper.template = "bootstrap3/whole_uni_formset.html"
        super(TaskForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False

    def clean(self):
        if self.cleaned_data["name"] == "":
            self.cleaned_data["name"] = self.file_name
        return self.cleaned_data

    def clean_file(self):
        new_file_name = self.cleaned_data["file"]
        new_file_type = new_file_name.content_type.rsplit("/", 1)[1]
        if new_file_type != "png":
            raise forms.ValidationError(
                "The file '%s' must be a .png image",
                params=(new_file_name,),
                code="invalid_file",
            )
        self.file_name = new_file_name.name.rsplit(".", 1)[0]
        return new_file_name

    class Meta:
        model = ConversionTask
        fields = ["name", "file"]


TaskFormSet = formset_factory(TaskForm)
