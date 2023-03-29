from django.db import models

class Action(models.Model):

    class ActionType(models.TextChoices):
        REMINDER = 'Rappel',
        CALL = 'Appel',
        EMAIL = 'Email',
        MEETING = 'Rendez-vous',
        VISIT = 'Visite',
        OTHER = 'Autre',
    
    action_type = models.CharField(
        max_length=30,
        choices=ActionType.choices,
        default=ActionType.OTHER,
    )

    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_at = models.DateTimeField()
    done_at = models.DateTimeField(null=True, blank=True)