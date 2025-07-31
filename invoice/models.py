# models.py
from django.db import models

class Invoice(models.Model):
    invoice_no = models.CharField(max_length=20)
    invoice_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    from_business = models.CharField(max_length=100)
    to_business = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Invoice {self.invoice_no} from {self.from_business} to {self.to_business} on {self.invoice_date}"
    
    def total_cost(self):
        return sum(item.total_price() for item in self.items.all())

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def total_price(self):
        return self.quantity * self.rate
    
    def __str__(self):
        return f"{self.name} ({self.quantity} @ {self.rate})"
