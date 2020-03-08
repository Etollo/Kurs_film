from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import ungettext_lazy as _

from account.forms import CustomUserAuthenticationForm, UserUpdateForm


def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('dashboard_url')

    if request.POST:
        form = CustomUserAuthenticationForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("dashboard_url")
    else:
        form = CustomUserAuthenticationForm()

    context['login_form'] = form

    return render(request, 'account/login.html', context)


@login_required
def update_user_view(request):
    context = {}
    print(request.FILES)
    if request.POST:
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            context['success_message'] = _('User data was updated successfully')

    else:
        form = UserUpdateForm(
            initial={
                "email": request.user.email,
                # "username": request.user.username,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "birthday": request.user.birthday,
                "gender": request.user.gender,
                "job_title": request.user.job_title,
                "phone": request.user.phone,
                "email_notify": request.user.email_notify,
                "user_language": request.user.user_language,
                "photos": request.user.photo,
            }
        )

    context['user_form'] = form
    return render(request, 'account/user_profile.html', context)