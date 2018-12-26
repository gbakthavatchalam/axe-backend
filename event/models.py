from django.db import models


# Create your models here.
class Acceptance(models.Model):
    id = models.BigIntegerField(primary_key=True, auto_created=True)
    event_id = models.ForeignKey('Event', models.DO_NOTHING, db_column='event_id')
    response = models.IntegerField(blank=True, null=True)
    participant = models.ForeignKey('User', models.DO_NOTHING, db_column='participant')

    class Meta:
        managed = False
        db_table = 'acceptance'
        unique_together = (('event_id', 'participant'),)


class Event(models.Model):
    id = models.BigIntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    host = models.ForeignKey('User', models.DO_NOTHING, db_column='host')

    class Meta:
        managed = False
        db_table = 'event'


class User(models.Model):
    display_name = models.CharField(max_length=25)
    mobile = models.BigIntegerField(primary_key=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'user'

