from base64 import b64encode
from secrets import token_bytes
from os.path import join, realpath


DEFAULT_SECRET_PATH = join('secrets', 'django_secret_key')


def generate_django_secret(out_path=DEFAULT_SECRET_PATH):
    random = token_bytes(128)
    b64_str = b64encode(random).decode('utf-8')
    open(out_path, 'w').write(b64_str)


if __name__ == '__main__':
    generate_django_secret()
