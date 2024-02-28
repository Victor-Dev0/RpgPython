import PySimpleGUI as sg
from models import Personagem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import auxiliar

CONN = "sqlite:///personagem.db"

engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

personagem = session.query(Personagem).first()

layout = [
    #informaçoes do jogador
    [sg.Text("Nome:", pad=(0,5)), sg.Text(personagem.Nome)],
    [sg.Text("Vida:", size=(5,0), pad=(0,5)), sg.Text(personagem.Vida, key="vida"),sg.VerticalSeparator(color='Red') , sg.Text("Exp:", size=(5,0), pad=(5,5)), sg.Text(personagem.Exp)],
    #eventos do jogo
    [(sg.Listbox(values=[], no_scrollbar=True, size=(400,17), key='eventos'))],
    #escolhas do jogador
    [sg.Button('1 - Ir a Batalha', key='batalha'), sg.Button('2 - Sair do Jogo', key='sair')]
]

window = sg.Window('Jogo Estrategia', layout, size=(500,400))
auxiliar.procura_heroi()

while True:
    event, values = window.read()
    
    
    if event == sg.WIN_CLOSED or event == 'sair':
        break

    if event == 'batalha':
        pass

    
window.close()