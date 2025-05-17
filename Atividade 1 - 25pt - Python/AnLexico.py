import re 
from collections import deque
from difflib import SequenceMatcher

class AnalisadorLexico:
    def __init__(self):
        self.alfabeto = set(
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            'áàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ'
            '!@#$%¨&*()_+-=[]{};:",./<>?\\| \t\n'
        )
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

    def verificadorCaracteres(self, texto):
        caracteres_invalidos = set()
        for char in texto:
            if char not in self.alfabeto:
                caracteres_invalidos.add(char)
        if caracteres_invalidos:
            raise ValueError(f"Erro lexico: Caracteres invalidos encontrados [Nao disponiveis no teclado]: {caracteres_invalidos}")
        
    def similaridade(self, a, b):
        return SequenceMatcher(None, a, b).radio()

    def encontrar_palavra_similar(self, palavra, palavras_conhecidas, limiar=0.7):
        for p in palavras_conhecidas:
            if self.similaridade(palavra.lower(), p.lower()) >= limiar:
                return p
        return None

    def analisar(self, texto):
        try:
            self.verificadorCaracteres(texto)

            tokens = re.findall(r"\b\w+\b", texto.lower())

            for token in tokens:
                if token not in self.stopwords:
                    if token not in self.tabela_simbolos:
                        self.tabela_simbolos.append(token)
                    
                    self.fila_token.append(token)  # Corrigido de 'fila_tokens' para 'fila_token'
            return {
                "tabela_simbolos": list(self.tabela_simbolos),
                "fila_tokens": list(self.fila_token)  # Corrigido de 'fila_tokens' para 'fila_token'
            }
        except ValueError as e:
            return {"erro": str(e)}
        
    def testar_query(self, query):
        print(f"\nTestando query: '{query}'")
        resultado = self.analisar(query)

        if "erro" in resultado:
            print("Erro encontrado:", resultado["erro"])
        else:
            print("Tabela de símbolos:", resultado["tabela_simbolos"])
            print("Fila de tokens:", resultado["fila_tokens"])  # Certifique-se de que está correto

        palavras_conhecidas = ["exceção", "linguagem", "natural", "analisador"]
        for palavra in resultado.get("tabela_simbolos", []):
            similar = self.encontrar_palavra_similar(palavra, palavras_conhecidas)
            if similar and palavra.lower() != similar.lower():
                print(f"Palavra similar encontrada: '{palavra}' -> '{similar}'")


# Exemplo de uso
if __name__ == "__main__":
    analisador = AnalisadorLexico()
    
    # Testes
    analisador.testar_query("O analisador léxico é uma fase importante do compilador.")
    analisador.testar_query("Este é um teste com caracteres inválidos ©®")
    analisador.testar_query("Exceção, excecao, excessão, Esceção")
    analisador.testar_query("A linguagem natural possui muitas stopwords como artigos e preposições.")