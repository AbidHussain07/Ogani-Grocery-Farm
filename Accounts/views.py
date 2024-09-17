from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

# Create your views here.

# def registration(request):
#     if request.method == "POST":
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         user = User.objects.filter(username = username)
#         if user.exists():
#             messages.info(request , "Username Already Taken Please Choose Another")
#             return redirect('/register/')
        
#         user = User.objects.filter(email = email)
#         if user.exists():
#             messages.info(request , "This Email-Id is already Registered.")
#             return redirect('/register/')
        
#         user = User.objects.create(
#             first_name=first_name,
#             last_name=last_name,
#             username=username,
#             email = email
#         )
#         user.set_password(password)
#         user.save()
#         messages.success(request , "Account Created Successfully!!!")
#         return redirect('/register/')
        
#     return render(request , 'authenticate/register.html')

# def login_page(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         if not User.objects.filter(username = username).exists():
#             messages.warning(request , "Invalid Username")
#             return redirect('/login/')
        
#         user = authenticate(username = username , password = password)
#         if user is None:
#             messages.warning(request , "Invalid Password")
#             return redirect('/login/')
        
#         else:
#             login(request , user)
#             return redirect('/')
            
#     return render(request , 'login.html')

# def logout_page(request):
#     logout(request)
#     return redirect('/login/')

# ====================================================================================================================================
from Accounts.forms import UserRegisterForm
from Accounts.models import User


def register_view(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request , f"Hey! {username} , Your Account has been created Successfully.")
            
            # # Send confirmation email
            # subject = "Welcome to Ogani Fresh Farm!"
            # message = f"""
            # Dear {username},

            # Thank you for registering with Ogani Fresh Farm!

            # Your account has been successfully created. You can now log in using your credentials.

            # If you have any questions or need assistance, feel free to contact us.

            # Best regards,
            # By Ogani Fresh Farm Team
            # """
            # from_email = settings.EMAIL_HOST_USER
            # recipient_list = [request.user.email]
            # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            # new_user = authenticate(username = form.cleaned_data['email'],
            #                         password = form.cleaned_data['password1'])
    
            return redirect('/user/login/')
    else:
        form = UserRegisterForm()
        
    context = {'form' : form}
    return render(request , 'authenticate/register.html' , context)

def login_view(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email = email)
            user = authenticate(request , email=email , password=password)
        
            if user is not None:
                login(request , user)
                messages.success(request , "You are Logged In.")
                return redirect("/")
            else:
                messages.warning(request , "Invalid Email or Password.")
                
        except:
            messages.warning(request , f"User with this {email} email doesn't exists.")
            
    return render(request , 'authenticate/login.html' )

def logout_view(request):
    logout(request)
    messages.success(request , "You are Logged Out !")
    return  redirect('/user/login/')

