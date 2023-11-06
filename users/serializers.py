from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        optional_fields = ['first_name', 'last_name', 'phone', 'avatar', 'country']
        data = {}
        for field in optional_fields:
            if field in validated_data:
                data[field] = validated_data[field]
            else:
                data[field] = None
        if not data['first_name']:
            data['first_name'] = ''
        if not data['last_name']:
            data['last_name'] = ''
        user = User.objects.create(
            email=validated_data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            avatar=data['avatar'],
            phone=data['phone'],
            country=data['country']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = '__all__'
        write_only_fields = ('password',)

