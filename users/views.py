from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from users.forms import RegisterForm


class RegisterUser(FormView):
    template_name = 'users/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:success')

    def form_valid(self, form):
        form.save()
        return super(RegisterUser, self).form_valid(form)
