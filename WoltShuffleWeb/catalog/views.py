from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from .actions import return_random_dish
from .actions import hash_dish_name
import environ
import hashlib

env = environ.Env()
environ.Env.read_env()


def home(request):
    context = {}
    return render(request, 'home.html', context=context)


def about_view(request):
    context = {}
    return render(request, 'about.html', context=context)


def shuffle_view(request, hashed_dish):
    context = {}

    if request.user.is_authenticated:

        if hashed_dish != 'base':
            if request.user.unwanted_dishes is None:
                request.user.unwanted_dishes = {hashed_dish}
            else:
                request.user.unwanted_dishes.add(hashed_dish)
            request.user.save()

        lat = request.user.latitude
        long = request.user.longitude

        set_of_unwanted_dishes = request.user.unwanted_dishes
        dish = return_random_dish(lat, long, set_of_unwanted_dishes, request.user.username)
        # if user has no available dishes around him
        if dish is None:
            return render(request, 'no_dishes.html', context)
        if dish is env("CLOSED_VENUES"):
            return render(request, 'no_venues_open.html', context)
        if dish is env("BROKEN_API"):
            return render(request, 'something_went_wrong.html', context)

        context['dish_name'] = dish.name
        context['restaurant'] = dish.restaurant
        context['description'] = dish.description
        context['price'] = dish.price
        context['img'] = dish.img
        context['restaurant_url'] = dish.restaurant_url
        context['hashed_dish'] = \
            hash_dish_name(dish.restaurant, dish.name)  # this is for if user preses NEVER AGAIN

        request.POST = request.POST.copy()
        request.POST['hashed_dish'] = hashed_dish  # this is for url creation from request
        return render(request, 'shuffle.html', context)

    else:
        return redirect("login")


def registration_view(request):
    context = {}
    if request.user.is_authenticated: return redirect("home")
    if request.POST:  # user is sending form data
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('home')
        else:  # user sent invalid data
            context['registration_form'] = form
    else:  # user is sending GET, meaning he wants the form itself:
        form = RegistrationForm(initial={
            "email": "",
            "username": "",
            "address": "",
        })
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
                "address": request.POST['address'],
                "longitude": request.POST['longitude'],
                "latitude": request.POST['latitude']
            }
            form.save()
            messages.success(request, 'Account details updated.')
            context['success_message'] = 'Updated'
    else:  # user sent GET request, so we shall present the form, pre-filled with user's current data
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
                "address": request.user.address,
                "longitude": request.user.longitude,
                "latitude": request.user.latitude
            }
        )

    context['account_form'] = form

    return render(request, "account.html", context)
