# Importação ds bilbiotecas para serem instanciadas
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Define a porta em que o sericodr vai escutar
port = 8000

# Define o manipulador de requesições
handler = SimpleHTTPRequestHandler

# Cria uma instancia do servidor
server = HTTPServer(('localhost', port), handler)

# Imprime uma mensagem indicando que o sericor está rodando
print(f"Servidor rodando em http://localhost:{port}")

# Inicia o servidor
server.serve_forever()
