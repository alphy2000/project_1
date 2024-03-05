from django.contrib import admin
from .models import *

# Register your models here.

# Signup
admin.site.register(usersignup)

# Cart
admin.site.register(mycart)

# Products
admin.site.register(products)

# Order details
admin.site.register(order)
admin.site.register(orderitem)
# admin.site.register(profile)



admin.site.register(PasswordReset)


admin.site.register(msg)