from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from . import forms
from utils.geradorsenha import new_password
from utils.send_email import send_new_password

User = get_user_model()


class Criar(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.contexto = {
            'criarform': forms.CriarForm(data=self.request.POST or None)
        }

        self.criarform = self.contexto['criarform']

        self.renderizar = render(
            self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):

        if not self.criarform.is_valid():
            return self.renderizar

        password = self.criarform.cleaned_data.get('password')

        usuario = self.criarform.save(commit=False)
        usuario.set_password(password)
        usuario.save()

        if password:
            autentica = authenticate(
                self.request,
                username=usuario.username,
                password=password
            )

            if autentica:
                login(self.request, user=usuario)

        messages.success(
            self.request,
            'Conta criada com sucesso.'
        )

        return redirect('home:index')


class Atualizar(View):
    template_name = 'perfil/atualizar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.contexto = {'atualizarform': forms.AtualizarForm(
            data=self.request.POST or None,
            usuario=self.request.user,
            instance=self.request.user,
        )}

        self.atualizarform = self.contexto['atualizarform']

        self.renderizar = render(
            self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):

        if not self.atualizarform.is_valid():
            return self.renderizar

        password = self.atualizarform.cleaned_data.get('password')
        email = self.atualizarform.cleaned_data.get('email')
        name = self.atualizarform.cleaned_data.get('name')

        usuario = get_object_or_404(
            User, username=self.request.user.username)

        if password:
            usuario.set_password(password)

        usuario.email = email
        usuario.name = name
        usuario.save()

        login(self.request, user=usuario)

        messages.success(
            self.request,
            'Seus dados foram atualizados.'
        )

        return redirect('perfil:atualizar')


class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request,
                'Usuário ou Senha inválidos'
            )
            return redirect('perfil:criar')

        user_autentica = authenticate(
            self.request, username=username, password=password)

        if not user_autentica:
            messages.error(
                self.request,
                'Usuário ou Senha inválidos'
            )
            return redirect('perfil:criar')

        login(self.request, user=user_autentica)

        messages.success(
            self.request,
            'Logado com sucesso'
        )
        return redirect('home:index')


class Logout(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('perfil:criar')


class PasswordForgot(View):
    template_name = 'perfil/novasenha.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.contexto = {
            'newpassform': forms.NewPasswordForm(data=self.request.POST or None)
        }

        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar


class PasswordReset(View):
    def post(self, *args, **kwargs):
        email = self.request.POST.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).get()

            newpassword = new_password()
            user.set_password(newpassword)
            user.save()

            send_new_password(self, user.name, email, newpassword)

            messages.success(
                self.request,
                'E-mail enviado com sucesso'
            )
            return redirect('perfil:criar')
        else:
            messages.error(
                self.request,
                'E-mail incorreto ou não existe'
            )
            return redirect('perfil:novasenha')
