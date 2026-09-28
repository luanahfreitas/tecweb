# =============================================================================
# notes/views.py — AS FUNÇÕES DE CADA PÁGINA
# Cada função recebe request (objeto) e devolve render(...) ou redirect(...).
#
# Tradução do 1A:
#   request.startswith('POST')        → request.method == 'POST'
#   montar params (split, unquote)    → request.POST.get('name_do_input')
#   load_template().format() + build_response(body=...) → render(request, 'notes/x.html', {...})
#   build_response(code=303, ...)     → redirect('name_do_path')
#   int(route.split('/')[-1])         → parâmetro note_id (vem do <int:note_id>)
#
# Molde de view com formulário:
#   if request.method == 'POST':  ler request.POST → criar/salvar → return redirect(...)
#   (GET) buscar dados → return render(request, 'notes/x.html', {'chave': valor})
# 📖 README_1B.md → Parte 1 → "3. Views"
# =============================================================================
from django.shortcuts import render, redirect
from .models import Note, Tag


# -----------------------------------------------------------------------------
# HOME — rota ''   GET: lista | POST: cria nota (com tags)
# -----------------------------------------------------------------------------
def index(request):
    if request.method == 'POST':
        # request.POST.get('x') → valor do campo com name="x" no HTML (ou None se não veio)
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tags_input = request.POST.get('tags', '')      # '' = padrão se o campo não vier

        # 1º cria a nota (ela precisa existir/ter id antes de ligar tags)
        note = Note.objects.create(title=title, content=content)

        # "faculdade, urgente, " → ['faculdade', 'urgente']
        # split(',') corta nas vírgulas · strip() tira espaços · if t.strip() descarta vazios
        tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
        for name in tag_names:
            # get_or_create: busca a tag pelo nome; se não existir, cria.
            # Devolve DOIS valores: (objeto, True se criou agora / False se já existia)
            tag, created = Tag.objects.get_or_create(name=name)
            note.tags.add(tag)                           # 2º liga a tag à nota (many-to-many)
        # 📖 README_1B → Parte 2 → "View index — criar nota com tags"

        # Todo POST termina em redirect → navegador faz GET / (F5 não reenvia)
        # 'index' = name do path, não a rota. (Django usa código 302)
        return redirect('index')

    # GET: busca todas as notas e manda para o template
    notes = Note.objects.all()
    # {'notes': notes} → no template a variável se chama notes ({% for note in notes %})
    return render(request, 'notes/index.html', {'notes': notes})


# -----------------------------------------------------------------------------
# APAGAR — rota 'delete/<int:note_id>/'   (link da lixeira → GET → apaga direto)
# -----------------------------------------------------------------------------
def delete(request, note_id):                    # note_id vem do <int:note_id>, já é número
    note = Note.objects.get(id=note_id)          # ⚠ id inexistente → DoesNotExist
    note.delete()
    return redirect('index')


# -----------------------------------------------------------------------------
# EDITAR — rota 'edit/<int:note_id>/'   GET: form preenchido | POST: salva
# -----------------------------------------------------------------------------
def edit(request, note_id):
    note = Note.objects.get(id=note_id)          # busca 1 vez: as duas metades usam
    if request.method == 'POST':
        # Alterar atributos + save() = UPDATE no banco (save já "commita")
        note.title = request.POST.get('titulo')
        note.content = request.POST.get('detalhes')
        note.save()

        # Tags: desliga TODAS (não apaga as tags) e religa as que vieram no form
        tags_input = request.POST.get('tags')
        note.tags.clear()
        if tags_input:
            tag_names = [name.strip() for name in tags_input.split(',') if name.strip()]
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                note.tags.add(tag)

        return redirect('index')
    else:
        # GET: manda a nota para o template preencher o formulário
        return render(request, 'notes/edit.html', {'note': note})


# -----------------------------------------------------------------------------
# LISTA DE TAGS — rota 'tags/'
# 📖 README_1B → Parte 2 → "Páginas de tags"
# -----------------------------------------------------------------------------
def tags(request):
    all_tags = Tag.objects.all()
    return render(request, 'notes/tags.html', {'tags': all_tags})


# -----------------------------------------------------------------------------
# NOTAS DE UMA TAG — rota 'tags/<int:tag_id>/'
# -----------------------------------------------------------------------------
def tag_detail(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    # filter(tags=tag) → só as notas que têm essa tag
    # (mesma coisa que tag.note_set.all(), o caminho inverso)
    notes = Note.objects.filter(tags=tag)
    return render(request, 'notes/tag_detail.html', {'tag': tag, 'notes': notes})
