import sqlite3
from flask import Blueprint,Flask,render_template,request,flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import app_config,app_active
from model import Usuario


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
    conn = sqlite3.connect('database/minisigaa.db',check_same_thread=False)
    cur = conn.cursor()

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
                    print(user);
                    if user.role == 1:
                        return adm(user.id)
                    elif user.role == 2:
                        return aluno(user.id)
                    else:
                        return professor(user.id)
                else:
                    flash('Senha Incorreta tenta de novo ai!')
                    return redirect(url_for('login'))
            else:
                flash('Deu certo não tente ai de novo please!')
                return redirect(url_for('login_post'))

    @app.route('/adm/<id>')
    def adm(id):
        user: Usuario = Usuario.query.filter_by(id=id).first()
        return render_template("adm.html",usu=user)

    @app.route('/lista_alunos')
    def modal():
        cur.execute("SELECT * FROM usuario where role=2")
        alunos = cur.fetchall()
        return render_template("modalListar.html",alu=alunos);


    @app.route('/aluno/<id>')
    def aluno(id):
        user: Usuario = Usuario.query.filter_by(id=id).first()
        return render_template("aluno.html",usu=user)

    @app.route('/professor/<id>')
    def professor(id):
        user: Usuario = Usuario.query.filter_by(id=id).first()
        return render_template("professor.html",usu=user)


    return app


