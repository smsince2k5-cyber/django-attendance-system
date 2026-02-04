import base64
import cv2
import numpy as np
from datetime import datetime
from django.shortcuts import render
from django.contrib import messages
from .models import Employee, Attendance

def checkin_view(request):
    if request.method == "POST":
        image_data = request.POST.get("image")

        if not image_data:
            messages.error(request, "No image captured.")
            return render(request, "attendance/checkin.html")

        # Decode base64 image
        format, imgstr = image_data.split(";base64,")
        img_bytes = base64.b64decode(imgstr)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        if len(faces) == 0:
            messages.error(request, "No face detected. Try again.")
            return render(request, "attendance/checkin.html")

        # Demo logic (first employee)
        employee = Employee.objects.first()
        now = datetime.now()

        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=now.date(),
            defaults={"check_in_time": now.time(), "status": "Present"}
        )

        if created:
            messages.success(request, f"Welcome {employee.name}, checked in successfully!")
        else:
            messages.info(request, f"{employee.name}, you already checked in today.")

    return render(request, "attendance/checkin.html")


def home(request):
    return render(request,"attendance\home.html")

def enroll_view(request):
    if request.method == "POST":
        employee_id = request.POST.get("employee_id")
        name = request.POST.get("name")
        image_data = request.POST.get("image")

        if not image_data:
            messages.error(request, "No image captured.")
            return render(request, "attendance/enroll.html")

        # Decode base64 image
        format, imgstr = image_data.split(";base64,")
        img_bytes = base64.b64decode(imgstr)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        if len(faces) == 0:
            messages.error(request, "No face detected. Try again.")
            return render(request, "attendance/enroll.html")

        # Save employee
        Employee.objects.create(
            employee_id=employee_id,
            name=name
        )

        messages.success(request, f"Employee {name} enrolled successfully!")

    return render(request, "attendance/enroll.html")
