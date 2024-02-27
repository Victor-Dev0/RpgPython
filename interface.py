import PySimpleGUI as sg

layout = [
    #informaçoes do jogador
    [sg.Text("Nome:", pad=(0,5)), sg.Text()],
    [sg.Text("Vida:", size=(15,0), pad=(0,5)), sg.Text(),sg.VerticalSeparator(color='Red') , sg.Text("Exp:", size=(10,0), pad=(5,5)), sg.Text()],
    #eventos do jogo
    [(sg.Listbox(values=[], no_scrollbar=True, size=(400,17)))],
    #escolhas do jogador
    [sg.Button('1 - Ir a Batalha'), sg.Button('2 - Sair do Jogo')]
]

window = sg.Window('Jogo Estrategia', layout, size=(500,400))

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break




window.close()