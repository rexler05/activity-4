from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomePageView, AboutPageView, ContactPageView,
    PetListView, PetDetailView, PetCreateView, PetUpdateView, PetDeleteView,
    AdoptionApplicationListView, AdoptionApplicationDetailView,
    AdoptionApplicationCreateView, AdoptionApplicationUpdateView, AdoptionApplicationDeleteView,AdoptionApplicationApproveView,AdoptionApplicationRejectView,
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateView,CommentDetailView, CommentUpdateView, CommentDeleteView,
    NotificationListView, NotificationDetailView, NotificationCreateView, NotificationUpdateView ,NotificationDeleteView,
)

urlpatterns = [
    # Home, About, Contact
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),

    # Pet URLs
    path('pets/', PetListView.as_view(), name='pet_list'),
    path('pets/<int:pk>/', PetDetailView.as_view(), name='pet_detail'),
    path('pets/create/', PetCreateView.as_view(), name='pet_create'),
    path('pets/<int:pk>/update/', PetUpdateView.as_view(), name='pet_update'),
    path('pets/<int:pk>/delete/', PetDeleteView.as_view(), name='pet_delete'),

    # Adoption Application URLs
    path('adoptions/', AdoptionApplicationListView.as_view(), name='adoption_application_list'),
    path('adoptions/<int:pk>/', AdoptionApplicationDetailView.as_view(), name='adoption_application_detail'),
    path('adoptions/create/<int:pet_pk>/', AdoptionApplicationCreateView.as_view(), name='adoption_application_create'),
    path('adoptions/<int:pk>/update/', AdoptionApplicationUpdateView.as_view(), name='adoption_application_update'),
    path('adoptions/approve/<int:pk>/', AdoptionApplicationApproveView.as_view(), name='adoption_application_approve'),
    path('adoptions/reject/<int:pk>/', AdoptionApplicationRejectView.as_view(),
         name='adoption_application_reject'),
    path('adoptions/<int:pk>/delete/', AdoptionApplicationDeleteView.as_view(), name='adoption_application_delete'),

    # Post URLs
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # Comment URLs
    path('post/<int:post_pk>/comment/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    # Notification URLs
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('notification/<int:pk>/', NotificationDetailView.as_view(), name='notification_detail'),
    path('notification/new/', NotificationCreateView.as_view(), name='notification_create'),
    path('notification/<int:pk>/delete/', NotificationDeleteView.as_view(), name='notification_delete'),
    path('notification/<int:pk>/update/', NotificationUpdateView.as_view(), name='notification_update'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
