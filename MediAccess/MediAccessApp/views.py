from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .models import User, PatientProfile, DoctorProfile
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'login_and_signup.html')

def signup(request):
    if request.method == 'POST':
        # Extract data from the signup form
        user_type = request.POST.get('user_type')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        profile_picture = request.FILES.get('profile_picture')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address_line1 = request.POST.get('address_line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('index')

        # Create a new User instance
        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        except Exception as e:
            messages.error(request, 'Username already exist!')
            return redirect('index')

        # Determine user type and create corresponding profile
        if user_type == 'Patient':
            user.is_patient = True
            profile = PatientProfile(user=user, address_line1=address_line1, city=city, state=state, pincode=pincode, profile_picture=profile_picture)
        elif user_type == 'Doctor':
            user.is_doctor = True
            profile = DoctorProfile(user=user, address_line1=address_line1, city=city, state=state, pincode=pincode, profile_picture=profile_picture)
        else:
            messages.error(request, 'Invalid user type')
            return redirect('index')

        # Save the profile
        profile.save()

        # Save the User instance with the correct user type flag
        user.save()

        messages.success(request, 'Signup successful. You can now log in.')
        return redirect('index')

    return render(request, 'login_and_signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Debugging line to print form inputs
        print(f"Login attempt with username: '{username}', password: '{password}'")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, 'Login successful.')
            return redirect('dashboard')
        else:
            print(f"Authentication failed for username: '{username}'")
            messages.error(request, 'Invalid credentials')
            return redirect('index')

    return render(request, 'login_and_signup.html')

def logout(request):
    auth_logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('index')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
