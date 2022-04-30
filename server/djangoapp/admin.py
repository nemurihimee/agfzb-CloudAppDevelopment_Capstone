from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    

# Register your models here.
    
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    



# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    pass
# CarMakeAdmin class with CarModelInline

# Register models here
admin.site.register(CarMake,CarMakeAdmin)
admin.site.register(CarModel,CarModelAdmin)
