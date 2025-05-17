from AnalisadorLexico import AnalisadorLexico
import re
import os

documentos = []
class GramaticaBNF:
    def __init__(self):
        self.regras = {
            "pergunta_formato": (
            re.compile(r'Qual documento esta no (\w+)\?$'),
            lambda m: f"O formato e {m.group(1)}."
            ),
            "pergunta_tamanho": (
            re.compile(r'Qual tamanho tem (\w+)\?$'),
            lambda m: f"Quero tamanho maior que <numero>."
            ),
            "pergunta_titulo": (
            re.compile(r'Qual documento tem (.+)\?$'),
            lambda m: f"O documento é {m.group(1)}."
            ),
            "pergunta_data": (
            re.compile(r'Quais documentos estao entre (\d{2}/\d{2}/\d{4}) e (\d{2}/\d{2}/\d{4})\?$'),
            lambda m: f"O documentos criados apartir de {m.group(1)} e finalizados ate {m.group(2)}."
            ),
            "pergunta_tipo_tamanho": (
            re.compile(r'Mostre documentos do tipo (\w+) com tamanho maior que (\d+)\?$'),
            lambda m: f"Os documentos do tipo {m.group(1)} maiores que {m.group(2)}."
            ),
            "resposta_formato": (
            re.compile(r'O formato e (\w+)\.$'),
            None
            ),
            "resposta_tamanho": (
            re.compile(r'Quero tamanho maior que (\d+)\.$'),
            None
            ),
            "resposta_titulo": (
            re.compile(r'O titulo é (.+)\.$'),
            None
            ),
            "resposta_doc_formato": (
            re.compile(r'O documento esta em (\w+)\.$'),
            None
            ),
            "resposta_doc_data": (
            re.compile(r'O documento foi criado em (\d{2}/\d{2}/\d{4})\.$'),
            None
            ),
            "resposta_pref_palavra": (
            re.compile(r'Prefiro documentos com (.+)\.$'),
            None
            )
        }
    
    def pesquisa_doc(self, formato):
        for doc in documentos:
            if doc.endswith(f".{formato}"):
                yield doc

    def validar(self, texto):
        for nome, (regra, resposta) in self.regras.items():
            match = regra.match(texto)
            if match:
                if nome.startswith("pergunta") and resposta:
                    return True, nome, resposta(match)
                else:
                    return True, nome, None
        return False, None, None

def analisar_entrada(texto):
    analisador = AnalisadorLexico()
    analisador.analisar_texto(texto)
    tokens = list(analisador.fila_token)
    gramatica = GramaticaBNF()
    valido, regra, resposta = gramatica.validar(texto)
    return valido, regra, resposta, tokens

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------------- Search Engine ---------------------------")
    while(True):
        entrada = input().strip()
        if(entrada == "sair"):
            break
        valido, regra, resposta, tokens = analisar_entrada(entrada)
        if valido:
            print(f"Valido! Regra reconhecida: {regra}")
            if regra.startswith("pergunta"):                
                print("\n\tPergunta do usuario.")
                print(f"\tResposta: {resposta}")
            else:
                print("Resposta do usuario.")
        else:
            print("Sentença inválida segundo a gramática BNF.")
        print("\nTokens identificados:", tokens)

    print("--------------------------- Close Search ---------------------------")