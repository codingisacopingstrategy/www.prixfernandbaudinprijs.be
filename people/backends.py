from people.models import FernandUser

class PassUserBackend(object):

    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, user=None):
        return user

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return FernandUser.objects.get(pk=user_id)
        except FernandUser.DoesNotExist:
            return None
