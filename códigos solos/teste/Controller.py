# Controller.py
import json
import os
from PerfilProdutor import PerfilProdutor

class ControllerPerfilProdutor:
    def __init__(self, arquivo="Cadastros.json"):
        self.arquivo = arquivo
        self.cadastros = self._carregar()

    def _carregar(self):
        if not os.path.exists(self.arquivo):
            return []
        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except:
            return []

        lista = []
        for r in dados:
            lista.append(PerfilProdutor(
                r.get("produtor", ""),
                r.get("tipo_solos", ""),
                r.get("fazenda", ""),
                r.get("talhao", ""),
                float(r.get("ph", 0)),
                float(r.get("p", 0)),
                float(r.get("k", 0)),
                float(r.get("mg", 0)),
                float(r.get("ca", 0)),
                float(r.get("s", 0)),
                r.get("data_coleta", "")
            ))
        return lista

    def _salvar(self):
        dados = []
        for c in self.cadastros:
            dados.append({
                "produtor": c.produtor,
                "tipo_solos": c.tipo_solos,
                "fazenda": c.fazenda,
                "talhao": c.talhao,
                "ph": c.ph,
                "p": c.p,
                "k": c.k,
                "mg": c.mg,
                "ca": c.ca,
                "s": c.s,
                "data_coleta": c.data_coleta
            })
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def criar(self, obj: PerfilProdutor):
        if self.buscar(obj.produtor):
            return False
        self.cadastros.append(obj)
        self._salvar()
        return True

    def buscar(self, nome):
        for c in self.cadastros:
            if c.produtor.lower() == nome.lower():
                return c
        return None

    def alterar(self, novo: PerfilProdutor):
        for i, c in enumerate(self.cadastros):
            if c.produtor.lower() == novo.produtor.lower():
                self.cadastros[i] = novo
                self._salvar()
                return True
        return False

    def deletar(self, nome):
        obj = self.buscar(nome)
        if obj:
            self.cadastros.remove(obj)
            self._salvar()
            return True
        return False
