

from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from api.models import PhotoModel, UserModel
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render

from django.conf import settings
from django.contrib.auth  import authenticate, login , logout
from django.core.mail import send_mail

import uuid

@csrf_exempt
def Home(request):

    context = {
        "request" : request,        
    }

    user_id = request.COOKIES.get('user_id')

    if user_id:
        profile = UserModel.objects.filter(id=user_id).first()
        
        if profile:
            user = profile.user
            email = user.email
            username = user.username
            login(request,user=user)
        send_login_mail(username=username,email=profile.user.email,date=profile.last_login)
    
        photo_model = PhotoModel.objects.filter(user=profile)

        photos = []

        for p in photo_model:
            photos.append(p.photo)
        
        context['photos'] = photos   

    return render(request,"home.html",context=context)


def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,"login.html")

def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,"register.html")


def VerifyPage(request):

    if request.user.is_authenticated:
        return render(request,"home.html")

    return render(request,"verify.html")


@csrf_exempt
def Register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":

        firstName = request.POST['firstname']
        lastName = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']  
        confirm_password = request.POST['confirm_password']   

        try:
            if password == confirm_password:

                if User.objects.filter(username=username).first():
                    return HttpResponse("User already Registered")
                
                elif User.objects.filter(email=email).first():
                    return HttpResponse("User already Registered")            

                else:
                    user = User.objects.create_user(username=username,email=email)
                    user.set_password(password)
                    user.first_name = firstName
                    user.last_name = lastName                
                    user.save()

                    auth_token = str(uuid.uuid4())
                    
                    profile = UserModel.objects.create(user=user,auth_token=auth_token)
                    profile.save()

                    send_mail_after_registration(email,auth_token,username)


                    return  redirect('verifypage')
            else:
                return HttpResponse("unmatched passwords ")

        except Exception as e:
            return HttpResponse(e)

    else:
        return HttpResponseBadRequest("Bad Request")

@csrf_exempt
def Login(request):

    if request.user.is_authenticated:
        return redirect('home')

    user_id = request.COOKIES.get('user_id')

    if user_id:
        user = User.objects.filter(id=user_id).first()

        if user:
            login(request,user=user)

        return redirect('home')


    if request.method == 'POST':
        username = request.POST['username']
        email = str(request.POST['email'])
        password = str(request.POST['password'])

        user = User.objects.filter(email=email).first()

        if user:

            if(user.check_password(password) and (user.username == username) and (user.email == email)):

                profile = UserModel.objects.filter(user=user).first()

                if profile:
                    if (not profile.is_verified):
                        return HttpResponseBadRequest("User Not Verified")
                        
                
                    authenticate(email=email,password=password)

                    login(request,user=user)

                    

                    send_login_mail(username=username,email=profile.user.email,date=profile.last_login)

                    response =  redirect("home")
                    response.set_cookie("user_id",str(profile.id))

                    return response
                else:
                    return HttpResponse("NO user profile found please register first .")
            else:
                return HttpResponse("invalid credentials")
        else:
            return HttpResponse("user not found")

    else:
        return HttpResponse("re-login please")
    

@csrf_exempt
@login_required
def Logout(request):   

    if request.method == 'POST':
        logout(request)

        response = redirect('home')
        response.delete_cookie("user_id")
             
        return response

    else:
        return HttpResponseBadRequest("bad request .")    


@csrf_exempt
def verify(request,auth_token):

    if request.user.is_authenticated:
        return redirect('home')

    try :
        profile = UserModel.objects.filter(auth_token=auth_token).first()

        if profile:
            profile.is_verified = True
            profile.save()

            response =  HttpResponseRedirect("http://localhost:8000/")              

            login(request,user=profile.user)

            send_registration_mail(email=profile.user.email,username=profile.user.username)

            response.set_cookie('user_id',profile.id)
            return response

        else:
            return HttpResponse("User Not Found,Please Register")

    except Exception as e:
        return HttpResponse(str(e)) 


def send_registration_mail(email,username):
    subject = 'PhotosHub:: Your Account is Registered..'
    message = f'HI , {str(username).upper()}  Your Account is registered now open PhotosHub site to add your photos'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)


def send_mail_after_registration(email,token,username):
    subject = 'PhotosHub:: Your Account needs To Be Verified .'
    message = f' HI , {str(username).upper()} please open the following link to verify your Account => http://localhost:8000/api/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)


def send_login_mail(username,email,date):
    subject = f'PhotosHub Login'
    message = f' HI , {str(username).upper()} your account got logged in at {date} .'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)



@csrf_exempt 
@login_required
def Upload(request):   

    if request.user.is_authenticated:
        user = User.objects.filter(username=request.user).first()
        user_model = UserModel.objects.filter(user=user).first()

        if user_model:
            if request.FILES.get("photo"):
                photo = PhotoModel(user=user_model,photo=request.FILES.get('photo'))
                photo.save() 
            else:
                return HttpResponse("invalid photo got .") 
        else:
            return HttpResponse("No user found ")  

        return redirect('home')

    else :
        return HttpResponse("user not found .") 
