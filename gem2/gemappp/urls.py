from django.contrib import admin
from django.urls import path,include

from gemappp import views

urlpatterns = [
    path('index/', views.index,name='index'),
    path('', views.login,name='login'),
    # path('enquiry/',views.enquiry,name='enquiry'),
    path('enquiry_form/',views.enquiry_form,name='enquiry_form'),
    # path('admission/',views.admission,name='admission'),
    path('admission_form/',views.admission_form,name='admission_form'),
    path('update/<int:id>/', views.update, name='update'),
    path('login/', views.login,name='login'),
    path('enq_details/',views.enq_details,name='enq_details'),
    path('test/', views.test,name='test'),
    path('report/', views.report,name='report'),
    path('stud_report/', views.stud_report,name='stud_report'),
    path('exam_report/', views.exam_report,name='exam_report'),
    path('old_stud_report/', views.old_stud_report,name='old_stud_report'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('logout', views.logout, name='logout'),
    path('delete/<int:taskid>/',views.delete,name='delete'),
    path('addon_home/', views.addon_home,name='addon_home'),
    path('addon_course/', views.addon_course,name='addon_course'),
    path('addon_clg/', views.addon_clg,name='addon_clg'),
    path('addon_staff/', views.addon_staff,name='addon_staff'),
    path('addon_scheme/', views.addon_scheme,name='addon_scheme'),
    path('tieup_page/', views.tieup_page, name='tieup_page'),
    path('session_form/', views.session_form, name='session_form'),
    path('discontinue_form/', views.discontinue_form, name='discontinue_form'),
    path('tieup_report/', views.tieup_report, name='tieup_report'),
    path('session_report/', views.session_report, name='session_report'),
    path('discontinue_report/', views.discontinue_report, name='discontinue_report'),
    path('start_exam/', views.start_exam, name='start_exam'),
    path('<str:course>/', views.take_exam, name='take_exam'),

    # path('get-student-details/<int:regno>/', get_student_details, name='get_student_details'),
       ]
