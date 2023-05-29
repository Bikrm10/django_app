from django.urls import path
from .views import clustering_predict_view

urlpatterns = [
    path('predict/', clustering_predict_view, name='clustering-predict'),
    # Other URL patterns
]