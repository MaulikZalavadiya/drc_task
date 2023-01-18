from utils.APIResponse import APIResponse
from rest_framework.decorators import api_view,permission_classes
from utils.send_mail import send_otp
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import User, Otp
import random
from rest_framework import status
from django.contrib.auth import login,logout
from rest_framework.authtoken.models import Token
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta, datetime


@permission_classes([AllowAny])
@api_view(['POST'])
def Send_opt_API(request):
        user=User.objects.filter(Q(email=request.data.get('email')) | Q(contact=request.data.get('contact'))).first()
        user.save()
        otp=random.randint(1000,9999)
        sent = send_otp(user.email,otp)
        # if sent:
        Otp.objects.filter(user=user).update(is_used=True)            
        Otp.objects.create(user=user,otp=otp)
        return APIResponse(
            {
                'email': user.email,
                'otp': otp,
            },
            status=status.HTTP_201_CREATED,
            notification=('msg', 'otp send Successfully Please check Your email!!!!'))


@permission_classes([AllowAny])
@api_view(['POST'])
def LoginAPI(request):
    email = request.data.get('email', None)
    contact = request.data.get('contact', None)
    otp = request.data['otp']
    try:
        if email:
            user = User.objects.get(email=email)
        else:
            user = User.objects.get(contact=contact)
        # if user.access_timer > datetime.now() and user.access_counter == 3:
        #     user.access_counter =0
            # return APIResponse(
            #     {},
            #     status=status.HTTP_404_NOT_FOUND,
            #     notification=('msg', 'please access after 5 min. !!!'))
    except Exception as e:
        print(e.args)
        return APIResponse(
                {},
                status=status.HTTP_404_NOT_FOUND,
                notification=('msg', 'please enter currect email !!!'))

    try:
        otp_obj = Otp.objects.get(user=user,otp=otp,is_used=False)
    except Exception as e:
        print(e.args)
        user.access_counter +=1
        if user.access_counter == 3:
            user.access_timer = datetime.now() + timedelta(minutes=5)
        user.save()
        return APIResponse(
                {},
                status=status.HTTP_404_NOT_FOUND,
                notification=('msg', 'please enter currect otp !!!!'))
    
    try:
        login(request, user)
        otp_obj.is_used=True
        # otp_obj.deleted_on = datetime.now()
        otp_obj.save()
        token, created = Token.objects.get_or_create(user=user)
        data = {
            "email": user.email,
            'token': token.key,
            'is_register':user.is_register
        }
        return APIResponse(
                data=data,
                status=status.HTTP_200_OK,
                notification=('msg', 'Login Successfully !!!!'))
    except:
        return APIResponse(
                {},
                status=status.HTTP_404_NOT_FOUND,
                notification=('msg', 'please connect your admin'))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def LogoutAPI(request):
    request.user.auth_token.delete()
    logout(request)
    return APIResponse(
        {},
            status=status.HTTP_200_OK,
            notification=('msg', 'logout successfuly !!!'))
