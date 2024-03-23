from api.models import User
from django.core.signing import Signer, BadSignature
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request


class TelegramIdSecureAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> tuple[User, None] | None:
        signed_id = request.META.get('HTTP_AUTHENTICATION')
        if not signed_id:
            return None

        signer = Signer()  # Signer use SECRET_KEY by default

        try:
            tg_id = signer.unsign(signed_id)
        except BadSignature:
            return None

        user = User.objects.filter(tg_id=tg_id).first()

        if user:
            return (user, None)
        else:
            return None
