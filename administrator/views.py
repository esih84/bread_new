from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login,logout
from .forms import *
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


def Register(request):
    if request.user.is_authenticated:
        return redirect('administrator:create_post')
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password2'])
            user.save()
            return redirect('administrator:login')
    else:
        form = UserCreateForm()
    context = {'form': form}
    return render(request, 'administrator/signup_and _login.html', context)


def Login(request):
    if request.user.is_authenticated:
        return redirect('administrator:create_post')
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("administrator:create_post")
        else:

            return render(request,  'administrator/login.html')
    else:
        return render(request,  'administrator/login.html', {})


@login_required(login_url='/administrator/login/')
def Logout(request):
    logout(request)
    return redirect('administrator:login')


@login_required(login_url='/administrator/login/')
def profile_view(request):
    context = {
        'profile': profile.objects.get(user_id=request.user.user_id),
        'post': buy.objects.filter(user_id=request.user.user_id)

    }
    return render(request, 'administrator/profile.html', context)


@login_required(login_url='/administrator/login/')
def profile_save(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        user_profile = UserProfileUpdate(request.POST, instance=request.user.profile)

        if user_profile.is_valid() or user_form.is_valid():
            user_form.save()
            user_profile.save()
            # messages.success(request, 'Your profile is updated successfully')
            return redirect('administrator:profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        user_profile = UserProfileUpdate(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'user_profile': user_profile,
    }
    return render(request, 'administrator/edit_profile.html', context)




@login_required(login_url='/administrator/login/')
def create_post(requests):
    context = {
        "post": post.objects.all(),
    }
    return render(requests, "administrator/product.html", context)


def Buy(request, id):
    if request.method == 'POST':
        buys = buy_form(request.POST)
        if buys.is_valid():
            data = buys.cleaned_data
            print(data)
            price = get_object_or_404(post, id=id).price
            total_price = price*data['bread_count']
            buy.objects.create(user_id=request.user.user_id, bread_count=data['bread_count'], Total_price=total_price, discount=data['discount'], post_id=id)
            posts =post.objects.get(id=id)
            posts.count = posts.count - data['bread_count']
            posts.save()
            return redirect('administrator:create_post')
    else:
        context = {
            "post": post.objects.get(id=id),
        }
        return render(request,  'administrator/shoping_cart.html', context)



