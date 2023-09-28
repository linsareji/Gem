from django.db import models
from django.db.models import Sum


# Create your models here.
class StudentEnquiry(models.Model):
    name = models.CharField(max_length=250)
    address = models.TextField()
    contact = models.IntegerField()
    course = models.CharField(max_length=250)
    enq_date = models.DateField()

    def __str__(self):
        return self.name


class StudentAdmission(models.Model):
    gemid = models.IntegerField(unique=True)
    stud_name = models.CharField(max_length=250)
    parent_name = models.CharField(max_length=250)
    parent_contact = models.IntegerField()
    stud_address = models.TextField()
    stud_contact = models.IntegerField()
    qualification = models.CharField(max_length=250)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=250)
    course1 = models.CharField(max_length=250)
    course2 = models.CharField(max_length=250, null=True)
    course_duration = models.IntegerField()
    scheme = models.CharField(max_length=250)
    fee = models.IntegerField(null=True)
    joining_date = models.DateField()
    exam_date = models.DateField(null=True)
    certificate_status = models.CharField(max_length=250)
    student_status = models.CharField(max_length=250)

    # dis_continue_date=models.DateField(null=True)
    # dis_continue=models.CharField(max_length=250,null=True)

    def __str__(self):
        return self.stud_name


class Add_collage(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Add_staff(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Add_course(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Add_scheme(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Gender(models.Model):
    gender = models.CharField(max_length=250)

    def __str__(self):
        return self.gender


class Certificate_status(models.Model):
    certificate = models.CharField(max_length=250)

    def __str__(self):
        return self.certificate


class Student_status(models.Model):
    Student_status = models.CharField(max_length=250)

    def __str__(self):
        return self.Student_status


class Admission(models.Model):
    regno = models.IntegerField(unique=True)
    stud_name = models.CharField(max_length=250)
    parent_name = models.CharField(max_length=250)
    parent_contact = models.IntegerField()
    stud_address = models.TextField()
    stud_contact = models.IntegerField()
    qualification = models.CharField(max_length=250)
    dob = models.DateField(null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    course = models.ForeignKey(Add_course, on_delete=models.CASCADE)
    course_duration = models.IntegerField()
    scheme = models.ForeignKey(Add_scheme, on_delete=models.CASCADE)
    fee = models.IntegerField(null=True)
    joining_date = models.DateField()
    exam_date = models.DateField(null=True)
    certificate_status = models.ForeignKey(Certificate_status, on_delete=models.CASCADE,default=1)
    student_status = models.ForeignKey(Student_status, on_delete=models.CASCADE,default=1)


    def __str__(self):
        return self.stud_name


class Tieup(models.Model):
    college = models.ForeignKey(Add_collage, on_delete=models.CASCADE)
    course = models.ForeignKey(Add_course, on_delete=models.CASCADE)
    fee = models.IntegerField()
    course_duration = models.IntegerField()
    tieup_date = models.DateField()

    def total_used_duration(self):
        total_duration = \
            Session.objects.filter(college=self.college, course=self.course).aggregate(total_duration=Sum('duration'))[
                'total_duration']
        return total_duration if total_duration else 0


class Session(models.Model):
    college = models.ForeignKey(Add_collage, on_delete=models.CASCADE)
    course = models.ForeignKey(Add_course, on_delete=models.CASCADE)
    staff = models.ForeignKey(Add_staff, on_delete=models.CASCADE)
    duration = models.IntegerField()  # Assuming duration is in minutes
    date = models.DateField()
    remarks = models.TextField()


class Discontinue(models.Model):
    regno = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    discontinue_date = models.DateField()
    remarks = models.TextField()

    def save(self, *args, **kwargs):
        student = Admission.objects.get(regno=self.regno)
        self.name = student.stud_name
        self.course = student.course
        super().save(*args, **kwargs)
