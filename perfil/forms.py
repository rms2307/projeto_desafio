from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CriarForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação senha'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password', 'password2')

    def clean(self, *args, **kwargs):
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'Senhas não conferem'
        error_msg_password_short = 'Minimo 6 caracteres'
        error_msg_required_field = 'Campo é obrigatório'

        if usuario_db:
            validation_error_msgs['username'] = error_msg_user_exists

        if email_db:
            validation_error_msgs['email'] = error_msg_email_exists

        if not password_data:
            validation_error_msgs['password'] = error_msg_required_field

        if not password2_data:
            validation_error_msgs['password2'] = error_msg_required_field

        if password_data != password2_data:
            validation_error_msgs['password'] = error_msg_password_match
            validation_error_msgs['password2'] = error_msg_password_match

        if len(password_data) < 6:
            validation_error_msgs['password'] = error_msg_password_short

        # Exibe mensagem de erro nos campos
        if validation_error_msgs:
            raise (forms.ValidationError(validation_error_msgs))


class AtualizarForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação senha'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'password2')

    def clean(self, *args, **kwargs):
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'Senhas não conferem'
        error_msg_password_short = 'Minimo 6 caracteres'

        if self.usuario:

            if usuario_db:
                if usuario_data != usuario_db.username:
                    validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                if email_data != email_db.email:
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match

                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short

        # Exibe mensagem de erro nos campos
        if validation_error_msgs:
            raise (forms.ValidationError(validation_error_msgs))


class NewPasswordForm(forms.Form):
    email = forms.EmailField(label='E-mail')
