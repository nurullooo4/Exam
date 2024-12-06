from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import get_user_model, logout
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from app_users.forms import UserCreationForm

User = get_user_model()


class RegistrationView(CreateView):
    model = User
    template_name = 'app_users/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     user = form.instance
    #
    #     subject = 'Welcome to Online Store!'
    #     message = f'Hello {user.firt_namez},\n\nThank you for registering at our store!'
    #     recipient_list = [user.email]
    #
    #     send_mail(
    #         subject=subject,
    #         message=message,
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=recipient_list,
    #         fail_silently=False,
    #     )
    #     return response


def logout_view(request):
    logout(request)
    return redirect('login')


class AccountView(UpdateView):
    model = User
    template_name = 'app_users/account.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    pk_url_kwarg = 'user_id'

    def get_object(self, queryset=None):
        user_id = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(User, id=user_id)

