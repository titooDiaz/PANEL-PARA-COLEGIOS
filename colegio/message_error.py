from django.contrib import messages

class messages_error:
    @staticmethod
    def errores_formularios(form_errors, mensaje, request):
        error_message = f'{mensaje} \n \n \n'
        for field, errors in form_errors.items():
            for error in errors:
                error_message += f' - **{field}**: {error} \n \n'
        messages.error(request, error_message)
