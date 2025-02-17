from django.db import models

# Create your models here.
class VendorDetails(models.Model):
    fullname=models.CharField(max_length=63)
    vendorname=models.CharField(max_length=63)
    username=models.CharField(max_length=63, unique="true")
    password=models.CharField(max_length=63)
    address=models.CharField(max_length=63)
    phonenumber=models.CharField(max_length=63)
    email=models.EmailField()
    dob=models.DateField()
    igst=models.CharField(max_length=63)
    
    def __str__(self):
        return self.fullname

class UploadDocuments(models.Model):
    aadhar_doc = models.FileField(upload_to='documents/', blank=True, null=True)
    gst_doc = models.FileField(upload_to='documents/', blank=True, null=True)
    bank_details = models.CharField(max_length=63, null=False, blank=False, default="Default Bank Details")
 # NOT NULL now

    def __str__(self):
        return self.bank_details
