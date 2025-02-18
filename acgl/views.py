from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import VendorDetails

# Home Page
def index(request):
    return render(request, 'index.html', {"variable1": "Jay Shree Krishna"})

# Login View
def login_details(request):
    if request.method == 'POST':
        username1 = request.POST.get('username1')
        password1 = request.POST.get('password1')

        try:
            vendor = VendorDetails.objects.get(username=username1)
        except VendorDetails.DoesNotExist:
            messages.error(request, "Username does not exist. Create a new account.")
            return redirect("login")

        if not check_password(password1, vendor.password_hash):  # Secure password check
            messages.error(request, "Incorrect password. Try again.")
            return redirect("login")

        request.session["vendor_id"] = vendor.vendor_id  # Store vendor ID in session
        return redirect("dashboard")  # Redirect to dashboard

    return render(request, "login.html")

# Step 1: Capture Basic Details
def account(request):
    if request.method == 'POST':
        request.session['form_data'] = {
            'vendor_name': request.POST.get('vendor_name'),
            'business_since': request.POST.get('business_since'),
            'nature_of_services': request.POST.get('nature_of_services'),
            'status': request.POST.get('status'),
            'address': request.POST.get('address'),
            'state': request.POST.get('state'),
            'city': request.POST.get('city'),
            'pin_code': request.POST.get('pin_code'),
            'username': request.POST.get('username'),
            'password_hash': make_password(request.POST.get('password')),  # Secure password hashing
        }
        return redirect("account2")
    return render(request, 'account.html')

# Step 2: Capture Bank Details
def account2(request):
    if request.method == 'POST':
        form_data = request.session.get('form_data', {})
        form_data.update({
            'bank_name': request.POST.get('bank_name'),
            'branch': request.POST.get('branch'),
            'account_number': request.POST.get('account_number'),
            'ifsc_code': request.POST.get('ifsc_code'),
            'account_type': request.POST.get('account_type'),
        })
        request.session['form_data'] = form_data
        return redirect("account3")
    return render(request, 'account2.html')

# Step 3: File Uploads & Save to Database
def account3(request):
    if request.method == 'POST' and request.FILES:
        form_data = request.session.get('form_data', {})

        # Handling file uploads using model FileField (No need for FileSystemStorage)
        form_data.update({
            'pan_doc': request.FILES.get('pan_doc'),
            'aadhar_doc': request.FILES.get('aadhar_doc'),
            'gst_doc': request.FILES.get('gst_doc'),
            'bank_doc': request.FILES.get('bank_doc'),
        })

        # Save form data to VendorDetails model
        vendor = VendorDetails(**form_data)
        try:
            vendor.save()

            # Clear session data after successful submission
            del request.session['form_data']

            messages.success(request, "Registration successful! You can now log in.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect("account3")

    return render(request, 'account3.html')

# Dashboard View
def dashboard(request):
    vendors = VendorDetails.objects.all()
    return render(request, "dashboard.html", {'vendors': vendors})

# Check if username exists (AJAX)
def check_username(request):
    username = request.GET.get('username', '')
    exists = VendorDetails.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

# Static Page Views
def about(request): return render(request, "about.html")
def login(request): return render(request, "login.html")
def rfq(request): return render(request, "RFQ.html")
def rfq2(request): return render(request, "RFQ2.html")
def otp(request): return render(request, "otp.html")
def company(request): return render(request, "company.html")
def service(request): return HttpResponse("This is service page")
def contact(request): return render(request, "contact.html")
def ACGL(request): return render(request, "ACGL_logo.jpg")
def user(request): return render(request, "user.html")
def vendor(request): return render(request, "vendor.html")

# File Download View
def download_file(request, file_field, vendor_id):
    vendor = VendorDetails.objects.get(pk=vendor_id)
    file = getattr(vendor, file_field)
    if file:
        response = HttpResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file.name}"'
        return response
    else:
        messages.error(request, "File not found.")
        return redirect("dashboard")