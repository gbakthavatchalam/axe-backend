from django.db import models


# Create your models here.
class AuthUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    display_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField(null=True)
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class Acceptance(models.Model):
    id = models.BigIntegerField(primary_key=True, auto_created=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='participants')
    response = models.IntegerField(blank=True, null=True)
    participant = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='participant')

    class Meta:
        managed = False
        db_table = 'acceptance'
        unique_together = (('event', 'participant'),)


class Event(models.Model):
    id = models.BigIntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    host = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='host')
    location = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'event'
