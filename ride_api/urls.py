from django.urls import path
from rest_framework import routers
from ride_api.views import RequesterView, RiderView, RiderMatchRequest, RequesterApplyMatchUpdate

router = routers.DefaultRouter()
router.register(r'requester', RequesterView, basename='requester')
router.register(r'rider', RiderView, basename='rider')
router.register(r'rider_match', RiderMatchRequest, basename='rider_match')

urlpatterns = [
    path('rider_match_apply/<int:pk>', RequesterApplyMatchUpdate.as_view())
]
urlpatterns.extend(router.urls)
