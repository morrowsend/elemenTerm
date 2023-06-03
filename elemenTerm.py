# #######  Enumerates Serial ports and prints the names and
# #######  type (bluetooth, USB, etc) in a dropdown menu
# import serial.tools.list_ports
# import serial

# import PySimpleGUI as sg


# debug =0;


# def main():
#     # sg.theme('TanBlue')

#     # column1 = [
#     #     [sg.Text('Column 1', background_color=sg.DEFAULT_BACKGROUND_COLOR,
#     #           justification='center', size=(10, 1))],
#     #     [sg.Spin(values=('Spin Box 1', '2', '3'),
#     #              initial_value='Spin Box 1', key='spin1')],
#     #     [sg.Spin(values=('Spin Box 1', '2', '3'),
#     #              initial_value='Spin Box 2', key='spin2')],
#     #     [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3', key='spin3')]]


#       



#     layout = [
#         [sg.Text('All graphic widgets in one form!', size=(30, 1), font=("Helvetica", 25))],
#         [sg.Combo((portList), key='combo', size=(20, 1))],

#         [sg.Text('Here is some text.... and a place to enter text')],
#         [sg.InputText('This is my text', key='in1')],
#         # [sg.CBox('Checkbox', key='cb1'), sg.CBox(
#         #     'My second checkbox!', key='cb2', default=True)],
#         # [sg.Radio('My first Radio!     ', "RADIO1", key='rad1', default=True),
#         #  sg.Radio('My second Radio!', "RADIO1", key='rad2')],
#         [sg.MLine(default_text='This is the default Text should you decide not to type anything', size=(35, 3),
#                   key='multi1')],

#         [sg.Button('Exit'),
#          sg.Text(' ' * 40), sg.Button('List Ports'), sg.Button('SaveSettings'), sg.Button('LoadSettings')]
#     ]

#     window = sg.Window('Form Fill Demonstration', layout, default_element_size=(40, 1), grab_anywhere=False)

#     while True:
#         event, values = window.read()

#         if event == 'SaveSettings':
#             filename = sg.popup_get_file('Save Settings', save_as=True, no_window=True)
#             window.SaveToDisk(filename)
#             # save(values)
#         elif event == 'LoadSettings':
#             filename = sg.popup_get_file('Load Settings', no_window=True)
#             window.LoadFromDisk(filename)
#             # load(form)
#         elif event == 'List Ports':
            
#             # This is the normal print that comes with simple GUI
#             sg.Print('Re-routing the stdout', do_not_reroute_stdout=False)

#             # this is clobbering the print command, and replacing it with sg's Print()
#             # print = sg.Print

#             # this will now output to the sg display.
#             print('This is a normal print that has been re-routed.')
#             portList = []

#             ser = serial.tools.list_ports.comports() #serial.Serial('COM6')  # open serial port
#             for specific_port in ser:
#                  print("device = ", specific_port.device) 
#                  print("name = ", specific_port.name) 
#                  print("description = ", specific_port.description) 
#                  print("hwid = ", specific_port.hwid)
#                  print("vid = ", specific_port.vid)
#                  print("pid = ", specific_port.pid)
#                  print("serial_number = ", specific_port.serial_number)
#                  print("location = ", specific_port.location)
#                  print("manufacturer = ", specific_port.manufacturer)
#                  print("product = ", specific_port.product)
#                  print("interface = ", specific_port.interface)
              



#         elif event in ('Exit', None):
#             break 
        
#     window.close()
# if __name__ == '__main__':
#     main()








### CHAT GPT CODE:


##### Working sends  multiple characters with each press of the "SEND" button
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
    


    while True:
        event, values = window.read( timeout=1000)

        if event != "timeout":
            sg.popup(event)


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
            

            # up button pressed, pull previous command
            # currentCommand = currentCommand-1
            # window['-INPUT-'].update(commandList[currentCommand])
            # commandList.append(values['-INPUT-'])

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






################  Clears screen with every serial print
# import serial
# import threading
# import queue
# import PySimpleGUI as sg

# def create_layout():
#     layout = [
#         [sg.Text('Serial Port:'), sg.Input(key='-PORT-', size=(10, 1)), sg.Button('Connect')],
#         [sg.Multiline(key='-OUTPUT-', size=(80, 20), autoscroll=True, reroute_stdout=True, write_only=True)],
#         [sg.Input(key='-INPUT-', size=(60, 1), enable_events=True), sg.Button('Send')],
#     ]
#     return layout

# def read_serial(serial_port, output_queue):
#     while True:
#         if serial_port and serial_port.in_waiting:
#             data = serial_port.read(serial_port.in_waiting).decode()
#             output_queue.put(data)

# def update_output(output_queue, window):
#     while True:
#         if not output_queue.empty():
#             data = output_queue.get()
#             window['-OUTPUT-'](data)  # Update the output area
#         else:
#             window.refresh()

# def main():
#     layout = create_layout()
#     window = sg.Window('Serial Terminal', layout, return_keyboard_events=True)

#     serial_port = None
#     output_queue = queue.Queue()

#     while True:
#         event, values = window.read()

#         if event == sg.WINDOW_CLOSED:
#             break
        
#         if event == 'Connect':
#             port = values['-PORT-']
#             try:
#                 serial_port = serial.Serial(port, 9600, timeout=0.1)
#                 window['-OUTPUT-'].print(f'Connected to {port}')
#                 threading.Thread(target=read_serial, args=(serial_port, output_queue), daemon=True).start()
#                 threading.Thread(target=update_output, args=(output_queue, window), daemon=True).start()
#             except serial.SerialException:
#                 window['-OUTPUT-'].print(f'Failed to connect to {port}')
        
#         if event == '-INPUT-' and serial_port:
#             data = values['-INPUT-']
#             serial_port.write(data.encode())
#             window['-INPUT-']('')
        
#         if event == 'Send' and serial_port:
#             data = values['-INPUT-']
#             serial_port.write(data.encode())
#             # window['-INPUT-']('')
        
#     window.close()

# if __name__ == '__main__':
#     main()





# ##### WORKING SEPARATE INPUT LINE CHARACTER BY CHARACTER
# import serial
# import threading
# import queue
# import PySimpleGUI as sg

# def create_layout():
#     layout = [
#         [sg.Text('Serial Port:'), sg.Input(key='-PORT-', size=(10, 1)), sg.Button('Connect')],
#         [sg.Multiline(key='-OUTPUT-', size=(80, 20), autoscroll=True, reroute_stdout=True, write_only=True)],
#         [sg.Input(key='-INPUT-', size=(60, 1), enable_events=True), sg.Button('Send')],
#     ]
#     return layout

# def read_serial(serial_port, output_queue):
#     while True:
#         if serial_port and serial_port.in_waiting:
#             data = serial_port.read(serial_port.in_waiting).decode()
#             output_queue.put(data)

# def update_output(output_queue, window):
#     received_data = ""
#     while True:
#         if not output_queue.empty():
#             data = output_queue.get()
#             received_data += data
#             window['-OUTPUT-'](received_data)  # Update the output area
#         else:
#             window.refresh()

# def main():
#     layout = create_layout()
#     window = sg.Window('Serial Terminal', layout, return_keyboard_events=True)

#     serial_port = None
#     output_queue = queue.Queue()

#     while True:
#         event, values = window.read()

#         if event == sg.WINDOW_CLOSED:
#             break
        
#         if event == 'Connect':
#             port = values['-PORT-']
#             try:
#                 serial_port = serial.Serial(port, 9600, timeout=0.1)
#                 window['-OUTPUT-'].print(f'Connected to {port}')
#                 threading.Thread(target=read_serial, args=(serial_port, output_queue), daemon=True).start()
#                 threading.Thread(target=update_output, args=(output_queue, window), daemon=True).start()
#             except serial.SerialException:
#                 window['-OUTPUT-'].print(f'Failed to connect to {port}')
        
#         if event == '-INPUT-' and serial_port:
#             data = values['-INPUT-']
#             serial_port.write(data.encode())
#             window['-INPUT-']('')
        
#         if event == 'Send' and serial_port:
#             data = values['-INPUT-']
#             serial_port.write(data.encode())
#             window['-INPUT-']('')
        
#     window.close()

# if __name__ == '__main__':
#     main()







##### ALMOST THERE!!! Just repeats its own output though...
# import serial
# import threading
# import queue
# import PySimpleGUI as sg

# def create_layout():
#     layout = [
#         [sg.Text('Serial Port:'), sg.Input(key='-PORT-', size=(10, 1)), sg.Button('Connect')],
#         [sg.Multiline(key='-OUTPUT-', size=(80, 20), autoscroll=True, reroute_stdout=True, write_only=False, enable_events=True)],
#     ]
#     return layout

# def read_serial(serial_port, output_queue):
#     while True:
#         if serial_port and serial_port.in_waiting:
#             data = serial_port.read(serial_port.in_waiting).decode()
#             output_queue.put(data)

# def update_output(output_queue, window):
#     received_data = ""
#     while True:
#         if not output_queue.empty():
#             data = output_queue.get()
#             received_data += data
#             window['-OUTPUT-'](received_data)  # Update the output area
#         else:
#             window.refresh()

# def main():
#     layout = create_layout()
#     window = sg.Window('Serial Terminal', layout)

#     serial_port = None
#     output_queue = queue.Queue()

#     while True:
#         event, values = window.read()

#         if event == sg.WINDOW_CLOSED:
#             break
        
#         if event == 'Connect':
#             port = values['-PORT-']
#             if serial_port is None:
#                 try:
#                     serial_port = serial.Serial(port, 9600, timeout=0.1)
#                     window['-OUTPUT-'].print(f'Connected to {port}')
#                     threading.Thread(target=read_serial, args=(serial_port, output_queue), daemon=True).start()
#                     threading.Thread(target=update_output, args=(output_queue, window), daemon=True).start()
#                     connect_button_text = "Disconnect"
#                 except serial.SerialException:
#                     window['-OUTPUT-'].print(f'Failed to connect to {port}')
#             else:
#                 serial_port.close()
#                 serial_port = None
#                 window['-OUTPUT-'].print(f'Disconnected from {port}')
#                 connect_button_text = "Connect"

#         window['Connect'].update(text=connect_button_text)
        
#         if event == '-OUTPUT-' and serial_port:
#             data = values['-OUTPUT-'].split('\n')[-1]  # Get the last line of the multiline input
#             serial_port.write(data.encode())
#             window['-OUTPUT-'](values['-OUTPUT-'] + '\n')  # Append a new line to maintain visual separation
    
#     window.close()

# if __name__ == '__main__':
#     main()





# #Capture keypresses on a window one at a time...
# ### ref: https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Keyboard.py
# # #!/usr/bin/env python
# import sys
# import PySimpleGUI as sg

# # Recipe for getting keys, one at a time as they are released
# # If want to use the space bar, then be sure and disable the "default focus"

# layout = [[sg.Text("Press a key or scroll mouse")],
#           [sg.Text("", size=(18, 1), key='text')],
#           [sg.Button("OK", key='OK')]]

# window = sg.Window("Keyboard Test", layout,
#                    return_keyboard_events=True, use_default_focus=False)

# # ---===--- Loop taking in user input --- #
# while True:
#     event, values = window.read()
#     text_elem = window['text']
#     if event in ("OK", None):
#         print(event, "exiting")
#         break
#     if len(event) == 1:
#         text_elem.update(value='%s - %s' % (event, ord(event)))
#     if event is not None:
#         text_elem.update(event)


# window.close()






############  Prints new line with each serial print DOES NOT ECHO locally
############  LIkely the same as one example
# import serial
# import threading
# import queue
# import PySimpleGUI as sg

# def create_layout():
#     layout = [
#         [sg.Text('Serial Port:'), sg.Input(key='-PORT-', size=(10, 1)), sg.Button('Connect')],
#         [sg.Multiline(key='-OUTPUT-', size=(80, 20), autoscroll=True, reroute_stdout=True, write_only=True)],
#         [sg.Input(key='-INPUT-', size=(60, 1), enable_events=True), sg.Button('Send')],
#     ]
#     return layout

# def read_serial(serial_port, output_queue):
#     while True:
#         if serial_port and serial_port.in_waiting:
#             data = serial_port.read(serial_port.in_waiting).decode()
#             output_queue.put(data)

# def update_output(output_queue, window):
#     received_data = ""
#     while True:
#         if not output_queue.empty():
#             data = output_queue.get()
#             received_data += data
#             window['-OUTPUT-'](received_data)  # Update the output area
#         else:
#             window.refresh()

# def main():
#     layout = create_layout()
#     window = sg.Window('Serial Terminal', layout, return_keyboard_events=True)

#     serial_port = None
#     output_queue = queue.Queue()

#     while True:
#         event, values = window.read()

#         if event == sg.WINDOW_CLOSED:
#             break
        
#         if event == 'Connect':
#             port = values['-PORT-']
#             try:
#                 serial_port = serial.Serial(port, 9600, timeout=0.1)
#                 window['-OUTPUT-'].print(f'Connected to {port}')
#                 threading.Thread(target=read_serial, args=(serial_port, output_queue), daemon=True).start()
#                 threading.Thread(target=update_output, args=(output_queue, window), daemon=True).start()
#             except serial.SerialException:
#                 window['-OUTPUT-'].print(f'Failed to connect to {port}')
        
#         if event == '-INPUT-' and serial_port:
#             data = values['-INPUT-']
#             serial_port.write(data.encode())
#             window['-INPUT-']('')
        
#         if event == 'Send' and serial_port:
#             data = values['-INPUT-']
#             serial_port.write(data.encode())
#             window['-INPUT-']('')
        
#     window.close()

# if __name__ == '__main__':
#     main()







# ###################  ALMOST THERE, It prints each serial statement correctly, but does not locally echo
# ###################  only issue is special keys. sending a SHIFT, RETURN, ARROW etc. reprints everything on the screen again as if it were all fresh inputs
# import serial
# import threading
# import queue
# import PySimpleGUI as sg

# def create_layout():
#     layout = [
#         [sg.Text('Serial Port:'), sg.Input(key='-PORT-', size=(10, 1)), sg.Button('Connect')],
#         [sg.Multiline(key='-OUTPUT-', size=(80, 20), autoscroll=True, reroute_stdout=True, write_only=False, enable_events=True)],
#     ]
#     return layout

# def read_serial(serial_port, output_queue):
#     while True:
#         if serial_port and serial_port.in_waiting:
#             data = serial_port.read(serial_port.in_waiting).decode()
#             output_queue.put(data)

# def update_output(output_queue, window):
#     received_data = ""
#     while True:
#         if not output_queue.empty():
#             data = output_queue.get()
#             received_data += data
#             window['-OUTPUT-'](received_data)  # Update the output area
#         else:
#             window.refresh()

# def main():
#     layout = create_layout()
#     window = sg.Window('Serial Terminal', layout)

#     serial_port = None
#     output_queue = queue.Queue()

#     while True:
#         event, values = window.read()

#         if event == sg.WINDOW_CLOSED:
#             break
        
#         if event == 'Connect':
#             port = values['-PORT-']
#             try:
#                 serial_port = serial.Serial(port, 9600, timeout=0.1)
#                 window['-OUTPUT-'].print(f'Connected to {port}')
#                 threading.Thread(target=read_serial, args=(serial_port, output_queue), daemon=True).start()
#                 threading.Thread(target=update_output, args=(output_queue, window), daemon=True).start()
#             except serial.SerialException:
#                 window['-OUTPUT-'].print(f'Failed to connect to {port}')
        
#         if event == '-OUTPUT-' and serial_port:
#             data = values['-OUTPUT-'][-1]  # Get the last character of the multiline input
#             serial_port.write(data.encode())
#             window['-OUTPUT-'](values['-OUTPUT-']+'\n')  # Append a new line to maintain visual separation
    
#     window.close()

# if __name__ == '__main__':
#     main()






# ### One you start the serial threads, it takes a whole processor 25% of my quad core. Even if you stop_ them...""
# import serial
# import serial.tools.list_ports

# import threading
# import queue
# import PySimpleGUI as sg

# stop_event= threading.Event()


# # Once serial threads are started they eat about 25% of my 
# # entire processor. One whole core... Even when I stop_event.clear()
# def read_serial(serial_port, output_queue, stop_event):
#     while True:
#         if serial_port and serial_port.in_waiting:
#             data = serial_port.read(serial_port.in_waiting).decode()
#             output_queue.put(data)

# def update_output(output_queue, window, stop_event):
#     received_data = ""
#     while True:
#         if not output_queue.empty():
#             data = output_queue.get()
#             received_data += data
#             window['-OUTPUT-'](received_data)  # Update the output area
#         else:
#             window.refresh()

# def main():
#     portList = []

#     ser = serial.tools.list_ports.comports() #serial.Serial('COM6')  # open serial port
#     for specific_port in ser:
#         # print("device = ", specific_port.device) 
#         # print("name = ", specific_port.name) 
#         # print("description = ", specific_port.description) 
#         # print("hwid = ", specific_port.hwid)
#         # print("vid = ", specific_port.vid)
#         # print("pid = ", specific_port.pid)
#         # print("serial_number = ", specific_port.serial_number)
#         # print("location = ", specific_port.location)
#         # print("manufacturer = ", specific_port.manufacturer)
#         # print("product = ", specific_port.product)
#         # print("interface = ", specific_port.interface)

#         # if("Bluetooth" in specific_port.description or "bluetooth" in specific_port.description):
#         #     portList.append(specific_port.name+" "+"(Bluetooth)")
#         # elif("CH340" in specific_port.description or "FTDI" in specific_port.description):
#         #     portList.append("(USB) "+specific_port.name)
#         # elif("Arduino" in specific_port.description):
#         #     portList.append(specific_port.description)
#         # else:
#         portList.append(specific_port.name)     
#         portList.sort() 
    
#     layout = [
#         [sg.Text('Serial Port:'), sg.Combo((portList), key='-PORT-', size=(20, 1), default_value=portList[0]), sg.Button('Connect', key='-CONNECT-')],
#         [sg.Multiline(key='-OUTPUT-', size=(80, 20), reroute_cprint=True, autoscroll=True, reroute_stdout=True, write_only=False, enable_events=True)],
#     ]    
    
#     window = sg.Window('Serial Terminal', layout, return_keyboard_events=True)
    
    
#     sg.cprint_set_output_destination(window, '-OUTPUT-')



#     serial_port = None
#     output_queue = queue.Queue()

#     while True:
#         event, values = window.read()

#         if event == sg.WINDOW_CLOSED:
#             break
        
#         if event == '-CONNECT-':
#             port = values['-PORT-']
#             if serial_port is None:
#                 try:
#                     serial_port = serial.Serial(port, 9600, timeout=0.1)
#                     # window['-OUTPUT-'].print(f'Connected to {port}')
#                     sg.cprint(f'Connected to {port}', colors='black on light green')

#                     threading.Thread(target=read_serial, args=(serial_port, output_queue, stop_event), daemon=True).start()
#                     threading.Thread(target=update_output, args=(output_queue, window, stop_event), daemon=True).start()
#                     window['-CONNECT-'].update("Disconnect")
#                 except serial.SerialException:
#                     # window['-OUTPUT-'].print(f'Failed to connect to {port}')
#                     sg.cprint(f'Failed to connect to {port}', colors='black on pink')
#             else:
#                 stop_event.clear() ## try to stop daemon threads ref:https://stackoverflow.com/questions/41131117/how-to-stop-daemon-thread
#                 serial_port.close()
#                 serial_port = None
#                 # window['-OUTPUT-'].print(f'Disconnected from {port}')
#                 sg.cprint(f'Disconnected from {port}', colors='black on pink')
#                 window['-CONNECT-'].update("Connect")
#         # Thanks ChatGPT... 
#         # This is dumb... it simply reads the last line int he multi window and sends it to serial
#         # This expects that when you type, your new text will be on a new line
#         # and if you press space or return or any special key, it will simply ignore the keycode you 
#         # pressed and instead copy the ASCII text in the previous line
#         if event == '-OUTPUT-' :#and serial_port:
#             data = values['-OUTPUT-'][-1]  # Get the last line of the multiline input
#             # sg.cprint("I sent ", hex(ord(data)), colors='black on light blue')
#             sg.cprint("\nI sent "+data, colors='black on light blue')
#             serial_port.write(data.encode())
#             #window['-OUTPUT-'](values['-OUTPUT-'])  # Append a new line to maintain visual separation
            
            
        
#     window.close()

# if __name__ == '__main__':
#     main()