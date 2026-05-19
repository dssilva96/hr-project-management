from django.db import models
import uuid


class Employee(models.Model):

  STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('terminated', 'Terminated'),
    ]
  employee_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
  first_name = models.CharField("first name", max_length=50)
  last_name= models.CharField("last name", max_length=50)
  email = models.EmailField("email", max_length=100, unique=True)
  position = models.CharField("position", max_length=100)
  mobile = models.CharField("mobile", max_length=20, blank=True, null=True)
  department = models.CharField("department", max_length=100, blank=True, null=True)
  date_joined = models.DateField("date joined", auto_now_add=True)
  status = models.CharField("status", max_length=20, choices=STATUS_CHOICES, default='active')

  def __str__(self):
      return f"{self.first_name} {self.last_name}"


class Team(models.Model):
  team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=120)
  description = models.TextField(blank=True)
  lead = models.ForeignKey(
      Employee,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      related_name='leading_teams',
  )
  members = models.ManyToManyField(Employee, blank=True, related_name='teams')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
      ordering = ['name']

  def __str__(self):
      return self.name
