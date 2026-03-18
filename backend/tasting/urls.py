from django.urls import path

from .views import TastingRecordDetailView, TastingRecordListView

urlpatterns = [
    path("records/", TastingRecordListView.as_view(), name="tasting-record-list"),
    path("records/<int:pk>/", TastingRecordDetailView.as_view(), name="tasting-record-detail"),
]
