from flask_sqlalchemy import SQLAlchemy
from config import app_config,app_active
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

config=app_config[app_active]

if __name__=='__main__':
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db=SQLAlchemy(app)
    migrate = Migrate(app,db)

    menager = Manager(app)
    menager.add_command('db',MigrateCommand)
else:
    db=SQLAlchemy(config.APP)

class Role(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(40),unique=True,nullable=False)

class Disciplinas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(40), unique=True, nullable=False)
    max = db.Column(db.Integer, nullable=True)
    n1 = db.Column(db.Integer, nullable=True)
    n2 = db.Column(db.Integer, nullable=True)
    n3 = db.Column(db.Integer, nullable=True)

    def __init__(self,descricao,max,n1,n2,n3):
        self.descricao=descricao
        self.max=max
        self.n1=n1
        self.n2=n2
        self.n3=n3

class Usuario(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(40),unique=True,nullable=False)
    senha = db.Column(db.String(40),nullable=False)
    disciplina_id = db.Column(db.Integer,db.ForeignKey(Disciplinas.id),nullable=True)
    role = db.Column(db.Integer,db.ForeignKey(Role.id),nullable=False)

    def __init__(self,nome,senha,disciplina_id,role):
        self.nome=nome
        self.senha=senha
        self.disciplina_id=disciplina_id
        self.role=role

if __name__=='__main__':
    menager.run()
