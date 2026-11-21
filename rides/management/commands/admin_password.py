from django.core.management.base import BaseCommand
import database
import os
import hashlib

def hash_pwd(password):
    salt = os.urandom(16).hex()
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"pbkdf2:sha256:100000${salt}${key.hex()}"

class Command(BaseCommand):
    help = 'Change password for RideBook Admin in the SQLite database'

    def add_arguments(self, parser):
        parser.add_argument('username_or_email', type=str, nargs='?', default='Admin', help='Admin username or email')
        parser.add_argument('new_password', type=str, nargs='?', default=None, help='New password')

    def handle(self, *args, **options):
        ident = options['username_or_email']
        new_pwd = options['new_password']

        admin = database.fetch_one("SELECT * FROM Admin WHERE username = %s OR email = %s", (ident, ident))
        if not admin:
            self.stderr.write(self.style.ERROR(f"Admin '{ident}' not found in database!"))
            return

        if not new_pwd:
            import getpass
            new_pwd = getpass.getpass(f"Enter new password for Admin ({admin['username']}): ")
            confirm_pwd = getpass.getpass("Confirm password: ")
            if new_pwd != confirm_pwd:
                self.stderr.write(self.style.ERROR("Passwords do not match!"))
                return

        hashed = hash_pwd(new_pwd)
        database.execute_query("UPDATE Admin SET password_hash = %s WHERE id = %s", (hashed, admin['id']))
        self.stdout.write(self.style.SUCCESS(f"Successfully updated password for Admin '{admin['username']}'!"))
