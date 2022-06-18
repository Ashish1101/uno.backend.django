# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import json
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User , KYC , TRANSACTION_TYPE_CHOICES
from apps.users.serializers import RegisterUserSerializer, VerifyOTPRequestSerializer, KycSerializer
from uno import settings
from generics.utils.services import aadhaar_send_otp , aadhaar_verify_otp


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class AuthView(viewsets.ViewSet):
    model = User
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer
    queryset = model.objects.all()

    @action(methods=['POST'], detail=False)
    def register(self, request):
        print(settings.AUTH_USER_MODEL)
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            otp = user.send_otp()
            return Response({
                "token": token,
                "otp": otp,
                "message": "Registration successfull"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
    def verify(self, request):

        serializer = VerifyOTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(
            id=request.user.id
        ).first()

        print("this is user", user)

        otp = serializer.validated_data['otp'] if 'otp' in serializer.validated_data else None

        if not user:
            raise AuthenticationFailed('User does not exist.')

        is_verified = user.verify_otp_or_mpin(supplied_otp=otp)
        print("this is verified", is_verified)
        if not is_verified:
            error_message = "please enter valid otp"
            return Response(
                {"message": error_message}
            )

        response = Response()
        refresh = RefreshToken.for_user(user)
        response.data = {
            "status": "success",
            "jwt": str(refresh.access_token)
        }
        return response

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
    def pan_verify(self, request):

        serializer = PanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(
            id=request.user.id
        ).first()

        print("this is user", user)

        otp = serializer.validated_data['otp'] if 'otp' in serializer.validated_data else None


class KycView(viewsets.ViewSet):
    queryset = KYC.objects.all()
    model = KYC
    permission_classes = [IsAuthenticated]
    serializer_class = KycSerializer

    @action(methods=['POST'], detail=False, description='user aadhaar kyc')
    def aadhaar_kyc(self, request):
        serializer = KycSerializer(data=request.data)
        user = request.user
        val = request.data
        if serializer.is_valid(raise_exception=True):
            response = aadhaar_send_otp(request.data.get('type_id'))
            if response.status_code == 200:
                if response.json().get('statusCode') == 101:
                    data = {'type': request.data.get('type'), 'type_id': request.data.get('type_id'),
                            'reference_id': response.json().get('requestId')}
                    serializer = KycSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save(created_by=user)
                        return Response(data={"message": response.json().get('result').get('message')},
                                        status=status.HTTP_201_CREATED)
                return Response(data={"message":"otp send failed"}, status=status.HTTP_400_BAD_REQUEST)
            print(response)
            return Response(data={"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, description="Function for Verifying Aadhaar Otp")
    def verify_aadhaar_otp(self, request):
        data = request.data
        user = request.user

        otp = data.get('otp', None)
        if not otp:
            return Response({"message": "otp required"}, status=status.HTTP_400_BAD_REQUEST)

        kyc_data = self.model.objects.filter(
            created_by=user,
            type='aadhaar'
        ).order_by('-created_on')
        if kyc_data is None:
            return Response(data={"message": "Data not found"}, status=status.HTTP_404_NOT_FOUND)
        serialized_data = self.serializer_class(kyc_data).data
        request_id = serialized_data.get('reference_id')
        aadhaar_no = serialized_data.get('type_id')
        response = aadhaar_verify_otp(otp, aadhaar_no, request_id)
        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        return response.Response(data=["Aadhaar verification failed!"], status=status.HTTP_400_BAD_REQUEST)













# @action(methods=["POST"], detail=False)
# def send_otp(self, request):
#     serializer = SendOTPRequestSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#     mobile = serializer.validated_data['mobile']
#     user = self.model.objects.filter(mobile=mobile).first()
#     send_on_email = request.query_params.get('send_on_email')
#
#     if user is None:
#         raise AuthenticationFailed('User does not exist.')
#
#     user.send_otp(send_on_email=send_on_email)
#
#     return Response(data={
#         'message': 'Otp Sent Successfully'
#     })
#
# @action(methods=["POST"], detail=False)
# def verify(self, request):
#     # validate request
#     serializer = VerifyOTPRequestSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#     mobile = serializer.validated_data['mobile']
#     otp = serializer.validated_data['otp'] if 'otp' in serializer.validated_data else None
#     mpin = serializer.validated_data['mpin'] if 'mpin' in serializer.validated_data else None
#
#     user = self.model.objects.filter(mobile=mobile).first()
#
#     if not user:
#         raise AuthenticationFailed('User does not exist.')
#
#     is_verified = user.verify_otp_or_mpin(supplied_otp=otp, supplied_mpin=mpin)
#     if not is_verified:
#         if otp is not None:
#             error_message = 'Invalid OTP'
#         else:
#             error_message = 'Invalid MPIN'
#         raise ValidationError(error_message)
#
#     response = Response()
#     refresh = RefreshToken.for_user(user)
#     response.data = {
#         "status": "success",
#         "jwt": str(refresh.access_token)
#     }
#     return response
#
# @action(methods=["POST"], detail=False)
# def create_user(self, request):
#     serializer = UserCreateSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#     user = self.model.objects.filter(mobile=serializer.validated_data.get('mobile')).first()
#
#     if user is not None and not user.is_mobile_verified:
#         serializer = UserCreateSerializer(data=request.data, instance=user)
#         serializer.is_valid(raise_exception=True)
#
#     user = serializer.save()
#
#     return Response({
#         'user_id': user.id
#     }, status=HTTPStatus.CREATED)
