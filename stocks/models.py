from django.db import models

class StockPrice(models.Model):
    stock_symbol = models.CharField(max_length=10)
    date = models.DateField(db_index=True)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['stock_symbol', 'date']),
        ]

    def __str__(self):
        return f"{self.stock_symbol} - {self.date}"
    
class StockPrediction(models.Model):
    stock_symbol = models.CharField(max_length=10)
    predicted_date = models.DateField(db_index=True)
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['stock_symbol', 'predicted_date'], name='unique_prediction_per_day')
        ]

    
    def __str__(self):
        return f"Prediction for {self.stock_symbol} on {self.predicted_date}: {self.predicted_price}"
