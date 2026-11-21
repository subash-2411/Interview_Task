from django.core.management.base import BaseCommand
import database
import os
import hashlib

def hash_pwd(password):
    salt = os.urandom(16).hex()
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"pbkdf2:sha256:100000${salt}${key.hex()}"

class Command(BaseCommand):
    help = 'Create a new Admin for RideBook AI in SQLite database'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, nargs='?', default=None, help='Admin username')
        parser.add_argument('email', type=str, nargs='?', default=None, help='Admin email')
        parser.add_argument('password', type=str, nargs='?', default=None, help='Admin password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if not username:
            username = input("Enter Admin Username: ").strip()
        if not email:
            email = input("Enter Admin Email: ").strip()
        if not password:
            import getpass
            password = getpass.getpass("Enter Admin Password: ").strip()

        if not username or not email or not password:
            self.stderr.write(self.style.ERROR("Username, email, and password are all required!"))
            return

        exists = database.fetch_one("SELECT * FROM Admin WHERE username = %s OR email = %s", (username, email))
        if exists:
            self.stderr.write(self.style.ERROR(f"Admin with username '{username}' or email '{email}' already exists!"))
            return

        hashed = hash_pwd(password)
        database.execute_query(
            "INSERT INTO Admin (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, hashed)
        )
        self.stdout.write(self.style.SUCCESS(f"Successfully created new Admin '{username}' ({email})!"))
