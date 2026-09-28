# =============================================================================
# notes/urls.py — AS ROTAS DO APP (é aqui que se adiciona rota nova)
# Equivale ao if/elif do servidor.py do 1A.
#
# Anatomia:  path('edit/<int:note_id>/', views.edit, name='edit')
#                  ↑ rota (termina com /)  ↑ função (SEM ())  ↑ apelido
#   <int:note_id> → pega o número da URL e entrega para a view como note_id
#                   (o nome aqui TEM que ser igual ao parâmetro da view)
#   name → usado em {% url 'edit' note.id %} e em redirect('edit')
# 📖 README_1B.md → Parte 0 → "Anatomia de um path"
# =============================================================================
from django.urls import path

from . import views   # "deste app, importe o views.py"

urlpatterns = [
    # Home: GET lista as notas | POST cria nota        📖 README_1B → Parte 1
    path('', views.index, name='index'),
    # Apagar (link da lixeira = GET, apaga direto)     📖 README_1B → Parte 1
    path('delete/<int:note_id>/', views.delete, name='delete'),
    # Editar: GET mostra o form | POST salva           📖 README_1B → Parte 1
    path('edit/<int:note_id>/', views.edit, name='edit'),
    # Lista de todas as tags                           📖 README_1B → Parte 2
    path('tags/', views.tags, name='tags'),
    # Notas de uma tag                                 📖 README_1B → Parte 2
    path('tags/<int:tag_id>/', views.tag_detail, name='tag_detail'),
]
