from django.shortcuts import render, redirect
# [SIMULADO 3.2 / 3.4] ✅ models novos importados (senão NameError)
from .models import Note, Tag, Pergunta, Categoria


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tags_input = request.POST.get('tags', '')

        note = Note.objects.create(title=title, content=content)

        tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            note.tags.add(tag)

        return redirect('index')

    notes = Note.objects.all()
    return render(request, 'notes/index.html', {'notes': notes})

def delete(request, note_id):
    note = Note.objects.get(id=note_id)
    note.delete()
    return redirect('index')

def edit(request, note_id):
    note = Note.objects.get(id=note_id)
    if request.method == 'POST':
        note.title = request.POST.get('titulo')
        note.content = request.POST.get('detalhes')
        note.save()

        tags_input = request.POST.get('tags')
        note.tags.clear()
        if tags_input:
            tag_names = [name.strip() for name in tags_input.split(',') if name.strip()]
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                note.tags.add(tag)

        return redirect('index')
    else:
        return render(request, 'notes/edit.html', {'note': note})

def tags(request):
    all_tags = Tag.objects.all()
    return render(request, 'notes/tags.html', {'tags': all_tags})

def tag_detail(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    notes = Note.objects.filter(tags=tag)
    return render(request, 'notes/tag_detail.html', {'tag': tag, 'notes': notes})

# [SIMULADO 3.2 + 3.3 + 3.5] view da página de perguntas
# 📖 README_SIMULADO → "Quando pedirem um formulário" / "listar" / "o dropdown"
def perguntas(request):
    if request.method == 'POST':
        # ✅ 'enunciado' e 'resposta' = os name dos inputs do perguntas.html
        enunciado = request.POST.get('enunciado')
        resposta = request.POST.get('resposta')
        # ✅ texto → True/False (BooleanField não aceita o texto 'Verdadeiro')
        resposta_correta = resposta == 'Verdadeiro'

        # ✅ 'categoria' = name do <select>. Chega o ID escolhido, como TEXTO ('1')
        categoria_id = request.POST.get('categoria')

        # ❌ ERRO que estava aqui (testado):
        #   Pergunta.objects.create(..., categoria=categoria)
        #   → ValueError: Cannot assign "'1'": "Pergunta.categoria" must be a "Categoria" instance.
        #   O campo 'categoria=' espera o OBJETO Categoria; o que chega do form é o ID (texto).
        # ✅ CORRIGIDO: usar categoria_id= (a coluna do id)
        Pergunta.objects.create(enunciado=enunciado, resposta_correta=resposta_correta, categoria_id=categoria_id)

        # ✅ todo POST termina em redirect (volta para /perguntas)
        return redirect('perguntas')

    # [3.3] ✅ lista de perguntas para o <ul> · [3.5] ✅ lista de categorias para o <select>
    todas = Pergunta.objects.all()
    categorias = Categoria.objects.all()
    # ✅ as chaves 'perguntas' e 'categorias' = os nomes usados nos {% for %} do template
    return render(request, 'notes/perguntas.html', {'perguntas': todas, 'categorias': categorias})

# [SIMULADO 3.4] ✅ mesmo molde da página de perguntas: POST cria + redirect · GET lista
def categorias(request):
    if request.method == 'POST':
        # ✅ 'nome' = name do input do categorias.html
        nome = request.POST.get('nome')
    
        Categoria.objects.create(nome=nome)
        
        return redirect('categorias')
        
    todas = Categoria.objects.all()
    return render(request, 'notes/categorias.html', {'categorias': todas})
