from django.contrib import admin
from acgl.models import VendorPersonalDetails, VendorBankAndDocuments

# Register your models here.
admin.site.register(VendorPersonalDetails)
admin.site.register(VendorBankAndDocuments)
