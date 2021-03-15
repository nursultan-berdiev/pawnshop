from django.contrib import admin
from .models import Zalog_types, Product, PrihodRashod, WorkDays

admin.site.register(Zalog_types),
admin.site.register(Product),
admin.site.register(PrihodRashod),
admin.site.register(WorkDays),

