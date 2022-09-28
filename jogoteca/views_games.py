from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Jogos
from helpers import recupera_arquivo, deleta_arquivo, FormularioJogo
from jogoteca import app, db
import time


print('Chamado as views')


@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    link_cadastro = 'http://127.0.0.1:5000/novo'
    return render_template('lista.html', title='Jogos', jogos=lista, link=link_cadastro)


@app.route('/inicio/<title>')
def inicio_com_paramentros(title=None):
    return render_template('lista.html', title=title)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    
    form = FormularioJogo()

    return render_template('novo.html', titulo='Jovo Jogo', form=form)







@app.route('/editar/<int:id>')
def editar(id):
    
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    jogo = Jogos.query.filter_by(id=id).first()

    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data  = jogo.categoria
    form.console.data  = jogo.console

    capa_jogo = recupera_arquivo(id)
    return render_template('editar.html', titulo='Editando Jogo',id=id, capa_jogo=capa_jogo, form=form)

@app.route('/atualizar', methods=['POST',])
def atualizar():

    form = FormularioJogo(request.form)
    if form.validate_on_submit(): 
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data 
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        timestamp = time.time()
        deleta_arquivo(jogo.id)
        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo excluído com sucesso!!!')
    return redirect(url_for('index'))



@app.route('/criar', methods=['POST', ])
def criar():

    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))


    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash(f'Jogo  {nome} já cadastado')
        return redirect(url_for('index'))

    timestamp = time.time()
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

