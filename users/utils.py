
import random 
import string

from django.contrib.auth.models import User

from .models import Profile
from foidata.data.data import FOIData


class UserUtils:

    def __init__(self):
        self.data = FOIData()

    def create_or_update(self):
        self.roster = self.data.roster
        
        created_count = 0 
        updated_count = 0

        for _, row in self.roster.iterrows():
            username = self.get_username(row)

            try:
                user = User.objects.get(profile__nation_id=int(row['NationId']))
            except User.DoesNotExist:
                user = None

            if user:
                user.username = username
                user.first_name = row['FirstName']
                user.last_name = row['LastName']
                user.email = row['Email']
                user.is_active = bool(row['Active'])
                user.save()

                profile = self.update_profile(user, row)

                updated_count += 1

                print(f'Updated: {user} - {profile}')

            else:
                password  = self.generate_password()

                user = User.objects.create_user(
                    username,
                    first_name = row['FirstName'],
                    last_name = row['LastName'],
                    email = row['Email'],
                    password = password,
                    is_active = bool(row['Active'])
                )

                user.save()
                
                profile = self.update_profile(user, row)

                created_count += 1

                print(f'Created: username: {user} - password: {password} - {profile}')

        return created_count, updated_count


    def update_profile(self, user, roster_row):
        row = roster_row
        profile = Profile.objects.get(user=user)

        profile.nation_id = int(row['NationId'])
        profile.city = row['City']
        profile.rank = row['Rank']
        profile.receive_emails = row['ReceiveEmails']

        profile.save()

        return profile




    def get_username(self, df_row):
        first_name = df_row['FirstName'].lower().strip()
        last_initial = df_row['LastName'][0].lower().strip()
        nation_id_str = str(df_row['NationId']).strip()

        return f'{first_name}{last_initial}{nation_id_str}'

    
    def generate_password(self, string_length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(string_length))
