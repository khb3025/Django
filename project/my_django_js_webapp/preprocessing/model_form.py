from django import forms
from sound.models import Metadata, Noise, Detail

class MetadataForm(forms.ModelForm):
    class Meta:
        model = Metadata
        fields = '__all__'
        
class NoiseForm(forms.ModelForm): 
    class Meta:
        model = Noise
        fields = '__all__' 

class DetailForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = '__all__'
        
