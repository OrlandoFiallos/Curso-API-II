from django.shortcuts import render
from .serializers import CategorySerializer, MenuItemSerializer,WatchesSerializer
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework import status
from .models import Category, MenuItem, Watches, WatchesCategory 
from django.core.paginator import Paginator, EmptyPage
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated 
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle 
from .throttles import TenCallsPerMinute


#Categorías
@api_view(['GET','POST'])
def category_list(request):
    #Lista todos los usuarios o crea uno nuevo
    if request.method == 'GET':
        items = Category.objects.all()
        serializer = CategorySerializer(items,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def category_detail(request, pk):
    try:
        item = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'message':'not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CategorySerializer(item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Menu Items
@api_view(['GET','POST'])
def menu_item_list(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        price_filter = request.query_params.get('price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage',default=2)
        page = request.query_params.get('page', default=1)
        
        if category_name:
            items = items.filter(category__title=category_name)
        if price_filter:
            items = items.filter(price__lte=price_filter)
        if search:
            items = items.filter(title__icontains=search)
        if ordering:
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)
        
        paginator = Paginator(items,per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serializer = MenuItemSerializer(items,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def menu_item_detail(request, pk):
    try:
        item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response({'message':'not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MenuItemSerializer(item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MenuItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WatchesViewSet(viewsets.ModelViewSet):
    # throttle_classes = [AnonRateThrottle, TenCallsPerMinute]
    queryset = Watches.objects.all()
    serializer_class = WatchesSerializer
    ordering_fields=['price','inventory']
    search_fields=['title','category__title']
    
    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle for throttle in throttle_classes]
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({'message':'Some secret message'})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({'message':'Only Manager should see this'})
    return Response({'message':'You are not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({'message':'succesfull'})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({'message':'Message for the logged in users only'})