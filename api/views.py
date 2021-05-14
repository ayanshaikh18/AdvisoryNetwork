from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Advisor, Booking, User
from api.serializer import AdvisorSerializer, AdviserViewSerializer


class AdvisorView(viewsets.ModelViewSet):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer


@api_view(['GET'])
def advisor_list(request, user_id):
    try:
        User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response("User doesn't exist", status=status.HTTP_404_NOT_FOUND)

    adv_serializer = AdviserViewSerializer(Advisor.objects.all(), many=True)
    print(adv_serializer.data)
    return Response(adv_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def book_advisor(request, user_id, advisor_id):
    try:
        User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response("User doesn't exist", status=status.HTTP_404_NOT_FOUND)

    try:
        adv = Advisor.objects.get(pk=advisor_id)
    except Advisor.DoesNotExist:
        return Response('Advisor not found', status=status.HTTP_404_NOT_FOUND)

    booking = Booking.objects.create(user_id=user_id, advisor_id=advisor_id, date=request.POST.get('date'))
    booking.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_bookings(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response("User doesn't exist", status=status.HTTP_404_NOT_FOUND)

    bookings = Booking.objects.filter(user=user)
    data = []
    for booking in bookings:
        adv = Advisor.objects.get(id=booking.id)
        data.append(({
            'advisor_name': adv.name,
            'advisor_profile_pic': adv.photo,
            'advisor_id': adv.id,
            'booking_time': booking.date,
            'booking_id': booking.id
        }))
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    try:
        user = User.objects.create_user(username=request.POST.get('email'), name=request.POST.get('name'),
                                        password=request.POST.get('password'), email=request.POST.get('email'))
    except Exception as e:
        return Response("Fields missing", status=status.HTTP_400_BAD_REQUEST)

    token, id = user.save()
    data = {
        "token": token,
        "id": id
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
    user = authenticate(username=request.POST.get('email'),
                        password=request.POST.get('password'))
    if user is None:
        return Response("Invalid Login", status=status.HTTP_400_BAD_REQUEST)

    token = user.jwt_token
    id = user.id
    data = {
        "token": token,
        "id": id
    }
    return Response(data, status=status.HTTP_200_OK)
