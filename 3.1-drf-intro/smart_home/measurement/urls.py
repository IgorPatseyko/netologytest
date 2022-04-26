from django.urls import path

from measurement.views import SensorView, MeasurementView

urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('sensors/', SensorView.as_view()),
    path('measurements/', MeasurementView.as_view()),
    path('sensors/<pk>/', SensorView.as_view()),

]
