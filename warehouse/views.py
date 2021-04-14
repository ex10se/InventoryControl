from django.db.models import F, Sum
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item
from .serializers import ItemSerializer


def index(request):
    return HttpResponseRedirect('resources')


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
        instance = Item.objects.get(id=data.get('id'))
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
        try:
            self.item_update(obj=self, request=request, partial=False)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        try:
            self.item_update(obj=self, request=request, partial=True)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        data = request.query_params if request.query_params else request.data
        try:
            instance = Item.objects.get(id=data.get('id'))
        except Item.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TotalCostView(APIView):
    def get(self, request, *args, **kwargs):
        # достаем из словаря {'total': <ЧИСЛО>} значение ключа total, которое высчитывается как сумма произведений
        # количества каждого ресурса на стоимость единицы
        total_cost = Item.objects.aggregate(total=Sum(F('amount') * F('price')))['total']
        return Response({'total_cost': total_cost})
