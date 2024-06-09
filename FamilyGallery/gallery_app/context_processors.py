from django.contrib.auth.models import Group

def user_groups(request):
    if request.user.is_authenticated:
        return {'user_groups': request.user.groups.all()}
    return {}