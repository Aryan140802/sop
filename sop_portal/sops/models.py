from django.db import models




class SOP(models.Model):
    title = models.CharField(max_length=255)
    team = models.CharField(max_length=100)
    sop_text = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
