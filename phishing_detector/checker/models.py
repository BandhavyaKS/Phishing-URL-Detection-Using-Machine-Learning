from django.db import models


class URLCheck(models.Model):
    url = models.CharField(max_length=500)
    prediction = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.url} - {self.prediction}'
