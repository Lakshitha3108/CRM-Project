# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404

from django.http import HttpResponse

from django.views.generic import View

from .models import DistrictChoices

from trainers.utility import get_employee_id,get_password

from authentication.permissions import permission_roles

from django.db import transaction

from .models import Trainers

from .forms import TrainerRegisterForm

from django.db.models import Q

from authentication.models import Profile

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

class GetTrainerObject():

    def get_trainer(self,request,uuid):

        try:
           trainer = Trainers.objects.get(uuid=uuid)

           return trainer

           

        except:
           
           return render(request,'errorpages/error-404.html')
       


# Create your views here.
@method_decorator(permission_roles(roles = ['Admin','Sales','Academic Counsellor','Trainer','Students']),name='dispatch')
class DashBoardView(View) :

    def get(self,request,*args,**kwargs):

        return render(request,'trainers/dashboard.html')
    
@method_decorator(permission_roles(roles = ['Admin','Academic Counsellor']),name='dispatch')   
class TrainersListView(View) :

    def get(self,request,*args,**kwargs):

        query = request.GET.get('query')


        trainers = Trainers.objects.filter(active_status = True)

        if query :

            trainers= Trainers.objects.filter(Q(active_status=True)&(Q(first_name_icontains=query)|Q(last_nameicontains=query)|Q(post_officeicontains=query)|Q(contacticontains=query)|Q(pin_codeicontains=query)|Q(house_nameicontains=query)|Q(emailicontains=query)|Q(coursenameicontains=query)|Q(batchnameicontains=query)|Q(district_icontains=query)))


        data = {'trainers':trainers,'query':query}

        return render(request,'trainers/trainer.html',context=data)
    

@method_decorator(permission_roles(roles = ['Admin']),name='dispatch')   
class TrainerRegistrationView(View):

    def get(self,request,*args,**kwargs):

        form  = TrainerRegisterForm()

        data = {'form':form}


        return render(request,'trainers/registration.html',context=data)
    
    def post(self,request,*args,**kwargs):

        form  = TrainerRegisterForm(request.POST,request.FILES)

        if form.is_valid():

            with transaction.atomic():
            
                trainer= form.save(commit=False)

                trainer.employee_id = get_employee_id()

                # student.join_date = '2025-02-05'

                username = trainer.email

                password = get_password()

                print(password)

                profile=Profile.objects.create_user(username=username,password=password,role= 'Trainer')

                trainer.profile = profile

                trainer.save()

            return redirect('trainers-lists')
        
        else: 
            data = {'form':form}
            return render (request,'trainers/registration.html',context=data)


        
    
@method_decorator(permission_roles(roles = ['Admin','Academic Counselor']),name='dispatch')   

class TrainerDetailsView(View):

   def get(self,request,*args,**kwargs):
       
       uuid = kwargs.get('uuid')
       
       
       trainer=GetTrainerObject().get_trainer(request,uuid)


       
       data = {'trainer':trainer}
       
       return render(request,'trainers/trainers-details.html',context=data)
   
@method_decorator(permission_roles(roles = ['Admin']),name='dispatch')   

class TrainerDeleteView(View):

   def get(self,request,*args,**kwargs):
       
       uuid = kwargs.get('uuid')

       trainer=GetTrainerObject().get_trainer(request,uuid)

       trainer.active_status = False

       trainer.save()    

       return redirect('trainers-lists')
   

@method_decorator(permission_roles(roles = ['Admin','Sales']),name='dispatch')   
   
class TrainerUpdateView(View):

    def get(self,request,*args,**kwargs):
        uuid = kwargs.get('uuid')

        trainer = GetTrainerObject().get_trainer(request,uuid)

        form = TrainerRegisterForm(instance=trainer)

        data = {'form':form}

        return render(request,'trainers/trainers-update.html',context=data)   
    

    def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        trainer = GetTrainerObject().get_trainer(request,uuid)

        form  = TrainerRegisterForm(request.POST,request.FILES,instance=trainer)   

        if form.is_valid():
            
            form.save()

            return redirect('trainers-lists')
        
        else: 
            data = {'form':form}

            return render (request,'trainers/trainers-update.html',context=data)