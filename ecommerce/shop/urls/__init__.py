from .auth import urlpatterns as auth_urlpatterns
from .payment import urlpatterns as payment_urlpatterns

urlpatterns = auth_urlpatterns + payment_urlpatterns
