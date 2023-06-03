import serial
import serial.tools.list_ports
import threading
import queue
import PySimpleGUI as sg
import time

stop_event= threading.Event()
commandList=[]


def read_serial(serial_port, output_queue, stop_event):
    while True:
        if serial_port and serial_port.in_waiting:
            data = serial_port.read(serial_port.in_waiting).decode()
            output_queue.put(data)
    time.sleep(0.1) 

def update_output(output_queue, window, values, stop_event):
    received_data = values['-OUTPUT-']
    auto=values['-AUTOSCROLL-']
    while True:
        if not output_queue.empty():
            data = output_queue.get()
            window['-OUTPUT-'].print(data, autoscroll=auto, end='')
            # received_data += data
            # sg.cprint(auto)  # cprint is too slow and has weird line breaks for no reason                     
        else:
            window.refresh()
        time.sleep(0.1)    



# Add your new theme colors and settings
sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {'BACKGROUND': '# 000066',
                                        'TEXT': '# FFCC66',
                                        'INPUT': '# 339966',
                                        'TEXT_INPUT': '# 000000',
                                        'SCROLL': '# 99CC99',
                                        'BUTTON': ('# 003333', '# FFCC66'),
                                        'PROGRESS': ('# D1826B', '# CC8019'),
                                        'BORDER': 1, 'SLIDER_DEPTH': 0, 
'PROGRESS_DEPTH': 0, }



def main():
    sg.theme('DarkBlue2')
    # print(sg.LOOK_AND_FEEL_TABLE['DarkGrey'])
    portList = []

    ser = serial.tools.list_ports.comports() #serial.Serial('COM6')  # open serial port
    for specific_port in ser:
        # print("device = ", specific_port.device) 
        # print("name = ", specific_port.name) 
        # print("description = ", specific_port.description) 
        # print("hwid = ", specific_port.hwid)
        # print("vid = ", specific_port.vid)
        # print("pid = ", specific_port.pid)
        # print("serial_number = ", specific_port.serial_number)
        # print("location = ", specific_port.location)
        # print("manufacturer = ", specific_port.manufacturer)
        # print("product = ", specific_port.product)
        # print("interface = ", specific_port.interface)

        if("Bluetooth" in specific_port.description or "bluetooth" in specific_port.description):
            portList.append(specific_port.name+" "+"(Bluetooth)")
        elif("USB" in specific_port.description or "FTDI" in specific_port.manufacturer):
            portList.append("(USB) "+specific_port.name)
        elif("Arduino" in specific_port.description):
            portList.append(specific_port.description)
        else:
            portList.append(specific_port.name)     
        portList.sort()

    if not portList:
        portList.append('None')
  
    layout = [
        [sg.Text('Serial Port:'), sg.Combo((portList), enable_events=True ,key='-PORT-', size=(20, 1), default_value=portList[0]), sg.Button('Connect', key='-CONNECT-', bind_return_key=True, focus=True), sg.Combo(['300','600','750','1200','2400','4800','9600','19200','31250','38400','57600','74880','115200','230400','250000','460800','500000','921600','1000000','2000000'], default_value='9600', key='-SPEED-', enable_events=True,size=10), sg.Combo(['No Line Ending', 'Newline', 'Carriage Return', 'Both NL & CR'], key='-LINE END-', default_value='Both NL & CR', enable_events=True),sg.Checkbox('Local Echo', enable_events=True), sg.Checkbox('Autoscroll', key='-AUTOSCROLL-', default=True, enable_events=True), sg.Checkbox('Line Mode', key='-LINEMODE-', enable_events=True), sg.Button('Clear Data')],
        [sg.Multiline(key='-OUTPUT-', size=(100, 20), horizontal_scroll=True, enable_events=True)],
        [sg.Input(key='-INPUT-', size=(95, 1)), sg.Button('Send')],
    ]
    
    window = sg.Window('Serial Terminal', layout, resizable=True, finalize=True, return_keyboard_events=True)

    sg.cprint_set_output_destination(window, '-OUTPUT-')



    serial_port = None
    output_queue = queue.Queue()


    window['-CONNECT-'].SetFocus()
    
    previousCommand = 1;

    while True:
        event, values = window.read( timeout=1000)

           
        if "Up" in event and len(commandList) > 0:            # up button pressed, pull previous command
            window['-INPUT-'].update(commandList[-previousCommand])
            previousCommand = previousCommand + 1
            if previousCommand > len(commandList):
                previousCommand = 1

        if "Down" in event and len(commandList) > 0:            # down button pressed, pull previous command
            window['-INPUT-'].update(commandList[-previousCommand])
            previousCommand = previousCommand - 1
            if previousCommand < 1:
                previousCommand = len(commandList)

        # Check to see if we are conencted to a serial port and if not, 
        # update the list of serial ports in case new ones have been plugged in or out.
        if not serial_port:
            portList2 =[]
            ser = serial.tools.list_ports.comports() #serial.Serial('COM6')  # open serial port
            for specific_port in ser:
                if("Bluetooth" in specific_port.description or "bluetooth" in specific_port.description):
                    portList2.append(specific_port.name+" "+"(Bluetooth)")
                elif("USB" in specific_port.description or "FTDI" in specific_port.manufacturer):
                    portList2.append("(USB) "+specific_port.name)
                elif("Arduino" in specific_port.description):
                    portList2.append(specific_port.description)
                else:
                    portList2.append(specific_port.name)     
                portList2.sort()

            if not portList2:
                portList2.append('None')
            
            window.Element('-PORT-').Update(values=portList2, value=portList2[0])  #update the value of the dropdown witht he new info



        if event == sg.WINDOW_CLOSED:
            break
        
        if not serial_port and (event == '-PORT-' or event == '-LINE END-' or event == '-SPEED-' or event == 'Local Echo' or event == '-AUTOSCCROLL-' or event == '-LINEMODE-'):
            window['-CONNECT-'].SetFocus() #Make sure pressing enter connects with these settings.
            window['Send'].BindReturnKey = False
            window['-CONNECT-'].BindReturnKey = True

        if serial_port and event == '-LINEMODE-':
            if values['-LINEMODE-']:
                window['-OUTPUT-'].SetFocus()
            else:
                window['-INPUT-'].SetFocus()

        if event == '-CONNECT-':
            
            # Search through all entries in portList for the one with the displayed comport NameError
            for portVal in portList:
                port = values['-PORT-'].split(') ')[1]#.split(')')[0]
                # print('PORT = '+port)

            
            if serial_port is None:
                try:
                    serial_port = serial.Serial(port, values['-SPEED-'], timeout=0.1)
                    # window['-OUTPUT-'].print(f'Connected to {port}')
                    sg.cprint(f'Connected to {port}', colors='black on light green')
                    threading.Thread(target=read_serial, args=(serial_port, output_queue, stop_event), daemon=True).start()
                    threading.Thread(target=update_output, args=(output_queue, window, values, stop_event), daemon=True).start()
                    window['-CONNECT-'].update("Disconnect")
                    #rebind the return key to the Send button
                    window['-CONNECT-'].BindReturnKey = False
                    window['Send'].BindReturnKey = True
                    # move focus to text input:
                    window['-INPUT-'].SetFocus()

                except serial.SerialException:
                    # window['-OUTPUT-'].print(f'Failed to connect to {port}')
                    sg.cprint(f'Failed to connect to {port}', colors='black on pink')

            else:
                stop_event.clear() ## try to stop daemon threads ref:https://stackoverflow.com/questions/41131117/how-to-stop-daemon-thread
                serial_port.close()
                serial_port = None
                # window['-OUTPUT-'].print(f'Disconnected from {port}')
                sg.cprint(f'Disconnected from {port}', colors='black on pink')
                window['-CONNECT-'].update("Connect")
                #rebind return key and focus on Connect button
                window['Send'].BindReturnKey = False
                window['-CONNECT-'].BindReturnKey = True
                window['-CONNECT-'].SetFocus() #Make sure pressing enter connects with these settings.




        
        
        
        if event == 'Send' and serial_port:
            previousCommand = 1
            commandList.append(values['-INPUT-']) 
            
            #save this to the list of commands 
            lineEnd =''
            if 'C' in values['-LINE END-'] or 'Both' in values['-LINE END-']:
                lineEnd+=chr(13)
            if 'New' in values['-LINE END-'] or 'Both' in values['-LINE END-']:
                lineEnd+=chr(10)
                
                
            data = values['-INPUT-']+lineEnd
            sg.cprint(f'sending {data}', colors='black on light blue')
            serial_port.write(data.encode())
            window['-INPUT-'].update("")

        if event == '-LINEMODE-':
            window['-INPUT-'].Update(visible=not(values['-LINEMODE-']))  
            window['Send'].Update(visible=not(values['-LINEMODE-']))
            # window.Element('-INPUT-').Update(visible=False)

        if event == '-OUTPUT-' and values['-LINEMODE-'] :
            lineEnd =''
            if 'C' in values['-LINE END-'] or 'Both' in values['-LINE END-']:
                lineEnd+=chr(13)
            if 'New' in values['-LINE END-'] or 'Both' in values['-LINE END-']:
                lineEnd+=chr(10)
                
            input_text = values['-OUTPUT-']
            last_letter = input_text[-1]  # get the last letter (the one user just typed)
            # print(f"User entered: {last_letter}")

            data = last_letter+lineEnd #attach line ending
            sg.cprint(f'sending {data}', colors='black on light blue') #debug
            serial_port.write(data.encode())
            # window['-INPUT-'].update("")
            # sg.cprint(values['-LINEMODE-'], colors='white on green')            
            ## Get the text from the multiline input field
            # input_text = values['-OUTPUT-']
            # last_letter = input_text[-1]        # Do something with the input text
            # print(f"User entered: {last_letter}")
        
        if event == 'Clear Data':
                window['-OUTPUT-'].update("")
        

        # print(f'Focus = {window.FindElementWithFocus().key}')
    window.close()

if __name__ == '__main__':
    main()


