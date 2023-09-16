from rest_framework import viewsets
from djshop.apps.catalog.models import Category
from djshop.apps.catalog.serializers.front import CategorySerilizer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerilizer