from django.db import models

class AgentInteraction(models.Model):
    # We add these two new fields
    session_id = models.CharField(max_length=100, default='') 
    conversation_id = models.CharField(max_length=100, default='') 
    
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} - {self.prompt[:20]}"