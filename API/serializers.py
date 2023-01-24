from rest_framework import serializers 
from .models import Category, MenuItem
from decimal import Decimal

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    
    def validate_price(self, value):
        if (value < 2):
            raise serializers.ValidationError('Price should not be less than 2.0')

    class Meta:
        model = MenuItem
        fields = ['id','title','price','stock', 'price_after_tax','category','category_id']
        # extra_kwargs = {
        #     'price':{
        #         'min_value':2
        #     },
        #     'stock':{
        #         'source':'inventory','min_value':0
        #     }
        # }

    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)
