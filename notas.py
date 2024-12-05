#!/usr/bin/env python3

#definindo as variáveis
total = 0
contador_notas = 0

#pedindo para o usuário informar o número de notas
numero_de_notas = input("Digite o número de notas que deseja inserir para o cálculo de média: ")

#verificando se a entrada é um número válido
if not numero_de_notas.isdigit() or int(numero_de_notas) <= 0:
    print("Valor inválido. O número de notas deve ser um inteiro positivo.")
    exit()  #encerra o programa se o valor for inválido

numero_de_notas = int(numero_de_notas)

#enquanto o contador de notas for menor que o número de notas
while contador_notas < numero_de_notas:
    try:
        #entrada da nota
        nota = float(input(f"Digite a {contador_notas + 1}ª nota: "))
        
        #validando a nota
        if nota < 0 or nota > 10:
            print("Nota inválida. Por favor, insira uma nota entre 0 e 10.")
            continue
        
        #somando a nota ao total
        total += nota
        contador_notas += 1  #incrementa o contador de notas
    
    except ValueError:
        print("Entrada inválida. Por favor, insira um número válido para a nota.")

#calculando a média da disciplina
media = total / numero_de_notas

#imprimindo a média com 2 casas decimais
print(f"A média da disciplina é: {media:.2f}")
