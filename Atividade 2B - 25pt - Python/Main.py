from AnalisadorSintatico import AnalisadorSintatico
import os

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------------- Search Engine ---------------------------")
    while(True):                
        entrada = input("> ").strip()
        sintatico = AnalisadorSintatico(entrada)
        if(entrada == "sair" or entrada == "0"):
            break
        # sintatico.print_simb_tok()
        sintatico.respostas()
        print("\n")

print("--------------------------- Close Search ---------------------------")
            
