from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone
from .models import TravelOption, Booking

def home(request):
    return render(request,"base.html")

#==========User Management============

def signup1(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirmation = request.POST.get("confirmation", "")

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
        elif password != confirmation:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")
    return render(request, "registration/signup.html")

def login1(request):
    if request.method == "POST":
        identifier = request.POST.get("username")  # email or username field from your form
        password = request.POST.get("password")

        user = None
        try:
            u = User.objects.get(email=identifier)
            user = authenticate(request, username=u.username, password=password)
        except User.DoesNotExist:
            user = authenticate(request, username=identifier, password=password)

        if user:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid credentials.")
    return render(request, "registration/login.html")


def logout1(request):
    logout(request)
    return redirect("login")

@login_required
def profile(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()

        if not username or not email:
            messages.error(request, "Username and Email are required.")
        elif User.objects.exclude(pk=request.user.pk).filter(username=username).exists():
            messages.error(request, "This username is already taken.")
        elif User.objects.exclude(pk=request.user.pk).filter(email=email).exists():
            messages.error(request, "This email is already in use.")
        else:
            request.user.username = username
            request.user.email = email
            request.user.save()
            messages.success(request, "Profile updated successfully!")
    return render(request, "registration/profile.html")

# #=========part 2=========================

def travel_list(request):
    options = TravelOption.objects.all()

    travel_type = request.GET.get("travel_type")
    source = request.GET.get("source")
    destination = request.GET.get("destination")
    travel_date = request.GET.get("travel_date")  # format: YYYY-MM-DD

    if travel_type:
        options = options.filter(travel_type=travel_type)
    if source:
        options = options.filter(source__icontains=source)
    if destination:
        options = options.filter(destination__icontains=destination)
    if travel_date:
        options = options.filter(travel_datetime__date__gte=travel_date)

    return render(request, "travel_list.html", {"options": options})

@login_required
def travel_option(request, travel_id):
    option = get_object_or_404(TravelOption, travel_id=travel_id)

    if request.method == "POST":
        seats = int(request.POST.get("number_of_seats", 1))
        if seats > option.available_seats:
            error = "Not enough seats available."
            return render(request, "travel_option.html", {"option": option, "error": error})
        
        booking = Booking.objects.create(
            user=request.user,
            travel_option=option,
            number_of_seats=seats
        )
        option.available_seats -= seats
        option.save()

        return redirect("booking_success", booking_id=booking.booking_id)

    return render(request, "travel_option.html", {"option": option})

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, "booking_history.html", {"bookings": bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    if booking.status == "confirmed":
        booking.status = "cancelled"
        booking.save()
        messages.success(request, f"Booking {booking.booking_id} has been cancelled.")
    else:
        messages.warning(request, f"Booking {booking.booking_id} cannot be cancelled.")

    return redirect("booking_history")


@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    return render(request, "booking_success.html", {"booking": booking})