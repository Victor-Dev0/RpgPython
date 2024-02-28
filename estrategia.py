import os
import random
import json
import time
import interface
from models import Personagem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CONN = "sqlite:///personagem.db"

engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


#Verificando se ja tem algum heroi salvo
with open("personagem.json", "r") as arq_personagem:
    personagem = json.load(arq_personagem)


if personagem["Nome"] == "":
    nome = interface.sg.popup_get_text("Escolha o nome do seu herói: ", "Salvar")
    personagem["Nome"] = nome
    novo_personagem = Personagem(Nome=personagem["Nome"], VidaMaxima=personagem["VidaMaxima"], Vida=personagem["Vida"], Dano=personagem["Dano"], Exp=personagem["Exp"], ExpMaxima=personagem["ExpMaxima"], Nivel=personagem["Nivel"])

    session.add(novo_personagem)
    session.commit()

with open("personagem.json", "w") as arq:
    json.dump(personagem, arq, indent=3)

#Definindo os inimigos
with open("inimigos.json", "r") as arq_inimigos:
    npcs = json.load(arq_inimigos)

#funçao para aumentar o nivel do jogador
def subir_nivel(personagem):
    novo_personagem = personagem
    novo_personagem["Nivel"] += 1
    novo_personagem["Exp"] = 0
    novo_personagem["ExpMaxima"] = novo_personagem["ExpMaxima"] * novo_personagem["Nivel"]
    novo_personagem["VidaMaxima"] += 10
    novo_personagem["Dano"] += 5
    return novo_personagem

#funçao para salvar alteraçao do personagem
def salvar_situacao(personagem):
    with open('personagem.json', 'w') as arq_salvar:
        json.dump(personagem, arq_salvar, indent=3)

#funçao para quando o personagem morrer
def resetar_personagem(personagem):
    with open('personagem.json', 'w') as arq_reset:
        personagem['Nome'] = ""
        personagem["VidaMaxima"] = 100
        personagem["Vida"] = 100
        personagem["Dano"] = 15
        personagem["Exp"] = 0
        personagem["ExpMaxima"] = 100
        personagem["Nivel"] = 1
        json.dump(personagem, arq_reset, indent=3)


#funçao principal
def jogo(personagem):
    # print(f"Nome: {personagem['Nome']}\nVida: {personagem['Vida']}\nExp: {personagem['Exp']}\nNivel: {personagem['Nivel']}")
    # print("________________________")
    # print(f"Bem vindo: {personagem['Nome']}")
    # print("Qual ação deseja tomar:\n1 - Ir a Batalha\n2 - Sair do Jogo")
    # resposta = input()

    # #após escolher sair do jogo o codigo para
    # if resposta == "2":
    #     quit()

    
    #escolha aleatoria de qual inimigo vai aperecer para a batalha
    inimigo = random.randint(0, 3)
    #pegando os dados do inimigo aleatorio
    inimigo_atual = npcs[inimigo]

    #print("Voce caminha em uma estrada e de repente")
    interface.window['eventos'].update(values='Voce caminha em uma estrada e de repente')
    time.sleep(1)
    #print(f"Aparece um monstro ele é um {inimigo_atual["Nome"]}")
    interface.window['eventos'].update(values=f'Aparece um monstro ele é um {inimigo_atual["Nome"]}')
    time.sleep(1)
    #definindo de quem será o turno se sera do inimigo ou do jogador
    turno = random.randint(1, 2)

    #enquanto a vida do jogador e do inimigo for maior que 0 o jogo continua
    while personagem["Vida"] and inimigo_atual["Vida"] > 0: 
        if turno == 1:
            interface.window['1 - Ir a Batalha'].update('1 - Ataque Fisico')
            interface.window['2 - Sair do jogo'].update('2 - Fugir')
            print("Turno do jogador!")
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
                        salvar_situacao(personagem)
                        print(f"Dano sofrido: {inimigo_atual['Dano']*2}")
                        turno = 2
                    elif ataque == 3:
                        personagem["Vida"] -= inimigo_atual["Dano"]
                        salvar_situacao(personagem)
                        print(f"Dano sofrido: {inimigo_atual['Dano']}")
                        turno = 2

                elif fulga > 10 and fulga <= 25:
                    print("Fulga bem sucedida porem tomou um dano!")
                    personagem["Vida"] -= inimigo_atual["Dano"] - 5
                    salvar_situacao(personagem)
                    print(f"Dano sofrido: {inimigo_atual['Dano'] - 5}")
                    break

                elif fulga > 25 and fulga <= 29:
                    print("Fulga sucedida sem tomar dano")
                    break

            #jogador escolheu ataque fisico
            if resposta == "1":
                time.sleep(0.5)
                inimigo_atual["Vida"] -= personagem["Dano"]
                if inimigo_atual["Vida"] <= 0:
                    inimigo_atual["Vida"] = 0
                time.sleep(0.5)
                print(f"Inimigo: {inimigo_atual['Nome']}, Vida: {inimigo_atual['Vida']}")
                turno = 2


        elif turno == 2:
            print("Turno do monstro!")
            acao_monstro = random.randint(0, 29)
            time.sleep(1)
            if acao_monstro >= 0 and acao_monstro <= 20:
                print("O monstro decidiu atacar!")
                time.sleep(1)
                personagem["Vida"] -= inimigo_atual["Dano"]
                salvar_situacao(personagem)
                turno = 1
            elif acao_monstro > 20 and acao_monstro <= 28:
                print("O monstro está com sorte!! Ai vai um ataque critico!")
                time.sleep(1)
                personagem["Vida"] -= inimigo_atual["Dano"] * 2
                salvar_situacao(personagem)
                turno = 1
            elif acao_monstro == 29:
                print("O monstro fugiu!")
                turno = 1
        print(f"Personagem: {personagem["Nome"]}\nVida: {personagem["Vida"]}")
        print("________________________")
        if personagem["Vida"] <= 0:
            personagem["Vida"] = 0
            print("O monstro venceu a batalha!")
            print("Fim de jogo..")
            resetar_personagem(personagem)
            quit()
        elif inimigo_atual["Vida"] <= 0:
            print("Muito bem voce venceu o monstro!")
            time.sleep(1)
            personagem["Exp"] += inimigo_atual["Exp"]
            personagem["Vida"] += inimigo_atual["Exp"] / 2
            #Se a vida do jogador for maior que a vida maxima permitida seta a vida para o valor da vida maxima
            if personagem["Vida"] > personagem["VidaMaxima"]:
                personagem["Vida"] = personagem["VidaMaxima"]
            #Verifica a xp do personagem para validar se ira subir de nivel
            if personagem["Exp"] >= personagem["ExpMaxima"]:
                personagem["Exp"] = personagem["ExpMaxima"]
                print("Parabens voce subiu de nivel!!")
                personagem = subir_nivel(personagem)
                time.sleep(0.5)
        

    print(f"Nome: {personagem['Nome']}\nVida: {personagem['Vida']}\nExp: {personagem['Exp']}\nNivel: {personagem['Nivel']}")
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



#jogo(personagem)