import redis

r = redis.Redis()

def is_user_online(user_id):
    return r.exists(f"user_online_{user_id}")

from users.models import CustomUserTeachers, CustomUserStudent
from django.shortcuts import get_object_or_404

def get_chat_target(request):
    if request.GET.get('teacher_id'):
        return get_object_or_404(CustomUserTeachers, pk=request.GET.get('teacher_id'))
    elif request.GET.get('student_id'):
        return get_object_or_404(CustomUserStudent, pk=request.GET.get('student_id'))
    return None

ROLE_RANK = {
    'student': 1,
    'guardian': 2,
    'teacher': 3,
    'admin': 4,
    'manager': 5,
}

def get_user_role(user):
    if user is None:
        return 'unknown'
    if hasattr(user, 'customuserstudent'):
        return 'student'
    elif hasattr(user, 'customuserguardian'):
        return 'guardian'
    elif hasattr(user, 'customuserteacher'):
        return 'teacher'
    elif hasattr(user, 'customusermanager'):
        return 'manager'
    elif hasattr(user, 'is_superuser') and user.is_superuser:
        return 'admin'
    return 'unknown'


def get_user1_user2_ids(user_a, user_b):
    role_a = get_user_role(user_a)
    role_b = get_user_role(user_b)

    rank_a = ROLE_RANK.get(role_a, 999)
    rank_b = ROLE_RANK.get(role_b, 999)

    if rank_a < rank_b:
        return user_a.id, user_b.id
    elif rank_b < rank_a:
        return user_b.id, user_a.id
    else:
        # Si tienen el mismo rango, ordena por ID (para evitar ambigüedad)
        return (user_a.id, user_b.id) if user_a.id < user_b.id else (user_b.id, user_a.id)
