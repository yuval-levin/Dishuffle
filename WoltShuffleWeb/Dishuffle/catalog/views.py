from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm


# Create your views here.
def home(request):
    """View function for home page of site."""

    context = {}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'home.html', context=context)

def registration_view(request):
    context = {}
    if request.POST:  # user is sending form data
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('home')
        else:  # user sent invalid data
            context['registration_form'] = form
    else:  # user is sending GET, meaning he wants the form itself:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)


def login_view(request):
    context = {}
    user = request.user
    # if user is already signed in, he has no business in "logim" page
    if user.is_authenticated:
        return redirect("home")
    # if we received a POST request, user just filled the form:
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            # if authentication worked, user will NOT be None
            if user:
                login(request, user)
                return redirect("home")

    else:  # else, we got a GET request, so we'll display the form
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return redirect('home')


def account_view(request):
    # if user is not logged in, he shouldn't be in "account" view
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    # if user filled the form, a POST request will be received
    if request.POST:
        # we send the user so we can access his PK in form
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
                "address": request.POST['address']
            }
            form.save()
            context['success_message'] = "Updated"
    else: # user sent GET request, so we shall present the form, pre-filled with user's current data
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
                "address": request.user.address
            }
        )

    context['account_form'] = form

    return render(request, "account.html", context)
