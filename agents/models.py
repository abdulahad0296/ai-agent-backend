from django.db import models

class AgentInteraction(models.Model):
    prompt = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.created_at.strftime('%H:%M')} - {self.prompt[:30]}..."
