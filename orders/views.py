from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer,OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def siparis_listesi(request):
   if request.method == 'GET':
        # DEĞİŞİKLİK 1: Tüm siparişleri değil, sadece Token sahibinin siparişlerini getir
        siparisler = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(siparisler, many=True)
        return Response(serializer.data)

   elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # DEĞİŞİKLİK 2: JSON'dan user ID beklemek yerine, Token sahibini otomatik ata
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def siparis_kalemi_ekle(request):
    serializer = OrderItemSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)