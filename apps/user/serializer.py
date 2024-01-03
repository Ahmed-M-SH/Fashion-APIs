from rest_framework import serializers
from apps.models import Notification, User
# from apps.address.serializer import UserAddressSerilazer


class UpdateUserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=True, use_url=True)
    email = serializers.EmailField(allow_blank=True)
    # age = serializers.IntegerField(allow_blank=True, )
    phone_number = serializers.CharField(allow_blank=True, )
    username = serializers.CharField(allow_blank=True, )
    register_data = serializers.CharField(allow_blank=True, read_only=True)
    name = serializers.CharField(allow_blank=True, )

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number',
                  'username', 'name', 'register_data', 'image']


class UserProfileSerializer(serializers.ModelSerializer):
    # user_address = UserAddressSerilazer(many=True, read_only=True)
    previous_ordersast = serializers.SerializerMethodField(read_only=True)
    being_prepared_ordersast = serializers.SerializerMethodField(
        read_only=True)

    def get_being_prepared_ordersast(self, obj):
        return obj.order.filter(is_delivered=False, is_proof=True).count()

    def get_previous_ordersast(self, obj):
        return obj.order.filter(is_delivered=True).count()

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number',
                  'username', 'name', 'register_data', 'image', 'previous_ordersast', 'being_prepared_ordersast']


class UserSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(use_url=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number',
                  'username', 'password',  'name', 'register_data', 'is_active', 'image', 'is_deleted']

    def create(self, validated_data):

        password = validated_data.pop("password", None)
        instence = self.Meta.model(**validated_data)
        if instence is not None:
            instence.set_password(password)
        instence.save()
        return instence


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = "__all__"
