from flask_sqlalchemy import SQLAlchemy
from config import app_config,app_active
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from datetime import datetime
config=app_config[app_active]

if __name__=='__main__':
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db=SQLAlchemy(app)
    migrate = Migrate(app,db)

    menager = Manager(app)
    menager.add_command('db',MigrateCommand)
else:
    db=SQLAlchemy(config.APP)

class Role(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(40),unique=True,nullable=False)

class Usuario(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(40),unique=True,nullable=False)
    senha = db.Column(db.String(40),nullable=False)
    ultimo_login = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.Integer,db.ForeignKey(Role.id),nullable=False)
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.ultimo_login=datetime.now()

class Disciplinas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(40), unique=True, nullable=False)
    codigo = db.Column(db.Integer, unique=True, nullable=False)
    max = db.Column(db.Integer, nullable=False)
    professor_id = db.Column(db.Integer,db.ForeignKey(Usuario.id),nullable=True)
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)

class Matricula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer,db.ForeignKey(Usuario.id),nullable=False)
    disciplina_id = db.Column(db.Integer,db.ForeignKey(Disciplinas.id),nullable=False)
    n1 = db.Column(db.Integer, nullable=True)
    n2 = db.Column(db.Integer, nullable=True)
    n3 = db.Column(db.Integer, nullable=True)
    def __init__(self,aluno_id,disciplina_id,n1,n2,n3):
        self.aluno_id =aluno_id
        self.disciplina_id = disciplina_id
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
if __name__=='__main__':
    menager.run()
