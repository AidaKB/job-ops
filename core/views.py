from dj_rest_auth.views import LoginView
from . import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class CustomLoginView(LoginView):
    serializer_class = serializers.CustomLoginSerializer
