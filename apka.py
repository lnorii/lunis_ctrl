import keyboard
import tkinter as tk
import os

SETTINGS_FILE = "ustawienia.txt"

# Ustawienia wyśrodkowania grafik cyfr
settings = {
    "srodek_licznika_x": 86,
    "srodek_licznika_y": 71,
    "odstep_miedzy_cyframi": 2
}

# Wczytywanie / generowanie ustawień
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                try:
                    key, value = line.split("=", 1)
                    if key.strip() in settings:
                        settings[key.strip()] = int(value.strip())
                except ValueError:
                    pass
else:
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        f.write("# Podaj współrzędne środka dla licznika i odstęp w pikselach\n")
        for key, value in settings.items():
            f.write(f"{key}={value}\n")

count = 0
digit_images = {}
current_canvas_items = []

# Ładowanie obrazków do pamięci
def load_images():
    for i in range(10):
        try:
            digit_images[str(i)] = tk.PhotoImage(file=f"{i}.png")
        except tk.TclError:
            print(f"Brak pliku {i}.png")

# Logika układania cyfr ze sobą
def draw_number():
    global current_canvas_items
    
    # Usuwamy poprzednie cyfry z ekranu
    for item in current_canvas_items:
        canvas.delete(item)
    current_canvas_items.clear()
    
    count_str = str(count)
    
    # Obliczanie całkowitej szerokości wszystkich cyfr razem
    total_width = 0
    for char in count_str:
        if char in digit_images:
            total_width += digit_images[char].width()
    
    total_width += (len(count_str) - 1) * settings["odstep_miedzy_cyframi"]
    
    # Wyliczanie punktu startowego, żeby całość była wyśrodkowana
    current_x = settings["srodek_licznika_x"] - (total_width // 2)
    y = settings["srodek_licznika_y"]
    
    # Rysowanie każdej cyfry od lewej do prawej
    for char in count_str:
        if char in digit_images:
            img = digit_images[char]
            # anchor="center" centruje środek cyfry na wyznaczonej wysokości Y
            item = canvas.create_image(current_x + (img.width() // 2), y, image=img, anchor="center")
            current_canvas_items.append(item)
            current_x += img.width() + settings["odstep_miedzy_cyframi"]

def on_ctrl_z():
    global count
    count += 1
    draw_number()

# Główne okno
root = tk.Tk()
root.title("Licznik")
root.attributes('-topmost', True)

# Automatyczne dostosowanie rozmiaru do pliku tlo.png
try:
    bg_image = tk.PhotoImage(file="tlo.png")
    szerokosc = bg_image.width()
    wysokosc = bg_image.height()
except tk.TclError:
    szerokosc, wysokosc = 172, 142  # Wartości awaryjne
    bg_image = None
    print("Brak pliku tlo.png w folderze")

root.geometry(f"{szerokosc}x{wysokosc}")

canvas = tk.Canvas(root, width=szerokosc, height=wysokosc, highlightthickness=0)
canvas.pack(fill="both", expand=True)

if bg_image:
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

load_images()
draw_number()

keyboard.add_hotkey('ctrl+z', on_ctrl_z, suppress=False)

root.mainloop()