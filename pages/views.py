from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from account.forms import RegistrationForm,AccountAuthenticationForm,ProfileUpdateForm
from account.models import DemandeAcces,Etudiant
from django.contrib import messages



def index(request):
    logout(request)
    return render(request , 'pages/index.html')

@user_passes_test(lambda u: u.user_type == 'student', login_url='signin')
@login_required(login_url='signin')
def studentdashbord(request):
	return render(request , 'users/Student/StudentHome.html')


@login_required(login_url='signin')
def studentedit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('studentdashbord')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'users/Student/Profile/profile-edit.html', context)

@user_passes_test(lambda u: u.user_type == 'teacher', login_url='signin')
@login_required(login_url='signin')
def professordashbord(request):
    user = request.user
    demande_acces = DemandeAcces.objects.filter(user=user).first()
    print(demande_acces)
    context = {
        'username': request.user.username,
        'demande_acces': demande_acces,
    }

    return render(request, 'users/Professor/ProfessorHome.html', context)





def about(request):
    return render(request , 'pages/about.html')

def contact(request):
    return render(request , 'pages/contact.html')


def pricing(request):
    return render(request , 'pages/pricing.html')


def signin(request):
    logout(request)
    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin:index')
                elif user.user_type == 'teacher':
                    return redirect('professordashbord')
                elif user.user_type == 'student':
                    return redirect('studentdashbord')
        else:
            context = {'login_form': form, 'message': 'Invalid email or password.'}
            return render(request, 'pages/signin.html', context)
    else:
        form = AccountAuthenticationForm()
    context = {'login_form': form}
    return render(request, 'pages/signin.html', context)



def signup(request):
    logout(request)
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data['user_type']
            user.user_type = user_type
            user.save()

            if user.user_type == 'teacher':
                demande_acces = DemandeAcces.objects.create(user=user, accepte=False)
                demande_acces.save()
                messages.info(request, "Your access request has been submitted. Please wait for admin approval.")
            else:
                etudiant = Etudiant.objects.create(user=user)
                etudiant.username = user.username
                etudiant.email = user.email
                etudiant.save()

            user = authenticate(request, email=user.email, password=form.cleaned_data['password1'])
            login(request, user)

             # Set default profile image for the account
            default_image_url = settings.STATIC_URL + 'assets/images/default/defaultimage.png'
            user.picture = default_image_url
            user.save()


            if user.user_type == 'teacher':
                return redirect('professordashbord')
            else:
                return redirect('studentdashbord')

        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'pages/signup.html', context)



def logout_view(request):
    logout(request)
    return redirect('index')