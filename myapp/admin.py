from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'password', 'phone', "role", "status","id_proof")
    search_fields = ('name', 'email')

@admin.register(Contact_detail)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message', 'timestamp')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['cate_name','cate_image']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('cat_course','name','description','course_image')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('course','name','description','subject_image')

@admin.register(TutorExpertise)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('tutor','category','course','subject','hourly_rate', 'duration_per_day',
                    'experience_years','qualification','languages','bio',
                    'available_days','profile_image')

@admin.register(TutorBooking)
class TutorbookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tutor', 'tutordata','booking_start_date', 'booking_end_date','total_cost',
                    'contact_email', 'communication_preference','razorpay_order_id','razorpay_payment_id',
                    'razorpay_signature','status', 'created_at')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student','tutors','ratings','comment','timestamp')