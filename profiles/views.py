from django.shortcuts import redirect, render
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from . token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            # email verification setup
            current_site = get_current_site(request)
            subject = 'Account verification email'
            message = render_to_string('profiles/registration/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
            })

            user.email_user(subject=subject, message=message)

            return redirect('email-verification-sent')

    context = {'form': form}
    return render(request, 'profiles/registration/register.html', context=context)


def email_verification(request, uidb64, token):
    unique_id = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    # Verification success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect('email-verification-success')

    # Verification failed
    else:
        return redirect('email-verification-failed')


def email_verification_sent(request):
    return render(request, 'profiles/registration/email-verification-sent.html')


def email_verification_success(request):
    return render(request, 'profiles/registration/email-verification-success.html')


def email_verification_failed(request):
    return render(request, 'profiles/registration/email-verification-failed.html')
