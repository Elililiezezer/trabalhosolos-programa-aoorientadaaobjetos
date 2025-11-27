# PerfilProdutor.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap

class PerfilProdutor:
    def __init__(self, produtor, tipo_solos, fazenda, talhao,
                 ph, p, k, mg, ca, s, data_coleta):

        self.produtor = produtor
        self.tipo_solos = tipo_solos
        self.fazenda = fazenda
        self.talhao = talhao

        self.ph = float(ph)
        self.p = float(p)
        self.k = float(k)
        self.mg = float(mg)
        self.ca = float(ca)
        self.s = float(s)

        self.data_coleta = data_coleta

    def imprimir_cadastro(self, caminho):
        c = canvas.Canvas(caminho, pagesize=A4)
        w, h = A4
        x = 50
        y = h - 50

        c.setFont("Helvetica-Bold", 18)
        c.drawString(x, y, f"Produtor: {self.produtor}")
        y -= 35

        c.setFont("Helvetica", 12)
        c.drawString(x, y, f"Data da Coleta: {self.data_coleta}")
        y -= 20

        c.drawString(x, y, f"Tipo de Solo: {self.tipo_solos}")
        y -= 20

        c.drawString(x, y, f"Talhão: {self.talhao}")
        y -= 30

        c.setFont("Helvetica-Bold", 14)
        c.drawString(x, y, "Análise Química do Solo:")
        y -= 25

        c.setFont("Helvetica", 12)
        for nome, valor in [
            ("pH", self.ph), ("P", self.p), ("K", self.k),
            ("Mg", self.mg), ("Ca", self.ca), ("S", self.s)
        ]:
            c.drawString(x + 10, y, f"{nome}: {valor}")
            y -= 18

        y -= 20
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x, y, "Fazenda / Observações:")
        y -= 25

        c.setFont("Helvetica", 12)
        texto = str(self.fazenda)
        for linha in wrap(texto, 90):
            c.drawString(x + 10, y, linha)
            y -= 16

        c.save()
