from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import HotelSerializer, ReviewSerializer, BookingSerializer
from .models import Hotel, Review, Booking
from django.core.mail import send_mail
from django.conf import settings
from customer.models import Customer
from rest_framework.response import Response
from datetime import datetime
from rest_framework.exceptions import ValidationError
# Create your views here.

class HotelViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        customer = serializer.validated_data['customer']
        hotel = serializer.validated_data['hotel']

        if customer.balance < hotel.price:
            raise ValidationError("Insufficient balance to complete the booking.")

        if serializer.is_valid():
            customer.balance -= hotel.price
            customer.save()
            booking = serializer.save()
            subject = 'Booking successfully done'
            message = f'Hello Mr. {customer.user.first_name}. your book has been done at {booking.created_at}'
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [customer.user.email])
            return Response({'success':'booking confirmed'})
        
        return Response(serializer.errors)


class HotelReviewsView(APIView):
    
    def get(self, request, hotel_id):
        try:
            hotel = Hotel.objects.get(pk=hotel_id)
        except Hotel.DoesNotExist:
            return Response({'error': 'Hotel not found'}, status=status.HTTP_404_NOT_FOUND)
        
        reviews = hotel.reviews.all() 
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)