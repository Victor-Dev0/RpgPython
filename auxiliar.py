import PySimpleGUI as sg
import json
from models import Personagem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CONN = "sqlite:///personagem.db"

engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

#Verificando se ja tem algum heroi salvo
def procura_heroi():
    with open("personagem.json", "r") as arq_personagem:
        personagem = json.load(arq_personagem)

    if personagem["Nome"] == "":
        nome = sg.popup_get_text("Escolha o nome do seu heroi: ", "Salvar")
        personagem["Nome"] = nome
        novo_personagem = Personagem(Nome=personagem["Nome"], VidaMaxima=personagem["VidaMaxima"], Vida=personagem["Vida"], Dano=personagem["Dano"], Exp=personagem["Exp"], ExpMaxima=personagem["ExpMaxima"], Nivel=personagem["Nivel"])

        session.add(novo_personagem)
        session.commit()
        
    with open("personagem.json", "w") as arq:
        json.dump(personagem, arq, indent=3)

#Definindo os inimigos
def defini_inimigos():
    with open("inimigos.json", "r") as arq_inimigos:
        npcs = json.load(arq_inimigos)
        
    return npcs

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

#funçao para aumentar o nivel do jogador
def subir_nivel(personagem):
    personagem_atual = session.query(Personagem).first()

    novo_personagem = personagem
    novo_personagem["Nivel"] += 1
    personagem_atual.Nivel = novo_personagem["Nivel"]

    novo_personagem["Exp"] = 0
    personagem_atual.Exp = novo_personagem["Exp"]

    novo_personagem["ExpMaxima"] = novo_personagem["ExpMaxima"] * novo_personagem["Nivel"]
    personagem_atual.ExpMaxima = novo_personagem["ExpMaxima"]

    novo_personagem["VidaMaxima"] += 10
    personagem_atual.VidaMaxima = novo_personagem["VidaMaxima"]

    novo_personagem["Dano"] += 5
    personagem_atual.Dano = novo_personagem["Dano"]

    session.add(personagem_atual)
    session.commit()
    return personagem_atual