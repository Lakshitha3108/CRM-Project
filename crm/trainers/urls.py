from django.urls import path

from . import views

urlpatterns = [
    path('trainers-lists/',views.TrainersListView.as_view(),name='trainers-lists'),
    path('trainer-registration-form/',views.TrainerRegistrationView.as_view(),name='trainer-registration-form'),
    path('trainer-details/<str:uuid>/',views.TrainerDetailsView.as_view(),name='trainer-details'),
    path('trainer-delete/<str:uuid>/',views.TrainerDeleteView.as_view(),name='trainer-delete'),
    path('trainer-update/<str:uuid>/',views.TrainerUpdateView.as_view(),name='trainer-update'),

]