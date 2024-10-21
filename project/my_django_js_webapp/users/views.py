from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.http import JsonResponse
from django.middleware.csrf import get_token


from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomLoginForm


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/common/main/')  # 성공 시 리다이렉트할 URL
    else:
            form = CustomLoginForm()
            messages.error(request, '로그인 실패. 사용자 id 또는 비밀번호를 확인하세요.')

    return render(request, 'accounts/login.html', {'form': form})



def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            # request.session['user_info'] = {
            #     'username': user.username,
            #     'email': user.email,
            #     # 필요한 다른 정보도 추가 가능
            # }
            # token, _ = Token.objects.get_or_create(user=user)
            return Response({'success': True, 
                             'user' : { 'username' : user.username,
                                        'email': user.email,
                                        } #유저 정보 보낼거 있으면 추가
                            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_user_info(request):
#     if 'user_info' in request.session:
#         return JsonResponse({'user': request.session['user_info']}, status=status.HTTP_200_OK)
#     else:
#         return JsonResponse({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    if user:
        user_info = {
            'username': user.username,
            'email': user.email,
            # 필요에 따라 다른 필드 추가 가능
        }
        return Response({'user': user_info}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
