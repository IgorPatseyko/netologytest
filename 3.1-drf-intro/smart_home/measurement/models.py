from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)


class Sensor(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)


class Measurement(models.Model):
    def __str__(self):
        return str(self.id)

    temperature = models.DecimalField(max_digits=5, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    sensors = models.ManyToManyField(Sensor, related_name='measurements')
