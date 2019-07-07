from rest_framework import viewsets, generics, permissions, status, views, mixins, generics, settings
from rest_framework.decorators import api_view, permission_classes, action
from .models import FilterGroup, FilterItem, Tweet
from django.contrib.auth.models import User
from .serializers import FilterGroupSerializer, FilterItemSerializer, UserSerializer, TweetSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from djoser.utils import login_user
from django.db.models import Q
from .pagination import StandardResultsSetPagination
from rest_framework.settings import api_settings


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def login(request):
    res = Response()
    username = username = request.POST.get('username')
    password = request.POST.get('password')

    if not User.objects.filter(Q(username=request.POST.get('username')) or Q(email=request.POST.get('username'))).exists():
        res.status_code = status.HTTP_200_OK
        res.data = {
            "status": 1,
            "message": "User not exist!"
        }
        return res

    user = authenticate(username=username, password=password)

    if user is None:
        res.status_code = status.HTTP_200_OK
        res.data = {
            "status": 1,
            "message": "Password Incorrect!"
        }
        return res

    res.data = {
        "status": 0,
        "token": login_user(request, user).key,
        "user": UserSerializer(user).data
    }
    return res


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        """ overide create for password hashing """
        existing_user = User.objects.filter(username=request.data['username'])

        if not existing_user:
            user_serializer = self.get_serializer(data=request.data)
            if user_serializer.is_valid():
                user = User(**request.data)
                user.password = make_password(request.data['username'])
                user.save()
                return Response(status=status.HTTP_201_CREATED, data=user_serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_409_CONFLICT)

    @action(detail=False, methods=['POST'])
    def mdelete(self, request):
        ids = request.data['ids']
        users = User.objects.filter(pk__in=ids)
        deleted = users.delete()

        return Response({
                        "delete_result": deleted
                        })

    @action(detail=False, methods=['POST'])
    def mactivate(self, request):
        ids = request.data['ids']
        flag = request.data['flag']
        users = User.objects.filter(pk__in=ids)
        result = users.update(is_active=flag)

        return Response({
                        "result": result
                        })


@api_view(['GET'])
def list_tweets(request):
    user = request.user
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    paginator = pagination_class()
    queryset = Tweet.objects.filter(streamer=user)
    page = paginator.paginate_queryset(queryset, request)
    serializer = TweetSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


class FilterGroupViewSet(viewsets.ModelViewSet):
    queryset = FilterGroup.objects.all()
    serializer_class = FilterGroupSerializer

    def get_queryset(self):
        return FilterGroup.objects.filter(user=self.request.user)


class FilterItemViewSet(viewsets.ModelViewSet):
    queryset = FilterItem.objects.all()
    serializer_class = FilterItemSerializer
