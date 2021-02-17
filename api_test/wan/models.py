from django.db import models

class hos(models.Model):
    device_name = models.TextField(default=0)
    max_temp = models.FloatField(default=0)
    min_temp = models.FloatField(default=0)
    mean_temp = models.FloatField(null=True)
    time = models.DateTimeField(auto_now_add=True)
    #all_temp = models.ForeignKey(We, related_name='all_temp', on_delete=models.CASCADE, blank=True)
    def __str__(self):
        return self.device_name, self.time

class We(models.Model):
    time = models.DateTimeField()
    temp = models.FloatField()
    #all_temp = models.ForeignKey(hos, related_name='all_temp', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.time)





class Dn(models.Model):
    device_name = models.TextField(default=0)
    device_mac = models.TextField(default=0)
    sensor_mac = models.TextField(default=0)
    device_model = models.TextField(default=0)
    device_interval = models.TextField(default=0)
    device_version = models.TextField(default=0)
    sensor_model = models.TextField(default=0)
    ch_no = models.TextField(default=0)
    ch_name = models.TextField(default=0)

    def __str__(self):
        return self.device_name
# Create your models here.
