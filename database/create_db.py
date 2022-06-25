import sqlite3

banco = sqlite3.connect('minisigaa.db')

con = banco.cursor()

# def con_db(scr):
#     con.execute(scr)
#     con.close()

# con.execute("CREATE TABLE alunos(id integer, nome text, senha text, disciplina_id integer,role integer)")
# con.execute("CREATE TABLE disciplinas(id integer, descricao text, max integer,n1 integer,n2 integer,n3 integer)")
# con.execute("CREATE TABLE professores(id integer, nome text, senha text, disciplina_id integer,role integer))")
# con.execute("CREATE TABLE adm(id integer, login text, senha text,role integer))")

# con.execute("INSERT INTO adm VALUES (1,'admin','admin')")


