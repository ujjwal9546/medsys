from django.forms import ModelForm
from django import forms
from .models import Doctor


SPECIALIZATION=[

('Cardiology','Cardiology'),
('Neurology','Neurology'),
('Orthopedic','Orthopedic'),
('Dermatology','Dermatology'),
('ENT','ENT'),
('Pediatric','Pediatric'),
('Psychiatry','Psychiatry'),
('General','General'),
('Other','Other'),

]


DAYS=[

('Mon','Mon'),
('Tue','Tue'),
('Wed','Wed'),
('Thu','Thu'),
('Fri','Fri'),
('Sat','Sat'),
('Sun','Sun')

]


class DoctorForm(forms.ModelForm):

 available_days=forms.MultipleChoiceField(

 choices=DAYS,

 widget=forms.CheckboxSelectMultiple,

 required=False

 )


 specialization=forms.ChoiceField(

 choices=SPECIALIZATION

 )


 class Meta:

  model=Doctor

  exclude=['user']


  widgets={

'available_from':
forms.TimeInput(
attrs={'type':'time'}
),

'available_to':
forms.TimeInput(
attrs={'type':'time'}
),

}


 # ADD THIS
 def __init__(self,*args,**kwargs):

  super().__init__(*args,**kwargs)


  if self.instance and self.instance.available_days:

   self.initial['available_days']=\
    self.instance.available_days.split(',')



 def clean_fee(self):

  fee=self.cleaned_data['fee']


  if fee<=0:

   raise forms.ValidationError(

   "Fee > 0"

   )


  return fee



 def save(self,*args,**kwargs):

  obj=super().save(

  commit=False

  )


  obj.available_days=",".join(

  self.cleaned_data[

  'available_days'

  ]

  )


  obj.save()


  return obj