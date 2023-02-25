from django.shortcuts import redirect, render
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from django.contrib.auth.models import User
# from django.contrib.sites.shortcuts import get_current_site
# from . token import user_tokenizer_generate
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.core.mail import EmailMessage
from django.contrib.auth.models import auth
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Welcome to GMW store! You are registered"
            )
            return redirect('dashboard')

            # # email verification setup
            # current_site = get_current_site(request)
            # subject = 'Account verification email'
            # message = render_to_string('profiles/registration/email-verification.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': user_tokenizer_generate.make_token(user),
            # })

            # user.email_user(subject=subject, message=message)

            # return redirect('email-verification-sent')

    context = {'form': form}
    return render(request, 'profiles/registration/register.html', context=context)


# def email_verification(request, uidb64, token):
#     unique_id = force_text(urlsafe_base64_decode(uidb64))
#     user = User.objects.get(pk=unique_id)

    # Verification success
    # if user and user_tokenizer_generate.check_token(user, token):
    #     user.is_active = True
    #     user.save()

    #     return redirect('email-verification-success')

    # # Verification failed
    # else:
    #     return redirect('email-verification-failed')


# def email_verification_sent(request):
#     return render(request, 'profiles/registration/email-verification-sent.html')


# def email_verification_success(request):
#     return render(request, 'profiles/registration/email-verification-success.html')


# def email_verification_failed(request):
#     return render(request, 'profiles/registration/email-verification-failed.html')


def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    context = {'form': form}
    return render(request, 'profiles/my-login.html', context=context)


def user_logout(request):
    try:
        for key in list(request.session.keys()):
            if key == 'session_key':
                continue
            else:
                del request.session[key]
    except KeyError:
        pass
    messages.success(request, "You have logged out successfully")
    return redirect('store')


@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'profiles/dashboard.html')


@login_required(login_url='my-login')
def profile_management(request):
    # Update username and email
    user_form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "You account have been updated")
            return redirect('dashboard')

    context = {'user_form': user_form}
    return render(request, 'profiles/profile-management.html', context=context)


@login_required(login_url='my-login')
def profile_delete(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Account deleted successfully")
        return redirect('store')
    return render(request, 'profiles/profile-delete.html')