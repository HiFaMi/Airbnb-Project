import itertools

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
import django_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.rooms import RoomReservation
from ..serializer.room_list import RoomListSerializer, RoomDetailSerializer, RoomReservationSerializer
from ..models import Rooms

User = get_user_model()


class SnippetPagination(PageNumberPagination):
    """
    조각 Pagination
    """
    page_size = 4
    page_size_query_param = 'page_size'


class Pagination(PageNumberPagination):
    """
    Pagination
    """
    page_size = 18
    page_query_param = 'page'


class RoomReservationAPI(generics.ListCreateAPIView):
    """
    예약 API
    """
    serializer_class = RoomReservationSerializer
    queryset = RoomReservation.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get(self, request, room_pk):
        room = RoomReservation.objects.filter(room=room_pk)
        serializer = RoomReservationSerializer(room, many=True)
        return Response(serializer.data)

    def post(self, request, room_pk):
        request.data['room'] = room_pk
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomsList(generics.ListAPIView):
    """
    전체 숙소 리스트 API
    """
    queryset = Rooms.objects.all()
    serializer_class = RoomListSerializer
    pagination_class = Pagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('address_city',)


class RoomsDetail(APIView):
    """
    숙소 상세페이지 API
    """

    def get(self, request, room_pk, format=None):
        room = Rooms.objects.filter(pk=room_pk)
        serializer = RoomDetailSerializer(room, many=True)
        return Response(serializer.data)


class MainPageRoomsList(generics.ListAPIView):
    serializer_class = RoomListSerializer

    def list(self, request):
        limit_num = 4
        address_response = {}
        address_list = ['서울', '인천', '대구', '부산']
        for i in address_list:
            address_response[i] = RoomListSerializer(Rooms.objects.filter(address_city__contains=i)[:limit_num],
                                                     many=True).data
            # aws
            address_response[i].append({'link': f'https://leesoo.kr/rooms/list?address_city={i}'})
            # localhost
            # address_response[i].append({'link': f'http://localhost:8000/rooms/list?address_city={i}'})
        return Response(address_response)
