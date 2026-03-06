from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import View
from django.db import transaction
from .forms import RegisterForm
from .models import Profile


class CustomLoginView(LoginView):
    template_name = 'profiles/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self._redirect_by_role(request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return self._redirect_by_role(user)

    def _redirect_by_role(self, user):
        if user.is_staff or user.is_superuser:
            return redirect('/admin/')
        return redirect('/')


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                return redirect('/admin/')
            return render(request, 'base.html')
        return redirect('/accounts/login/')


class RegisterView(View):
    template_name = 'profiles/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                    )
                    Profile.objects.update_or_create(
                        user=user,
                        defaults={
                            'role': form.cleaned_data['role'],
                            'pincode': form.cleaned_data['pincode'],
                            'personal_id': form.cleaned_data['personal_id'],
                        }
                    )
                return redirect('login')

            except Exception as e:
                form.add_error(None, f'Registration failed: {str(e)}')

        return render(request, self.template_name, {'form': form})