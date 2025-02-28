import random
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class VendorPersonalDetails(models.Model):
    vendor_id = models.BigAutoField(primary_key=True)  # Auto-incremented ID
    vendor_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=255, unique=True)  # Ensure unique email
    phonenumber = models.CharField(max_length=15)
    business_since = models.DateField(null=True, blank=True)
    nature_of_services = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=[('Service', 'Service'), ('Material', 'Material'), ('Both', 'Both')], default='Service')
    address = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    pin_code = models.CharField(max_length=20, blank=True)
    username = models.CharField(max_length=50, unique=True)  # Ensure username is unique
    password_hash = models.CharField(max_length=255)  # Store hashed password
    submission_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.password_hash and not self.password_hash.startswith('pbkdf2_sha256$'):
            self.password_hash = make_password(self.password_hash)
        super(VendorPersonalDetails, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.vendor_name} - {self.vendor_id}"
class VendorBankAndDocuments(models.Model):
    vendor_code = models.CharField(
        max_length=5, unique=True, primary_key=True, blank=True
    )
    vendor = models.OneToOneField(
        "VendorPersonalDetails", on_delete=models.CASCADE, related_name="bank_and_docs"
    )

    # Bank Details
    bank_name = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    account_type = models.CharField(
        max_length=10, choices=[("Savings", "Savings"), ("Current", "Current")], default="Savings"
    )

    # Document Upload Fields
    pan_doc = models.FileField(upload_to="documents/", blank=True, null=True)
    aadhar_doc = models.FileField(upload_to="documents/", blank=True, null=True)
    gst_doc = models.FileField(upload_to="documents/", blank=True, null=True)
    bank_doc = models.FileField(upload_to="documents/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.vendor_code:  # Generate only if empty
            self.vendor_code = self.generate_unique_vendor_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_vendor_code():
        while True:
            new_code = str(random.randint(10000, 99999))
            if not VendorBankAndDocuments.objects.filter(vendor_code=new_code).exists():
                return new_code

    def __str__(self):
        return f"Bank & Docs - {self.vendor.vendor_name} ({self.vendor_code})"

class AdminUser(models.Model):
    admin_name = models.CharField(max_length=100, blank=False)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255)
    phonenumber = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True)
    password_hash = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.password_hash and not self.password_hash.startswith('pbkdf2_sha256$'):
            self.password_hash = make_password(self.password_hash)
        super(AdminUser, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.admin_name} - {self.username}"

class CFOUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.password_hash and not self.password_hash.startswith('pbkdf2_sha256$'):
            self.password_hash = make_password(self.password_hash)
        super(CFOUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

class CEOUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.password_hash and not self.password_hash.startswith('pbkdf2_sha256$'):
            self.password_hash = make_password(self.password_hash)
        super(CEOUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

# New User Models
class HODUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.password_hash and not self.password_hash.startswith('pbkdf2_sha256$'):
            self.password_hash = make_password(self.password_hash)
        super(HODUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

class DesignHeadUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.password_hash and not self.password_hash.startswith('pbkdf2_sha256$'):
            self.password_hash = make_password(self.password_hash)
        super(DesignHeadUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

class QualityHeadUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.password_hash and not self.password_hash.startswith('pbkdf2_sha256$'):
            self.password_hash = make_password(self.password_hash)
        super(QualityHeadUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

class FinanceHeadUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.password_hash and not self.password_hash.startswith('pbkdf2_sha256$'):
            self.password_hash = make_password(self.password_hash)
        super(FinanceHeadUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
class Requirement(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved by CFO', 'Approved by CFO'),
        ('Approved by CEO', 'Approved by CEO'),
        ('Rejected by CFO', 'Rejected by CFO'),
        ('Rejected by CEO', 'Rejected by CEO'),
    ]

    requested_by = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)  # Auto-set system date and time
    rfq_no = models.CharField(max_length=10, unique=True, blank=False, null=False)  # New RFQ field

    department = models.CharField(max_length=100)
    priority = models.CharField(max_length=50, choices=[('Material', 'Material'), ('Service', 'Service')])
    item_description = models.TextField()
    justification = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    next_approver = models.CharField(max_length=50, blank=True, null=True)
    modification_description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)  

    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quotation_deadline = models.DateField(null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    delivery_address = models.CharField(max_length=255, default="Pune", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.rfq_no:  # Generate unique 10-digit RFQ No
            self.rfq_no = self.generate_unique_rfq()
        super().save(*args, **kwargs)

    def generate_unique_rfq(self):
        while True:
            rfq = str(random.randint(1000000000, 9999999999))  # Generate a 10-digit number
            if not Requirement.objects.filter(rfq_no=rfq).exists():
                return rfq

    def __str__(self):
        return f"{self.requested_by} - {self.department} - {self.status}"
class RFQResponse(models.Model):
    rfq_number = models.CharField(max_length=50)
    date_submitted = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp
    response_deadline = models.DateTimeField()
    vendor_code = models.ForeignKey(VendorBankAndDocuments, on_delete=models.CASCADE, null=False)

    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    item_number = models.CharField(max_length=50)
    description = models.TextField()
    specification = models.TextField()
    per_unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    gst = models.DecimalField(max_digits=5, decimal_places=2)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    attachment = models.FileField(upload_to="rfq_attachments/", blank=True, null=True)
    
    hod_verification = models.BooleanField(default=False)
    design_head_verification = models.BooleanField(default=False)
    quality_head_verification = models.BooleanField(default=False)
    finance_head_verification = models.BooleanField(default=False)
     # Ensure uniqueness
    negotiated_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    final_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    negotiation_comments = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"RFQ {self.rfq_number} - {self.vendor_code}"
