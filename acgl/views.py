import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout as auth_logout
from .models import VendorPersonalDetails, VendorBankAndDocuments, AdminUser, CFOUser, CEOUser, HODUser, DesignHeadUser, QualityHeadUser, FinanceHeadUser, Requirement
from .forms import VendorPersonalDetailsForm
from reportlab.pdfgen import canvas

# Home Page
def index(request):
    return render(request, 'index.html', {"variable1": "Jay Shree Krishna"})

# Login View
def login_details(request):
    if request.method == 'POST':
        username1 = request.POST.get('username1')
        password1 = request.POST.get('password1')
        
        try:
            admin_user = AdminUser.objects.get(username=username1)
            if check_password(password1, admin_user.password_hash):
                request.session["admin_username"] = admin_user.username  # Store admin username in session
                return redirect("admin_dashboard")  # Redirect to admin dashboard
            else:
                messages.error(request, "Incorrect password. Try again.")
                return redirect("login")
        except AdminUser.DoesNotExist:
            pass

        try:
            vendor = VendorPersonalDetails.objects.get(username=username1)
            if check_password(password1, vendor.password_hash):
                request.session["vendor_id"] = vendor.vendor_id  # Store vendor ID in session
                request.session["vendor_name"] = vendor.vendor_name
                request.session["vendor_username"] = vendor.username
                return redirect("dashboard")  # Redirect to dashboard
            else:
                messages.error(request, "Incorrect password. Try again.")
                return redirect("login")
        except VendorPersonalDetails.DoesNotExist:
            pass

        try:
            cfo_user = CFOUser.objects.get(username=username1)
            if check_password(password1, cfo_user.password_hash):
                request.session["cfo_username"] = cfo_user.username  # Store CFO username in session
                return redirect("cfo_dashboard")  # Redirect to CFO dashboard
            else:
                messages.error(request, "Incorrect password. Try again.")
                return redirect("login")
        except CFOUser.DoesNotExist:
            pass

        try:
            ceo_user = CEOUser.objects.get(username=username1)
            if check_password(password1, ceo_user.password_hash):
                request.session["ceo_username"] = ceo_user.username  # Store CEO username in session
                return redirect("ceo_dashboard")  # Redirect to CEO dashboard
            else:
                messages.error(request, "Incorrect password. Try again.")
                return redirect("login")
        except CEOUser.DoesNotExist:
            pass

        try:
            hod_user = HODUser.objects.get(username=username1)
            if check_password(password1, hod_user.password_hash):
                request.session["hod_username"] = hod_user.username  # Store HOD username in session
                return redirect("hod_dashboard")  # Redirect to HOD dashboard
            else:
                messages.error(request, "Incorrect password. Try again.")
                return redirect("login")
        except HODUser.DoesNotExist:
            pass

        try:
            design_head_user = DesignHeadUser.objects.get(username=username1)
            if check_password(password1, design_head_user.password_hash):
                request.session["design_head_username"] = design_head_user.username  # Store Design Head username in session
                return redirect("design_head_dashboard")  # Redirect to Design Head dashboard
            else:
                messages.error(request, "Incorrect password. Try again.")
                return redirect("login")
        except DesignHeadUser.DoesNotExist:
            pass

        try:
            quality_head_user = QualityHeadUser.objects.get(username=username1)
            if check_password(password1, quality_head_user.password_hash):
                request.session["quality_head_username"] = quality_head_user.username  # Store Quality Head username in session
                return redirect("quality_head_dashboard")  # Redirect to Quality Head dashboard
            else:
                messages.error(request, "Incorrect password. Try again.")
                return redirect("login")
        except QualityHeadUser.DoesNotExist:
            pass

        try:
            finance_head_user = FinanceHeadUser.objects.get(username=username1)
            if check_password(password1, finance_head_user.password_hash):
                request.session["finance_head_username"] = finance_head_user.username  # Store Finance Head username in session
                return redirect("finance_head_dashboard")  # Redirect to Finance Head dashboard
            else:
                messages.error(request, "Incorrect password. Try again.")
                return redirect("login")
        except FinanceHeadUser.DoesNotExist:
            messages.error(request, "Username does not exist. Create a new account.")
            return redirect("login")

    return render(request, "login.html")

# Logout View
def logout(request):
    auth_logout(request)
    return redirect("login")

# Step 1: Capture Basic Details


# Step 1: Capture Personal Details
def account(request):
    if request.method == 'POST':
        form = VendorPersonalDetailsForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.password_hash = make_password(form.cleaned_data['password'])  # Hash password
            vendor.save()  # Save immediately

            messages.success(request, "Personal details saved successfully.")
            return redirect("login")  # Redirect to dashboard
        else:
            print("Form is not valid. Errors:")
            for field, errors in form.errors.items():
                print(f"Field: {field}")
                for error in errors:
                    print(f"  Error: {error}")
        messages.error(request, "Please fix the errors below.")
    else:
        form = VendorPersonalDetailsForm()

    return render(request, 'account.html', {'form': form})

def account2(request):
    if "vendor_username" not in request.session:
        return redirect("login")  # Redirect to login page

    if request.method == 'POST':
        username = request.user.username  

        request.session['bank_data'] = {
            'bank_name': request.POST.get('bank_name'),
            'branch': request.POST.get('branch'),
            'account_number': request.POST.get('account_number'),
            'ifsc_code': request.POST.get('ifsc_code'),
            'account_type': request.POST.get('account_type'),
            'username': username,
        }

        messages.success(request, "Bank details saved. Proceed to document upload.")
        return redirect("account3")

    return render(request, 'account2.html')
# Step 2: Fill Bank Details
def account3(request):
    if "vendor_username" not in request.session:
        return redirect("login")  # Redirect to login page

    if request.method == "POST" and request.FILES.keys():
        bank_data = request.session.get("bank_data", {})

        if not bank_data:
            messages.error(request, "Session expired. Please restart from Step 2.")
            return redirect("account2")

        try:
            vendor = VendorPersonalDetails.objects.get(username=request.session["vendor_username"])
        except VendorPersonalDetails.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("account")

        # Check if VendorBankAndDocuments already exists for this vendor
        if VendorBankAndDocuments.objects.filter(vendor=vendor).exists():
            messages.error(request, "Bank & document details already submitted.")
            return redirect("dashboard")

        # Create and save Bank & Document Details
        bank_doc_entry = VendorBankAndDocuments(
            vendor=vendor,
            bank_name=bank_data.get("bank_name", ""),
            branch=bank_data.get("branch", ""),
            account_number=bank_data.get("account_number", ""),
            ifsc_code=bank_data.get("ifsc_code", ""),
            account_type=bank_data.get("account_type", "Savings"),
            pan_doc=request.FILES.get("pan_doc"),
            aadhar_doc=request.FILES.get("aadhar_doc"),
            gst_doc=request.FILES.get("gst_doc"),
            bank_doc=request.FILES.get("bank_doc"),
        )
        
        bank_doc_entry.save()  # This will generate a unique vendor_code

        # Clear session data
        del request.session["bank_data"]

        messages.success(request, "Bank & document details saved successfully!")
        return redirect("dashboard")

    return render(request, "account3.html")

# Dashboard View
# def dashboard(request):
#     if "vendor_id" not in request.session:
#         return redirect("login")
#     vendors = VendorPersonalDetails.objects.all()
#     return render(request, "dashboard.html", {'vendors': vendors})
def dashboard(request):
    if "vendor_id" not in request.session:
        return redirect("login")
    
    try:
        vendor = VendorPersonalDetails.objects.get(vendor_id=request.session["vendor_id"])
        has_bank_details = VendorBankAndDocuments.objects.filter(vendor=vendor).exists()
        request.session["has_bank_details"] = has_bank_details  # Store in session
    except VendorPersonalDetails.DoesNotExist:
        return redirect("login")
    
    vendors = VendorPersonalDetails.objects.all()
    return render(request, "dashboard.html", {"vendors": vendors})

# CFO Dashboard View
def cfo_dashboard(request):
    if "cfo_username" not in request.session:
        return redirect("login")
    requirements = Requirement.objects.filter(next_approver='CFO').order_by('-id')
    return render(request, "cfo_dashboard.html", {'requirements': requirements})

# CEO Dashboard View
def ceo_dashboard(request):
    if "ceo_username" not in request.session:
        return redirect("login")
    requirements = Requirement.objects.filter(next_approver='CEO', status='Approved by CFO').order_by('-id')
    return render(request, "ceo_dashboard.html", {'requirements': requirements})

# HOD Dashboard View
def hod_dashboard(request):
    if "hod_username" not in request.session:
        return redirect("login")
    requirements = Requirement.objects.filter(next_approver='HOD').order_by('-id')
    return render(request, "hod_dashboard.html", {'requirements': requirements})

# Design Head Dashboard View
def design_head_dashboard(request):
    if "design_head_username" not in request.session:
        return redirect("login")
    requirements = Requirement.objects.filter(next_approver='Design Head').order_by('-id')
    return render(request, "design_head_dashboard.html", {'requirements': requirements})

# Quality Head Dashboard View
def quality_head_dashboard(request):
    if "quality_head_username" not in request.session:
        return redirect("login")
    requirements = Requirement.objects.filter(next_approver='Quality Head').order_by('-id')
    return render(request, "quality_head_dashboard.html", {'requirements': requirements})

# Finance Head Dashboard View
def finance_head_dashboard(request):
    if "finance_head_username" not in request.session:
        return redirect("login")
    requirements = Requirement.objects.filter(next_approver='Finance Head').order_by('-id')
    return render(request, "finance_head_dashboard.html", {'requirements': requirements})

# Admin Dashboard View
def admin_dashboard(request):
    if "admin_username" not in request.session:
        return redirect("login")
    requirements = Requirement.objects.all().order_by('-id')
    return render(request, "admin_dashboard.html", {'requirements': requirements})

# Vendor Details View
def vendor(request):
    if "admin_username" not in request.session and "cfo_username" not in request.session and "ceo_username" not in request.session and "hod_username" not in request.session and "design_head_username" not in request.session and "quality_head_username" not in request.session and "finance_head_username" not in request.session:
        return redirect("login")
    vendors = VendorPersonalDetails.objects.all()
    return render(request, "vendor.html", {'vendors': vendors})

# Check if username exists (AJAX)
def check_username(request):
    username = request.GET.get('username', '')
    exists = VendorPersonalDetails.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

# Static Page Views
def about(request): return render(request, "about.html")
def login(request): return render(request, "login.html")
def rfq(request): return render(request, "RFQ.html")
def rfq2(request): return render(request, "RFQ2.html")
def rfq3(request): return render(request, "RFQ3.html")
def otp(request): return render(request, "otp.html")
def company(request): return render(request, "company.html")
def service(request): return HttpResponse("This is service page")
def contact(request): return render(request, "contact.html")
def ACGL(request): return render(request, "ACGL_logo.jpg")
def user(request): return render(request, "user.html")
def po(request): return render(request, "po.html")
def annexure(request): return render(request, "annexure.html")

# File Download View
def download_file(request, file_field, vendor_id):
    vendor = VendorPersonalDetails.objects.get(pk=vendor_id)
    file = getattr(vendor, file_field)
    if file:
        response = HttpResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file.name}"'
        return response
    else:
        messages.error(request, "File not found.")
        return redirect("dashboard")


# Submit Requirement Form
def submit_requirement(request):
    if request.method == 'POST':
        requested_by = request.POST.get('requested_by')
        date = request.POST.get('date')

        # Get lists of requirements
        departments = request.POST.getlist('department[]')
        priorities = request.POST.getlist('priority[]')
        item_descriptions = request.POST.getlist('item_description[]')
        justifications = request.POST.getlist('justification[]')
        estimated_costs = request.POST.getlist('estimated_cost[]')
        quotation_deadlines = request.POST.getlist('quotation_deadline[]')
        quantities = request.POST.getlist('quantity[]')
        durations = request.POST.getlist('duration[]')

        # Iterate through each set of requirement fields
        for i in range(len(departments)):
            requirement = Requirement(
                requested_by=requested_by,
                date=date,
                department=departments[i],
                priority=priorities[i],
                item_description=item_descriptions[i],
                justification=justifications[i],
                estimated_cost=estimated_costs[i],
                quotation_deadline=quotation_deadlines[i],
                quantity=quantities[i] if quantities[i] else None,
                duration=durations[i] if durations[i] else None,
                status='Pending',
                next_approver='CFO'
            )
            requirement.save()

        messages.success(request, "Requirements submitted successfully!")
        return redirect("annexure")

    return render(request, 'annexure.html')

# CFO Review Requirements List
def cfo_review_list(request):
    if "cfo_username" not in request.session:
        return redirect("login")
    requirements = Requirement.objects.filter(next_approver='CFO')
    return render(request, 'cfo_review.html', {'requirements': requirements})

def cfo_review(request, requirement_id):
    if "cfo_username" not in request.session:
        return redirect("login")
    requirement = get_object_or_404(Requirement, id=requirement_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            requirement.status = 'Approved by CFO'
            requirement.next_approver = 'CEO'
        elif action == 'reject':
            requirement.status = 'Rejected by CFO'
            requirement.next_approver = None
        elif action == 'modify':
            modification_description = request.POST.get('modification_description')
            requirement.status = 'Modification Required'
            requirement.next_approver = 'Admin'
            requirement.modification_description = modification_description
        requirement.save()

        messages.success(request, "Requirement updated successfully!")
        return redirect("cfo_review_list")

    return render(request, 'cfo_review_detail.html', {'requirement': requirement})

# CEO Review Requirements List
def ceo_review_list(request):
    if "ceo_username" not in request.session:
        return redirect("login")
    requirements = Requirement.objects.filter(next_approver='CEO', status='Approved by CFO')
    return render(request, 'ceo_review.html', {'requirements': requirements})

def ceo_review(request, requirement_id):
    if "ceo_username" not in request.session:
        return redirect("login")
    requirement = get_object_or_404(Requirement, id=requirement_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            requirement.status = 'Approved by CEO'
            requirement.next_approver = None
        elif action == 'reject':
            requirement.status = 'Rejected by CEO'
            requirement.next_approver = None
        elif action == 'modify':
            modification_description = request.POST.get('modification_description')
            requirement.status = 'Modification Required'
            requirement.next_approver = 'Admin'
            requirement.modification_description = modification_description
        requirement.save()

        messages.success(request, "Requirement updated successfully!")
        return redirect("ceo_review_list")

    return render(request, "ceo_review_detail.html", {'requirement': requirement})
def generate_pdf(request, requirement_id):
    # Fetch the requirement
    requirement = get_object_or_404(Requirement, id=requirement_id)

    # Create a PDF response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="Requirement_{requirement_id}.pdf"'

    # Create the PDF document
    pdf = canvas.Canvas(response)
    pdf.setTitle(f"Requirement_{requirement_id}")

    # Write content to PDF
    pdf.drawString(100, 800, f"Requirement ID: {requirement.id}")
    pdf.drawString(100, 780, f"Requested By: {requirement.requested_by}")
    pdf.drawString(100, 760, f"Department: {requirement.department}")
    pdf.drawString(100, 740, f"Priority: {requirement.priority}")
    pdf.drawString(100, 720, f"Item Description: {requirement.item_description}")
    pdf.drawString(100, 700, f"Justification: {requirement.justification}")
    pdf.drawString(100, 680, f"Status: {requirement.status}")
    pdf.drawString(100, 660, f"Next Approver: {requirement.next_approver}")
    pdf.drawString(100, 640, f"Modification Description: {requirement.modification_description or 'N/A'}")
    pdf.drawString(100, 620, f"Delivery Address: {requirement.delivery_address or 'N/A'}")  # New field

    # Save and close PDF
    pdf.showPage()
    pdf.save()

    return response

def update_delivery_address(request, requirement_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            delivery_address = data.get("delivery_address", "").strip()
            
            if not delivery_address:
                return JsonResponse({"success": False, "message": "Invalid Address"}, status=400)

            # Get the requirement object
            requirement = get_object_or_404(Requirement, id=requirement_id)
            requirement.delivery_address = delivery_address  # Assuming `delivery_address` is a field
            requirement.save()

            return JsonResponse({"success": True, "message": "Delivery Address Updated"})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)