import string
import secrets


def new_password():
    dados = string.ascii_letters + string.digits

    while True:
        password = ''.join(secrets.choice(dados) for i in range(6))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password
