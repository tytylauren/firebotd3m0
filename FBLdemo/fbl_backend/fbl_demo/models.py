from django.db import models

class Drone(models.Model):
    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='inactive')  # e.g., 'active', 'inactive', 'flying', etc.
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

