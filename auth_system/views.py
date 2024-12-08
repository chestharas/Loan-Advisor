from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.http import HttpResponse
import random
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile
# from django.contrib.auth.hashers import 


def index(request):
    return HttpResponse("Welcome to the Auth System Home Page!")


def signup(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # Save form data (e.g., first name, last name, gender, phone number)
            form.save()

            # Store the phone number in the session
            phone_number = form.cleaned_data.get('phone_number')
            request.session['phone_number'] = phone_number

            # Generate OTP and store it in the session
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp

            # Redirect to the "Verify OTP" page
            return redirect('auth-verify')
    else:
        form = UserProfileForm()
    return render(request, 'auth_system/signup.html', {'form': form})


def generate_otp(request):
    # Example phone number (this could come from the session or database)
    phone_number = request.session.get('phone_number', 'Unknown Number')

    # Generate a 6-digit OTP
    otp = random.randint(100000, 999999)

    # Store the OTP in the session for later verification
    request.session['otp'] = otp

    # Pass the OTP and phone number to the template
    return render(request, 'auth_system/get_otp.html', {'otp': otp, 'phone_number': phone_number})

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')  # Retrieve OTP from session

        if entered_otp and int(entered_otp) == stored_otp:
            # Clear the OTP from the session after successful verification
            request.session['otp'] = None
            # Redirect to the create password page
            return redirect('auth-create-password')
        else:
            return render(request, 'auth_system/verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'auth_system/verify_otp.html')

def create_password(request):
    # Check if the request is a POST request
    if request.method == 'POST':
        # Retrieve password inputs from the form
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Get the phone number from the session
        phone_number = request.session.get('phone_number')

        # Ensure passwords match and are not empty
        if password and confirm_password and password == confirm_password:
            try:
                # Fetch the user by phone number
                user_profile = UserProfile.objects.get(phone_number=phone_number)

                # Hash and save the password
                user_profile.password = make_password(password)
                user_profile.save()

                # Redirect to the dashboard after successful password creation
                request.session['user_id'] = user_profile.id  # Store user ID in session
                return redirect('dashboard-index')
            except UserProfile.DoesNotExist:
                # Handle the case where the user profile does not exist
                return render(
                    request,
                    'auth_system/create_password.html',
                    {'error': 'User does not exist. Please contact support.'}
                )
        else:
            # Handle password mismatch or empty fields
            error = "Passwords do not match or are invalid. Please try again."
            return render(request, 'auth_system/create_password.html', {'error': error})

    # Render the create password form for GET requests
    return render(request, 'auth_system/create_password.html')

def sign_in(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        # Check if user exists
        try:
            user = UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            return render(request, 'auth_system/sign_in.html', {'error': 'Invalid phone number or password'})

        # Verify the password
        if check_password(password, user.password):
            # Store user information in session
            request.session['user_id'] = user.id
            return redirect('dashboard-index')  # Redirect to dashboard
        else:
            return render(request, 'auth_system/sign_in.html', {'error': 'Invalid phone number or password'})

    return render(request, 'auth_system/sign_in.html')
