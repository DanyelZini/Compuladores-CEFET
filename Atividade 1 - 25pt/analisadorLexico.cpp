#include <iostream>
#include <fstream>
#include <string>
#include <locale>
#include <algorithm>
#include <cctype>
#include <cstdlib>

#include <set>
#include <queue>
#include <list>

using namespace std;

/**
 *  @brief Conjunto de stopwords.
 *  @details Este conjunto contém palavras comuns que são ignoradas durante a análise léxica.
 *  *  @note As stopwords foram carregadas a partir de um arquivo externo.
 *  @link https://github.com/stopwords-iso/stopwords-pt/blob/master/stopwords-pt.txt @endlink
 */
set<string> stopwords;

set<string> tabela_simbolos;
queue<string> token_fila;

/**
   *  @brief Carrega um arquivo txt em um conjunto.
   *
   *  @ingroup .txt
   *
   *  @tparam T Tipo do conjunto (set, list, etc.)
   * 
   *  @param nome_arquivo Nome do arquivo a ser carregado.
   *  @param dados Conjunto a ser carregado. 
  */
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
        exit(EXIT_FAILURE);
    }
}

/**
   *  @brief Salva um conjunto em um arquivo txt.
   *
   *  @ingroup .txt
   *
   *  @tparam T Tipo do conjunto (set, list, etc.)
   * 
   *  @param nome_arquivo Nome do arquivo a ser salvo.
   *  @param dados Conjunto a ser salvo.
  */
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

/**
   *  @brief Converte uma string para minúsculas.
   *
   *  @ingroup .string
   * 
   *  @param palavra String a ser convertida.
   *  
   *  @return String convertida para minúsculas.
  */
string toLowerCase(const string palavra) {
    string resultado = palavra;
    transform(resultado.begin(), resultado.end(), resultado.begin(), [](unsigned char c) {
        return tolower(c);
    });
    return resultado;
}

/**
   *  @brief Verifica a similaridade de uma palavra com as palavras da tabela de símbolos.
   *
   *  @ingroup .string
   * 
   *  @param palavra String a ser verificada.
   *  
   *  @return String semelhante encontrada na tabela de símbolos ou uma string vazia se não houver similaridade.
  */
string similaridadeTabSimb(string palavra) {
    int tam = palavra.size();
    string palavraMin = toLowerCase(palavra), strMin;

    for (string str : tabela_simbolos) {
        int nCorretos = 0;
        int menorTam = min(tam, (int)str.size());

        for (int i = 0; i < menorTam; i++) {
            strMin = toLowerCase(str);
            if (palavraMin[i] == strMin[i]) {
                nCorretos++;
            }
        }

        float similaridade = (float)nCorretos / max(tam, (int)str.size());
        if (similaridade >= 0.7) {
            return str;
        }
    }

    return "";
}

/**
   *  @brief Verifica se um caractere é válido.
   *
   *  @ingroup .string
   * 
   *  @param c Caractere a ser verificado.
   *  
   *  @return true se o caractere for válido, false caso contrário.
  */
bool validarChar(const char& c) {
    string carac_esp = ".,;:?!\"'()[]{}-_+=*/\\@#$%&|<>^~´`";
    string letras_acentuadas = "áéíóúãõâêôçÁÉÍÓÚÃÕÂÊÔÇ";

    if (isalpha(c) || isdigit(c) || carac_esp.find(c) != string::npos || isspace(c) || letras_acentuadas.find(c) != string::npos) {
        return true;
    } else {
        cerr << "[ERRO] Caractere inválido encontrado: " << string(1, c) << endl;
        exit(EXIT_FAILURE);
    }
}

/**
   *  @brief Valida uma palavra e a insere na tabela de símbolos se não for uma stopword.
   *
   *  @ingroup .string
   * 
   *  @param str String a ser validada.
   *  
   *  @return true se a palavra for válida, false caso contrário.
  */
bool validarPalavra(const string& str) {
    string carac_esp = ".,;:?!\"'()[]{}+=*/\\#$%&|<>^~´`";
    string palavra = "";

    for (size_t i = 0; i < str.size(); i++) {
        if (!validarChar(str[i])) {
            return false;
        }

        if (carac_esp.find(str[i]) != string::npos) {
            if (!palavra.empty()) { 
                if (stopwords.find(toLowerCase(palavra)) == stopwords.end()) {
                    string similar = similaridadeTabSimb(palavra);
                    string palavraParaInserir = similar.empty() ? palavra : similar; // Preserva a palavra original
                    tabela_simbolos.insert(palavraParaInserir);
                    token_fila.push(palavra); // Insere a palavra original
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
        string palavraParaInserir = similar.empty() ? palavra : similar; // Preserva a palavra original
        tabela_simbolos.insert(palavraParaInserir);
        token_fila.push(palavra);
    }

    return true;
}

/**
 *  @file analisadorLexico.cpp
 *  @brief Analisador léxico em C++.
 *  @details Este programa lê um arquivo de texto, valida as palavras, remove stopwords e gera uma tabela de símbolos.
 *  @author Danyel Martins Zini Silva - 20243014020
 * 
 *  * @note Este código esta no repositório do GitHub: @link https://github.com/DanyelZini/Compuladores-CEFET @endlink
 */
int main() {
    setlocale(LC_ALL, "pt_BR.UTF-8");
    carregarArquivo("./entrada/stopwords.txt", stopwords);

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

    cout << "Processamento concluido. Arquivos gerados na pasta ./saida/" << endl;

    return 0;
}