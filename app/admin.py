# from django.contrib import admin
# from .models import TravelOption, Booking

# @admin.register(TravelOption)
# class TravelOptionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'type', 'price')
#     search_fields = ('name', 'type')
#     list_filter = ('type',)


# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'travel_option', 'passengers', 'total_price', 'booking_date')
#     search_fields = ('user__username', 'travel_option__name')
#     list_filter = ('travel_option__type', 'booking_date')


from django.contrib import admin
from .models import TravelOption, Booking

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ("travel_id", "travel_type", "source", "destination", "travel_datetime", "price", "available_seats")
    list_filter = ("travel_type", "source", "destination")
    search_fields = ("source", "destination")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("booking_id", "user", "travel_option", "number_of_seats", "total_price", "booking_date", "status")
    list_filter = ("status", "travel_option__travel_type")
    search_fields = ("user__username", "travel_option__source", "travel_option__destination")
