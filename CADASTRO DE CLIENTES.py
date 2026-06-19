import json
import os
import re
import uuid
from datetime import datetime

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError as erro:
    raise RuntimeError("Tkinter não está disponível. Instale tkinter para usar a interface gráfica.") from erro

BASE_DIR = os.path.dirname(__file__)
ARQUIVO_CLIENTES = os.path.join(BASE_DIR, "clientes.json")

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
DIGITOS_REGEX = re.compile(r"\d")


def carregar_clientes():
    if not os.path.exists(ARQUIVO_CLIENTES):
        return []
    try:
        with open(ARQUIVO_CLIENTES, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except ValueError:
        print("Aviso: arquivo clientes.json está corrompido. Recriando base vazia.")
        return []
    except Exception as erro:
        print("Erro ao carregar clientes:", erro)
        return []


def salvar_clientes(clientes):
    with open(ARQUIVO_CLIENTES, "w", encoding="utf-8") as arquivo:
        json.dump(clientes, arquivo, indent=2, ensure_ascii=False)


def validar_email(email):
    return bool(EMAIL_REGEX.match(email.strip()))


def validar_cpf(cpf):
    digitos = "".join(DIGITOS_REGEX.findall(cpf))
    return len(digitos) == 11


def validar_telefone(telefone):
    digitos = "".join(DIGITOS_REGEX.findall(telefone))
    return 10 <= len(digitos) <= 11


def validar_dados(nome, telefone, email, cpf):
    erros = []
    if not nome.strip():
        erros.append("Nome é obrigatório.")
    if not validar_telefone(telefone):
        erros.append("Telefone inválido.")
    if not validar_email(email):
        erros.append("Email inválido.")
    if not validar_cpf(cpf):
        erros.append("CPF deve ter 11 dígitos.")
    return erros


def validar_duplicidade(clientes, email, cpf, cliente_atual=None):
    for cliente in clientes:
        if cliente_atual is not None and cliente["id"] == cliente_atual["id"]:
            continue
        if cliente["cpf"] == cpf:
            return "CPF já cadastrado."
        if cliente["email"] == email:
            return "E-mail já cadastrado."
    return None


def encontrar_clientes_por_nome(clientes, nome):
    termo = nome.upper().strip()
    return [c for c in clientes if termo in c["nome"]]


class CadastroClientesGUI:
    def __init__(self):
        self.clientes = carregar_clientes()
        self.selecionado_id = None
        self.root = tk.Tk()
        self.root.title("Cadastro de Clientes")
        self.criar_componentes()
        self.carregar_clientes_na_lista()
        self.root.mainloop()

    def criar_componentes(self):
        frame_esquerdo = tk.Frame(self.root)
        frame_esquerdo.pack(side="left", padx=10, pady=10, fill="y")

        self.listbox = tk.Listbox(frame_esquerdo, width=45, height=20)
        self.listbox.pack(side="left", fill="y")
        self.listbox.bind("<<ListboxSelect>>", self.on_selecao)

        scrollbar = tk.Scrollbar(frame_esquerdo, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        frame_direito = tk.Frame(self.root)
        frame_direito.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        campos = [("Nome", "nome"), ("Telefone", "telefone"), ("E-mail", "email"), ("CPF", "cpf")]
        self.entradas = {}
        for idx, (rotulo, chave) in enumerate(campos):
            tk.Label(frame_direito, text=rotulo).grid(row=idx, column=0, sticky="w", pady=4)
            entrada = tk.Entry(frame_direito, width=40)
            entrada.grid(row=idx, column=1, pady=4)
            self.entradas[chave] = entrada

        botoes = tk.Frame(frame_direito)
        botoes.grid(row=len(campos), column=0, columnspan=2, pady=8)

        tk.Button(botoes, text="Cadastrar", width=12, command=self.cadastrar_gui).grid(row=0, column=0, padx=4)
        tk.Button(botoes, text="Atualizar", width=12, command=self.atualizar_gui).grid(row=0, column=1, padx=4)
        tk.Button(botoes, text="Excluir", width=12, command=self.excluir_gui).grid(row=0, column=2, padx=4)
        tk.Button(botoes, text="Limpar", width=12, command=self.limpar_formulario).grid(row=0, column=3, padx=4)

        tk.Label(frame_direito, text="Buscar por nome:").grid(row=len(campos) + 1, column=0, sticky="w", pady=4)
        self.busca_entry = tk.Entry(frame_direito, width=40)
        self.busca_entry.grid(row=len(campos) + 1, column=1, pady=4)

        tk.Button(frame_direito, text="Buscar", width=12, command=self.buscar_gui).grid(
            row=len(campos) + 2, column=0, columnspan=2, pady=4
        )
        tk.Button(frame_direito, text="Mostrar todos", width=12, command=self.carregar_clientes_na_lista).grid(
            row=len(campos) + 3, column=0, columnspan=2, pady=4
        )

        self.status = tk.Label(self.root, text="", anchor="w")
        self.status.pack(fill="x", padx=10, pady=6)

    def carregar_clientes_na_lista(self, clientes=None):
        self.listbox.delete(0, tk.END)
        self.clientes = clientes if clientes is not None else carregar_clientes()
        for cliente in self.clientes:
            self.listbox.insert(tk.END, "{} ({})".format(cliente["nome"], cliente["email"]))
        self.status["text"] = "{} cliente(s) exibido(s)".format(len(self.clientes))
        self.selecionado_id = None
        self.limpar_formulario()

    def on_selecao(self, event):
        selecionados = self.listbox.curselection()
        if not selecionados:
            return
        cliente = self.clientes[selecionados[0]]
        self.selecionado_id = cliente["id"]
        for chave, entrada in self.entradas.items():
            entrada.delete(0, tk.END)
            entrada.insert(0, cliente.get(chave, ""))

    def ler_campos_gui(self):
        return {
            "nome": self.entradas["nome"].get().strip(),
            "telefone": self.entradas["telefone"].get().strip(),
            "email": self.entradas["email"].get().strip(),
            "cpf": self.entradas["cpf"].get().strip(),
        }

    def limpar_formulario(self):
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)
        self.selecionado_id = None
        self.listbox.selection_clear(0, tk.END)

    def cadastrar_gui(self):
        dados = self.ler_campos_gui()
        erros = validar_dados(dados["nome"], dados["telefone"], dados["email"], dados["cpf"])
        if erros:
            messagebox.showerror("Erro de validação", "\n".join(erros))
            return
        duplicidade = validar_duplicidade(self.clientes, dados["email"].upper(), dados["cpf"])
        if duplicidade:
            messagebox.showerror("Erro de validação", duplicidade)
            return
        novo = {
            "id": str(uuid.uuid4()),
            "nome": dados["nome"].upper(),
            "telefone": dados["telefone"],
            "email": dados["email"].upper(),
            "cpf": dados["cpf"],
            "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.clientes.append(novo)
        salvar_clientes(self.clientes)
        self.carregar_clientes_na_lista()
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso.")

    def atualizar_gui(self):
        if not self.selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um cliente para atualizar.")
            return
        dados = self.ler_campos_gui()
        erros = validar_dados(dados["nome"], dados["telefone"], dados["email"], dados["cpf"])
        if erros:
            messagebox.showerror("Erro de validação", "\n".join(erros))
            return
        cliente = next((c for c in self.clientes if c["id"] == self.selecionado_id), None)
        if not cliente:
            messagebox.showerror("Erro", "Cliente não encontrado.")
            return
        duplicidade = validar_duplicidade(self.clientes, dados["email"].upper(), dados["cpf"], cliente_atual=cliente)
        if duplicidade:
            messagebox.showerror("Erro de validação", duplicidade)
            return
        cliente.update({
            "nome": dados["nome"].upper(),
            "telefone": dados["telefone"],
            "email": dados["email"].upper(),
            "cpf": dados["cpf"],
        })
        salvar_clientes(self.clientes)
        self.carregar_clientes_na_lista()
        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso.")

    def excluir_gui(self):
        if not self.selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um cliente para excluir.")
            return
        cliente = next((c for c in self.clientes if c["id"] == self.selecionado_id), None)
        if not cliente:
            messagebox.showerror("Erro", "Cliente não encontrado.")
            return
        if not messagebox.askyesno("Confirmar", "Deseja excluir este cliente?"):
            return
        self.clientes.remove(cliente)
        salvar_clientes(self.clientes)
        self.carregar_clientes_na_lista()
        messagebox.showinfo("Sucesso", "Cliente excluído com sucesso.")

    def buscar_gui(self):
        nome = self.busca_entry.get().strip()
        if not nome:
            self.carregar_clientes_na_lista()
            return
        resultados = encontrar_clientes_por_nome(self.clientes, nome)
        self.carregar_clientes_na_lista(resultados)


if __name__ == "__main__":
    CadastroClientesGUI()
