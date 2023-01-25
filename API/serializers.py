from rest_framework import serializers 
from .models import Category, MenuItem, Watches, WatchesCategory
from decimal import Decimal
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
import bleach

class CategorySerializer(serializers.ModelSerializer):
    # def validate_title(self,value):
    #     return bleach.clean(value)
    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])    
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    # stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    # title = serializers.CharField(max_length=255,validators=[UniqueValidator(MenuItem.objects.all())])
    
    # def validate_price(self, value):
    #     if (value < 2):
    #         raise serializers.ValidationError('Price should not be less than 2.0')
    
    def validate(self, attrs):
        if(attrs['price']<2):
            raise serializers.ValidationError('Price should not be less than 2.0')
        if attrs['inventory'<0]:
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)

    class Meta:
        model = MenuItem
        fields = ['id','title','price','inventory', 'price_after_tax','category','category_id']
        # extra_kwargs = {
        #     'title':{
        #         'validators':[
        #             UniqueValidator(queryset=MenuItem.objects.all())
        #         ]
        #     }
        # }
        validators = [
            UniqueTogetherValidator(
                queryset=MenuItem.objects.all(),
                fields=['title','price']),
        ]

    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)

#modelo Watches

class WatchesCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchesCategory
        fields = '__all__'
class WatchesSerializer(serializers.ModelSerializer):
    category = WatchesCategorySerializer(read_only=True)
    class Meta:
        model = Watches
        fields = ['id','title','price','inventory','category']