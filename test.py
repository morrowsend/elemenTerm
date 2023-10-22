import PySimpleGUI as sg

layout = [
    [sg.Push(), sg.Button ('Clear Data')],
    [sg.Multiline(size=(40, 5), key='-ML-')],
]
window = sg.Window('window', layout, finalize=True)
window['-ML-'].bind("<Key>", "")

while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == 'Clear Data':
        window['-ML-'].update("")
    elif event == '-ML-':
        e = window['-ML-'].user_bind_event
        if e.char:
            print(e.char)

window.close()