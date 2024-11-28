from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (HomePageView,
                    AboutPageView,
                    ContactPageView,
                    BlogListView,
                    BlogDetailView,
                    BlogCreateView,
                    BlogUpdateView,
                    BlogDeleteView,
                    RegisterView,
                    LoginPageView,
                    LogoutPageView,
                    ProfileView,
                    ProfileUpdateView,
                    PetCreateView,
                    PetListView,
                    PetDetailView,
                    PetUpdateView,
                    PetDeleteView,
                    AdoptionApplicationCreateView,
                    AdoptionApplicationsListView,
                    AdoptionApplicationDetailView,
                    ApproveAdoptionView,
                    DenyAdoptionView,
                    NotificationListView,
                    MarkNotificationAsReadView
                    )
urlpatterns = [
    path('', LoginPageView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('account_settings/edit/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('home/', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    # Pet URLs



    path('news/', BlogListView.as_view(), name='news'),
    path('news/<int:pk>', BlogDetailView.as_view(), name='blog_detail'),
    path('news/create', BlogCreateView.as_view(), name='blog_create'),
    path('news/<int:pk>/edit', BlogUpdateView.as_view(), name='blog_update'),
    path('news/<int:pk>/delete', BlogDeleteView.as_view(), name='blog_delete'),



    path('pets/', PetListView.as_view(), name='pets'),
    path('pets/create/', PetCreateView.as_view(), name='pet_create'),
    path('pets/<int:pk>/', PetDetailView.as_view(), name='pet_detail'),
    path('pets/<int:pk>/edit/', PetUpdateView.as_view(), name='pet_update'),
    path('pets/<int:pk>/delete/', PetDeleteView.as_view(), name='pet_delete'),
    path('pets/<int:pk>/apply/', AdoptionApplicationCreateView.as_view(), name='adoption_application_create'),



    path('adoption/applications/', AdoptionApplicationsListView.as_view(), name='adoption_application'),
    path('adoption/<int:pk>', AdoptionApplicationDetailView.as_view(), name='adoption_application_detail'),

    # List and Detail Views
    path('adoption/applications/', AdoptionApplicationsListView.as_view(), name='adoption_application'),
    path('adoption/<int:pk>/', AdoptionApplicationDetailView.as_view(), name='adoption_application_detail'),

    # Approve/Deny Actions
    path('adoption/<int:pk>/approve/', ApproveAdoptionView.as_view(), name='adoption_approval'),
    path('adoption/<int:pk>/deny/', DenyAdoptionView.as_view(), name='adoption_application_deny'),

    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/read/', MarkNotificationAsReadView.as_view(), name='mark_notification_as_read'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

