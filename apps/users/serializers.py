from django.db import IntegrityError
from rest_framework import serializers
from apps.users.models import User, KYC , TRANSACTION_TYPE_CHOICES
from generics.utils.services import isPanValid , isAadhaarValid


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['mobile']


    def validate(self, data):
        mobile = data['mobile']

        if len(mobile) is not 10:
            raise serializers.ValidationError("Please enter valid number")
        return super().validate(data)

    def create(self, validated_data):
        mobile = validated_data['mobile']
        try:
            instance = super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError("User with this number already exists.")
        except Exception as e:
            raise serializers.ValidationError("Something Went Wrong!")

        return instance


class VerifyOTPRequestSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    otp = serializers.CharField(required=False, max_length=6, min_length=6)


class KycSerializer(serializers.ModelSerializer):
    type_id = serializers.CharField(required=True)
    type = serializers.CharField(required=True)

    def validate(self, data):
        print(data)
        if data.get('type') == 'aadhaar':
            if not isAadhaarValid(data.get('type_id')):
                raise serializers.ValidationError("Incorrect Aadhaar")
            return super().validate(data)
        if data.get('type') == 'pan':
            if not isPanValid(data.get('type_id')):
                raise serializers.ValidationError("Incorrect Pan")
            return super().validate(data)
        raise serializers.ValidationError('Unknown type')

    def create(self, validate_data):
        print(validate_data)
        try:
            instance = super().create(validate_data)
        except IntegrityError as e:
            raise serializers.ValidationError("Kyc with {} is already exists".format(validate_data.get('type_id')))
        except Exception as e:
            raise serializers.ValidationError("Something Went Wrong!")
        return instance

    class Meta:
        model = KYC
        fields = ['type', 'type_id']





    class Meta:
        model = KYC
        fields = '__all__'

