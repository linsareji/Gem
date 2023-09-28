from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(StudentEnquiry),
admin.site.register(StudentAdmission),
admin.site.register(Add_collage),
admin.site.register(Add_staff),
admin.site.register(Add_course),
admin.site.register(Add_scheme),
admin.site.register(Tieup),
admin.site.register(Session),
admin.site.register(Discontinue),
admin.site.register(Admission),
admin.site.register(Gender),
admin.site.register(Student_status),
admin.site.register(Certificate_status),
