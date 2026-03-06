from django.contrib import admin
from .models import Company, Branch, Country, State, City, Employee, CostCenter


admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Company)
admin.site.register(Branch)
admin.site.register(CostCenter)
admin.site.register(Employee)