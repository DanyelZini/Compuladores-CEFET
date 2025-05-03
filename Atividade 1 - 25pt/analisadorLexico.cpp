#include <iostream>
#include <fstream>
#include <string>
#include <locale>

#include <set>
#include <queue>
#include <list>

using namespace std;
set<string> stopwords;
set<string> letras_validas;
set<string> tabela_simbolos;
queue<string> token_fila;
queue<string> letras_invalidas;

// inserir lista de stopwords de um .txt em uma arvore. https://github.com/stopwords-iso/stopwords-pt/blob/master/stopwords-pt.txt
template <typename T>
void carregarArquivo(const string& nome_arquivo, T& dados) {
    ifstream arq(nome_arquivo);
    string palavra;

    if(arq.is_open()) {
        while (arq >> palavra) {
            dados.insert(palavra);
        }
        arq.close();
    } else {
        cerr << "Erro ao abrir o arquivo de stopwords: " << nome_arquivo << endl;
    }
}

bool validarChar(const char& c) {
    string carac_esp = ".,;:?!\"'()[]{}-_+=*/\\@#$%&|<>^~´`";
    string letras_acentuadas = "áéíóúãõâêôçÁÉÍÓÚÃÕÂÊÔÇ";

    if (isalpha(c) || isdigit(c) || carac_esp.find(c) != string::npos || isspace(c) || letras_acentuadas.find(c) != string::npos) {
        return true;
    } else {
        return false;
    }
}

string similaridadeTabSimb(const string& palavra) {
    int tam = palavra.size();

    for (const string& str : tabela_simbolos) {
        int nCorretos = 0;
        int menorTam = min(tam, (int)str.size());

        for (int i = 0; i < menorTam; i++) {
            if (palavra[i] == str[i]) {
                nCorretos++;
            }
        }

        float similaridade = (float)nCorretos / max(tam, (int)str.size());
        if (similaridade >= 0.75) {
            return str;
        }
    }

    return "";
}

bool validarPalavra(const string& str) {
    string carac_esp = ".,;:?!\"'()[]{}+=*/\\#$%&|<>^~´`";
    string palavra = "";

    for (size_t i = 0; i < str.size(); i++) {
        if (!validarChar(str[i])) {
            cerr << "Caractere inválido encontrado: " << str[i] << endl;
            return false;
        }

        if (carac_esp.find(str[i]) != string::npos) {
            if (!palavra.empty()) { 
                if (stopwords.find(palavra) == stopwords.end()) {
                    string similar = similaridadeTabSimb(palavra);
                    if (!similar.empty()) {
                        tabela_simbolos.insert(similar);
                    } else {
                        tabela_simbolos.insert(palavra);
                    }
                    token_fila.push(palavra);                    
                }
                token_fila.push(string(1, str[i]));
                palavra.clear();
            }
        } else {
            palavra += str[i];
        }
    }

    if (!palavra.empty() && stopwords.find(palavra) == stopwords.end()) {
        string similar = similaridadeTabSimb(palavra);
        if (!similar.empty()) {
            palavra = similar;
        }
        token_fila.push(palavra);
        tabela_simbolos.insert(palavra);
    }

    return true;
}

template <typename T>
void salvarArquivo(const string& nome_arquivo, const T& dados) {
    ofstream saida(nome_arquivo);

    if (!saida.is_open()) {
        cerr << "Erro ao abrir o arquivo: " << nome_arquivo << endl;
        return;
    }

    if constexpr (is_same_v<T, queue<string>>) {
        auto copia = dados;
        while (!copia.empty()) {
            saida << copia.front() << endl;
            copia.pop();
        }
    } else {
        for (const auto& item : dados) {
            saida << item << endl;
        }
    }

    saida.close();
}

int main() {
    setlocale(LC_ALL, "pt_BR.UTF-8");
    carregarArquivo("./entrada/stopwords.txt", stopwords);
    carregarArquivo("./entrada/letrasvalidos.txt", letras_validas);

    cout << " - ANALISADOR LEXICO - " << endl;

    ifstream arquivo("./entrada/texto.txt");
    string palavra;

    if (!arquivo.is_open()) {
        cerr << "Erro ao abrir o arquivo de entrada!" << endl;
        return 1;
    }

    while (arquivo >> palavra) {
        validarPalavra(palavra);
    }

    salvarArquivo("saida/stopwords-pt.txt", stopwords);
    salvarArquivo("saida/tabela-simbolos.txt", tabela_simbolos);
    salvarArquivo("saida/token-fila.txt", token_fila);
    salvarArquivo("saida/letras-invalidas.txt", letras_invalidas);

    cout << "Processamento concluído. Arquivos gerados na pasta ./saida/" << endl;

    return 0;
}