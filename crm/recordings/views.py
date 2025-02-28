from django.shortcuts import render

from django.views.generic import View



# Create your views here.


class RecordingsView(View):

    def get(self,request,*args,**Kwargs):

        return render(request,'recordings/recordings.html')