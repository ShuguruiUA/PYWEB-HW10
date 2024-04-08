from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm
from django.contrib import messages
from django.urls import reverse_lazy


# Create your views here.


class RegisterView(View):
    template_name = 'register.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f'User "{username}" registered successfully')
            return redirect(to="users:signin")
        return render(request, self.template_name, {"form": self.form_class})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "password_reset.html"
    email_template_name = "password_reset_email.html"
    html_email_template_name = "password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = "password_reset_subject.txt"
