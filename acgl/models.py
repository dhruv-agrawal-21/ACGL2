from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator

class VendorDetails(models.Model):
    vendor_id = models.BigAutoField(primary_key=True)  # Auto-incremented ID
    vendor_name = models.CharField(max_length=100, blank=True)
    business_since = models.DateField(null=True, blank=True)
    nature_of_services = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=[('Service', 'Service'), ('Material', 'Material'), ('Both', 'Both')], default='Service')
    address = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    pin_code = models.CharField(max_length=20, blank=True)
    username = models.CharField(max_length=50, unique=True)  # Ensure username is unique
    password_hash = models.CharField(max_length=255)  # Should be hashed securely
    bank_name = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    account_type = models.CharField(max_length=10, choices=[('Savings', 'Savings'), ('Current', 'Current')], default="Savings")

    # File Upload Fields with validators
    pan_doc = models.FileField(upload_to='documents/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])])
    aadhar_doc = models.FileField(upload_to='documents/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])])
    gst_doc = models.FileField(upload_to='documents/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])])
    bank_doc = models.FileField(upload_to='documents/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])])

    submission_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.password_hash and not self.password_hash.startswith('pbkdf2_sha256$'):
            self.password_hash = make_password(self.password_hash)
        super(VendorDetails, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.vendor_name} - {self.vendor_id}"