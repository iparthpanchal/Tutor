from django.db import models
from django.utils.safestring import mark_safe
# Create your models here.
from datetime import timedelta
from decimal import Decimal
from datetime import datetime
class Login(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, default="admin@123")
    phone = models.CharField(max_length=20, null=True, blank=True)

    ROLE = (
        ("Tutor", "Tutor"),
        ("Student", "Student"),
    )
    role = models.CharField(max_length=10, choices=ROLE, default='User')

    STATUS = (
        ("0", "unapproved"),
        ("1", "approved")
    )
    status = models.CharField(max_length=10, choices=STATUS, default='0')

    id_proof = models.FileField(upload_to='id_proofs/', null=True, blank=True, default=None)

    def pic(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.id_proof.url))
    pic.allow_tags = True

    def __str__(self):
        return self.name

class Contact_detail(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=30)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    cate_name = models.CharField(max_length=30)
    cate_image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def cate_pic(self):
        return mark_safe('<img src = "{}" width="100">'.format(self.cate_image.url))
    cate_pic.allow_tags=True

    def __str__(self):
        return self.cate_name

class Course(models.Model):
    cat_course = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=100, unique=True)  # e.g., "10th", "12th", "BCA"
    description = models.TextField(blank=True, null=True)
    course_image = models.ImageField(upload_to='course_images/', blank=True, null=True)

    def course_pic(self):
        return mark_safe('<img src = "{}" width="100">'.format(self.course_image.url))
    course_pic.allow_tags=True

    def __str__(self):
        return self.name

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)  # e.g., "Mathematics", "Physics"
    description = models.TextField(blank=True, null=True)
    subject_image = models.ImageField(upload_to='subject_images/', blank=True, null=True)

    def sub_pic(self):
        return mark_safe('<img src = "{}" width="100">'.format(self.subject_image.url))

    sub_pic.allow_tags = True

    def __str__(self):
        return f"{self.name} ({self.course.name})"

class TutorExpertise(models.Model):
    tutor = models.ForeignKey('Login', on_delete=models.CASCADE, limit_choices_to={'role': 'Tutor'})
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    duration_per_day = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,help_text="Number of hours available per day")  # NEW FIELD
    experience_years = models.PositiveIntegerField()
    qualification = models.CharField(max_length=200, blank=True, null=True)
    languages = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    available_days = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(upload_to='tutor_profiles/', blank=True, null=True)

    def tutor_pic(self):
        return mark_safe('<img src = "{}" width="100">'.format(self.profile_image.url))
    tutor_pic.allow_tags=True

    class Meta:
        unique_together = ('tutor', 'subject')

    def __str__(self):
        return f"{self.tutor.name} - {self.subject.name}"

class TutorBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('paid', 'paid'),
        ('not paid', 'not paid'),
    ]
    user = models.ForeignKey('Login', on_delete=models.CASCADE, related_name="students")
    tutor = models.ForeignKey('Login', on_delete=models.CASCADE, related_name="alltutors")
    tutordata = models.ForeignKey(TutorExpertise, on_delete=models.CASCADE, related_name="alltutors", null=True, blank=True)
    booking_start_date = models.DateTimeField(null=True, blank=True)
    booking_end_date = models.DateTimeField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    communication_preference = models.CharField(max_length=20, blank=True, null=True,choices=[('email', 'Email'), ('phone', 'Phone'), (
    'video_call', 'Video Call')])
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking:  by {self.user.name} with {self.tutor.name}'

    def calculate_total_cost(self):
        # Ensure tutor data is linked
        if not self.tutordata:
            self.total_cost = Decimal('0.00')
            return self.total_cost

        hourly_rate = Decimal(self.tutordata.hourly_rate)
        duration_per_day = Decimal(self.tutordata.duration_per_day or 0)

        # Convert start and end from string to datetime if needed
        if isinstance(self.booking_start_date, str):
            try:
                self.booking_start_date = datetime.strptime(self.booking_start_date, "%Y-%m-%d %H:%M")
            except ValueError:
                self.booking_start_date = datetime.strptime(self.booking_start_date, "%Y-%m-%d")

        if isinstance(self.booking_end_date, str):
            try:
                self.booking_end_date = datetime.strptime(self.booking_end_date, "%Y-%m-%d %H:%M")
            except ValueError:
                self.booking_end_date = datetime.strptime(self.booking_end_date, "%Y-%m-%d")

        # Calculate total days between start and end
        total_days = (self.booking_end_date.date() - self.booking_start_date.date()).days
        if total_days < 0:
            total_days = 0

        # Total cost = hourly_rate * duration_per_day * total_days
        self.total_cost = hourly_rate * duration_per_day * Decimal(total_days)
        return self.total_cost

    def save(self, *args, **kwargs):
        self.calculate_total_cost()
        super().save(*args, **kwargs)

class Feedback(models.Model):
    student = models.ForeignKey('Login', on_delete=models.CASCADE, default="",related_name='all_students')
    tutors = models.ForeignKey('Login', on_delete=models.CASCADE, limit_choices_to={'role': 'Tutor'}, default='',related_name='all_tutors')
    ratings = models.IntegerField()
    comment = models.CharField(max_length=300, default="")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback from {self.student.name}"
