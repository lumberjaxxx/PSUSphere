from django.db import models

# Create your models here.
class BaseModel(models.Model): 
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class College(BaseModel):
    college_name = models.CharField(max_length=150)

    def __str__(self):
        return self.college_name

class Program(BaseModel):
    prog_name = models.CharField(max_length=150)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="programs")

    def __str__(self):
        return self.prog_name

class Organization(BaseModel):
    name = models.CharField(max_length=250)
    college = models.ForeignKey(College, null=True, blank=True, on_delete=models.CASCADE, related_name="organizations")
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Student(BaseModel):
    student_id = models.CharField(max_length=15)
    lastname = models.CharField(max_length=25)
    firstname = models.CharField(max_length=25)
    middlename = models.CharField(max_length=25, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return f"{self.lastname}, {self.firstname}"

class OrgMember(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="memberships")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="members")
    date_joined = models.DateField()

    def __str__(self):
        return f"{self.student} in {self.organization}"
