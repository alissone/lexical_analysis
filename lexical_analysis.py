#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Alisson Amorim @ github.com/alissone/"
__copyright__ = "Copyright 2021"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "alissond@acad.ifma.edu.br"
__status__ = "Work in progress"

import re
import unicodedata
from dataclasses import dataclass

"""
This is a lexical analysis program of Portugol language
The tokenizer was inspired by `re` documentation, where 
"""


@dataclass
class Token:
    """Class to represent token data"""
    typ: str
    val: str
    lin: int
    col: int


reserved_words = [
    "E",
    "VETOR",
    "INICIO",
    "CASO",
    "CONST",
    "DIV",
    "FAÇA",
    "SENAO",
    "FIM",
    "PARA",
    "FUNCAO",
    "SE",
    "MOD",
    "NAO",
    "DE",
    "OU",
    "PROCEDIMENTO",
    "ALGORITMO",
    "REGISTRO",
    "REPITA",
    "ENTAO",
    "TIPO",
    "ATE",
    "VAR",
    "ENQUANTO"
]

token_pattern = r"""
(?P<identifier>[a-zA-Z_][a-zA-Z0-9_]*)
|(?P<newline>\n)
|(?P<whitespace>\s+)
|(?P<inteiro>[0-9]+)
|(?P<atribuicao><-)
|(?P<pontoponto>\.\.)
|(?P<ponto>\.)
|(?P<doispontos>:)
|(?P<pontovirgula>;)
|(?P<virgula>,)
|(?P<colchete_esq>\[)
|(?P<colchete_dir>\])
|(?P<parentese_esq>\()
|(?P<parentese_dir>\))
|(?P<igual>=)
|(?P<menor_igual><=)
|(?P<maior_igual>>=)
|(?P<diferente><>)
|(?P<maior_que>>)
|(?P<menor_que><)
|(?P<comentario>//)
|(?P<divisao>/)
|(?P<menos>-)
|(?P<mul>\*)
|(?P<soma>\+)
|(?P<desconhecido>.)
"""

token_re = re.compile(token_pattern, re.VERBOSE)


class TokenizerException(Exception):
    pass


def normalize_accents(s: str) -> str:
    """
    Substitui letras com acentos por seus caracters mais próximos
    em ascii. 

    Exemplo: 'Açafrão' 🡆 'Acafrao'.
    """
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def normalize_case(s: str) -> str:
    """Substitui letras maiusculas e minusculas por apenas minusculas,
    pois a capitalização será ignorada pelo programa.

    Exemplo: 'MatLAB' 🡆 'matlab'
    """
    return s.lower()


def tokenize(text):
    # text preprocessing to remove unwanted characters
    text = normalize_accents(text)
    text = normalize_case(text)

    # counters to aid debugging syntax errors
    line_start = 0
    line = 0
    pos = 0

    while True:
        m = token_re.match(text, pos)
        if not m:  # exit loop when there is no character left
            break
        pos = m.end()
        token_name = m.lastgroup  # group name from regex `token_pattern`

        if token_name == "newline":
            line_start = pos
            line += 1

        # group content with the current group name
        token_value = m.group(token_name)
        yield Token(typ=token_name, val=token_value, lin=line, col=pos)

    if pos != len(text):
        raise TokenizerException(
            f"Exception when parsing the character 🡆 {text[pos]} 🡄 at pos {pos}/{len(text)} of {text}"
        )


# Testing
texto1 = r'       se n2=0 entao // verifica divisão por zero'
texto2 = r'''
       caso "/"
       se n2=0 entao // verifica divisao por zero
          escreva("       Erro! Divisao por zero, entre com um denominador diferente de 0")
       senao
          saida <- n1 / n2
       fimse
       @
      
fimescolha
'''

print(' texto1 '.center(60, '='))
for tok in tokenize(texto1):
    print(tok)

print(' texto2 '.center(60, '='))
for tok in tokenize(texto2):
    print(tok)
