import logging

from django.db import connection
from django.utils import timezone
from rest_framework import viewsets, status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ride_api.constants import REQUEST_STATUS_CHOICES, ASSET_CHOICES
from ride_api.exceptions import SQLException
from ride_api.models import Requester, Rider
from ride_api.pagination import RequesterPagination
from ride_api.serializers import RequesterSerializer, RiderSerializer, RiderMatchRequestSerializer, \
    RequesterApplySerializer
from ride_api.utils import dict_fetchall

logging.basicConfig(level=logging.NOTSET)


class RequesterView(viewsets.ModelViewSet):
    serializer_class = RequesterSerializer
    queryset = Requester.objects.all()
    pagination_class = RequesterPagination
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_query_filter(self):
        filter_dict = {'user': self.request.user}
        req_status = self.request.query_params.get('status')
        if req_status in REQUEST_STATUS_CHOICES:
            dict_key = "pick_up_time__{}".format("gte" if req_status == "PENDING" else "lt")
            filter_dict[dict_key] = timezone.now()
        elif req_status:
            error_message = {'message': "Invalid status, valid status {}".format(REQUEST_STATUS_CHOICES)}
            logging.error(error_message)
            raise ValidationError(error_message)

        asset_type = self.request.query_params.get('asset_type')
        assets_list = {asset[0] for asset in ASSET_CHOICES}
        if asset_type in assets_list:  # set of assets from constants
            filter_dict['asset_type'] = asset_type
        elif asset_type:
            error_message = {'message': "Invalid asset_type, valid asset_type {}".format(assets_list)}
            logging.error(error_message)
            raise ValidationError(error_message)
        return filter_dict

    def get_sorted_query_set(self, query_set):
        sort_by = self.request.query_params.get('sort_by')
        order = "-" if self.request.query_params.get('order_by') == 'desc' else ""
        requester_fields = [field.name for field in Requester._meta.get_fields()]
        if sort_by in requester_fields:
            return query_set.order_by("{}{}".format(order, sort_by))
        elif sort_by:
            error_message = {'message': "Invalid sort_by. valid sort_by {}".format(requester_fields)}
            logging.error(error_message)
            raise ValidationError(error_message)
        return query_set

    def list(self, *args, **kwargs):
        query_filter = self.get_query_filter()
        query_set = Requester.objects.filter(**query_filter).order_by('id')
        query_set = self.get_sorted_query_set(query_set)
        page = self.request.query_params.get('page')
        if not page:  # for / no pagination
            logging.info("RequesterView: no pagination, returning all results")
            serializer = RequesterSerializer(query_set, many=True, context={'request': self.request})
            return Response(serializer.data)
        return self.get_paginated_response(self.paginate_queryset(query_set))


class RiderView(viewsets.ModelViewSet):
    serializer_class = RiderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Rider.objects.filter(user=self.request.user).all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RiderMatchRequest(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, *args, **kwargs):
        # orm is not optimal when it comes join with non foreign key fields. orm way - subquery
        # raw query would get this job done single DB call

        # use existing connection, django.db provides singleton eager initialize
        cursor = connection.cursor()
        query = "select * from (select * from ride_api_requester where user_id={}) as req   join (select  id as " \
                "rider_id, source, destination, pick_up_time, asset_count from " \
                "ride_api_rider) as ride on ride.source= req.source and ride.destination = req.destination and " \
                "req.asset_count <= ride.asset_count and (select date(req.pick_up_time)) = (select date(" \
                "ride.pick_up_time)); ".format(self.request.user.id)
        logging.info("executing query:{}".format(query))
        try:
            cursor.execute(query)
            rows = dict_fetchall(cursor)
        except Exception as e:
            logging.error("error while executing query:{}".format(e))
            raise SQLException({'message': "error while executing query"},
                               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = RiderMatchRequestSerializer(rows, many=True, context={'request': self.request})
        return Response({"results": serializer.data, "total": len(serializer.data)})


class RequesterApplyMatchUpdate(generics.UpdateAPIView):
    serializer_class = RequesterApplySerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        req = Requester.objects.filter(**{'user': self.request.user, 'id': kwargs['pk']}).first()
        if not req:
            error_message = {"message": "Invalid request id"}
            logging.error(error_message)
            raise ValidationError(error_message)
        rider = Rider.objects.filter(id=request.data['rider_assigned'], source=req.source, destination=req.destination,
                                     pick_up_time__date=req.pick_up_time.date()).first()
        if not rider:
            error_message = {"message": "Rider cannot be assigned to this particular request"}
            logging.error(error_message)
            raise ValidationError(error_message)

        req.rider_assigned = rider
        req.save()
        return Response({'message': 'successfully rider assigned'}, status=status.HTTP_200_OK)
