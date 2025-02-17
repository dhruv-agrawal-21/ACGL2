from django.shortcuts import render, HttpResponse
from datetime import datetime
from acgl.models import VendorDetails
from acgl.models import UploadDocuments
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.
def index(request):
    # Here we will fetch data from our databse and send it in form of variables
    context={
        "variable1":"Jay Shree Krishna"
    }
    return render(request,'index.html',context)
def login_details(request):
        if request.method=='POST':
            username1=request.POST.get('username1')
            password1=request.POST.get('password1')
            try:
                vendor = VendorDetails.objects.get(username=username1)
            except VendorDetails.DoesNotExist:
                messages.error(request,"Username does not exist.Create a new account")
                return render(request,"login.html")
            
            if vendor.password != password1:
                messages.error(request, "Incorrect password. Try again.")
                return render(request, "login.html")

            request.session["vendor_id"] = vendor.id  # Store vendor ID in session
            return render(request, "dashboard.html", {"message": "Login successful"})#ld=logindetails(username1=username1,password1=password1)
            #ld.save()
            #return render(request,"index.html",{"message":"Successfully sign in",})
        return render(request,"index.html")
def upload_documents(request):
        if request.method=='POST':
            aadhar_doc = request.FILES.get('aadhar-doc')
            gst_doc = request.FILES.get('gst-doc')
            bank_details = request.POST.get('bank_details')
            uploaddocuments=UploadDocuments(aadhar_doc=aadhar_doc,bank_details=bank_details,gst_doc=gst_doc)
            uploaddocuments.save()
            return render(request,"index.html",{"message":"Data saved sucessfully!", })
        return render(request,'account2.html')
def save_vendor_details(request):
        if request.method == 'POST':
            fullname =request.POST.get('fullname')
            vendorname =request.POST.get('vendorname')
            username =request.POST.get('username')
            password =request.POST.get('password')
            address =request.POST.get('address')
            phonenumber =request.POST.get('phonenumber')
            email =request.POST.get('email')
            dob =request.POST.get('dob')
            igst =request.POST.get('igst')
            vendordetails=VendorDetails(fullname=fullname,vendorname=vendorname,username=username,password=password,address=address,phonenumber=phonenumber,email=email,dob=dob,igst=igst)
            vendordetails.save()
            return render(request,"account2.html",{"message":"Data saved sucessfully!", })
        return render(request,'account.html')
    # return HttpResponse("This is about page")
def about(request):
    return render(request,"about.html")
def login(request):
    return render(request,"login.html")
def account(request):
    return render(request,"account.html")
def rfq(request):
    return render(request,"RFQ.html")
def rfq2(request):
    return render(request,"RFQ2.html")
def otp(request):
    return render(request,"otp.html")
def company(request):
    return render(request,"company.html")
def service(request):
    return HttpResponse("This is service page")
def contact(request):
    return render(request,"contact.html")
def ACGL(request):
    return render(request,"ACGL_logo.jpg")
def account2(request):
    return render(request,"account2.html")
def dashboard(request):
    return render(request,"dashboard.html")
def user(request):
    return render(request,"user.html")
def check_username(request):
    username = request.GET.get('username', '')
    exists = VendorDetails.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

