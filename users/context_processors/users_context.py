from django.core.exceptions import ObjectDoesNotExist

from houses.models import Flat
from users.models import CustomUser, MessageUsers

# TODO 'Change request USER_ID -> request.user.id

def user_info(request):
    request_path_list = request.path.split('/')
    if request_path_list[1] == 'users' and request_path_list[2] == 'cabinet':
        flats = Flat.objects.filter(owner_id=12).\
            select_related('house')
        unread_message = MessageUsers.objects.filter(user_id=12, read=False).\
            order_by('-message_id')
        return {
            'flats': flats,
            'unread_message': unread_message,
            'unread_message_count': unread_message.count()
            }
    else:
        return {}
