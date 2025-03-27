from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='sn_add'),
    path('snippets/list', views.snippets_page, name='sn_list'),
    path('snippets/<int:id>', views.snippets_detail, name='sn_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
