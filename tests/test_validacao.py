import importlib.util
import os
import sys
import types

BASE_DIR = os.path.dirname(__file__)
arquivo_principal = os.path.abspath(os.path.join(BASE_DIR, "..", "CADASTRO DE CLIENTES.py"))

if "tkinter" not in sys.modules:
    tk = types.ModuleType("tkinter")
    tk.messagebox = types.ModuleType("tkinter.messagebox") # type: ignore
    sys.modules["tkinter"] = tk
    sys.modules["tkinter.messagebox"] = tk.messagebox

spec = importlib.util.spec_from_file_location("cadastro_clientes", arquivo_principal)
if spec is None or spec.loader is None:
    raise ImportError("Não foi possível importar CADASTRO DE CLIENTES.py")
cadastro = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cadastro)

validar_email = cadastro.validar_email
validar_cpf = cadastro.validar_cpf
validar_telefone = cadastro.validar_telefone
validar_dados = cadastro.validar_dados

def test_validar_email():
    assert validar_email("teste@dominio.com")
    assert not validar_email("email-invalido")

def test_validar_cpf():
    assert validar_cpf("123.456.789-09")
    assert not validar_cpf("123")

def test_validar_telefone():
    assert validar_telefone("(11) 98765-4321")
    assert not validar_telefone("123")

def test_validar_dados():
    erros = validar_dados("João", "11987654321", "joao@dominio.com", "12345678909")
    assert erros == []
    erros = validar_dados("", "email", "123", "111")
    assert len(erros) == 4
