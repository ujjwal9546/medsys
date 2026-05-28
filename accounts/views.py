from django.shortcuts import render, redirect
from .forms import RegisterForm,AddAdminForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .models import User
from doctor.models import Doctor
from staff.models import Staff
from appointment.models import Appointment
from patient.models import Patient

from staff.forms import StaffForm
from appointment.forms import AppointmentForm
from doctor.forms import DoctorForm

def home(request):
    doctors = Doctor.objects.all()
    categories = [
        'All',
        'Cardiology',
        'Neurology',
        'Orthopedic',
        'Dermatology',
        'ENT',
        'Psychiatry',
        'General',
        'Pediatric',
        'Gynecology',
        'Other'
    ]
    return render(
        request,
        'home.html',
        {
        'doctors': doctors,
        'categories': categories
        }
    )


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
        user=authenticate(
            username=u,
            password=p
        )
        if user:
            if user.role in [
                'doctor',
                'admin'
            ] and not user.approved:
                return render(
                    request,
                    'login.html',
                    {
                        'e':
                        '⏳ Approval Pending'
                    }
                )
            login(
                request,
                user
            )
            if user.role=='admin':
                return redirect(
                    'admin_dashboard'
                )
            if user.role=='doctor':
                return redirect(
                    'doctor_dashboard'
                )
            if user.role=='staff':
                return redirect(
                    'staff_dashboard'
                )
            return redirect(
                'patient_dashboard'
            )
        return render(
            request,
            'login.html',
            {
                'e':
                '❌ Invalid username or password'
            }
        )
    return render(
        request,
        'login.html'
    )


def user_logout(request):
 logout(request)
 return redirect('login')

@login_required
def patient_dashboard(request):
   return render(request,'patient_dashboard.html')

@login_required
def doctor_dashboard(request):
   return render(request,'doctor_dashboard.html')

@login_required
def admin_dashboard(request):
   return render(request,'admin_dashboard.html')

@login_required
def staff_dashboard(request):

    staff=Staff.objects.get(
        user=request.user
    )

    return render(

        request,

        'staff_dashboard.html',

        {
            'staff':staff
        }

    )
    

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
def add_admin(request):
    if request.user.role!='admin':
        return redirect('/')
    f=AddAdminForm(
        request.POST or None
    )
    if request.method=="POST":
        if f.is_valid():
            u=f.save(
                commit=False
            )
            u.role='admin'
            u.approved=True
            u.set_password(
                f.cleaned_data['password']
            )
            u.save()
            return render(
                request,
                'add_admin.html',
                {
                    'f':AddAdminForm(),
                    'success':
                    '✅ New admin created'
                }
            )
    return render(
        request,
        'add_admin.html',
        {
            'f':f
        }
    )


@login_required
def add_staff(request):

    f=StaffForm(
        request.POST or None
    )

    if request.method=="POST":

        if f.is_valid():

            u=f.save(
                commit=False
            )

            u.role='staff'

            u.approved=True

            u.set_password(
                f.cleaned_data['password']
            )

            u.save()

            d=Doctor.objects.get(
                user=request.user
            )

            Staff.objects.create(

                user=u,

                doctor=d,

                designation='assistant'

            )

            return redirect(
                'view_staff'
            )

    return render(

        request,

        'add_staff.html',

        {
            'f':f
        }

    )
    
@login_required
def view_staff(request):

    doctor=Doctor.objects.get(
        user=request.user
    )

    staffs=Staff.objects.filter(
        doctor=doctor
    )

    return render(

        request,

        'view_staff.html',

        {
            'staffs':staffs
        }

    )


@login_required
def staff_appointments(request):

    staff=Staff.objects.get(
        user=request.user
    )

    appointments=Appointment.objects.filter(

        doctor=staff.doctor,

        payment_status='submitted',

        status='pending',

        hidden_by_doctor=False

    ).order_by(
        '-created'
    )

    return render(

        request,

        'staff_appointments.html',

        {
            'a':appointments,
            'doctor':staff.doctor
        }

    )

@login_required
def staff_history(request):

    staff=Staff.objects.get(
        user=request.user
    )

    appointments=Appointment.objects.filter(

        doctor=staff.doctor,

        hidden_by_doctor=False

    ).exclude(

        status='pending'

    ).order_by(
        '-created'
    )

    return render(

        request,

        'staff_history.html',

        {
            'a':appointments,
            'doctor':staff.doctor
        }

    )    

def doctors(request):
    d = Doctor.objects.all()
    categories = [
        'All',
        'Cardiology',
        'Neurology',
        'Orthopedic',
        'Dermatology',
        'ENT',
        'Psychiatry',
        'General',
        'Pediatric',
        'Gynecology',
        'Other'
    ]
    return render(
        request,
        'doctors.html',
        {
        'd': d,
        'categories': categories
        }
    )

def doctor_profile(request,id):
 d=Doctor.objects.get(id=id)
 return render(request,'doctor_profile.html',{'d':d})

@login_required
def book_appointment(request, id):

    d = Doctor.objects.get(id=id)

    f = AppointmentForm(
        request.POST or None,
        doctor=d
    )

    # admin cannot book
    if request.user.role == 'admin':

        return redirect(
            'admin_dashboard'
        )

    # create patient profile automatically
    patient, created = Patient.objects.get_or_create(

        user=request.user,

        defaults={
            'age': 20,
            'gender': 'Other'
        }

    )

    if request.method == "POST":

        if f.is_valid():

            a = f.save(
                commit=False
            )

            a.patient = patient

            a.doctor = d

            a.amount = d.fee

            a.save()

            return redirect(
                'upload_payment',
                id=a.id
            )

    return render(

        request,

        'book_appointment.html',

        {
            'f': f,
            'd': d
        }

    )
    

@login_required
def upload_payment(request, id):
    a = Appointment.objects.get(id=id)
    if a.final_amount == 0:
        a.final_amount = a.amount
        a.save()
    if request.method == "POST":
        if 'apply_coupon' in request.POST:
            coupon = request.POST.get('coupon')
            if coupon and coupon.strip().upper() == "MED10":
                a.coupon_code = "MED10"
                a.discount = (a.amount * 10) // 100
                a.final_amount = a.amount - a.discount
            else:
                a.coupon_code = ""
                a.discount = 0
                a.final_amount = a.amount
            a.save()
            return render(
                request,
                'upload_payment.html',
                {
                    'a': a,
                    'success': '🎉 Coupon Applied Successfully'
                }
            )
        if 'submit_payment' in request.POST:
            if not request.FILES.get('payment_screenshot'):
                return render(
                    request,
                    'upload_payment.html',
                    {
                        'a': a,
                        'e': '❌ Upload payment screenshot first'
                    }
                )
            a.payment_screenshot = request.FILES['payment_screenshot']
            a.payment_status = 'submitted'
            a.save()
            send_mail(
                'Payment Submitted',
                f'''
Patient:
{a.patient.user.username}
submitted payment proof
''',
                settings.EMAIL_HOST_USER,
                [a.doctor.user.email],
                fail_silently=True
            )
            return redirect(
                'my_appointments'
            )
    return render(
        request,
        'upload_payment.html',
        {
            'a': a
        }
    )
    
@login_required
def verify_payment(request, id):
    a = Appointment.objects.get(id=id)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "approve":
            a.payment_status = "verified"
            a.status = "approved"
        elif action == "reject":
            a.payment_status = "rejected"
            a.status = "pending"
        a.save()
        return redirect('doctor_appointments')
    return render(request, 'verify_payment.html', {'a': a})

@login_required
def my_appointments(request):

    patient, created = Patient.objects.get_or_create(

        user=request.user,

        defaults={
            'age': 20,
            'gender': 'Other'
        }

    )

    a = Appointment.objects.filter(

        patient=patient,

        hidden_by_patient=False,

        payment_status__in=[
            'submitted',
            'verified',
            'rejected'
        ]

    ).order_by(
        '-created'
    )

    return render(

        request,

        'my_appointments.html',

        {
            'a': a
        }

    )    
@login_required
def doctor_appointments(request):
    d = Doctor.objects.get(
        user=request.user
    )
    a = Appointment.objects.filter(
        doctor=d,
        status='pending',
        payment_status='submitted'
    ).order_by(
        '-created'
    )
    return render(
        request,
        'doctor_appointments.html',
        {
            'a': a
        }
    )

@login_required
def approve_appointment(request,id):

    x=Appointment.objects.get(
        id=id
    )

    if request.user.role=='staff':

        staff=Staff.objects.get(
            user=request.user
        )

        if x.doctor != staff.doctor:

            return redirect('/')

    if x.payment_status != 'submitted':

        return redirect(
            'doctor_appointments'
        )

    x.payment_status='verified'

    x.status='approved'

    x.save()

    send_mail(

        'Appointment Approved',

        f'''

Your payment has been verified

Doctor:
{x.doctor.user.name or x.doctor.user.username}

Date:
{x.date}

Time:
{x.time}

Appointment approved

''',

        settings.EMAIL_HOST_USER,

        [x.patient.user.email],

        fail_silently=True

    )

    if request.user.role=='staff':

        return redirect(
            'staff_appointments'
        )

    return redirect(
        'doctor_appointments'
    )
    

@login_required
def reject_appointment(request,id):

    x=Appointment.objects.get(
        id=id
    )

    if request.user.role=='staff':

        staff=Staff.objects.get(
            user=request.user
        )

        if x.doctor != staff.doctor:

            return redirect('/')

    x.status='rejected'

    x.payment_status='rejected'

    x.save()

    send_mail(

        'Appointment Rejected',

        f'''

Appointment rejected

Doctor:
{x.doctor.user.name or x.doctor.user.username}

Date:
{x.date}

''',

        settings.EMAIL_HOST_USER,

        [x.patient.user.email],

        fail_silently=True

    )

    if request.user.role=='staff':
        return redirect(
            'staff_appointments'
        )

    return redirect(
        'doctor_appointments'
    )
    
    
@login_required
def delete_patient_appointment(request,id):
    a=Appointment.objects.get(id=id)
    a.hidden_by_patient=True
    if (
        a.hidden_by_patient
        and
        a.hidden_by_doctor
    ):
        a.delete()
    else:
        a.save()
    return redirect(
        'my_appointments'
    )

@login_required
def delete_doctor_appointment(request,id):
    a=Appointment.objects.get(
        id=id
    )
    a.hidden_by_doctor=True
    a.save()
    return redirect(
        'doctor_history'
    )
    

@login_required
def clear_patient_history(request):
    appointments=Appointment.objects.filter(
        patient__user=request.user,
        hidden_by_patient=False
    )
    for a in appointments:
        a.hidden_by_patient=True
        if (
            a.hidden_by_patient
            and
            a.hidden_by_doctor
        ):
            a.delete()
        else:
            a.save()
    return redirect(
        'my_appointments'
    )


@login_required
def clear_doctor_history(request):
    doctor=Doctor.objects.get(
        user=request.user
    )
    appointments=Appointment.objects.filter(
        doctor=doctor,
        hidden_by_doctor=False
    ).exclude(
        status='pending'
    )
    for a in appointments:
        a.hidden_by_doctor=True
        if (
            a.hidden_by_patient
            and
            a.hidden_by_doctor
        ):
            a.delete()
        else:
            a.save()
    return redirect(
        'doctor_history'
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
            'doctor_dashboard'
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

@login_required
def doctor_history(request):
    doctor=Doctor.objects.get(
        user=request.user
    )
    a=Appointment.objects.filter(
        doctor=doctor,
        hidden_by_doctor=False
    ).exclude(
        status='pending'
    ).order_by(
        '-created'
    )
    return render(
        request,
        'doctor_history.html',
        {
            'a':a
        }
    )