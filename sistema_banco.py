import os
# possibilita a manipulação do servidor 
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import urlparse, parse_qs

# importar a função (do outro arquivo) para salvar os dados no banco de dados
from database import conectar 

# Atribui para uma variaveis a função do outro arquivo
conexao = conectar()

# Importa a bilbioteca (conecta com os comandos do código com o workbench)
from mysql import connector



# biblioteca que cipritografa as senhas
import hashlib

# CRIAÇÃO DO SERVIDOR
class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            # Tenta abrir o arquivo idx.html
            f = open(os.path.join(path, 'login.html'), 'r')
            # Se existir, envia o conteúdo do arquivo
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close()
            return None
        except FileNotFoundError:
            pass

        return super().list_directory(path)
    

    # CANAL DE COMUNICAÇÃO
    def do_GET(self):
        if self.path == '/login':
            # Tenta abrir o arquivo login.html
            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r') as login_file:
                    content = login_file.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File not found")

        # criação de rota para página de suscesso de login
        elif self.path == '/usuario_cadastrado':
            try:
                # Responde ao cliente com a menssagem de login/senha incorreta
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                # Lê o conteúdo da página html
                with open(os.path.join(os.getcwd(), 'sucesso.html'), 'r', encoding='utf-8') as login_file:
                    content = login_file.read()            
                self.wfile.write(content.encode('utf-8'))
                
            except FileNotFoundError:
                self.send_error(404, "File not found")

        # criação de rota para página de erro
        elif self.path == '/login_failed':
            try:
                # Responde ao cliente com a menssagem de login/senha incorreta
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                # Lê o conteúdo da página html
                with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                    content = login_file.read()

                    # Adiciona a mensagem de erro no conteúdo da página
                mensagem = "Login e/ou senha incorreta. Tente novamente"
                content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                        f'<div class="error-message">{mensagem}</div>')
                
                self.wfile.write(content.encode('utf-8'))
            
            except FileNotFoundError:
                self.send_error(404, "File not found")


        # criação do usuário não existente 
        elif self.path.startswith('/cadastro'):
            try:
                # Extraindo os parâmetros da URL
                query_params = parse_qs(urlparse(self.path).query)
                login = query_params.get('login', [''])[0]
                senha = query_params.get('senha', [''])[0]

                # Mensagem de boas-vindas
                welcome_message = f"Olá {login}, seja bem-vindo! Percebemos que você é novo por aqui. Complete o seu cadastro."

                # Responde ao cliente com a página de cadastro
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()

                # Lê o conteúdo da página cadastro.html
                with open(os.path.join(os.getcwd(), 'cadastro.html'), 'r', encoding='utf-8') as cadastro_file:
                    content = cadastro_file.read()

                # Substitui os marcadores de posição pelos valores correspondentes
                content = content.replace('{login}', login)
                content = content.replace('{senha}', senha)
                content = content.replace('{welcome_message}', welcome_message)

                # Envia o conteúdo modificado para o cliente
                self.wfile.write(content.encode('utf-8'))
                return  # Adicionando um return para evitar a execução do restante do código
            
            except FileNotFoundError:
                self.send_error(404, "File not found")
        
        # criação de rota para página de suscesso do cadastro da turma
        elif self.path == '/cad_turma':
            try:
                # fazer try
                # Responde ao cliente com a menssagem de login/senha incorreta
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                # Lê o conteúdo da página html
                with open(os.path.join(os.getcwd(), 'cadastro_turma.html'), 'r', encoding='utf-8') as login_file:
                    content = login_file.read()            
                self.wfile.write(content.encode('utf-8'))

            except FileNotFoundError:
                self.send_error(404, "File not found")

        # criação de rota para página de erro do cadastro de turma
        elif self.path == '/failed_turma':
            try:
                # Responde ao cliente com a menssagem de login/senha incorreta
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                # Lê o conteúdo da página html
                with open(os.path.join(os.getcwd(), 'erro.html'), 'r', encoding='utf-8') as login_file:
                    content = login_file.read()            
                self.wfile.write(content.encode('utf-8'))

            except FileNotFoundError:
                self.send_error(404, "File not found")

          # criação de rota para página de suscesso do cadastro da turma
        elif self.path == '/cad_ativ':
            try:
                # Responde ao cliente com a menssagem de login/senha incorreta
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                # Lê o conteúdo da página html
                with open(os.path.join(os.getcwd(), 'cadastro_atividade.html'), 'r', encoding='utf-8') as login_file:
                    content = login_file.read()            
                self.wfile.write(content.encode('utf-8'))

            except FileNotFoundError:
                self.send_error(404, "File not found")

        else:
            # Se não for a rota "/login", continua com o comportamento padrão
            super().do_GET()

    # FUNÇÕES PARA REAIZAR AS VALIDAÇÕES DE LOGIN 

    # Função para adicionar um professor não cadastrado no banco 
    def usuario_existente(self, login, senha):
        # Atribui para uma variavel os comando do banco de dados através de uma biblioteca para  programa em python
        cursor = conexao.cursor()
        # Seeleciona a tabelaonde se armazena os dados de login
        cursor.execute("SELECT senha FROM dados_login WHERE login = %s", (login,))
        # Faz a leitura linha a lina da tabela localizada no banco de dados 
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:           
            senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest() 
            return senha_hash == resultado[0]
        return False
    
    
    # Função para verificar se o Login do Professor ja existe no banco
    def adicionar_usuario(self, login, senha, nome):
        cursor = conexao.cursor()
        # Criptografa a senha antes de ser inseridade no banco
        senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
        # Comando que insere os valores no banco de dados
        cursor.execute("INSERT INTO dados_login (login,senha,nome) VALUES (%s, %s, %s)", (login,senha_hash,nome))
        conexao.commit()
        cursor.close()

    # Funções para Cadastro da Turma
    def turma_existente(self,  turma):
        # Atribui para uma variavel os comando do banco de dados através de uma biblioteca para  programa em python
        cursor = conexao.cursor()
        # Seleciona a tabelaonde se armazena o nome da turma
        cursor.execute("SELECT descricao FROM turmas WHERE descricao = %s", (turma,))
        # Faz a leitura linha a lina da tabela localizada no banco de dados 
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:         
            # Se tiver conteúdo retrona verdadeiro para o post  
            return True
        # Se NÃO tiver conteúdo retrona falso para o post  
        return False
    
    def adicionar_turma(self, turma, id_professor):
        cursor = conexao.cursor()
        # Comando que insere os valores no banco de dados
        cursor.execute("INSERT INTO turmas (descricao) VALUES (%s)", (turma,))
        cursor.execute("SELECT id_turma FROM turmas WHERE descricao = %s", (turma,))
        resultado = cursor.fetchone()
        cursor.execute("INSERT INTO turmas_professor (id_turma, id_professor) VALUES (%s, %s)", (resultado[0], id_professor))
        conexao.commit()
        cursor.close()
 
    
    # Função que irá carregar as turmas do professor  na tela
    def carrega_turmas_professor (self, login):
        cursor = conexao.cursor()
        cursor.execute("SELECT id_professor, nome FROM dados_login WHERE login = %s", (login,))
        resultado = cursor.fetchone()
        cursor.close()

        # resultado[0] atrás do id_professor e resultado[1] trás o nome do professor
        id_professor = resultado[0]

        # código para obter as turmas do professor
        cursor = conexao.cursor()
        cursor.execute ("SELECT turmas.id_turma, turmas.descricao FROM turmas_professor INNER JOIN turmas ON turmas_professor.id_turma = turmas.id_turma WHERE turmas_professor.id_professor = %s", (id_professor,))
        turmas = cursor.fetchall()
        cursor.close()

        # Construindo dinamicamente as linhas da tabela com as turmas do professor
        linhas_tabela = ""
        for turma in turmas:
            id_turma = turma[0]
            descricao_turma = turma[1]
            link_atividade = "<button id='excluir' type='submit'>Excluir</button> <button id='visualizar' type='submit'>Visualizar</button>"
            linha = "<tr><td style='text-align:center'>{}</td><td style='text-align:center'>{}</td></tr>".format(
                descricao_turma, link_atividade)
            linhas_tabela += linha

        with open(os.path.join(os.getcwd(), 'cadastro_turma.html'), 'r', encoding='utf-8') as cad_turma_file:
            content = cad_turma_file.read()
            content = content.replace('{nome_professor}', resultado[1])
            content = content.replace('{id_professor}', str(id_professor))
            content = content.replace('{login}', str(login))

        # Substituindo o marcador de posição pelas linhas da tabela
        content = content.replace('<!-- teste -->', linhas_tabela)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        self.wfile.write(content.encode('utf-8'))


    # Funções para Cadastro da Atividade
    def atividade_existente(self, descricao):
        # Atribui para uma variavel os comando do banco de dados através de uma biblioteca para  programa em python
        cursor = conexao.cursor()
        # Seleciona a tabelaonde se armazena a descrição da atividade
        cursor.execute("SELECT descricao FROM atividades WHERE descricao = %s", (descricao,))
        # Faz a leitura linha a lina da tabela localizada no banco de dados 
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:         
            # Se tiver conteúdo retrona verdadeiro para o post  
            return True
        # Se NÃO tiver conteúdo retrona falso para o post  
        return False
    
    def adicionar_atividade(self, descricao):
        cursor = conexao.cursor()
        # Comando que insere os valores no banco de dados
        cursor.execute("INSERT INTO atividades (descricao) VALUES (%s)", (descricao,))
        conexao.commit()
        cursor.close()
    

    # Captura dos dados do formulário através do 'action' inserir nor 'form'
    def do_POST(self):
        # Usuário logado com Sucesso
        # Verifica se a rota é "/enviar_login"
        if self.path == '/enviar_login':
            content_length = int(self.headers['Content-Length'])
            # Lê o corpo da requisição
            body = self.rfile.read(content_length).decode('utf-8')
            # Parseia os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)

            # Verifica se o usuário já existe
            login = form_data.get('email', [''])[0]
            senha = form_data.get('senha', [''])[0]

            if self.usuario_existente(login, senha):
                self.carrega_turmas_professor(login)
                # Substitui pela função carregar turmas (que abrira a pagina de cadastro de turmas com as turmas existentes)
                # # Responde ao cliente indicando que o usuário logou com sucesso
                # self.send_response(302)
                # self.send_header('Location', '/cad_turma')
                # self.end_headers()
                # # Adicionando um return para evitar a execução do restante do código
                # return  
                       
            else:
                # Verifica se o usuario já está cadastrado. Caso não esteja foi caso de login errado
                cursor = conexao.cursor()
                cursor.execute("SELECT login FROM dados_login WHERE login = %s", (login,))
                resultado = cursor.fetchone()

                # Verifica se o login já existe no arquivo
                if resultado:
                    # Redireciona o cliente para a rota "/login_failed"
                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    cursor.close()
                    # Adicionando um return para evitar a execução do restante do código
                    return 

                else:
                    # Redireciona o cliente para a rota "/cadastro" com os dados de login e senha
                    # self.adicionar_usuário(login, senha, nome='None')
                    self.send_response(302)
                    self.send_header('Location', f'/cadastro?login={login}&senha={senha}')
                    self.end_headers()
                    cursor.close()
                    # Adicionando um return para evitar a execução do restante do código
                    return  


        elif self.path.startswith('/confirmar_cadastro'):
            # Obtém o comprimento do corpo da requisição
            content_length = int(self.headers['Content-Length'])
            # Lê o corpo da requisição
            body = self.rfile.read(content_length).decode('utf-8')
            # Parseia os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)

            #query_params = parse_qs(urlparse(self.path).query)
            login = form_data.get('email', [''])[0]
            senha = form_data.get('senha', [''])[0]
            nome = form_data.get('nome', [''])[0]

            # senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()

            # Chama a função para adicionar o usuário
            self.adicionar_usuario(login, senha, nome)

            # A apresenta a rota de sucesso
            self.send_response(302)
            self.send_header('Location', '/cad_turma')
            self.end_headers()
            return


        # CADASTRAR TURMA
        elif self.path == '/cad_turma':
            # CAPTURA AS INFORMAÇÕES
            content_length = int(self.headers['Content-Length'])
            # Lê o corpo da requisição
            body = self.rfile.read(content_length).decode('utf-8')
            # Parseia os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)
            turma = form_data.get('turma', [''])[0]
            id_professor = form_data.get('id_professor', [''])[0]
            login = form_data.get('login', [''])[0]
        
            print(f"Cad_turma, dados do formulário {turma}, {id_professor}")


            # Verifica se o valor está vazio e da erro
            if turma.strip() == '':
                # Se algum campo estiver vazio, redireciona para a página de falha cadastro 
                self.send_response(302)
                self.send_header("Location", "/failed_turma")
                self.end_headers()
                return
        
            # Verifica se já existe
            elif self.turma_existente(turma) == True:
                # Se algum campo estiver vazio, redireciona para a página de falha cadastro 
                self.send_response(302)
                self.send_header("Location", "/failed_turma")
                self.end_headers()
                return

            # Adiciona a turma
            else:
                self.adicionar_turma(turma, id_professor)
                self.carrega_turmas_professor(login)
                # self.send_response(302)
                # self.send_header('Location', '/usuario_cadastrado')
                # self.end_headers()
                # return
            

        # CADASTRAR ATIVIDADE
        elif self.path == '/cad_ativ':
            # Cadastra a turma se ela não existir
            content_length = int(self.headers['Content-Length'])
            # Lê o corpo da requisição
            body = self.rfile.read(content_length).decode('utf-8')
            # Parseia os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)

            descricao = form_data.get('descricao', [''])[0]

            # Verifica se o valor está vazio e da erro
            if descricao.strip() == '':
                # Se algum campo estiver vazio, redireciona para a página de falha cadastro 
                self.send_response(302)
                self.send_header("Location", "/failed_turma")
                self.end_headers()
                return
        
            # Verifica se o usuário já existe
            elif self.atividade_existente(descricao) == True:
                # Se algum campo estiver vazio, redireciona para a página de falha cadastro 
                self.send_response(302)
                self.send_header("Location", "/failed_turma")
                self.end_headers()
                return

            # Adiciona a atividade
            else:
                self.adicionar_atividade(descricao)
                self.send_response(302)
                self.send_header('Location', '/usuario_cadastrado')
                self.end_headers()
                return
            

        else:
            # Se não for a rota "/enviar_login", continua com o comportamento padrão
            super(MyHandler, self).do_POST()


# Define o IP e a porta a serem utilizados
endereco_ip = "0.0.0.0"
porta = 8000

# Cria um servidor na porta e IP especificados
with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor iniciado em {endereco_ip}:{porta}")
    # Mantém o servidor em execução
    httpd.serve_forever()