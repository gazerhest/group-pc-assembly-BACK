from django.urls import path

from assembly import views

urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('manufacturers/', views.ManufacturerList.as_view(), name='manufacturer-list'),
    path('manufacturers/<int:pk>/', views.ManufacturerDetail.as_view(), name='manufacturer-detail'),
    path('parts/', views.PartList.as_view(), name='part-list'),
    path('parts/compare/', views.PartCompare.as_view(), name='part-compare'),
    path('parts/<int:pk>/', views.PartDetail.as_view(), name='part-detail'),
    path('parts/<int:pk>/reviews/', views.PartReviewList.as_view(), name='part-review-list'),
    path('reviews/<int:pk>/', views.PartReviewDetail.as_view(), name='review-detail'),
    path('builds/', views.BuildList.as_view(), name='build-list'),
    path('builds/compare/', views.BuildCompare.as_view(), name='build-compare'),
    path('builds/share/<str:share_token>/', views.BuildShare.as_view(), name='build-share'),
    path('builds/<int:pk>/', views.BuildDetail.as_view(), name='build-detail'),
]
