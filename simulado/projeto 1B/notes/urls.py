from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<int:note_id>/', views.delete, name='delete'),
    path('edit/<int:note_id>/', views.edit, name='edit'),
    path('tags/', views.tags, name='tags'),
    path('tags/<int:tag_id>/', views.tag_detail, name='tag_detail'),
    # [SIMULADO 3.2] ✅ rota localhost:8000/perguntas (sem barra no fim → /perguntas/ dá 404, tudo bem)
    #   views.perguntas = def perguntas · name='perguntas' = redirect('perguntas')
    path('perguntas', views.perguntas, name='perguntas'),
    # [SIMULADO 3.4] ✅ rota localhost:8000/categorias
    path('categorias', views.categorias, name='categorias'),
]