from .auth import urlpatterns as auth_urlpatterns
from .payment import urlpatterns as payment_urlpatterns
from .product import urlpatterns as product_urlpatterns
from .category import urlpatterns as category_urlpatterns
from .brand import urlpatterns as brand_urlpatterns
from .fine import urlpatterns as fine_urlpatterns

from .user import urlpatterns as user_urlpatterns

urlpatterns = (
    auth_urlpatterns
    + payment_urlpatterns
    + product_urlpatterns
    + category_urlpatterns
    + brand_urlpatterns
    + fine_urlpatterns
    + user_urlpatterns
)
