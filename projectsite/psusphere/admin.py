
from django.contrib import admin
from .models import College, Program, Organization, Student, OrgMember
from .models import Incident, Locations, Firefighters, FireStation, FireTruck, WeatherConditions


admin.site.register(College)

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("prog_name","college")
    search_fields = ("prog_name","college_college_name")

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name","college","description")
    search_fields = ("name","college_college_name")

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "lastname", "firstname", "middlename", "program","college") 
    search_fields = ("lastname", "firstname","college_college_name")



@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    list_display = ("student", "get_member_program", "organization", "date_joined",)
    search_fields = ("student__lastname", "student__firstname",)
    
    def get_member_program(self, obj):
        try: 
            member = Student.objects.get(id=obj.student_id)
            return member.program
        
        except Student.DoesNotExist:
            return None
        

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("location", "date_time", "severity_level","description")
    search_fields = ("location",)

# admin.site.register(Locations)
@admin.register(Locations)
class LocationsAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude", "address", "city", "country")
    search_fields = ("name",)


# admin.site.register(Firefighters)
@admin.register(Firefighters)
class FirefightersAdmin(admin.ModelAdmin):
    list_display = ("name", "rank", "experience_level","station")
    search_fields = ("location",)

# admin.site.register(FireStation)
@admin.register(FireStation)
class FireStationAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude", "address", "city", "country")
    search_fields = ("name",)


# admin.site.register(FireTruck)
@admin.register(FireTruck)
class FireTruckAdmin(admin.ModelAdmin):
    list_display = ("model", "truck_number", "capacity", "station")
    search_fields = ("model",)


# admin.site.register(WeatherConditions)
@admin.register(WeatherConditions)
class WeatherConditionsAdmin(admin.ModelAdmin):
    list_display = ("incident", "temperature", "humidity", "wind_speed", "weather_description")
    search_fields = ("incident",)
