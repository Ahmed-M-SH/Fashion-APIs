from rest_framework import serializers
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(use_url=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number',
                  'username', 'password',  'name', 'image']

    def create(self, validated_data):

        password = validated_data.pop("password", None)
        instence = self.Meta.model(**validated_data)
        if instence is not None:
            instence.set_password(password)
        instence.save()
        return instence
