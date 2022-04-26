# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, MeasurementSerializer, SensorSerializerWithId


class SensorView(APIView):
    def get(self, request, *args, **kwargs):
        if kwargs:
            sensors = Sensor.objects.filter(id=kwargs['pk'])
            ser = SensorSerializerWithId(sensors, many=True)
        else:
            sensors = Sensor.objects.all()
            ser = SensorSerializer(sensors, many=True)
        return Response(ser.data)

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')

        Sensor.objects.create(name=name, description=description).save()
        return Response({'status': 'ok'})

    def patch(self, request, *args, **kwargs):
        sensor = Sensor.objects.get(id=kwargs['pk'])
        sensor.description = request.data.get('description')
        sensor.save()
        return Response({'status': 'ok'})



class MeasurementView(ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def post(self, request, *args, **kwargs):
        temperature = request.data.get('temperature')
        sensors = Sensor.objects.filter(pk=int(request.data.get('sensor')))
        new_meas = Measurement.objects.create(temperature=temperature)
        new_meas.save()
        for sensor in sensors:
            new_meas.sensors.add(sensor)

        return self.list(request, *args, **kwargs)


