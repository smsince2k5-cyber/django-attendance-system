from django.db import models
# models.py
class Employee(models.Model):
    id = models.AutoField(primary_key=True)  # auto increment
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    check_in_time = models.TimeField()
    status = models.CharField(max_length=20)
