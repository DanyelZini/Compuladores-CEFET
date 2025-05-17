import re
from collections import deque
from difflib import SequenceMatcher

class AnalisadorLexico:
    def __init__(self):
        self.alfabeto = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                            'áàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ'
                            '!@#$%¨&*()_+-=[]{};:",./<>?\\| \t\n')
        self.stopwords = {
            'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 
            'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 
            'dos', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 
            'sua', 'ou', 'ser', 'quando', 'muito', 'há', 'nos', 'já', 'está', 
            'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 
            'era', 'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus', 'quem', 
            'nas', 'me', 'esse', 'eles', 'estão', 'você', 'tinha', 'foram', 
            'essa', 'num', 'nem', 'suas', 'meu', 'às', 'minha', 'têm', 'numa', 
            'pelos', 'elas', 'havia', 'seja', 'qual', 'será', 'nós', 'tenho', 
            'lhe', 'deles', 'essas', 'esses', 'pelas', 'este', 'fosse', 'dele', 
            'tu', 'te', 'vocês', 'vos', 'lhes', 'meus', 'minhas', 'teu', 'tua', 
            'teus', 'tuas', 'nosso', 'nossa', 'nossos', 'nossas', 'dela', 
            'delas', 'esta', 'estes', 'estas', 'aquele', 'aquela', 'aqueles', 
            'aquelas', 'isto', 'aquilo', 'estou', 'está', 'estamos', 'estão', 
            'estive', 'esteve', 'estivemos', 'estiveram', 'estava', 'estávamos', 
            'estavam', 'estivera', 'estivéramos', 'esteja', 'estejamos', 
            'estejam', 'estivesse', 'estivéssemos', 'estivessem', 'estiver', 
            'estivermos', 'estiverem', 'hei', 'há', 'havemos', 'hão', 'houve', 
            'houvemos', 'houveram', 'houvera', 'houvéramos', 'haja', 'hajamos', 
            'hajam', 'houvesse', 'houvéssemos', 'houvessem', 'houver', 
            'houvermos', 'houverem', 'houverei', 'houverá', 'houveremos', 
            'houverão', 'houveria', 'houveríamos', 'houveriam', 'sou', 'somos', 
            'são', 'era', 'éramos', 'eram', 'fui', 'foi', 'fomos', 'foram', 
            'fora', 'fôramos', 'seja', 'sejamos', 'sejam', 'fosse', 'fôssemos', 
            'fossem', 'for', 'formos', 'forem', 'serei', 'será', 'seremos', 
            'serão', 'seria', 'seríamos', 'seriam', 'tenho', 'tem', 'temos', 
            'têm', 'tinha', 'tínhamos', 'tinham', 'tive', 'teve', 'tivemos', 
            'tiveram', 'tivera', 'tivéramos', 'tenha', 'tenhamos', 'tenham', 
            'tivesse', 'tivéssemos', 'tivessem', 'tiver', 'tivermos', 
            'tiverem', 'terei', 'terá', 'teremos', 'terão', 'teria', 
            'teríamos', 'teriam'
        }
        self.tabela_simbolos = []
        self.fila_token = deque()

    def similaridade(self, palavra, tabela_simbolos):
        tam = len(palavra)
        palavra_min = palavra.lower()
        
        for str in tabela_simbolos:
            n_corretos = 0
            menor_tam = min(tam, len(str))
            str_min = str.lower()

            for i in range(menor_tam):
                if palavra_min[i] == str_min[i]:
                    n_corretos = n_corretos + 1
            
            similaridade = (float)(n_corretos / max((int)(tam), (int)(len(str))))
            if similaridade >= 0.7:
                return str
        
        return ""
    
    def validar_char(self, c):
        carac_especiais = set(".,;:?!\"'()[]{}-_+=*/\\@#$%&|<>^~´`“”")
        
        if (c.isalnum() or c in carac_especiais or c.isspace() or c in self.alfabeto):
            return True
        
        raise ValueError(f"Caractere inválido encontrado: {repr(c)}") 
       
    def validar_palavra(self, texto):
        carac_esp = ".,;:?!\"'()[]{}+=*/\\#$%&|<>^~´`"
        palavra = ""
        
        for char in texto:
            if not self.validar_char(char):
                return False
            if char in carac_esp:
                if palavra:
                    if palavra.lower() not in self.stopwords:
                        palavra_similar = self.similaridade(palavra, self.tabela_simbolos)
                        palavra_para_inserir = palavra_similar if palavra_similar else palavra
                        if palavra_para_inserir not in self.tabela_simbolos:
                            self.tabela_simbolos.append(palavra_para_inserir)
                        self.fila_token.append(palavra)
                    self.fila_token.append(char)
                    palavra = ""
                else:
                    self.fila_token.append(char)
                    palavra = ""
            else:
                palavra += char
        
        if palavra:            
            similar = self.similaridade(palavra, self.tabela_simbolos)
            palavra_para_inserir = similar if similar else palavra
            if palavra_para_inserir not in self.tabela_simbolos and palavra_para_inserir.lower() not in self.stopwords:
                self.tabela_simbolos.append(palavra_para_inserir)
            self.fila_token.append(palavra)
        
        return True
    
    def analisar_texto(self, texto):
        palavras = texto.split()
        for palavra in palavras:
            self.validar_palavra(palavra)

    
if __name__ == "__main__":
    analisador = AnalisadorLexico()

    texto = input("Digite o texto a ser analisado: ")
    analisador.analisar_texto(texto)
    
    print("Tabela de símbolos:", analisador.tabela_simbolos)
    print("Fila de tokens:", list(analisador.fila_token))
