import os
import random
import json
import time

#Verificando se ja tem algum heroi salvo
with open("personagem.json", "r") as arq:
    personagem = json.load(arq)


if personagem["Nome"] == "":
    nome = input("Escolha o nome do seu herói: ")
    personagem["Nome"] = nome
    
with open("personagem.json", "w") as arq:
    json.dump(personagem, arq, indent=3)


npcs = [
    {"Nome": "Duende", "Vida": 50, "Dano": 5, "Exp": 10},
    {"Nome": "Orc", "Vida": 70, "Dano": 10, "Exp": 15},
    {"Nome": "Mini-Chefe", "Vida": 100, "Dano": 15, "Exp": 20},
    {"Nome": "Chefão", "Vida": 200, "Dano": 30, "Exp": 40}
]


def jogo():
    print(f"Nome: {personagem['Nome']}\nVida: {personagem['Vida']}\nExp: {personagem['Exp']}\nLevel: {personagem['Level']}")
    print("________________________")
    print(f"Bem vindo: {personagem['Nome']}")
    print("Qual ação deseja tomar:\n1 - Ir a Batalha\n2 - Sair do Jogo")
    resposta = input()
    if resposta == "2":
        quit()
    while resposta == "1":
        inimigo = random.randint(0, 3)

        inimigo_atual = npcs[inimigo]

        turno = random.randint(1, 2)
        while personagem["Vida"] and inimigo_atual["Vida"] > 0:
            if turno == 1:
                print("Turno do jogador!")
                print("_________")
                print("O que deseja fazer?\n1 - Ataque Fisico\n2 - Fugir")
                resposta = input()
                #jogador escolheu fugir
                if resposta == "2":
                    fulga = random.randint(0, 29)

                    if fulga <= 10:
                        print("Fulga mal sucedida!")
                        ataque = random.randint(0, 5)
                        
                        if ataque == 5:
                            print("Sofreu dano critico")
                            personagem["Vida"] -= inimigo_atual["Dano"] * 2
                            turno = 2
                        elif ataque == 3:
                            personagem["Vida"] -= inimigo_atual["Dano"]
                            turno = 2

                    elif fulga > 10 and fulga <= 25:
                        print("Fulga bem sucedida porem tomou um dano!")
                        personagem["Vida"] -= inimigo_atual["Dano"] - 5
                        turno = 2

                    elif fulga > 25 and fulga <= 29:
                        print("Fulga sucedida sem tomar dano")
                        turno = 2

                #jogador escolheu ataque fisico
                if resposta == "1":
                    inimigo_atual["Vida"] -= personagem["Dano"]
                    turno = 2


            elif turno == 2:
                print("Turno do monstro!")
                acao_monstro = random.randint(0, 29)
                if acao_monstro >= 0 and acao_monstro <= 20:
                    print("O monstro decidiu atacar!")
                    personagem["Vida"] -= inimigo_atual["Dano"]
                    turno = 1
                elif acao_monstro > 20 and acao_monstro <= 28:
                    print("O monstro está com sorte!! Ai vai um ataque critico!")
                    personagem["Vida"] -= inimigo_atual["Dano"] * 2
                    turno = 1
                elif acao_monstro == 29:
                    print("O monstro fugiu!")
                    turno = 1

            if personagem["Vida"] == 0:
                print("O monstro venceu a batalha!")
                print("Fim de jogo..")
                personagem["Nome"] = ""
                with open("personagem.json", "w") as arq:
                    json.dump(personagem, arq, indent=3)
                quit()
            elif inimigo_atual["Vida"] <= 0:
                print("Muito bem voce venceu o monstro!")
                personagem["Exp"] += inimigo_atual["Exp"]
                print(f"Nome: {personagem['Nome']}\nVida: {personagem['Vida']}\nExp: {personagem['Exp']}\nLevel: {personagem['Level']}")

        print(f"Nome: {personagem['Nome']}\nVida: {personagem['Vida']}\nExp: {personagem['Exp']}\nLevel: {personagem['Level']}")
        print("________________________")
        print("Qual ação deseja tomar:\n1 - Ir a Batalha\n2 - Sair do Jogo")
        resposta = input()

        if resposta == "2":
            print("Salvando jogo!")
            with open("personagem.json", "w") as arq:
                json.dump(personagem, arq, indent=3)
            
            time.sleep(2)
            print("Jogo salvo!")
            quit()



jogo()