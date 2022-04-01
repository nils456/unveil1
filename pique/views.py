from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from pique.models import  Content, Downloads, CellNo
from pique.forms import ContentForm, NewUserForm, CellForm, DownloadForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def model_form_upload(request):
    form = ContentForm()
    if request.method == 'POST':
        print("inside if")
        form = ContentForm(request.POST, request.FILES)
        cont = Content()
        if form.is_valid():
            print("is valid")
            user = request.user
            id2 = user.id
            if User.objects.filter(id=id2).exists():
                usr = User.objects.get(id=id2)
                print(usr)
            #    form.usr = usr
            #    print(form.usr)
            #    form.save()
                cont.usr = usr
                print(cont.usr)
                cont.type = request.POST.get('type')
                print(cont.type)
                cont.category = request.POST.get('category')
                cont.keywords = request.POST.get('keywords')
                cont.filename = request.FILES.get('filename')
                cont.downloaded = 0
                cont.save()
                return redirect('home')

    else:
        print("inside else")
        form = ContentForm()
    return render(request, 'upload.html', {'form':form})

def index(request):
    usrlist = User.objects.order_by('emailid')
    my_dict = {'usr_records':usrlist}
    return render(request,'index.html',context=my_dict)

def register(request):

    registered = False
    user_form = NewUserForm()
    cell_form = CellForm()

    if request.method == 'POST':
        print("inside POST")
        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = NewUserForm(data=request.POST)
        cell_form = CellForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and cell_form.is_valid():
            print("inside valid")
            # Save User Form to Database
            user = user_form.save()
            print(user.first_name)
            # Hash the password
            user.set_password(user.password)
            # Update with Hashed password
            user.save()
          #Now we deal with the extra info!
            cell = CellNo()
            usr = User.objects.get(id=user.id)
            cell.usr = usr
            print(cell.usr)
            num = request.POST.get('number')
            print(num)
            cell.number = num
            cell.save()
            # Registration Successful!
            registered = True
            return redirect('home')
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors)
            print(cell_form.errors)
    else:
        print("inside else")# Was not an HTTP post so we just render the forms as blank.
        user_form = NewUserForm()
        cell_form = CellForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'sign_up.html',
                          {'user_form':user_form,
                           'cell_form':cell_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('home'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'login.html', {})

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('home'))
# Create your views here.
def user(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
           form.user_id = form.username
           form.save(commit=True)

           return home(request)
        else:
           print("ERROR FORM INVALID")
    return render(request,'sign_up.html', {'form':form})
def update_download_count(request):
    print("inside update_download_count")

    if request.is_ajax and request.method == "GET":
        print("inside if")
        id1 = request.GET.get("id1", None)
        print(id1)
        form = DownloadForm()
        form.contnt = id1
        if Content.objects.filter(id=id1).exists():
           print("inside exists")
           cont = Content.objects.get(id=id1)
           print(cont)
           dwnld = Downloads()
           cont.update_dwnlds()
           user = request.user
           id2 = user.id
           if User.objects.filter(id=id2).exists():
              usr = User.objects.get(id=id2)
              dwnld.usr = usr
              dwnld.contnt = cont
              dwnld.save()

        #   for cnt in cont:
        #       print("inside for")

        #       form.contnt = cnt
        #       print(form.contnt)
        #       form.usr = request.user
        #       print(form.usr)
        #       dwnld = form
        #       dwnld.save()
              return JsonResponse({"valid":True }, status = 200)
        else:
              print("inside first else")
              return JsonResponse({"valid":False}, status = 200)
    else:
            print("inside final else")
            return JsonResponse({"valid":False}, status = 400)
def home(request):
    if request.method == "POST" :
           print("Inside post")
           print(request)
           category1 =  request.POST.get('category')
           keyword1 = request.POST.get('keywords')
           type1 = request.POST.get('contype')
           print(category1)
           print(keyword1)
           print(type1)
           contentlist = None
           if type1 is not None and type1 != '':
              print("Inside first if")
              contentlist =  Content.objects.filter(type=type1)
              if category1 is not None and category1 != '':
                 print("Inside second if")
                 contentlist =  Content.objects.filter(category=category1, type=type1)
                 if keyword1 is not None and keyword1 != '':
                    print("Inside third if")
                    contentlist =  Content.objects.filter(type=type1, category=category1, keywords__contains=keyword1)
              else:
                 if keyword1 is not None and keyword1 != '':
                    print("Inside first elseif")
                    contentlist =  Content.objects.filter(type=type1, keywords__contains=keyword1)
           else:
               if category1 is not None and category1 != '':
                    print("Inside second elseif")
                    contentlist =  Content.objects.filter(category=category1)
                    if keyword1 is not None and keyword1 != '':
                        print("Inside second elseif if")
                        contentlist =  Content.objects.filter(category=category1, keywords__contains=keyword1)
               else:
                    if keyword1 is not None and keyword1 != '':
                        print("Inside second elseif if elseif")
                        contentlist =  Content.objects.filter(keywords__contains=keyword1)
           if contentlist.exists():
                print(contentlist)

           my_dict = {'content_records':contentlist}
           return render(request,'home.html',context=my_dict)
    else:
         firsttime = True
         my_dict = {'firsttime' : firsttime}
         return render(request,'home.html', context=my_dict)

    # Create your views here.
