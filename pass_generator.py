#!/usr/bin/python3
import random
import string

def generate_password(length=20):
    """Generate a random password with given length, excluding certain characters."""
    # Define allowed characters excluding double quotes and curly braces
    allowed_characters = string.ascii_letters + string.digits + string.punctuation
    allowed_characters = allowed_characters.replace('"', '').replace('{', '').replace('}', '').replace('\\', '')
    return ''.join(random.choice(allowed_characters) for _ in range(length))

def generate_student_passwords(start_id, end_id, password_length=20):
    """Generate passwords for a range of student IDs."""
    passwords = {}
    for student_id in range(start_id, end_id + 1):
        password = generate_password(length=password_length)
        passwords[f'student_pass_{student_id}'] = password
    return passwords

# Parameters
start_student_id = 0  # Starting student ID
end_student_id = 10   # Ending student ID
password_length = 30  # Length of each password

# Generate and print passwords for the specified range of student IDs
student_passwords = generate_student_passwords(start_student_id, end_student_id, password_length)

# Print the generated passwords
for student_id, password in student_passwords.items():
    print(f'{student_id}: "{password}"')

