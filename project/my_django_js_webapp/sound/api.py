from rest_framework import serializers, viewsets
from .models import Metadata, Detail, Noise

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = '__all__'

class NoisedataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noise
        fields = '__all__'

class DetaildataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = '__all__'


        

class MetadataViewSet(viewsets.ModelViewSet):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer

class NoisedataViewSet(viewsets.ModelViewSet):
    queryset = Noise.objects.all()
    serializer_class = NoisedataSerializer

class DetaildataViewSet(viewsets.ModelViewSet):
    queryset = Detail.objects.all()
    serializer_class = DetaildataSerializer
