from django.shortcuts import render,redirect,get_object_or_404

from django.http import HttpResponse

from django.views.generic import View

from . models import DistrictChoices,BatchChoices,CourseChoices,TrainerChoices

from django . db . models import Q

from .utility import get_admission_number,get_password,send_email

from .models import students

from .forms import StudentRegisterForm

from authentication.models import Profile

from django.db import transaction

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from authentication.permissions import permission_roles
import  threading 
import datetime

# payment related imports

from payments.models import Payment




# Create your views here.

class GetStudentObject:

    def get_student(self,request,uuid):

        try:
            
            student = students.objects.get(uuid=uuid)

            return student
        
        except students.DoesNotExist:

            return render(request,'errorpages/error-404.html')


# @method_decorator(login_required(login_url='login'),name='dispatch')    

# @method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch')
class DashboardView(View):

    def get(self,request,*args,**kwargs):


        return render(request, "students/dashboard.html")
# @method_decorator(permission_roles(roles=['Admin','Sales','Trainer','Academic Counsellor']),name='dispatch')
class StudentsListView(View):

    def get(self,request,*args,**kwargs):

        query = request.GET.get('query')

        role = request.user.role

        if role in ('Trainer'):

            all_students = students.objects.filter(active_status = True,trainer__profile=request.user)

            if query :

            #all_students = students.objects.filter(Q(active_status = True)&(Q(first_name_icontains = query)|Q(last_nameicontains = query)|Q(emailicontains = query)|Q(contact_numicontains = query)|Q(house_nameicontains = query)|Q(pincode_icontains = query)))
           

             all_students = students.objects.filter(Q(active_status=True)&Q(trainer__profile=request.user)&(Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(contact_num__icontains=query)|Q(house_name__icontains=query)|Q(post_office__icontains=query)|Q(pincode__icontains=query)|Q(course__code__icontains=query)))
            
        elif role in ['Academic Counsellor']:

               all_students = students.objects.filter(active_status = True,batch_academic_counsellor_profile=request.user)


               if query :

                all_students = students.objects.filter(Q(active_status=True)&Q(batch_academic_counsellorprofile=request.user)&(Q(first_nameicontains=query)|Q(last_nameicontains=query)|Q(post_officeicontains=query)|Q(contacticontains=query)|Q(pin_codeicontains=query)|Q(house_nameicontains=query)|Q(emailicontains=query)|Q(coursenameicontains=query)|Q(batchnameicontains=query)|Q(district_icontains=query)))

        else :


        # all_students = students.objects.all()

            all_students = students.objects.filter(active_status=True)

            if query :

            # all_students = students.objects.filter(Q(active_status = True)&(Q(first_name_icontains = query)|Q(last_nameicontains = query)|Q(emailicontains = query)|Q(contact_numicontains = query)|Q(house_nameicontains = query)|Q(pincode_icontains = query)))
           

               all_students = students.objects.filter(Q(active_status=True)&(Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(contact_num__icontains=query)|Q(house_name__icontains=query)|Q(post_office__icontains=query)|Q(pincode__icontains=query)|Q(course__code__icontains=query)))

        # for student in all_students:

        #     print(student.photo)

        data = {'students' : all_students,'query' : query}

        return render(request, "students/students.html",context=data)
    
@method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch')
class StudentRegisterView(View):

     def get(self,request,*args,**kwargs):


        form = StudentRegisterForm()

        

        # data = {'districts':DistrictChoices,'batches':BatchChoices, 'courses':CourseChoices,'Trainers':TrainerChoices,'form':form}

        #data = {'numbers':[1,2,3,4,5]}
        
        data = {'form':form}

        return render(request,"students/register.html",context=data)
    
     def post(self,request,*args,**kwargs):

        form = StudentRegisterForm(request.POST,request.FILES)

        if form.is_valid():
            
            with transaction.atomic():

                student = form.save(commit=False)

                student.adm_num = get_admission_number()

                # student.join_date = '2025-02-05'

                username = student.email

                password = get_password()

                print(password)

                profile = Profile.objects.create_user(username=username,password=password,role='Student')   #here if we create admin instead of user give is staff and is supereuser
                
                student.profile = profile

                student.save()

                # payment section 

                fee = student.course.offer_fee if student.course.offer_fee else student.course.fee

                Payment.objects.create(student=student,amount = fee)

                
            
                # if payment_structure_form.is_valid()

                # sending login credentials to student through mail

                subject = 'Login Credentials'

                recepients = [student.email]

                template = 'email/login-credential.html'

                join_date = student.join_date

                date_after_10_days = join_date + datetime.timedelta(days=10)

                print(date_after_10_days)

                context = {'name':f'{student.first_name} {student.last_name}','username':username,'password':password,'date_after_10_days': date_after_10_days}

                # send_email(subject,recepients,template,context)

                thread = threading.Thread(target=send_email,args=(subject,recepients,template,context))

                thread.start()

                return redirect('students-list')
        
        else :

            data ={'form' :form}

            return render(request,"students/register.html",context=data)

         
        #  form_data = request.POST

        #  first_name = form_data.get("first_name") 
        #  last_name = form_data.get("last_name")
        #  photo=form_data.get("photo")
        #  email=form_data.get("email")
        #  contact_num=form_data.get("contact_num")
        #  house_name=form_data.get("house_name")
        #  post_office=form_data.get("post_office")
        #  pincode=form_data.get("pincode")
        #  course=form_data.get("course")
        #  district=form_data.get("district")
        #  batch=form_data.get("batch")
        #  batch_date=form_data.get("batch_date")
        #  trainer=form_data.get("trainer")

        #  admission_num=get_admission_number()

        #  print(admission_num)

        #  print(first_name)
        #  print(last_name)
        #  print(email)
        #  print(contact_num)
        #  print(house_name)
        #  print(post_office)
        #  print(pincode)
        #  print(course)
        #  print(district)
        #  print(batch)
        #  print(batch_date)
        #  print(trainer)

        #  join_date='2024-08-16'

        #  students.objects.create(first_name=first_name,
        #                          last_name=last_name,
        #                          photo=photo,
        #                          email=email,
        #                          contact_num=contact_num,
        #                          house_name=house_name,
        #                          post_office=post_office,
        #                          district=district,
        #                          pincode=pincode,
        #                          admission_num=admission_num,
        #                          course=course,
        #                          batch=batch,
        #                          batch_date=batch_date,
        #                          join_date=join_date,
        #                          trainer_name=trainer)
        


        # return render(request,"students/students.html")
# @method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch')    
class StudentDetailView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')


        # student = get_object_or_404(students,pk=pk)

        student = GetStudentObject().get_student(request,uuid)
        # try:
            
        #     student = students.objects.get(pk=pk)


        #     print(student)
        # except:

        #     return redirect('error-404')

        data= {'student': student}

        return render(request,"students/student-detail.html",context=data)

# class Error404View(View):

    def get(self,request,*args,**kwargs):


        pass
    
        return render(request,"students/error-404.html")
    # roles Sales,Admin,Trainer,Academic Counsellor
# @method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch')    
class StudentDeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        # try:
            
        #     student = students.objects.get(pk=pk)


        #     print(student)
        # except:

        #     return redirect('error-404')

        student = GetStudentObject().get_student(request,uuid)
        
        # student.delete()
        student.active_status = False

        student.save()
        

        return redirect("students-list")
# @method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch')    
class StudentUpdateView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = GetStudentObject().get_student(request,uuid)

        form = StudentRegisterForm(instance=student)

        data = {'form':form}

        
        return render(request,"students/student-update.html",context=data)
    
    def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = GetStudentObject().get_student(request,uuid)

        form = StudentRegisterForm(request.POST,request.FILES,instance=student)

        if form.is_valid():

            form.save()

            return redirect('students-list')
        
        else :
            
            data = {'form':form}

            return render(request,"students/student-update.html",context=data)