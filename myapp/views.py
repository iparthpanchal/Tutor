from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
# Create your views here.

def checksession(request):
    uid = request.session.get('log_id')

    if not uid:
        return None

    try:
        userdata = Login.objects.get(id=uid)
        is_tutor = userdata.role == "Tutor"


        context = {
            'userdata': userdata,
            'is_tutor': is_tutor,
        }
        return context
    except Login.DoesNotExist:
        return None

def index(request):
    context = checksession(request)
    if context is None:
        context = {}
    categories = Category.objects.all()
    context['alldata'] = categories
    return render(request,'index.html',context)

def about(request):
    context = checksession(request)
    return render(request,'about-us.html',context)

def contact(request):
    context = checksession(request)
    if request.method == "POST":
        Name = request.POST.get('first_name')
        Email = request.POST.get('email')
        Subject = request.POST.get('subject')
        Message = request.POST.get('message')

        if Contact_detail.objects.filter(email=Email).exists():
            messages.error(request, 'You have already filled out contact details.')
            return redirect('contact')  # Assuming you have a URL pattern named 'contact1'
        else:
            contactdata = Contact_detail(name=Name, email=Email, subject=Subject, message=Message)
            contactdata.save()
            messages.success(request, 'Your contact details have been saved.')
            return redirect('index')  # Ensure 'index' is the name of your URL pattern or view function
    return render(request,'contact.html', context)

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name1')
        email = request.POST.get('email1')
        password = request.POST.get('password1')
        phone = request.POST.get('phone1')
        role = request.POST.get('usertype')

        # Create a new Login object
        new_user = Login(name=name, email=email, password=password, phone=phone, role=role)

        # Check if role is Seller and if id_proof1 exists in request.FILES
        if role == 'Tutor' and 'id_proof1' in request.FILES:
            id_proof = request.FILES['id_proof1']
            new_user.id_proof = id_proof
            messages.info(request, 'Registration done successfully. Please wait for your profile approval. It will take around 2-3 days.')
        else:
            messages.success(request, 'Data inserted successfully. You can login now.')

        new_user.save()

        # Redirect to a success page
        return redirect('index')

    return render(request, 'sign-up.html')

def login(request):
    if request.method == "POST":
        Email1 = request.POST['email2']
        Password1 = request.POST['password2']
        try:
            user = Login.objects.get(email=Email1, password=Password1)

        except Login.DoesNotExist:
            user = None

        if user is not None:
            if user.role == "Tutor" and user.status == "0":
                print(user.role)
                print(user.status)
                messages.error(request, 'Your Profile is Under Approval Process. This may take upto 3 working days.')
            else:
                request.session['log_id'] = user.id
                request.session.save()
                messages.success(request, 'Login successful...')
                return redirect('/')
        else:
            messages.error(request, 'Invalid Email Id and Password. Please try again.')
            return redirect('/login')
    return render(request, 'sign-in.html')

def logout(request):
    try:
        del request.session['log_id']
        messages.success(request,'your logout successfully.')
    except:
        pass
    return render(request,'index.html')

def forgotpassword(request):
    if request.method == 'POST':
        username = request.POST.get('email2')
        try:
            user = Login.objects.get(email=username)

        except Login.DoesNotExist:
            user = None
        # if user exist then only below condition will run otherwise it will give error as described in else condition.
        if user is not None:
            #################### Password Generation ##########################
            import random

            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

            nr_letters = 6
            nr_symbols = 1
            nr_numbers = 3
            password_list = []

            for char in range(1, nr_letters + 1):
                password_list.append(random.choice(letters))

            for char in range(1, nr_symbols + 1):
                password_list += random.choice(symbols)

            for char in range(1, nr_numbers + 1):
                password_list += random.choice(numbers)

            print(password_list)
            random.shuffle(password_list)
            print(password_list)

            password = ""  # we will get final password in this var.
            for char in password_list:
                password += char

            ##############################################################

            msg = "hello here it is your new password  " + password  # this variable will be passed as message in mail

            ############ code for sending mail ########################

            from django.core.mail import send_mail

            send_mail(
                'Your New Password',
                msg,
                'parthinfolabz19@gmail.com',
                [username],
                fail_silently=False,
            )
            # NOTE: must include below details in settings.py
            # detail tutorial - https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
            # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            # EMAIL_HOST = 'smtp.gmail.com'
            # EMAIL_USE_TLS = True
            # EMAIL_PORT = 587
            # EMAIL_HOST_USER = 'mail from which email will be sent'
            # EMAIL_HOST_PASSWORD = 'pjobvjckluqrtpkl'   #turn on 2 step verification and then generate app password which will be 16 digit code and past it here

            #############################################

            # now update the password in model
            cuser = Login.objects.get(email=username)
            cuser.password = password
            cuser.save(update_fields=['password'])

            print('Mail sent')
            messages.info(request, 'mail is sent')
            return redirect(index)

        else:
            messages.info(request, 'This account does not exist')
        return redirect(index)


def category_course(request):
    context = checksession(request)
    if context is None:
        context = {}
    categories = Category.objects.all()
    context['alldata'] = categories
    return render(request,'course.html', context)

def course(request,cid):
    context = checksession(request)
    allcourses = Course.objects.filter(cat_course=cid)
    context.update({'available_courses':allcourses})
    return render(request,'show_courses.html', context)

def subject(request,sid):
    context = checksession(request)
    allcourses = Subject.objects.filter(course=sid)
    context.update({'available_subjects':allcourses})
    return render(request,'show_subjects.html', context)

def add_expertise(request):
    context =checksession(request)
    uid = request.session['log_id']
    categories = Category.objects.all()

    selected_category_id = request.GET.get('category')  # or POST, but GET is easier here
    selected_course_id = request.GET.get('course')

    courses = Course.objects.filter(cat_course_id=selected_category_id) if selected_category_id else []
    subjects = Subject.objects.filter(course_id=selected_course_id) if selected_course_id else []

    if request.method == "POST":
        subject_id = request.POST.get('subject')
        subject = Subject.objects.get(id=subject_id)

        TutorExpertise.objects.create(
            tutor=Login(id=uid),
            category=subject.course.cat_course,
            course=subject.course,
            subject=subject,
            hourly_rate=request.POST.get('hourly_rate'),
            duration_per_day=request.POST.get('duration_per_day'),
            experience_years=request.POST.get('experience_years'),
            qualification=request.POST.get('qualification'),
            languages=request.POST.get('languages'),
            bio=request.POST.get('bio'),
            available_days=request.POST.get('available_days'),
            profile_image=request.FILES.get('profile_image')
        )
        messages.success(request,'Your data has been saved.')
        return redirect('index')

    context.update({
        'categories': categories,
        'courses': courses,
        'subjects': subjects,
        'selected_category_id': selected_category_id,
        'selected_course_id': selected_course_id,
    })
    return render(request, 'add_expertise.html', context)

def tutors(request,tid):
    context = checksession(request)
    alldata = TutorExpertise.objects.filter(subject=tid)
    context.update({'alldata':alldata})
    return render(request,'instructor.html',context)

def tutors_detail(request,t_id):
    context = checksession(request)
    alldata = TutorExpertise.objects.get(id=t_id)
    context.update({'alldata':alldata})
    return render(request,'instructor-details.html',context)

from django.shortcuts import get_object_or_404

from django.contrib import messages

def add_tutor_booking(request, tutordata_id):
    context = checksession(request)
    uid = request.session['log_id']
    user_instance = get_object_or_404(Login, id=uid)
    tutordata_instance = get_object_or_404(TutorExpertise, id=tutordata_id)

    if request.method == "POST":
        booking_start_date = request.POST.get('start_date')
        booking_end_date = request.POST.get('end_date')
        contact_email = request.POST.get('contact_email')
        communication_preference = request.POST.get('communication_preference')

        booking = TutorBooking(
            tutor=tutordata_instance.tutor,
            user=user_instance,
            tutordata=tutordata_instance,
            booking_start_date=booking_start_date,
            booking_end_date=booking_end_date,
            contact_email=contact_email,
            communication_preference=communication_preference,
        )

        try:
            booking.calculate_total_cost()
        except Exception as e:
            print("Cost calculation error:", e)

        booking.save()
        messages.success(request, 'Your booking has been successfully saved!')
        return redirect('index')

    context.update({'tutordata': tutordata_instance})
    return render(request, 'tutor_booking.html', context)

def request_student(request):
    context = checksession(request)
    # Get the logged-in user ID from the session
    uid = request.session.get('log_id')

    # Retrieve the FreelancerProfile based on the logged-in user
    tutor = get_object_or_404(Login, id=uid)

    # Filter orders that belong to the logged-in freelancer
    orders = TutorBooking.objects.filter(tutor=tutor)

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(TutorBooking, id=order_id, tutor=tutor)  # Ensure the order belongs to this freelancer

        # Check if the freelancer accepted or rejected the order
        if 'accept' in request.POST:
            order.status = 'accepted'
            messages.success(request, f'Request #{order_id} has been accepted.')
        elif 'reject' in request.POST:
            order.status = 'rejected'
            messages.success(request, f'Request #{order_id} has been rejected.')

        # Save the status update
        order.save()

        # Redirect to the same page to refresh the order list
        return redirect('request_student')  # Make sure the URL name matches the view

    context.update({
        'orders': orders,
    })
    return render(request, 'request.html', context)

def user_orders(request):
    context = checksession(request)
    uid = request.session.get('log_id')
    if request.method == 'POST':
        order_id = request.POST.get('order_id')

        action = 'accept' if 'accept' in request.POST else 'reject'
        order = get_object_or_404(TutorBooking, id=order_id, user=Login(id=uid))

        # Update order status based on action
        if action == 'accept':
            order.status = 'accepted'
        elif action == 'reject':
            order.status = 'rejected'

        # Calculate the total price
        total_price = order.total_cost

        # Initialize Razorpay client and create an order
        client = razorpay.Client(auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f'))
        amount = int(total_price * 100)  # Convert to paisa
        data = {
            "amount": amount,
            "currency": "INR",
            "receipt": f"order_{uid}",
            "payment_capture": 1
        }

        try:
            razorpay_payment = client.order.create(data=data)
            razorpay_order_id = razorpay_payment['id']
            order.razorpay_order_id = razorpay_order_id
            order.save()

            context = {
                'razorpay_payment': {
                    'amount': amount,
                    'order_id': razorpay_order_id,
                    'key': "rzp_test_VQhEfe2NCXbbwI",  # Your Razorpay key
                },
                'order': order,
            }
            return render(request, 'user_request.html', context)

        except razorpay.errors.BadRequestError as e:
            messages.error(request, f'BadRequestError: {str(e)}')
            return redirect('user_orders')  # Redirect on error
        except razorpay.errors.ServerError as e:
            messages.error(request, f'ServerError: {str(e)}')
            return redirect('user_orders')  # Redirect on error
        except Exception as e:
            print(f"Error occurred: {str(e)}")  # Log the error
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return redirect('user_orders')

    # Display user orders
    orders = TutorBooking.objects.filter(user=Login(id=uid))
    context.update({
        'orders': orders
    })
    return render(request, 'user_request.html', context)

import razorpay
from django.core.mail import send_mail

def success(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature'],
    }

    client = razorpay.Client(
        auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f')
    )

    try:
        # Verify the payment signature
        client.utility.verify_payment_signature(params_dict)

        # Get the order based on the Razorpay order ID
        order = TutorBooking.objects.get(razorpay_order_id=response['razorpay_order_id'])

        # Update the Razorpay payment ID and signature in the order
        order.razorpay_payment_id = response['razorpay_payment_id']
        order.razorpay_signature = response['razorpay_signature']

        # Set the status to 'paid' if payment is successful
        order.status = 'paid'
        order.save()

        # Send a confirmation email
        subject = 'Payment Successful'
        message = f"Dear {order.user.name},\n\n" \
                  f"Your payment for Order ID {order.id} has been successfully processed. Thank you for choosing us!\n\n" \
                  f"Best regards,\nYour Team"
        sender_email = 'dpoza8125@gmail.com'  # Replace with your sender email address
        recipient_email = [order.user.email]

        send_mail(subject, message, sender_email, recipient_email, fail_silently=False)

        return render(request, 'success.html', {'status': True})

    except razorpay.errors.SignatureVerificationError:
        # Handle signature verification errors
        print("Signature verification failed.")
        return render(request, 'success.html', {'status': False})

    except Exception as e:
        # Handle other exceptions
        print(f"Error occurred: {str(e)}")
        return render(request, 'success.html', {'status': False})

def storefeedback(request):
    context = checksession(request)
    user_id = request.session.get('log_id')
    alltutors = Login.objects.filter(role='Tutor')


    context.update({'tutors': alltutors})
    if request.method == 'POST':
        ratings = request.POST.get('ratings')
        feedback_message = request.POST.get('feedback_message')
        tutor = request.POST.get('tutor')

        if Feedback.objects.filter(student=Login(id=user_id)).exists():
            messages.error(request, 'you have already filled feedback.')
            return redirect('/payment')
        else:
        # Assuming 'product' is a ForeignKey in the Feedback model pointing to Product
            feedback = Feedback.objects.create(
                student=Login(id=user_id),
                tutors=Login(id=tutor),
                ratings=ratings,
                comment=feedback_message,
            )
        messages.success(request, "feedback is submitted")
        return redirect(index)
    return render(request, 'feedback_page.html', context)