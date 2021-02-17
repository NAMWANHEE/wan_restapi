from rest_framework import serializers
from .models import We, Dn, hos
class WeSerializer(serializers.ModelSerializer):
    #all_temp = hosSerializer(many=True)
    class Meta:
        model = We
        fields ='__all__'
class hosSerializer(serializers.ModelSerializer):
    #all_temp = WeSerializer(many=True,read_only=True)
    class Meta:
        model = hos
        fields = '__all__'




class DnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dn
        #fields = ['device_name','device_mac','sensor_mac']
        fields = '__all__'



