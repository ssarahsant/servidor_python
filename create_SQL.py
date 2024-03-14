# Importa a bilbioteca (conecta com os comandos do código com o workbench)
from mysql import connector

# Conecta ao servidor MySQL
conexao = connector.connect(
    host='localhost',
    user='root',
    password='senai'
)

# Cria um cursor para executar comando SQL
cursor = conexao.cursor()

# Cria o banco de dados 'pwbe_escola' se ele ainda não existir
cursor.execute("CREATE DATABASE IF NOT EXISTS pwbe_escola")

# Seleciona o banco de dados
cursor.execute('USE pwbe_escola')

# Cria a tabela 'dados_login'
cursor.execute('CREATE TABLE IF NOT EXISTS dados_login (id_professor INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), login VARCHAR(255), senha VARCHAR(255))')

# Cria a tabela 'turmas'
cursor.execute('CREATE TABLE IF NOT EXISTS turmas (id_turma INT AUTO_INCREMENT PRIMARY KEY, descricao VARCHAR(255))')

# Cria a tabela 'atividades'
cursor.execute('CREATE TABLE IF NOT EXISTS atividades (id_atividade INT AUTO_INCREMENT PRIMARY KEY, descricao VARCHAR(255))')

# Cria a tabela 'turmas_professor' com o relacionamento entre 'dados_login' e 'turmas'
cursor.execute('CREATE TABLE IF NOT EXISTS turmas_professor (id INT AUTO_INCREMENT PRIMARY KEY, id_professor INT, id_turma INT, FOREIGN KEY (id_professor) REFERENCES dados_login(id_professor), FOREIGN KEY(id_turma) REFERENCES turmas(id_turma))')

# Cria a tabela 'atividade_turma' cok o relacionamento entre 'turmas' e 'atividades'
cursor.execute('CREATE TABLE IF NOT EXISTS atividades_turma (id INT AUTO_INCREMENT PRIMARY KEY, id_turma INT, id_atividade INT, FOREIGN KEY (id_turma) REFERENCES turmas(id_turma), FOREIGN KEY (id_atividade) REFERENCES atividades(id_atividade)) ')

# Fecha o crusor e a conexão
# Informa que ja acabou as requsições e sobrecarregar  processameno devido a quanitdade de processamentos desencadeados pelas requisições
cursor.close()
conexao.close()

print("Banco de dados e tabelas criados com sucesso.")