from django.contrib import admin
from bug_bounty.models import Company, Program, Reports

# Register your models here.
admin.site.register(Company)
admin.site.register(Program)
admin.site.register(Reports)


