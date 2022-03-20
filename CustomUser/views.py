from .models import user
from .forms import CustomUserCreationForm, ModifiedAuthenticationForm, CustomUserDeletionForm, CustomOTPTokenForm, CustomOTPTokenFormChangeEmail

from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import resolve_url, get_object_or_404
from django.urls import reverse_lazy

from django_email_verification import send_email
from django_otp.decorators import otp_required


# Create your views here.



class UserCreate(FormView):
    template_name = 'CustomUser/user_create_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("CustomUser:login")

    def form_valid(self, form):
        """
        The implemetation below is according to the doc. But things 
        don't work unless we manually configure is_active=False during 
        saving the user. I did it inside the "CustomUserCreationForm" 
        by re-defining the save() method.
        """
        user = form.save()
        returnVal = super(UserCreate, self).form_valid(form)
        send_email(user)
        messages.success(self.request, 'Congratulations! Your account has been created. Please click on the link we have sent to your email address to ACTIVATE your account. Once activated, you can log into your account.')
        return returnVal



class UserLogin(LoginView):
    template_name = 'CustomUser/login.html'
    form_class = ModifiedAuthenticationForm # The built-in AuthenticationForm doesn't show inactive-account errors

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # if a user is authenticated, we shouldn't show the login form
            messages.info(self.request, "You are already logged in")
            return HttpResponseRedirect(self.get_success_url())
        return super().get(request, *args, **kwargs)
            
    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        LOGIN_REDIRECT_URL = reverse_lazy('CustomUser:profile', args = [self.request.user.uuid_value])
        return resolve_url(self.next_page or LOGIN_REDIRECT_URL)



class UserProfile(LoginRequiredMixin, DetailView):
    model = user
    template_name = 'CustomUser/user_profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(user, uuid_value=self.kwargs.get('uuid_value'))



class UserUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = user
    fields = ['first_name', 'last_name']
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        return get_object_or_404(user, uuid_value=self.kwargs.get('uuid_value'))

    def test_func(self):
        if self.request.user == user.objects.get(uuid_value = self.kwargs['uuid_value']):
            return True
        return False

    def form_valid(self, form):
        messages.success(self.request, "Your Profile is updated!")
        return super().form_valid(form)



class UserOTPVerifyEmailChange(LoginRequiredMixin, LoginView):
    template_name = 'CustomUser/user_change_email_form.html'
    authentication_form = CustomOTPTokenFormChangeEmail
    
    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        messages.success(self.request, "Your Email has been changed!")
        LOGIN_REDIRECT_URL = reverse_lazy('CustomUser:profile', args = [self.request.user.uuid_value])
        return resolve_url(self.next_page or LOGIN_REDIRECT_URL)



class UserPasswordChange(PasswordChangeView):
    template_name = 'CustomUser/password_change_form.html'
    
    def get_success_url(self):
        messages.success(self.request, "Your password hass been changed!")
        return reverse_lazy('CustomUser:profile', args = [self.request.user.uuid_value])



class UserPasswordReset(PasswordResetView):
    template_name = 'CustomUser/password_reset_form.html'
    email_template_name = 'CustomUser/password_reset_email.html'
    subject_template_name = 'CustomUser/password_reset_subject.txt'
    success_url = reverse_lazy('CustomUser:password_reset_done')

    def form_valid(self, form):
        if not user.objects.filter(email=form.cleaned_data.get("email")):
            messages.error(self.request, 'No account found with that email! Please check the email address and try again.')
            return HttpResponseRedirect(reverse_lazy('CustomUser:password_reset'))
        return super().form_valid(form)



class UserPasswordResetDone(PasswordResetDoneView):
    template_name = 'CustomUser/password_reset_done.html'



class UserPasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'CustomUser/password_reset_confirm.html'
    
    def get_success_url(self):
        messages.success(self.request, "Your password has been reset. Please login again with the new password.")
        return reverse_lazy('CustomUser:login')



class UserLogout(LogoutView):
    template_name = 'CustomUser/logged_out.html'



@method_decorator(otp_required(redirect_field_name='next', login_url=reverse_lazy('CustomUser:otp_verify'), if_configured=False), name='dispatch')
class UserDelete(FormView):
    template_name = 'CustomUser/user_delete_form.html'
    form_class = CustomUserDeletionForm
    success_url = reverse_lazy('CustomUser:logout')

    def form_valid(self, form):
        SadUser = self.request.user
        if SadUser.check_password(form.cleaned_data['password']):
            # It's not recommended to delete the user altogether; rather you can set SadUser.is_active = False
            SadUser.delete()
            messages.info(self.request, "Your Account has been deleted!")
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Incorrect Password!')
            self.extra_context = {'messages':messages}
            return HttpResponseRedirect(reverse_lazy('CustomUser:delete'))



class UserOTPVerify(LoginRequiredMixin, LoginView):
    template_name = 'CustomUser/user_otp_verify_form.html'
    authentication_form = CustomOTPTokenForm

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        PROFILE_REDIRECT_URL = reverse_lazy('CustomUser:profile', args = [self.request.user.uuid_value])
        messages.success(self.request, "Email Verification Successful!")
        return resolve_url(self.next_page or PROFILE_REDIRECT_URL)



