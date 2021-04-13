from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.db.models import F, Sum
from rest_framework.views import APIView

from .serializers import ItemSerializer
from .models import Item


class ItemView(GenericAPIView):
    """
    API endpoint для работы со складскими ресурсами
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'id'

    @staticmethod
    def item_update(obj, request, partial):  # patch и put методы
        # либо параметры заданы в URL, либо в теле запроса
        data = request.query_params if request.query_params else request.data
        instance = Item.objects.get(id=data['id'])
        serializer = obj.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        total_count = Item.objects.count()
        return Response({'resources': serializer.data,
                         'total_count': total_count})

    def post(self, request, *args, **kwargs):
        data = request.query_params if request.query_params else request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        self.item_update(obj=self, request=request, partial=False)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        self.item_update(obj=self, request=request, partial=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        data = request.query_params if request.query_params else request.data
        instance = Item.objects.get(id=data['id'])
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TotalCostView(APIView):
    def get(self, request, *args, **kwargs):
        # достаем из словаря {'total': <ЧИСЛО>} значение ключа total, которое высчитывается как сумма произведений
        # количества каждого ресурса на стоимость единицы
        total_cost = Item.objects.aggregate(total=Sum(F('amount') * F('price')))['total']
        return Response({'total_cost': total_cost})
