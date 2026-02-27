from rest_framework import viewsets, permissions

from pay.models import Card
from pay.serializers import CardSer

class CardView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    class Meta:
        model = Card
        fields = ['name','number','balance','email']
