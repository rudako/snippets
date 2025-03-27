from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='sn_add'),
    path('snippets/list', views.snippets_page, name='sn_list'),
    path('snippets/<int:id>', views.snippets_detail, name='sn_detail'),
    path('snippets/<int:id>/edit', views.snippets_edit, name='sn_edit'),
    path('snippets/<int:id>/delete', views.snippets_delete, name='sn_delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
