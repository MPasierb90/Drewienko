from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.dispatch import receiver
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, FormView, DetailView, TemplateView, UpdateView
from .forms import SignUpForm, UserEditForm, UserProfileEditForm
from .models import User, UserProfile


class UserEditView(FormView):
    template_name = "portal_v1/user_profile_edit.html"
    form_class = UserEditForm


class UserProfileEditView(FormView):
    template_name = "portal_v1/user_profile_edit.html"
    form_class = UserProfileEditForm


class UserProfileView(DetailView):
    model = User
    template_name = "portal_v1/user_profile.html"
    context_object_name = "user_profile"


class UserProfileEdit(TemplateView, LoginRequiredMixin):
    template_name = "portal_v1/user_profile_edit.html"
    success_url = "edit-user-profile"

    def get(self, request, *args, **kwargs):
        user_change = UserEditForm(self.request.GET or None)
        user_profile_edit = UserProfileEditForm(self.request.GET or None)
        context = self.get_context_data(**kwargs)
        context['user_change'] = user_change
        context['user_profile_edit'] = user_profile_edit
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user_change = UserEditView.form_class(request.POST)
        user_profile_edit = UserProfileEditView.form_class(request.POST)
        if user_profile_edit.is_valid() and user_change.is_valid():
            user_change.save()
            user_profile_edit.save()
            return redirect('user-profile')
        else:
            return redirect('edit-user-profile')


class ChangePassword(FormView, LoginRequiredMixin):
    template_name = "portal_v1/password_change.html"
    form_class = PasswordChangeForm

    def get_form(self):
        if self.request.POST:
            return self.form_class(self.request.user, self.request.POST)
        return self.form_class(self.request.user)

    def form_valid(self, form):
        messages.success(request=self.request, message="Hasło zmienione prawidłowo")
        form.save()
        return redirect(reverse('login'))

    def get_success_url(self) -> str:
        return reverse("user-profile")


class RegisterView(CreateView):
    template_name = "portal_v1/register.html"
    form_class = SignUpForm

    def form_valid(self, form):
        messages.success(self.request, "Użytkownik zarejestrowany. Możesz się zalogować.")
        return super(RegisterView, self).form_valid(form)

    def get_success_url(self) -> str:
        return reverse("login")


class LoginView(View):
    template_name = "portal_v1/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("announcement-home")
        return render(request, self.template_name, {})

    def post(self, request):
        username: str = request.POST.get("username")
        password: str = request.POST.get("password")

        user: User or None = authenticate(username=username,
                                          password=password)

        if user:
            login(request, user)
            return redirect("announcement-home")

        messages.error(request, "Zła nazwa użytkownika lub hasło")
        return redirect("login")


def logout_view(request):
    logout(request)
    return redirect("announcement-home")


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, 'Wylogowano pomyślnie')


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, 'Zalogowano pomyślnie')

# @receiver(user_login_failed)
# def on_user_login_failed(sender, request, **kwargs):
#     messages.add_message(request, messages.INFO, 'Błędna nazwa użytkownika lub hasło')
