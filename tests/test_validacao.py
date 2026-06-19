import os
from validacao import validar_email, validar_cpf, validar_telefone, validar_dados_cliente

def test_validar_email():
    assert validar_email("teste@dominio.com")
    assert not validar_email("email-invalido")

def test_validar_cpf():
    assert validar_cpf("123.456.789-09")
    assert not validar_cpf("123")

def test_validar_telefone():
    assert validar_telefone("(11) 98765-4321")
    assert not validar_telefone("123")

def test_validar_dados_cliente():
    erros = validar_dados_cliente("João", "joao@dominio.com", "11987654321", "12345678909", "Rua A")
    assert erros == []
    erros = validar_dados_cliente("", "email", "123", "111", "")
    assert len(erros) == 4
