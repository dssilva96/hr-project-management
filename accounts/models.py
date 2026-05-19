from django.db import models



class UserProfiles(models.Model):
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
        ('supervisor', 'Supervisor'),
    ]

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    

    def __str__(self):
        return self.user.username
