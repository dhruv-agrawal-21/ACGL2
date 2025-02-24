import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout as auth_logout
from .models import VendorPersonalDetails, VendorBankAndDocuments, AdminUser, CFOUser, CEOUser, HODUser, DesignHeadUser, QualityHeadUser, FinanceHeadUser, Requirement,RFQResponse
from .forms import VendorPersonalDetailsForm
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt


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
                request.session["username"] = vendor.username
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
    vendors = VendorPersonalDetails.objects.select_related('bank_and_docs').all()
    return render(request, "vendor.html", {'vendors': vendors})
def vendor1(request):
    if "admin_username" not in request.session and "cfo_username" not in request.session and "ceo_username" not in request.session and "hod_username" not in request.session and "design_head_username" not in request.session and "quality_head_username" not in request.session and "finance_head_username" not in request.session:
        return redirect("login")
    vendors = VendorBankAndDocuments.objects.all()
    return render(request, "vendor1.html", {'vendors': vendors})
def rfq2(request):
    if "admin_username" not in request.session and "cfo_username" not in request.session and "ceo_username" not in request.session and "hod_username" not in request.session and "design_head_username" not in request.session and "quality_head_username" not in request.session and "finance_head_username" not in request.session:
        return redirect("login")
    vendors = RFQResponse.objects.select_related('vendor_code').all()
    return render(request, "RFQ2.html", {'vendors': vendors})
def rfq(request):
    if "admin_username" not in request.session and "cfo_username" not in request.session and "ceo_username" not in request.session and "hod_username" not in request.session and "design_head_username" not in request.session and "quality_head_username" not in request.session and "finance_head_username" not in request.session:
        return redirect("login")
    vendors = RFQResponse.objects.select_related('vendor_code').all()
    return render(request, "RFQ.html", {'vendors': vendors})

# Check if username exists (AJAX)
def check_username(request):
    username = request.GET.get('username', '')
    exists = VendorPersonalDetails.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

# Static Page Views
def about(request): return render(request, "about.html")
def login(request): return render(request, "login.html")
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

def submit_requirement(request):
    if request.method == 'POST':
        requested_by = request.POST.get('requested_by')

        # Get lists of requirements
        departments = request.POST.getlist('department[]')
        priorities = request.POST.getlist('priority[]')
        item_descriptions = request.POST.getlist('item_description[]')
        justifications = request.POST.getlist('justification[]')
        estimated_costs = request.POST.getlist('estimated_cost[]')
        quotation_deadlines = request.POST.getlist('quotation_deadline[]')
        quantities = request.POST.getlist('quantity[]')
        durations = request.POST.getlist('duration[]')

        for i in range(len(departments)):
            requirement = Requirement(
                requested_by=requested_by,
                department=departments[i],
                priority=priorities[i],
                item_description=item_descriptions[i],
                justification=justifications[i],
                estimated_cost=estimated_costs[i] if estimated_costs[i] else None,
                quotation_deadline=quotation_deadlines[i] if quotation_deadlines[i] else None,
                quantity=int(quantities[i]) if quantities[i].isdigit() else None,
                duration=durations[i] if durations[i] else None,
                status='Pending',
                next_approver='CFO'
            )
            requirement.save()  # Ensures RFQ No is generated
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
    # Create PDF response
    requirement = get_object_or_404(Requirement, id=requirement_id)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="RFQ.pdf"'

    # Initialize PDF canvas
    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    total_pages = 3

    # Header & Footer function
    def draw_header(pdf, page_number, total_pages):
        pdf.setFont("Helvetica", 9)
        pdf.drawString(500, height - 30, f"Page: {page_number}/{total_pages}")  # Ensure it's at the top

    def draw_footer(pdf):
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(50, 30, "Regd Off: Ahura Centre, B-Wing, 2nd Floor, Mahakali Caves Road, Andheri(E), Mumbai-400093.")  # Ensure it's at the bottom
        
    
    # **Step 1: Draw Header First**
    draw_header(pdf, 1, 3)
    
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 60, "RFQ REQUEST (Domestic PO)")

    # **Left Side Content**
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 90, "Company:")
    pdf.drawString(150, height - 90, "Company Name")  # Placeholder
    pdf.drawString(50, height - 110, "Phone:")
    pdf.drawString(150, height - 110, ":")
    pdf.drawString(50, height - 130, "Email:")
    pdf.drawString(150, height - 130, "supportforacgl@gmail.com")
    pdf.drawString(50, height - 150, "Document Date:")
    pdf.drawString(150, height - 150, datetime.today().strftime('%d-%m-%Y'))
    pdf.drawString(50, height - 170, "Validity Period:")
    pdf.drawString(150, height - 170, "Quotation Deadline")

    # **Right Side Content**
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(400, height - 90, "ZENCON INFOTECH PRIVATE LIMITED")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(400, height - 110, "Pune - 411001 INDIA")

    # **Step 2: Add Message Before Table**
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 210, "We request you to provide a quotation for the following materials/services as per the terms,")
    pdf.drawString(50, height - 225, "conditions, and instructions specified below. Kindly share your best offer, including pricing,")
    pdf.drawString(50, height - 240, "delivery schedule, and other relevant details.")
    pdf.drawString(50, height - 255, "AT website_name")
    pdf.drawString(50, height - 270, "Looking forward to your prompt response.")
    if requirement.quantity:
        quantity_or_duration = requirement.quantity  # Use quantity if available
    elif requirement.duration:
        quantity_or_duration = requirement.duration  # Use duration if quantity is missing
    else:
        quantity_or_duration = "N/A"  # Default to "N/A" if both are missing
    # **Step 3: Table for Item Details**
    table_data = [
        ["Item Description", "Material Code", "Quantity", "UOM"],  # Header row
        [requirement.item_description, "", quantity_or_duration, ""]  # Data row
    ]

    table = Table(table_data, colWidths=[200, 100, 100, 100])

    # Table Styling
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Draw the table at a specific position
    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 50, height - 330)  # Adjust position
    # **Step 4: Terms & Conditions (Left Side)**
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, height - 390, "TERMS & CONDITIONS")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 410, "• Central GST: %")
    pdf.drawString(50, height - 425, "• Freight:")
    pdf.drawString(50, height - 440, "• Packing & Forwarding: NIL")
    pdf.drawString(50, height - 455, "• Handling Charges: NIL")
    pdf.drawString(50, height - 470, "• Incoterms: /")
    pdf.drawString(50, height - 485, "• Dispatch Mode:")
    pdf.drawString(50, height - 500, f"• Delivery Address: {requirement.delivery_address or 'N/A'}")
    pdf.drawString(50, height - 515, f"• Delivery Period: {requirement.quotation_deadline.strftime('%d-%m-%Y') if requirement.quotation_deadline else 'N/A'}")
    pdf.drawString(50, height - 530, "• Insurance:")
    pdf.drawString(50, height - 545, "• Payment Terms: Payable immediately Due net")


    # Footer for Page 1
    draw_footer(pdf)
    
    # Save current page
    pdf.showPage()
    
    # **Page 2**
    draw_header(pdf, 2,3)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 60, "ORDER Request:")
    pdf.drawString(50, height - 80, "You need below. Your quotation should include pricing, delivery schedule, applicable taxes, and other relevant details.")

    pdf.drawString(50, height - 110, "Order Acknowledgment:")
    pdf.drawString(50, height - 130, "You are required to confirm the submission of this RFQ within 7 working days from the date of issue by submitting form on the website")
    

    pdf.drawString(50, height - 170, "Accident/Damages Compensation:")
    pdf.drawString(50, height - 190, "In case of an accident involving the supplier’s vehicle due to negligence or otherwise—either by the supplier's employee or any")
    pdf.drawString(50, height - 205, "engaged workforce—the supplier shall bear all costs incurred by company_name for such incidents. company_name")
    pdf.drawString(50, height - 220, "reserves the right to claim damages from the supplier.")

    pdf.drawString(50, height - 250, "Product Harmful Effects:")
    pdf.drawString(50, height - 270, "Along with your quotation, kindly provide information on any harmful effects of the product being supplied, including its impact")
    pdf.drawString(50, height - 285, "on the environment and safety measures during handling.")

    pdf.drawString(50, height - 310, "Goods and Services Tax (GST):")
    pdf.drawString(50, height - 330, "1. The Tax Invoice must be raised in the format prescribed under GST laws along with the necessary documentation for the")
    pdf.drawString(50, height - 345, "   movement of goods.")
    pdf.drawString(50, height - 360, "2. The supplier must timely upload all required transaction data in GSTR-1 and GSTR-3.")
    pdf.drawString(50, height - 375, "3. If GST is payable under reverse charge by company_name, it should be clearly mentioned on the invoice.")
    pdf.drawString(50, height - 390, "4. In case of advance payment, the supplier shall raise the necessary documents and ensure compliance with GST laws.")
    pdf.drawString(50, height - 405, "5. Any loss to company_name due to non-compliance (e.g., incorrect declaration, failure/delay in tax deposit or")
    pdf.drawString(50, height - 420, "   transaction upload, confiscation of goods due to improper documentation) will be recovered from the supplier along with")
    pdf.drawString(50, height - 435, "   any applicable interest/penalty.")
    pdf.drawString(50, height - 450, "6. ACGL will deduct tax at source (TDS) as per GST regulations wherever applicable.")

    pdf.drawString(50, height - 480, "Tax Collection at Source (TCS) Compliance:")
    pdf.drawString(50, height - 500, "As per Section 194Q of the Income Tax Act, 1961, company_name will deduct TDS on payments made towards the purchase")
    pdf.drawString(50, height - 515, "of goods in applicable situations.")

    pdf.drawString(50, height - 530, "• ACGL will not pay TCS under Section 206C(1H) if TDS is deducted under Section 194Q.")
    pdf.drawString(50, height - 545, "• If TCS is collected by the supplier, they must provide a valid TCS certificate as per IT Act provisions.")
    pdf.drawString(50, height - 560, "• Any loss due to incorrect TCS return filing by the supplier will be recovered.")

    # Footer for Page 2
    draw_footer(pdf)
    pdf.showPage()

    # **Page 3**
    draw_header(pdf, 3, 3)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 60, "Additionally, per Sections 206AB/206CCA, if the supplier has not filed income tax returns for the last two assessment years and the")
    pdf.drawString(50, height - 75, "TDS/TCS exceeds 50,000 per year, a higher tax rate will apply. The supplier must provide a declaration of compliance with these")
    pdf.drawString(50, height - 90, "provisions.")

    pdf.drawString(50, height - 120, "Test Certificates:")
    pdf.drawString(50, height - 140, "The supplier must ensure that all supplied materials are accompanied by relevant test certificates; failure to do so may lead to")
    pdf.drawString(50, height - 155, "rejection of materials.")

    pdf.drawString(50, height - 180, "Confidentiality Terms:")
    pdf.drawString(50, height - 200, "1. Any confidential information shared with the supplier (including documents, drawings, models, designs, specifications, or")
    pdf.drawString(50, height - 215, "   pricing details) must be kept strictly confidential.")
    pdf.drawString(50, height - 230, "2. The supplier shall not disclose such information to any third party without prior written consent from company_name.")
    pdf.drawString(50, height - 245, "3. The confidentiality obligation survives even after the RFQ process or contract termination.")
    pdf.drawString(50, height - 260, "4. Any violation may result in legal action and compensation claims.")

    pdf.drawString(50, height - 290, "Quotation Submission:")
    pdf.drawString(50, height - 310, "Please submit your quotation at the earliest, including all technical and commercial details.")

    pdf.drawString(50, height - 340, "ACGL")

    # Footer for Page 3
    draw_footer(pdf)
    pdf.showPage()

    # Finalize PDF
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

def submit_rfq(request):
    if request.method == "POST":
        # Get the logged-in user's username from the session
        username = request.session.get("username")
        if not username:
            return render(request, "RFQ3.html", {"error": "User not logged in"})

        try:
            # Retrieve the vendor_id from VendorPersonalDetails using the username
            vendor_personal_details = VendorPersonalDetails.objects.get(username=username)
            vendor_id = vendor_personal_details.vendor_id

            # Retrieve the vendor_code from VendorBankAndDocuments using the vendor_id
            vendor_bank_details = VendorBankAndDocuments.objects.get(vendor_id=vendor_id)
            vendor_code = vendor_bank_details.vendor_code

            # Retrieve other form data
            rfq_number = request.POST.get("rfq_number")
            response_deadline = request.POST.get("response_deadline")
            company_name = request.POST.get("company_name")
            contact_person = request.POST.get("contact_person")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            address = request.POST.get("address")

            item_numbers = request.POST.getlist("item_number[]")
            descriptions = request.POST.getlist("description[]")
            specifications = request.POST.getlist("specification[]")
            per_unit_prices = request.POST.getlist("per_unit_price[]")
            quantities = request.POST.getlist("quantity[]")
            total_prices = request.POST.getlist("total_price[]")
            gst_values = request.POST.getlist("gst[]")
            gst_amounts = request.POST.getlist("gst_amount[]")
            total_amounts = request.POST.getlist("total_amount[]")
            attachments = request.FILES.getlist("attachments[]")

            # Loop through all items and create RFQResponse objects
            for i in range(len(item_numbers)):
                RFQResponse.objects.create(
                    rfq_number=rfq_number,
                    response_deadline=response_deadline,
                    vendor_code=vendor_bank_details,  # Use the vendor_code object
                    company_name=company_name,
                    contact_person=contact_person,
                    phone=phone,
                    email=email,
                    address=address,
                    item_number=item_numbers[i],
                    description=descriptions[i],
                    specification=specifications[i],
                    per_unit_price=per_unit_prices[i],
                    quantity=quantities[i],
                    total_price=total_prices[i],
                    gst=gst_values[i],
                    gst_amount=gst_amounts[i],
                    total_amount=total_amounts[i],
                    attachment=attachments[i] if i < len(attachments) else None
                )

            return redirect("dashboard")  # Redirect to a success page

        except VendorPersonalDetails.DoesNotExist:
            return render(request, "RFQ3.html", {"error": "Vendor details not found"})
        except VendorBankAndDocuments.DoesNotExist:
            return render(request, "RFQ3.html", {"error": "Vendor bank details not found"})
        except IntegrityError as e:
            return render(request, "RFQ3.html", {"error": f"Database error: {str(e)}"})

    return render(request, "RFQ3.html")

@csrf_exempt
def send_to_another_page(request):
    if request.method == 'POST':
        selected_rfqs = request.POST.getlist('rfqs')  # Get selected RFQs
        # Logic to move RFQs to another page
        # Example: Update a field in the model or move to another table
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@csrf_exempt
def delete_rfqs(request):
    if request.method == 'POST':
        selected_rfqs = request.POST.getlist('rfqs')  # Get selected RFQs
        # Logic to delete RFQs
        RFQResponse.objects.filter(rfq_number__in=selected_rfqs).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})