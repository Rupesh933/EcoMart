from django.http import HttpResponse
from apps.accounts.models import Account
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

from .forms import RegisterationForm

# verification email imports (kept for future use when SMTP is configured)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator


def register(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)

        if form.is_valid():
            first_name    = form.cleaned_data['first_name']
            last_name     = form.cleaned_data['last_name']
            phone_number  = form.cleaned_data['phone_number']
            email         = form.cleaned_data['email']
            password      = form.cleaned_data['password']

            # Generate a unique username from the email prefix
            base_username = email.split('@')[0]
            username = base_username
            counter = 1
            while Account.objects.filter(username=username).exists():
                username = f'{base_username}{counter}'
                counter += 1

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                phone_number=phone_number,
            )
            # Account is active immediately — no email verification needed in dev
            user.is_active = True
            user.save()

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = RegisterationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def signin(request):
    """Login view (named 'signin' to avoid shadowing auth.login)."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in successfully!')
            # Respect 'next' parameter if present
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def signout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid  = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid or expired activation link.')
        return HttpResponse('Activation failed.')


def forgotPassword(request):
    return render(request, 'accounts/forgotPassword.html')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
