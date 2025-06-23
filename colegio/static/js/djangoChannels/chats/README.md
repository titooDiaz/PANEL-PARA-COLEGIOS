<p align="center">
  <img width="150px" src="https://i.ibb.co/bXvzjXm/LOGO-h1.png" alt="Logo de h1">
  <img width="150px" src="https://github.com/user-attachments/assets/e0551b39-11a1-4ce3-b5e2-2c6c18882bf0" alt="Logo del proyecto">
</p>

## 🧠 Live Chat Integration Guide

To integrate a page with the **real-time chat system** powered by Django Channels, you must follow the following setup:

---

### ✅ Required HTML Template Setup

Include the following block in the template (`.html`) file where the chat will run:

```html
<div class="hidden">
    <span id="secret_token">{{ csrf_token }}</span>
    <span id="url_chat_file">{% url "upload_chat_file" %}</span>
    <span id="photo_url">{{ selected_teacher.photo.url }}</span>
    <span id="user1Id">{{ request.user.id }}</span>
    <span id="user2Id">{{ selected_teacher.id }}</span>
    <span id="sender">{{ request.user.id }}</span>
    <span id="receiver">{{ selected_teacher.id }}</span>
    <script src="{% static 'js/djangoChannels/chats/chats.js' %}"></script>
</div>
```

---

### ⚠️ Important Rule: `user1Id` Must Be the Lower-Ranked User

The **real-time channel room name** is based on `user1Id_user2Id`.
To **prevent duplicated room names** and ensure stable socket connections, **`user1Id` must always be the user with the lower rank**, according to the following hierarchy:

```
students < guardians < teachers < admins < managers
```

So, if a student is chatting with a teacher:

```html
<span id="user1Id">{{ student.id }}</span>
<span id="user2Id">{{ teacher.id }}</span>
```

If you reverse them by mistake, WebSocket errors will occur due to inconsistent group names.

#### Role Ranking Table

| Role     | Rank (lower is better) |
| -------- | ---------------------- |
| student  | 1                      |
| guardian | 2                      |
| teacher  | 3                      |
| admin    | 4                      |
| manager  | 5                      |

Use this ranking to determine who should be assigned to `user1Id`.

---

### 🧐 Django View Requirement

Each page must also use a corresponding Django `View` to send the necessary context variables, like `selected_teacher`, `csrf_token`, etc. Here's a working example:

```python
class ProfessorMessages(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        school_user = user.school
        students = CustomUserStudent.objects.filter(school=school_user)

        selected_student_id = request.GET.get('student_id')
        selected_student = None
        messages = None
        form = ChatMessageForm()

        if selected_student_id:
            selected_student = get_object_or_404(CustomUserStudent, pk=selected_student_id)
            messages = ChatMessage.objects.filter(
                sender__in=[user, selected_student],
                receiver__in=[user, selected_student]
            ).order_by('sent_at')

        context = {
            'vista': 'profesores',
            'abierto': 'mensajes',
            'students': students,
            'selected_student': selected_student,
            'messages_users': messages,
            'form': form,
        }
        return render(request, 'users/teachers/messages/messages.html', context)
```

This ensures that the front-end JavaScript has access to all required values to open a WebSocket connection and send/receive messages properly.
