from django.db import models


class Order(models.Model):
    payout = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True, db_index=True)
    keitaro_subid = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    prospect_id = models.IntegerField(default=0)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    delivery_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


# --- Keitaro postbacks ---
from django.db import models

class KeitaroEvent(models.Model):
    subid   = models.CharField(max_length=255, db_index=True)
    status  = models.CharField(max_length=64, db_index=True)
    payout  = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    raw     = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['subid'])]
        constraints = []
