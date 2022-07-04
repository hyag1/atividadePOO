import sqlite3
from flask import Blueprint,Flask,render_template,request,flash, redirect, url_for,Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert
from config import app_config,app_active
from model import *


config=app_config[app_active]

def create_app(config_name):
    app = Flask(__name__,template_folder='templates')
    app.secret_key=config.SECRET
    app.config.from_object(app_config[app_active])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
    db=SQLAlchemy(app)
    db.init_app(app)
    conn = sqlite3.connect('database/minisigaa.db', check_same_thread=False)
    cur = conn.cursor()

    @app.route("/")
    def index():
        return render_template("index.html")
    # @app.route("/perfil")
    # def perfil(data:Usuario=0):
    #     if(data==0):
    #         flash('Nenhum usuário logado')
    #         return redirect(url_for('index'))
    #     else:
    #         return render_template("perfil.html",data=data)


    @app.route('/login')
    def login():
        return render_template("login.html")

    @app.route('/login', methods=['POST'])
    def login_post():
        if request.method == 'POST':
            login = request.form['login']
            senha = request.form['senha']
            user: Usuario = Usuario.query.filter_by(nome=login).first()
            if user:
                if senha == user.senha:
                    if user.role == 1:
                        return redirect(url_for('adm',id = user.id))
                    elif user.role == 2:
                        return redirect(url_for('aluno', id=user.id))
                    else:
                        return redirect(url_for('professor', id=user.id))
                else:
                    flash('Senha Incorreta tenta de novo ai!')
                    return redirect(url_for('login'))
            else:
                flash('Deu certo não tente ai de novo please!')
                return redirect(url_for('login_post'))

    @app.route('/login/adm/<id>')
    def adm(id):
        user: Usuario = Usuario.query.filter_by(id=id).first()
        return render_template("adm.html",usu=user)

    @app.route('/lista_alunos')
    def modal_lista_alunos():
        cur.execute("SELECT * FROM usuario where role=2")
        alunos = cur.fetchall()
        return render_template("modalListarAlunos.html",alu=alunos)

    @app.route('/login/aluno/<id>/listardisciplinas')
    def modal_lista_disciplinas(id):
        cur.execute("SELECT * FROM disciplinas")
        disciplina_array = cur.fetchall()
        return render_template("modalListarDisciplinas.html", disciplinas=disciplina_array,val =id)

    @app.route('/login/aluno/<id>/listardisciplinas',methods = ['POST'])
    def matricular(id):
        ide = request.form['id']
        disci = request.form['disci']
        disciplina: Disciplinas = Disciplinas.query.filter_by(id=disci).first()
        cur.execute("SELECT * FROM matricula")
        matriculas = cur.fetchall()
        if len(matriculas)!=0:
            for matricula in matriculas:
                if str(matricula[1]) == ide and str(matricula[2]) == disci:
                    flash('Você já está cadastrado nesta disciplina!')
                    return redirect(url_for('aluno',id = ide))
                else:
                    pass
            cur.execute("INSERT INTO matricula (aluno_id, disciplina_id) VALUES (?, ?)", [ide, disci])
            conn.commit()
            flash('Ótimo você se matriculou na disciplina!')
            return redirect(url_for('aluno',id = ide))
        else:
            cur.execute("INSERT INTO matricula (aluno_id, disciplina_id) VALUES (?, ?)",[ide,disci])
            conn.commit()
            flash('Ótimo você se matriculou na disciplina!')
            return redirect(url_for('aluno',id = ide))

    @app.route('/login/aluno/<id>/matriculado')
    def minhas_disciplinas(id):
        historico=[]
        disciplinas=[]
        cur.execute("SELECT * FROM matricula where aluno_id = ?",[id])
        matriculas = cur.fetchall()
        for matricula in matriculas:
            cur.execute("SELECT * FROM disciplinas where id = ?", [matricula[1]])
            disciplinas_name = cur.fetchall()
            disciplinas.append(disciplinas_name)
        for matricula in matriculas:
            for disciplina in disciplinas_name:
                print(disciplina)
                print(matricula)
                historico.append([disciplina[2],disciplina[3],matricula[3],matricula[4],matricula[5]])
        print(historico)
        return render_template("historico.html",hist = historico)



    # @app.route('/lista_disciplinas/<int:ide>', methods=['POST'])
    # def excluir_disciplina(ide):
    #     disciplina_to_del = Disciplinas.query.filter_by(id = ide).frist()
    #     if request.method == 'POST':
    #         if disciplina_to_del:
    #             db.session.delete(disciplina_to_del)
    #             db.session.commit()
    #         else:
    #             flash('Disciplina não encontrada')
    #         return flash('Disciplina '+disciplina_to_del[3]+' excluida!');

    @app.route('/login/aluno/<id>')
    def aluno(id):
        user: Usuario = Usuario.query.filter_by(id=id).first()
        return render_template("aluno.html",usu=user, ident = id)

    @app.route('/login/professor/<id>')
    def professor(id):
        user: Usuario = Usuario.query.filter_by(id=id).first()
        return render_template("professor.html",usu=user)


    return app


