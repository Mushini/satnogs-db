from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User


MODE_CHOICES = ['FM', 'AFSK', 'BFSK', 'APRS', 'SSTV', 'CW', 'FMN']


class Satellite(models.Model):
    """Model for SatNOGS satellites."""
    norad_cat_id = models.PositiveIntegerField()
    name = models.CharField(max_length=45)

    def __unicode__(self):
        return '{0} - {1}'.format(self.norad_cat_id, self.name)


class Transponder(models.Model):
    """Model for antennas transponders."""
    description = models.TextField()
    alive = models.BooleanField(default=True)
    uplink_low = models.PositiveIntegerField(blank=True, null=True)
    uplink_high = models.PositiveIntegerField(blank=True, null=True)
    downlink_low = models.PositiveIntegerField(blank=True, null=True)
    downlink_high = models.PositiveIntegerField(blank=True, null=True)
    mode = models.CharField(choices=zip(MODE_CHOICES, MODE_CHOICES),
                            max_length=10)
    invert = models.BooleanField(default=False)
    baud = models.FloatField(validators=[MinValueValidator(0)])
    satellite = models.ForeignKey(Satellite, related_name='transponders',
                                  null=True)

    def __unicode__(self):
        return self.description


class Suggestion(Transponder):
    citation = models.URLField(max_length=255, blank=True)
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)
    transponder = models.ForeignKey(Transponder, blank=True, null=True,
                                    on_delete=models.SET_NULL, related_name='suggestions')

    def __unicode__(self):
        return self.description
