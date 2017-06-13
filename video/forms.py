from django import forms
from .models import Videos
class VideoForm(forms.Form):
    video_name = forms.CharField(required=True, max_length=200, min_length=2, strip=True)
    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        if kwargs.get('data'):
            self.video_url = kwargs.get('data').get('data').get('video_access_path')
            self.creator_id = kwargs.get('data').get('data').get('creator_id')
        super().__init__(*args, **kwargs)

    def clean(self):
        self.cleaned_data['video_url'] = self.video_url
        self.cleaned_data['creator_id'] = self.creator_id
        if not self.cleaned_data.get('video_url'):
            raise forms.ValidationError("Upload not successfull. Please try again.")
        if not self.cleaned_data.get('video_name'):
            raise forms.ValidationError("Video name is required")
        if not self.cleaned_data.get('video_name'):
            raise forms.ValidationError("Video name is required")
        return self.cleaned_data

    def save(self):
        video_obj = Videos.objects.create(**self.cleaned_data)
        return video_obj