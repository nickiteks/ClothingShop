from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# TODO app_name  =
urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('<int:product_id>/', views.product, name='product'),
    path('<int:product_id>/leave_comment/', views.leave_comment, name='leave_comment')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
