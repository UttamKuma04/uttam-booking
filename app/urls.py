from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # Auth & profile
    path("signup/", views.signup1, name="signup"),
    path("login/", views.login1, name="login"),
    path("logout/", views.logout1, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("travels/", views.travel_list, name="travel_options_list"),
    path("travels/<int:travel_id>/book/", views.travel_option, name="book_travel_option"),
    path("booking/success/<int:booking_id>/", views.booking_success, name="booking_success"),
    path("bookings/", views.booking_history, name="booking_history"),
    path('bookings/', views.booking_history, name='bookings'),
    path("bookings/cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),

]