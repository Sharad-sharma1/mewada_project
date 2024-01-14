from django.contrib import admin
from django.urls import path
from mapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', views.profile, name='profile'),
    path('premium_profile/', views.premium_profile, name='premium_profile'),
    path('', views.staff_login, name='staff_login'),
    path('staff_logout/', views.staff_logout, name='staff_logout'),
    path('add_user/', views.add_user, name='add_user'),
    path('add_premium_user/', views.add_premium_user, name='add_premium_user'),
    path('show_user/', views.show_user, name='show_user'),
    path('show_premium_user/', views.show_premium_user, name='show_premium_user'),
    path('update_user/<int:id>/', views.update_user, name='update_user'),
    path('update_premium_user/<int:id>/', views.update_premium_user, name='update_premium_user'),
    path('add_village/', views.add_village, name='add_village'),
    path('update_village/<int:id>/', views.update_village, name='update_village'),
    path('add_area/', views.add_area, name='add_area'),
    path('update_area/<int:id>/', views.update_area, name='update_area'),
    path('downlaod/<str:filterr>/<str:table_data>', views.download_csv, name='downlaod'),
    path('downlaodpdf/<str:filterr>/<str:table_data>', views.download_pdf, name='downlaodpdf'),
    path('downlaodstickerpdf/<str:filterr>/<str:table_data>', views.download_sticker_pdf, name='downlaodstickerpdf'),
    path('downlaodsplitstickerpdf/<str:filterr>/<str:table_data>', views.download_split_sticker_pdf, name='downlaodsplitstickerpdf'),
    path('print_user/', views.print_user, name='print_user'),
    path('print_premium_user/', views.print_premium_user, name='print_premium_user'),
    path('ajax_load_data/', views.ajax_load_data, name='ajax_load_data'),
    path('download_csvarea/', views.download_csvarea, name='download_csvarea'),
    path('download_csvvillage/', views.download_csvvillage, name='download_csvvillage'),
    
]