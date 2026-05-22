from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.core.mail import send_mail
from django.conf import settings
from doctor.models import Doctor
from staff.models import Staff
from appointment.models import Appointment
from staff.forms import StaffForm
from appointment.forms import AppointmentForm
from patient.models import Patient
from doctor.forms import DoctorForm
import razorpay

def home(request):
    return render(request, "home.html")

def register(request):
 f=RegisterForm(request.POST or None)
 if request.method=='POST':
  if f.is_valid():
   u=f.save(commit=False)
   if u.role=='staff':
    return render(
  request,
  'register.html',
  {
   'f':f,
   'e':'Staff cannot self register'
  }
 )
   u.set_password(f.cleaned_data['password'])
   u.approved=False
   if u.role=='patient':
    u.approved=True
   u.save()
   if u.role=='doctor':
    Doctor.objects.get_or_create(
     user=u,
     defaults={
      'specialization':'General',
      'qualification':'NA',
      'experience':0,
      'fee':0,
      'hospital':'NA'
     }
    )

   if u.role=='patient':

    Patient.objects.get_or_create(
     user=u,
     defaults={
      'age':20,
      'gender':'Other'
     }
    )

   return redirect('/login/')

 return render(request,'register.html',{'f':f})

def user_login(request):

 if request.method=='POST':

  u=request.POST['username']
  p=request.POST['password']

  user=authenticate(username=u,password=p)

  if user:

   # ONLY block doctor + admin
   if user.role in ['doctor','admin'] and not user.approved:

    return render(
     request,
     'login.html',
     {'e':'Approval Pending'}
    )

   login(request,user)

   if user.role=='admin':
    return redirect('admin_dashboard')

   if user.role=='doctor':
    return redirect('doctor_dashboard')

   if user.role=='staff':
    return redirect('staff_dashboard')

   return redirect('patient_dashboard')

 return render(request,'login.html')

def user_logout(request):
 logout(request)
 return redirect('login')

@login_required
def patient_dashboard(request):return render(request,'patient_dashboard.html')

@login_required
def doctor_dashboard(request):return render(request,'doctor_dashboard.html')

@login_required
def admin_dashboard(request):return render(request,'admin_dashboard.html')

@login_required
def staff_dashboard(request):return render(request,'staff_dashboard.html')

@login_required
def approve_users(request):
 users=User.objects.filter(approved=False)
 return render(request,'approve.html',{'users':users})

@login_required
def approve(request,id):
 u=User.objects.get(id=id)
 u.approved=True
 u.save()
 send_mail('Approved','Account approved',settings.EMAIL_HOST_USER,[u.email],fail_silently=True)
 return redirect('approve_users')

@login_required
def reject(request,id):
 u=User.objects.get(id=id)
 send_mail('Rejected','Account rejected',settings.EMAIL_HOST_USER,[u.email],fail_silently=True)
 u.delete()
 return redirect('approve_users')

@login_required
def add_staff(request):
 f=StaffForm(request.POST or None)
 if f.is_valid():
  u=f.save(commit=False);u.role='staff';u.approved=True;u.set_password(f.cleaned_data['password']);u.save()
  d=Doctor.objects.get(user=request.user)
  Staff.objects.create(user=u,doctor=d,designation='assistant')
  return redirect('doctor_dashboard')
 return render(request,'add_staff.html',{'f':f})

@login_required
def doctors(request):
 d=Doctor.objects.all()
 return render(request,'doctors.html',{'d':d})


@login_required
def doctor_appointments(request):
 a=Appointment.objects.filter(
 doctor__user=request.user
 )
 return render(
 request,
 'doctor_appointments.html',
 {'a':a}
 )

@login_required
def approve_appointment(request,id):
 x=Appointment.objects.get(id=id)
 x.status='approved'
 x.save()
 return redirect(
 'doctor_appointments'
 )

@login_required
def reject_appointment(request,id):
 x=Appointment.objects.get(id=id)
 x.status='rejected'
 x.save()
 return redirect(
 'doctor_appointments'
 )

@login_required
def doctor_profile(request,id):
 d=Doctor.objects.get(id=id)
 return render(request,'doctor_profile.html',{'d':d})

@login_required
def book_appointment(request,id):

 d=Doctor.objects.get(id=id)

 f=AppointmentForm(
  request.POST or None
 )

 if request.user.role != 'patient':
  return redirect('patient_dashboard')

 patient = Patient.objects.get(user=request.user)

 if f.is_valid():

  a=f.save(commit=False)

  a.patient=patient

  a.doctor=d

  a.amount=d.fee

  a.save()

  return redirect(
   f'/payment/{a.id}'
  )


 return render(
  request,
  'book_appointment.html',
  {'f':f,'d':d}
 )

import razorpay


@login_required
def payment(request,id):

 a=Appointment.objects.get(id=id)

 client=razorpay.Client(

  auth=(

   settings.RAZORPAY_KEY,

   settings.RAZORPAY_SECRET

  )

 )


 order=client.order.create({

 'amount':a.amount*100,

 'currency':'INR',

 'payment_capture':1

 })


 return render(

  request,

  'payment.html',

  {

   'a':a,

   'order':order,

   'key':settings.RAZORPAY_KEY

  }

 )

@login_required
def payment_success(

 request,

 id,

 txn

):

 a=Appointment.objects.get(
  id=id
 )


 a.paid=True

 a.transaction=txn

 a.status='pending'


 a.save()


 send_mail(

 'Payment Success',


 f'''

Payment completed


Doctor:

{a.doctor.user.username}


Date:

{a.date}


Time:

{a.time}


Amount:

₹{a.amount}


Transaction:

{txn}


Appointment waiting for approval


 ''',


 settings.EMAIL_HOST_USER,


 [a.patient.user.email],


 fail_silently=True

 )


 # Optional doctor email


 send_mail(

 'New Appointment Request',


 f'''

New paid appointment


Patient:

{a.patient.user.username}


Date:

{a.date}


Time:

{a.time}


Amount:

₹{a.amount}

 ''',


 settings.EMAIL_HOST_USER,


 [a.doctor.user.email],


 fail_silently=True

 )


 return redirect(

 'my_appointments'

 )

@login_required
def my_appointments(request):

 a=Appointment.objects.filter(
 patient__user=request.user
 ).order_by('-created')

 return render(
 request,
 'my_appointments.html',
 {'a':a}
 )

@login_required
def doctor_appointments(request):

 d=Doctor.objects.get(
  user=request.user
 )

 a=Appointment.objects.filter(
  doctor=d
 ).order_by('-id')

 return render(
  request,
  'doctor_appointments.html',
  {'a':a}
 )


@login_required
def approve_appointment(request,id):

 x=Appointment.objects.get(id=id)

 x.status='approved'

 x.save()

 send_mail(
 'Appointment Approved',
 'Your appointment approved',
 settings.EMAIL_HOST_USER,
 [x.patient.user.email],
 fail_silently=True
 )

 return redirect(
 'doctor_appointments'
 )


@login_required
def reject_appointment(request,id):

 x=Appointment.objects.get(id=id)

 x.status='rejected'

 x.save()

 send_mail(
 'Appointment Rejected',
 'Your appointment rejected',
 settings.EMAIL_HOST_USER,
 [x.patient.user.email],
 fail_silently=True
 )

 return redirect(
 'doctor_appointments'
 )

@login_required
def edit_doctor(request):

 doctor,_=Doctor.objects.get_or_create(
  user=request.user
 )

 if request.method=="POST":

  f=DoctorForm(
   request.POST,
   request.FILES,
   instance=doctor
  )

  if f.is_valid():

   x=f.save(
    commit=False
   )

   x.user=request.user

   x.save()

   return redirect(
    'doctor_profile',
    id=x.id
   )

  print(
   f.errors
  )

 else:

  f=DoctorForm(
   instance=doctor
  )


 return render(
  request,
  'edit_doctor.html',
  {
   'f':f,
   'doctor':doctor
  }
 )