from django.contrib import admin
from .models import Client, Zalog, Zalog_types, Loan

admin.site.register(Client),
admin.site.register(Zalog),
admin.site.register(Zalog_types),
admin.site.register(Loan),

