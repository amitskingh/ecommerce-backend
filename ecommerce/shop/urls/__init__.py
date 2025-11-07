from .auth import urlpatterns as auth_urlpatterns
from .payment import urlpatterns as payment_urlpatterns
from .product import urlpatterns as product_urlpatterns


urlpatterns = auth_urlpatterns + payment_urlpatterns + product_urlpatterns
