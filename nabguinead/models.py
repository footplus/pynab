from django.db import models

from nabcommon import singleton_model


class Config(singleton_model.SingletonModel):
    guinea_frequency = models.IntegerField(default=30)
    next_guinea = models.DateTimeField(null=True)

    class Meta:
        app_label = "nabguinead"
