# interface.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry

from Controller import ControllerPerfilProdutor
from PerfilProdutor import PerfilProdutor


class CadastrosView:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Análise de Solo")

        try:
            self.root.state("zoomed")
        except:
            try:
                self.root.attributes("-zoomed", True)
            except:
                self.root.geometry("1200x700")

        self.controller = ControllerPerfilProdutor()

        self._criar_interface()

        self._configurar_expansao()

        self._listar()

    def _configurar_expansao(self):
        """Permite expansão completa em tela cheia."""
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.frame.grid_columnconfigure(0, weight=0)   # labels
        self.frame.grid_columnconfigure(1, weight=1)   # campos
        self.frame.grid_columnconfigure(2, weight=1)   # lista

        for i in range(30):
            self.frame.grid_rowconfigure(i, weight=1)

    def _criar_interface(self):
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Produtor:").grid(row=0, column=0, sticky="e")
        self.e_produtor = tk.Entry(self.frame)
        self.e_produtor.grid(row=0, column=1, pady=3, sticky="ew")

        tk.Label(self.frame, text="Fazenda / Observações:").grid(row=1, column=0, sticky="ne")
        self.e_fazenda = tk.Text(self.frame, height=3)
        self.e_fazenda.grid(row=1, column=1, pady=3, sticky="nsew")

        tk.Label(self.frame, text="Talhão:").grid(row=2, column=0, sticky="e")
        self.e_talhao = tk.Entry(self.frame)
        self.e_talhao.grid(row=2, column=1, pady=3, sticky="ew")

        tk.Label(self.frame, text="Tipo de Solo:").grid(row=3, column=0, sticky="e")
        self.e_solo = ttk.Combobox(
            self.frame,
            state="readonly",
            values=[
                "Argissolo", "Latossolo", "Neossolo", "Nitossolo",
                "Chernossolo", "Gleissolo", "Vertissolo", "Planossolo"
            ]
        )
        self.e_solo.grid(row=3, column=1, pady=3, sticky="ew")

        campos = ["PH", "P", "K", "Mg", "Ca", "S"]
        self.quimicos = {}

        linha = 4
        for c in campos:
            tk.Label(self.frame, text=f"{c}:").grid(row=linha, column=0, sticky="e")
            e = tk.Entry(self.frame)
            e.grid(row=linha, column=1, pady=3, sticky="ew")
            self.quimicos[c.lower()] = e
            linha += 1

        tk.Label(self.frame, text="Data da Coleta:").grid(row=linha, column=0, sticky="e")
        self.e_data = DateEntry(self.frame, date_pattern="dd/mm/yyyy")
        self.e_data.grid(row=linha, column=1, pady=3, sticky="w")
        linha += 1

        # LISTA
        self.lista = tk.Listbox(self.frame)
        self.lista.grid(row=0, column=2, rowspan=15, padx=20, sticky="nsew")
        self.lista.bind("<<ListboxSelect>>", self._selecionar)

        # BOTÕES
        self.btn_frame = tk.Frame(self.frame)
        self.btn_frame.grid(row=linha, column=0, columnspan=3, pady=20)

        tk.Button(self.btn_frame, text="Adicionar", width=12, command=self.adicionar).grid(row=0, column=0, padx=5)
        tk.Button(self.btn_frame, text="Atualizar", width=12, command=self.atualizar).grid(row=0, column=1, padx=5)
        tk.Button(self.btn_frame, text="Remover", width=12, command=self.remover).grid(row=0, column=2, padx=5)
        tk.Button(self.btn_frame, text="Imprimir PDF", width=12, command=self.imprimir).grid(row=0, column=3, padx=5)
        tk.Button(self.btn_frame, text="Limpar", width=12, command=self.limpar).grid(row=0, column=4, padx=5)

    def _listar(self):
        self.lista.delete(0, tk.END)
        for c in self.controller.cadastros:
            self.lista.insert(tk.END, c.produtor)

    def _selecionar(self, event):
        sel = self.lista.curselection()
        if not sel:
            return

        nome = self.lista.get(sel[0])
        c = self.controller.buscar(nome)

        self.e_produtor.delete(0, tk.END)
        self.e_produtor.insert(0, c.produtor)

        self.e_fazenda.delete("1.0", tk.END)
        self.e_fazenda.insert(tk.END, c.fazenda)

        self.e_talhao.delete(0, tk.END)
        self.e_talhao.insert(0, c.talhao)

        self.e_solo.set(c.tipo_solos)

        self.quimicos["ph"].delete(0, tk.END)
        self.quimicos["ph"].insert(0, c.ph)

        self.quimicos["p"].delete(0, tk.END)
        self.quimicos["p"].insert(0, c.p)

        self.quimicos["k"].delete(0, tk.END)
        self.quimicos["k"].insert(0, c.k)

        self.quimicos["mg"].delete(0, tk.END)
        self.quimicos["mg"].insert(0, c.mg)

        self.quimicos["ca"].delete(0, tk.END)
        self.quimicos["ca"].insert(0, c.ca)

        self.quimicos["s"].delete(0, tk.END)
        self.quimicos["s"].insert(0, c.s)

        try:
            self.e_data.set_date(c.data_coleta)
        except:
            pass

    def montar_perfil(self):
        produtor = self.e_produtor.get().strip()
        fazenda = self.e_fazenda.get("1.0", "end-1c").strip()
        talhao = self.e_talhao.get().strip()
        solo = self.e_solo.get().strip()
        ph = self.quimicos["ph"].get().strip()
        p = self.quimicos["p"].get().strip()
        k = self.quimicos["k"].get().strip()
        mg = self.quimicos["mg"].get().strip()
        ca = self.quimicos["ca"].get().strip()
        s = self.quimicos["s"].get().strip()

        if not produtor:
            messagebox.showerror("Erro", "O campo PRODUTOR é obrigatório.")
            return None

        if not fazenda:
            messagebox.showerror("Erro", "O campo FAZENDA é obrigatório.")
            return None

        if not talhao:
            messagebox.showerror("Erro", "O campo TALHÃO é obrigatório.")
            return None

        if not solo:
            messagebox.showerror("Erro", "Selecione o TIPO DE SOLO.")
            return None

        if not ph:
            messagebox.showerror("Erro", "O campo PH é obrigatório.")
            return None

        if not p:
            messagebox.showerror("Erro", "O campo P é obrigatório.")
            return None

        if not k:
            messagebox.showerror("Erro", "O campo K é obrigatório.")
            return None

        if not mg:
            messagebox.showerror("Erro", "O campo Mg é obrigatório.")
            return None

        if not ca:
            messagebox.showerror("Erro", "O campo Ca é obrigatório.")
            return None

        if not s:
            messagebox.showerror("Erro", "O campo S é obrigatório.")
            return None

        try:
            ph = float(self.quimicos["ph"].get())
            p = float(self.quimicos["p"].get())
            k = float(self.quimicos["k"].get())
            mg = float(self.quimicos["mg"].get())
            ca = float(self.quimicos["ca"].get())
            s = float(self.quimicos["s"].get())

        except:
            messagebox.showerror("Erro", "Os valores químicos devem ser números.")
            return None

        try:
            produtor = str(self.e_produtor["produtor"].get())
            fazenda = str(self.e_fazenda["fazenda"].get())

        except:
            messagebox.showerror("Erro", "Os campos Produtor e Fazenda devem ser em formado de texto.")
            return None

        return PerfilProdutor(
            produtor,
            solo,
            fazenda,
            talhao,
            ph, p, k, mg, ca, s,
            self.e_data.get()
        )

    def adicionar(self):
        perfil = self.montar_perfil()
        if perfil and self.controller.criar(perfil):
            messagebox.showinfo("Sucesso", "Cadastro salvo.")
            self._listar()
            self.limpar()

    def atualizar(self):
        perfil = self.montar_perfil()
        if perfil and self.controller.alterar(perfil):
            messagebox.showinfo("Sucesso", "Cadastro atualizado.")
            self._listar()

    def remover(self):
        sel = self.lista.curselection()
        if not sel:
            return
        nome = self.lista.get(sel[0])
        if self.controller.deletar(nome):
            messagebox.showinfo("Sucesso", "Removido.")
            self._listar()
            self.limpar()

    def imprimir(self):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showerror("Erro", "Selecione um item.")
            return

        nome = self.lista.get(sel[0])
        perfil = self.controller.buscar(nome)

        caminho = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile=f"{perfil.produtor}.pdf"
        )

        if caminho:
            perfil.imprimir_cadastro(caminho)
            messagebox.showinfo("OK", "PDF gerado!")

    def limpar(self):
        self.e_produtor.delete(0, tk.END)
        self.e_fazenda.delete("1.0", tk.END)
        self.e_talhao.delete(0, tk.END)
        self.e_solo.set("")
        for e in self.quimicos.values():
            e.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    CadastrosView(root)
    root.mainloop()
