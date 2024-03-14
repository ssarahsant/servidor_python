# Código de funções para realizar comunicações com o banco
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "senai",
        database = "pwbe_escola"
    )
