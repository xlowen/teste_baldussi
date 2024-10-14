from django.contrib import admin
from .models import Location, UserInformation, UserProfile

admin.site.register(UserProfile)
admin.site.register(Location)
admin.site.register(UserInformation)