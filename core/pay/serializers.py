from rest_framework import serializers
from pay.models import Card

class CardSer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('name','number','balance','email')

