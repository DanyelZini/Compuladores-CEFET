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
void carregarArquivo(const string &nome_arquivo, T &dados)
{
    ifstream arq(nome_arquivo);
    string palavra;

    if (arq.is_open())
    {
        while (arq >> palavra)
        {
            dados.insert(palavra);
        }
        arq.close();
    }
    else
    {
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
void salvarArquivo(const string nome_arquivo, const T dados)
{
    ofstream saida(nome_arquivo);

    if (!saida.is_open())
    {
        cerr << "Erro ao abrir o arquivo: " << nome_arquivo << endl;
        return;
    }

    if constexpr (is_same_v<T, queue<string>>)
    {
        auto copia = dados;
        while (!copia.empty())
        {
            saida << copia.front() << endl;
            copia.pop();
        }
    }
    else
    {
        for (const auto &item : dados)
        {
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
string toLowerCase(const string palavra)
{
    string resultado = palavra;
    transform(resultado.begin(), resultado.end(), resultado.begin(), [](unsigned char c)
              { return tolower(c); });
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
string similaridadeTabSimb(string palavra)
{
    int tam = palavra.size();
    string palavraMin = toLowerCase(palavra), strMin;

    for (string str : tabela_simbolos)
    {
        int nCorretos = 0;
        int menorTam = min(tam, (int)str.size());

        for (int i = 0; i < menorTam; i++)
        {
            strMin = toLowerCase(str);
            if (palavraMin[i] == strMin[i])
            {
                nCorretos++;
            }
        }

        float similaridade = (float)nCorretos / max(tam, (int)str.size());
        if (similaridade >= 0.7)
        {
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
bool validarChar(const char c)
{
    string carac_esp = ".,;:?!\"'()[]{}-_+=*/\\@#$%&|<>^~´`";
    string letras_acentuadas = "áéíóúãõâêôçÁÉÍÓÚÃÕÂÊÔÇ";

    if (isalpha(c) || isdigit(c) || carac_esp.find(c) != string::npos || isspace(c) || letras_acentuadas.find(c) != string::npos)
    {
        return true;
    }
    else
    {
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
bool validarPalavra(const string str)
{
    string carac_esp = ".,;:?!\"'()[]{}+=*/\\#$%&|<>^~´`";
    string palavra = "";

    for (size_t i = 0; i < str.size(); i++)
    {
        if (!validarChar(str[i]))
        {
            return false;
        }

        if (carac_esp.find(str[i]) != string::npos)
        {
            if (!palavra.empty())
            {
                if (stopwords.find(toLowerCase(palavra)) == stopwords.end())
                {
                    string similar = similaridadeTabSimb(palavra);
                    string palavraParaInserir = similar.empty() ? palavra : similar;
                    tabela_simbolos.insert(palavraParaInserir);
                    token_fila.push(palavra);
                }
                token_fila.push(string(1, str[i]));
                palavra.clear();
            }
        }
        else
        {
            palavra += str[i];
        }
    }

    if (!palavra.empty() && stopwords.find(palavra) == stopwords.end())
    {
        string similar = similaridadeTabSimb(palavra);
        string palavraParaInserir = similar.empty() ? palavra : similar;
        tabela_simbolos.insert(palavraParaInserir);
        token_fila.push(palavra);
    }

    return true;
}

/**
 *  @brief Menu do ChatBot, entrada de dados e processamento.
 *
 *  @ingroup .menu
 *
 *  @return void
 */
void menuChatBot()
{
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif

    cout << " - CHATBOT - " << endl;
    cout << "Digite uma frase (ou 'sair' para encerrar):" << endl;

    string linha, palavra = "";
    cin.ignore();
    while (true)
    {
        cout << "> ";
        getline(cin, linha);

        if (toLowerCase(linha) == "sair")
        {
            break;
        }

        for (size_t i = 0; i < linha.size(); i++)
        {
            if (isspace(linha[i]) || i == linha.size() - 1)
            {
                if (i == linha.size() - 1 && !isspace(linha[i]))
                {
                    palavra += linha[i];
                }
                if (!palavra.empty())
                {
                    validarPalavra(palavra);
                    palavra.clear();
                }
            }
            else
            {
                palavra += linha[i];
            }
        }

        string palavra = "";

        cout << "Tokens processados. Continue ou digite 'sair' para encerrar." << endl;
    }
}

/**
 *  @brief Menu para processar um arquivo .txt.
 *
 *  @ingroup .menu
 *
 *  @return void
 */
void menuArquivoTxt()
{
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
    cout << "Adicione o arquivo na pasta ./entrada/ para ocorra a leitura." << endl;
    cout << "Digite o nome do arquivo(sem o .txt) para processar (ou 'sair' para voltar ao menu):" << endl;

    string nomeArquivo;
    cin.ignore();
    while (true)
    {
        cout << "> ";
        getline(cin, nomeArquivo);

        if (toLowerCase(nomeArquivo) == "sair")
        {
            break;
        }

        ifstream arquivo("./entrada/" + nomeArquivo + ".txt");
        if (!arquivo.is_open())
        {
            cerr << "Erro ao abrir o arquivo: " << nomeArquivo << endl;
            continue;
        }

        string palavra;
        while (arquivo >> palavra)
        {
            validarPalavra(palavra);
        }

        arquivo.close();
        cout << "Arquivo processado. Digite outro arquivo ou 'sair' para voltar ao menu." << endl;
    }
}

/**
 *  @brief Lê os tokens na fila e os exibe.
 *
 *  @ingroup .menu
 *
 *  @return void
 */
void lerTokenFila()
{
    cout << "Tokens na fila:" << endl;
    auto copia = token_fila;
    while (!copia.empty())
    {
        cout << copia.front() << endl;
        copia.pop();
    }
    cout << "Digite algo para continuar..." << endl
         << "> ";
    string dummy;
    cin >> dummy;
}

/**
 *  @file analisadorLexico.cpp
 *  @brief Analisador léxico em C++.
 *  @details Este programa lê um arquivo de texto, valida as palavras, remove stopwords e gera uma tabela de símbolos.
 *  @author Danyel Martins Zini Silva - 20243014020
 *
 *  * @note Este código esta no repositório do GitHub: @link https://github.com/DanyelZini/Compuladores-CEFET @endlink
 */
int main()
{

    setlocale(LC_ALL, "pt_BR.UTF-8");
    carregarArquivo("./entrada/stopwords.txt", stopwords);

    int option;
    do
    {
    #ifdef _WIN32
        system("del /Q .\\saida\\*.txt");
        system("cls");
    #else
        system("rm -f ./saida/*.txt");
        system("clear");
    #endif
        cout << " - ANALISADOR LEXICO - " << endl;
        cout << "\tMenu:" << endl;
        cout << "\t1. ChatBot" << endl;
        cout << "\t2. Arquivo \".txt\"" << endl;
        cout << "\t3. Token Fila" << endl;
        cout << "\t4. Tabela de Simbolos" << endl;
        cout << "\t0. Sair" << endl;
        cout << "Escolha uma opcao: " << endl
             << "> ";
        cin >> option;

        switch (option)
        {
        case 1:
            menuChatBot();
            break;
        case 2:
            menuArquivoTxt();
            break;
        case 3:
            lerTokenFila();
            break;
        case 4:
            cout << "Tabela de simbolos:" << endl;
            for (const auto &item : tabela_simbolos)
            {
                cout << item << endl;
            }
            cout << "Digite algo para continuar..." << endl
                 << "> ";
            string dummy;
            cin >> dummy;
            break;
        }
    } while (option != 0);

    // Salva os dados nos arquivos ./saida
    salvarArquivo("saida/stopwords-pt.txt", stopwords);
    salvarArquivo("saida/tabela-simbolos.txt", tabela_simbolos);
    salvarArquivo("saida/token-fila.txt", token_fila);

    cout << endl
         << " - FIM DO ANALISADOR LEXICO - " << endl;

    cout << endl
         << "Processamento concluido. Arquivos gerados na pasta ./saida/" << endl;

    return 0;
}