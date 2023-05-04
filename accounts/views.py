from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from accounts.serializers import LoginSerializer
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.db.utils import IntegrityError
from accounts.serializers import UserNameSerializer
from accounts.models import Student, UploadTask
from school.models import StudentProfile
from asgiref.sync import async_to_sync

from accounts.taskHandler import Status, TaskHandler

import uuid
import csv
import string
import random
from datetime import datetime
import time
from deficiency_portal_backend.settings import BASE_DIR
import os

# Create your views here.
class CheckAuthenticatedView(APIView):
    permission_classes =[AllowAny]
    def get(self, request, format=None):
        user = self.request.user

        try:
            isAuthenticated = user.is_authenticated

            print(user)

            if isAuthenticated:
                return Response({ 'isAuthenticated': 'success', "role": user.role})
            else:
                return Response({ 'isAuthenticated': 'error' })
        except:
            return Response({ 'error': 'Something went wrong when checking authentication status' })

class LoginView(APIView):
    permission_classes =[AllowAny]
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        auth.login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({ 'success': 'Logged Out' })
        except:
            return Response({ 'error': 'Something went wrong when logging out' })

class ChangePasword(APIView):
    def post(self, request, format=None):
        user = request.user
        current_pass = request.user.password
        current_pass_entered = request.data["old_pass"]
        new_pass = request.data["new_pass"]
        re_new_pass = request.data["re_new_pass"]
        
        if not check_password(current_pass_entered, current_pass):
            return Response({"error": "You entered an incorrect current password"})
        
        if new_pass != re_new_pass:
            return Response({"error": "Passwords do not match"})
        
        user.set_password(new_pass)
        user.save()
        update_session_auth_hash(request, request.user)
        return Response({"success": "You changed your password successfully"})


class UserName(APIView):
    def get(self, reuquest, format=None):
        user = self.request.user

        serializer = UserNameSerializer(user)

        return Response(serializer.data)
    
class InsertUsers(APIView):
    def post(self, request, format=None):
        try:
            file = request.FILES['file']
        except MultiValueDictKeyError:
            return Response({"error": "Please upload a file"})
            
        data = self.process_file(file)
        task_id = TaskHandler().start_task( self.insert_data, [ data ] )

        uploadTask = UploadTask(file_name=file.name, job_id=task_id)
        uploadTask.save()

        print(uploadTask)

        # to_mail = self.insert_data(data)
        # response = self.generate_csv_response(to_mail)        
        # print(response)
        # print(to_mail[0])

        response = Response({"success": "Your file is being uploaded"})

        return response

    def generate_csv(self, to_mail, job_id):
        file_path = os.path.join(BASE_DIR, f"email_list\{job_id}.csv")

        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename="export.csv"'

        # Define the CSV writer with the same keys as the dictionaries
        fieldnames = to_mail[0].keys()
        writer = csv.DictWriter(open(file_path, 'w'), fieldnames=fieldnames)
        
        # Write the header row to the CSV file
        writer.writeheader()
        
        # Write each dictionary as a row to the CSV file
        for row in to_mail:
            writer.writerow(row)
        
        return f"email_list\{job_id}.csv"

    def process_file(self, file):
        reader = csv.DictReader(file.read().decode('latin-1').splitlines())

        data = [row for row in reader]

        return data
    

    def insert_data(self, data, task_progress ):
        to_mail = []

        task_progress.set( Status.STARTED, progress_message="The process has been started" )

        for row in data:
            try:
                profile = {}
                department = row.pop('department')
                password = self.generate_password()
                student = Student.objects.create_user(**row, password=password)
                student_profile = StudentProfile(user=student, student_id=student.username, department_id=department)
                student_profile.save()

                profile["student_id"] = row["username"]
                profile["password"] = password
                profile["department"] = department
                profile["email"] = row["email"]

                to_mail.append(profile)
            except IntegrityError:
                print(f"User with index {row['username']} already exists")

        task_progress.set( Status.SUCCESS, output=to_mail )
        task_id = task_progress.task_id
        uploadTask = UploadTask.objects.get(job_id=task_id)
        

        try:
            csv = self.generate_csv(to_mail, task_id)
            
            print(f"{task_id} is done. {csv} is created")
            uploadTask.done_uploading = True
            uploadTask.csv_generated = True
            uploadTask.csv_filename = f"{task_id}.csv"
            
        except Exception as e:
            print(e)
            uploadTask.failed = True

        finally:
            uploadTask.save()
            print(uploadTask)


    def generate_password(self):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(alphabet) for i in range(8))
        return password