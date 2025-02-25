from django.contrib import admin
from acgl.models import VendorPersonalDetails, VendorBankAndDocuments, AdminUser, CFOUser, CEOUser, HODUser, DesignHeadUser, QualityHeadUser, FinanceHeadUser, Requirement, RFQResponse

# Register your models here.
admin.site.register(VendorPersonalDetails)
admin.site.register(VendorBankAndDocuments)
admin.site.register(AdminUser)
admin.site.register(CFOUser)
admin.site.register(CEOUser)
admin.site.register(HODUser)
admin.site.register(DesignHeadUser)
admin.site.register(QualityHeadUser)
admin.site.register(FinanceHeadUser)
admin.site.register(Requirement)
admin.site.register(RFQResponse)
