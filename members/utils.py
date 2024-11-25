
from .models import Member

import requests

def complex_hash(key, table_size = 20):
  hash_value = 0
  prime = 31
  for i, char in enumerate(key):
    hash_value += ord(char) * (prime ** i)
  return hash_value % table_size

def isAuthenticated(request):
    member_id = request.session.get('member_id')
    if member_id:
        try:
            member = Member.objects.get(id=member_id)
            return {'is_authenticated': True}
        except Member.DoesNotExist:
            return {'is_authenticated': False}
    return {'is_authenticated': False}

def getUserAvatar(request):
    member_id = request.session.get('member_id')
    avatar_url = None

    if member_id:
        member = Member.objects.filter(id=member_id).first()
        if member and member.avatar:
            avatar_url = member.avatar
        else:
            avatar_url = 'https://t4.ftcdn.net/jpg/05/49/98/39/360_F_549983970_bRCkYfk0P6PP5fKbMhZMIb07mCJ6esXL.jpg'

    return {'avatar_url': avatar_url}
        

def is_password_strong(password, min_length=8):
    contains_special_character = False
    contains_uppercase_character = False
    contains_number = False
    contains_lowercase_character = False

    # Check if the password meets the minimum length requirement
    if len(password) < min_length:
        return False

    for ch in password:
        if ch.islower():
            contains_lowercase_character = True
        elif ch.isupper():
            contains_uppercase_character = True
        elif ch.isdigit():
            contains_number = True
        elif not ch.isalnum():
            contains_special_character = True

    # Assess the password by checking all conditions
    return all([
        contains_special_character,
        contains_uppercase_character,
        contains_number,
        contains_lowercase_character
    ])
      

def check_image_url(url):
    try:
        response = requests.get(url)
        # Check if the response is successful and content type is an image
        if response.status_code == 200 and 'image' in response.headers['Content-Type']:
            return True
    except requests.RequestException as e:
        print(f'Error checking image URL: {e}')
    return False
