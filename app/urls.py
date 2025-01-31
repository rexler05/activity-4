from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    PetListView, PetDetailView, PetCreateView, PetUpdateView, PetDeleteView,
    AdoptionApplicationListView, AdoptionApplicationDetailView, AdoptionApplicationCreateView,
    AdoptionApplicationUpdateView, AdoptionApplicationDeleteView,
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentListView, CommentDetailView, CommentCreateView, CommentUpdateView, CommentDeleteView,
    NotificationListView, NotificationDetailView, NotificationCreateView, NotificationUpdateView,
    NotificationDeleteView, HomePageView, AboutPageView, ContactPageView
)

urlpatterns = [

    path('', HomePageView.as_view(), name='home'),
    path('about', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    # Pet URLs
    path('pets/', PetListView.as_view(), name='pet_list'),
    path('pets/<int:pk>/', PetDetailView.as_view(), name='pet_detail'),
    path('pets/create/', PetCreateView.as_view(), name='pet_create'),
    path('pets/<int:pk>/update/', PetUpdateView.as_view(), name='pet_update'),
    path('pets/<int:pk>/delete/', PetDeleteView.as_view(), name='pet_delete'),

    # AdoptionApplication URLs
    path('adoptions/', AdoptionApplicationListView.as_view(), name='adoption_application_list'),
    path('adoptions/<int:pk>/', AdoptionApplicationDetailView.as_view(), name='adoption_application_detail'),
    path('adoptions/create/', AdoptionApplicationCreateView.as_view(), name='adoption_application_create'),
    path('adoptions/<int:pk>/update/', AdoptionApplicationUpdateView.as_view(), name='adoption_application_update'),
    path('adoptions/<int:pk>/delete/', AdoptionApplicationDeleteView.as_view(), name='adoption_application_delete'),

    # Post URLs
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # Comment URLs
    path('comments/', CommentListView.as_view(), name='comment_list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
    path('comments/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    # Notification URLs
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification_detail'),
    path('notifications/create/', NotificationCreateView.as_view(), name='notification_create'),
    path('notifications/<int:pk>/update/', NotificationUpdateView.as_view(), name='notification_update'),
    path('notifications/<int:pk>/delete/', NotificationDeleteView.as_view(), name='notification_delete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)