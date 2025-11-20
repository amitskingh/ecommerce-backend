from rest_framework import serializers
from ..models import User


class UserStripeAccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["stripe_account_id"]

    def to_representation(self, instance):
        return {"stripe_account_id": instance.stripe_account_id}