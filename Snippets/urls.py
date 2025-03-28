from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views
from django.contrib import admin

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='sn_add'),
    path('snippets/list', views.snippets_page, name='sn_list'),
    path('snippets/my_list', views.my_snippets, name='sn_mylist'),
    path('snippets/<int:id>', views.snippets_detail, name='sn_detail'),
    path('snippets/<int:id>/edit', views.snippets_edit, name='sn_edit'),
    path('snippets/<int:id>/delete', views.snippets_delete, name='sn_delete'),
    path('comments/add', views.comments_add, name='comments_add'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.create_user, name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
