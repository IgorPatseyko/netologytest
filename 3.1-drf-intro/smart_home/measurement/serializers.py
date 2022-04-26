from rest_framework import serializers

# TODO: опишите необходимые сериализаторы
from measurement.models import Measurement, Sensor


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['id', 'temperature', 'created_at']


class MeasurementSerializerWithoutId(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at']


class SensorSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializerWithoutId(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['name', 'description', 'measurements']

    def create(self, validated_data):
        return Sensor.objects.create(**validated_data)


class SensorSerializerWithId(serializers.ModelSerializer):
    measurements = MeasurementSerializerWithoutId(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
