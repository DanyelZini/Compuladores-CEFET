import os
import re
from AnalisadorLexico import AnalisadorLexico
from collections import deque

class AnalisadorSintatico:
    def __init__(self, texto):
        self.lexico = AnalisadorLexico()
        self.lexico.analisar_texto(texto)
        self.tabela_funcao = self.classificar_tabela()
        self.pergunta = True if '?' in texto else False
        self.texto = texto

        self.ultima_regra_incompleta = None

        self.Pergunta = [
            (['interrogativo', 'entidade'], 'pergunta_formato_titulo'),
            (['interrogativo', 'atributo'], 'pergunta_tamanho'),
            (['verbo_demostrar', 'entidade', 'atributo', 'atributo'], 'pergunta_tipo'),
            (['verbo_demostrar', 'entidade'], 'pergunta_palavra_chave')
        ]

        self.Comando = [
            (['verbo_adicao', 'entidade', 'atributo'], 'comando_adicionar')
        ]

        self.Arquivos = [
            ("relatorio.pdf", 1440),
            ("musica.mp3", 5120),
            ("video.mp4", 20480),
            ("documentos.zip", 10240),
            ("dados.rar", 8192),
            ("notas.txt", 256),
            ("apresentacao.pdf", 980),
            ("backup.zip", 15360),
            ("filme.mp4", 40960),
            ("audio.mp3", 3072),
            ("leitura.txt", 512),
            ("projeto.rar", 6144)
        ]

    def classificar_funcao(self, palavra):
        palavra = palavra.lower()
        if palavra in {'qual', 'quais', 'quem', 'quando', 'onde', 'como'}:
            return 'interrogativo'
        elif palavra in {'documento', 'documentos', 'arquivo', 'arquivos'}:
            return 'entidade'
        elif palavra in {'mostre', 'mostrar', 'existe', 'liste', 'encontre', 'busque', 'procure', 'apresente', 'exiba'}:
            return 'verbo_demostrar'
        elif palavra in {'tamanho', 'tipo', 'formato', 'nome', 'quantidade'}:
            return 'atributo'
        elif palavra in {'pdf', 'mp3', 'mp4', 'zip', 'rar', 'txt', 'doc'}:
            return 'tipo'
        elif palavra in {'adicionar', 'adicione', 'insira', 'inclua'}:
            return 'verbo_adicao'
        else:
            return 'identificador'

    def classificar_tabela(self):
        tabela_auxiliar = []
        for aux in self.lexico.tabela_simbolos:
            tabela_auxiliar.append(self.classificar_funcao(aux))
        self.tabela_simbolos_funcionais = list(zip(self.lexico.tabela_simbolos, tabela_auxiliar))
        return tabela_auxiliar

    def verificar_regra_por_similaridade(self, simbolos, tabela):
        correspondencias = 0
        for palavra_regra in tabela:
            for simb in simbolos:
                similar = self.lexico.similaridade(palavra_regra, [simb])
                if similar:
                    correspondencias += 1
                    break
        return correspondencias >= len(tabela)

    def respostas(self):
        tab_func = [s.lower() for s in self.tabela_funcao]
        simbolos = [s.lower() for s in self.lexico.tabela_simbolos]
        regra_reconhecida = False

        def buscar_por_formato(simb):
            arquivos = [arq for arq, _ in self.Arquivos if arq[-3:] == simb]
            if not arquivos:
                arquivos = [arq for arq, _ in self.Arquivos if arq.rsplit('.', 1)[0] == simb]
            return arquivos

        def buscar_com_tamanho(simb):
            arquivos = [[arq, tam] for arq, tam in self.Arquivos if arq[-3:] == simb]
            if not arquivos:
                arquivos = [[arq, tam] for arq, tam in self.Arquivos if arq.rsplit('.', 1)[0] == simb]
            return arquivos

        def buscar_por_nome(simb):
            for arq, _ in self.Arquivos:
                if simb == arq.rsplit('.', 1)[0]:
                    return arq
            return None

        def buscar_por_tipo_e_nome(formato, titulo):
            arquivos = []
            for arq, _ in self.Arquivos:
                if arq.rsplit('.', 1)[0] == titulo and arq[-3:] == formato:
                    arquivos.append(arq)
            return arquivos
        
        def adicionar_arquivo(nome, tam):
            if '.' not in nome:
                print("Informe o tipo do arquivo (ex: pdf, mp3, txt):")
                tipo = input("> ").strip().lower()
                nome = f"{nome}.{tipo}"
            self.Arquivos.append((nome, int(tam)))
            print(f"Arquivo '{nome}' de tamanho {tam} adicionado com sucesso!!!")

        if self.pergunta:
            for tabela, nome_regra in self.Pergunta:
                if self.verificar_regra_por_similaridade(tab_func, tabela):
                    regra_reconhecida = True
                    self.ultima_regra_incompleta = None

                    simb = simbolos[-1]

                    match nome_regra:
                        case "pergunta_formato_titulo":
                            if len(tab_func) <= 2 and 'identificador' not in tab_func:
                                print("Informe o tipo de documento")
                                formato = input("> ").strip().lower()
                                simbolos.append(formato)
                                tab_func.append(self.classificar_funcao(formato))
                                simb = simbolos[-1]
                            arquivos = buscar_por_formato(simb)
                            print(arquivos if arquivos else "Nenhum arquivo encontrado!!!")

                        case "pergunta_tamanho":
                            arquivos = buscar_com_tamanho(simb)
                            print(arquivos if arquivos else "Nenhum arquivo encontrado!!!")

                        case "pergunta_palavra_chave":
                            arq = buscar_por_nome(simb)
                            if arq:
                                print(f"Arquivo {simb} encontrado!\n\tNome: {arq}\n")
                            else:
                                print("Nenhum arquivo encontrado!!!")

                        case "pergunta_tipo":
                            if len(simbolos) >= 2:
                                formato = simbolos[-3]
                                titulo = simbolos[-1]
                                arquivos = buscar_por_tipo_e_nome(formato, titulo)
                                print(arquivos if arquivos else "Nenhum arquivo encontrado!!!")
                            else:
                                print("Informações insuficientes para buscar por tipo e nome.")
                    break
            if not regra_reconhecida:
                encontrou_estrutura_parcial = False

                for tabela, nome_regra in self.Pergunta:
                    correspondencias = 0
                    for cat in tab_func:
                        if cat in tabela:
                            correspondencias += 1
                    if 0 < correspondencias < len(tabela):
                        faltando = [cat for cat in tabela if cat not in tab_func]
                        self.ultima_regra_incompleta = nome_regra
                        for f in faltando:
                            print(f"Qual {f} você deseja saber?")
                        encontrou_estrutura_parcial = True
                        break
                if not encontrou_estrutura_parcial:
                    print("\n -- Nao entendi. -- ")
        else:
            for tabela, nome_regra in self.Comando:
                if self.verificar_regra_por_similaridade(tab_func, tabela):
                    regra_reconhecida = True

                    match nome_regra:
                        case 'comando_adicionar':
                            if len(tab_func) >= 5:
                                print(simbolos[-3], simbolos[-1])
                                adicionar_arquivo(simbolos[-3], simbolos[-1])
                            else:
                                print("Comando incompleto!!!")
                                break



    def print_simb_tok(self):
        print("Tabela de Simbolo:", self.lexico.tabela_simbolos, "\n")
        print("Tabela de Token:", self.lexico.fila_token, "\n")
        print("Pergunta? ", self.pergunta, "\n")
        print("Tabela Funcoes ", self.tabela_funcao, "\n")
        print("Símbolos classificados:")
        for simb, func in self.tabela_simbolos_funcionais:
            print(f"  {simb} -> {func}")
