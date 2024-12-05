#!/usr/bin/env python3

#função recursiva para contar o número total de nós (ramos internos e folhas) em uma árvore representada como um dicionário de dicionários.
def contar_nos(arvore):
    total = 1  #conta o nó atual (a chave atual)
    for subarvore in arvore.values():
        total += contar_nos(subarvore)  #soma os nós das subárvores recursivamente
    return total

#teste com a árvore fornecida
arvore = {
    "Filo1": {
        "Classe1": {
            "Ordem1": {
                "Familia1": {},
                "Familia2": {}
            },
            "Ordem2": {
                "Familia3": {
                    "Genero3": {},
                    "Genero4": {}
                }
            }
        },
        "Classe2": {
            "Ordem3": {},
            "Ordem4": {
                "Familia4": {},
                "Familia5": {
                    "Genero1": {},
                    "Genero2": {
                        "Especie1": {},
                        "Especie2": {}
                    }
                }
            }
        }
    }
}

#chamando a função
total_nos = contar_nos(arvore)
print(f"Total de nós na árvore: {total_nos}")  # Deve exibir 19

