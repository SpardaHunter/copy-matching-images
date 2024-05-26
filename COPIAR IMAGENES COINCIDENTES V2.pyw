import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, messagebox

def seleccionar_carpeta(entry, variable):
    carpeta_seleccionada = filedialog.askdirectory()
    if carpeta_seleccionada:
        variable.set(carpeta_seleccionada)
        entry.delete(0, tk.END)
        entry.insert(0, carpeta_seleccionada)

def procesar_coincidencias():
    opcion_seleccionada = opcion_var.get()
    
    imagenes_folder = imagenes_var.get()
    roms_folder = roms_var.get()
    output_folder = output_var.get()
    
    if opcion_seleccionada == "COPIAR IMAGENES":
        output_txt_path = "roms_sin_coincidencias_totales.txt"

        roms_sin_coincidencias_en_imagenes = []
        roms_sin_coincidencias_totales = []

        total_imagenes = len(os.listdir(imagenes_folder))
        progreso["maximum"] = total_imagenes

        for i, imagen_filename in enumerate(os.listdir(imagenes_folder), start=1):
            imagen_name, imagen_extension = os.path.splitext(imagen_filename)
            imagen_path = os.path.join(imagenes_folder, imagen_filename)

            matching_roms = [rom for rom in os.listdir(roms_folder) if rom.startswith(imagen_name)]

            if matching_roms:
                matching_rom_path = os.path.join(roms_folder, matching_roms[0])
                output_path = os.path.join(output_folder, imagen_filename)
                shutil.copyfile(imagen_path, output_path)
                print(f"Se ha copiado la imagen de {imagen_path} a {output_path}")
            else:
                print(f"No se encontró un archivo ROM correspondiente para {imagen_filename} en ROMS")
                roms_sin_coincidencias_en_imagenes.append(imagen_name)

            progreso["value"] = i
            root.update()

        for rom_filename in os.listdir(roms_folder):
            rom_name, rom_extension = os.path.splitext(rom_filename)
            rom_path = os.path.join(roms_folder, rom_filename)

            matching_imagenes = [imagen for imagen in os.listdir(imagenes_folder) if imagen.startswith(rom_name)]

            if not matching_imagenes:
                print(f"No se encontró un archivo IMAGEN correspondiente para {rom_filename} en IMAGENES")
                roms_sin_coincidencias_totales.append(rom_name)

        if roms_sin_coincidencias_en_imagenes:
            mensaje = "Archivos ROMS sin coincidencias en IMAGENES:\n"
            for rom_sin_coincidencia_en_imagenes in roms_sin_coincidencias_en_imagenes:
                mensaje += f"- {rom_sin_coincidencia_en_imagenes}\n"
        else:
            mensaje = "Todos los archivos ROMS tienen coincidencias en IMAGENES."

        if roms_sin_coincidencias_totales:
            with open(output_txt_path, "w") as output_txt:
                output_txt.write("\nArchivos ROMS sin coincidencias totales:\n")
                for rom_sin_coincidencia_total in roms_sin_coincidencias_totales:
                    output_txt.write(f"- {rom_sin_coincidencia_total}\n")
            mensaje += f"\nSe ha guardado la lista en el archivo: {output_txt_path}"

        messagebox.showinfo("Proceso Completado", mensaje)
    
    elif opcion_seleccionada == "COPIAR ROMS":
        total_roms = len(os.listdir(roms_folder))
        progreso["maximum"] = total_roms

        for i, rom_filename in enumerate(os.listdir(roms_folder), start=1):
            rom_name, rom_extension = os.path.splitext(rom_filename)
            rom_path = os.path.join(roms_folder, rom_filename)

            matching_imagenes = [imagen for imagen in os.listdir(imagenes_folder) if imagen.startswith(rom_name)]

            if matching_imagenes:
                output_path = os.path.join(output_folder, rom_filename)
                shutil.copyfile(rom_path, output_path)
                print(f"Se ha copiado la ROM de {rom_path} a {output_path}")
            else:
                print(f"No se encontró un archivo IMAGEN correspondiente para {rom_filename} en IMAGENES")

            progreso["value"] = i
            root.update()

        messagebox.showinfo("Proceso Completado", "Se han copiado las ROMs correspondientes.")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Proceso de Coincidencias")

# Variables para almacenar las carpetas seleccionadas
imagenes_var = tk.StringVar()
roms_var = tk.StringVar()
output_var = tk.StringVar()
opcion_var = tk.StringVar(value="COPIAR IMAGENES")

# Cuadros de texto para mostrar las carpetas seleccionadas
imagenes_entry = tk.Entry(root, textvariable=imagenes_var, state="readonly", width=40)
roms_entry = tk.Entry(root, textvariable=roms_var, state="readonly", width=40)
output_entry = tk.Entry(root, textvariable=output_var, state="readonly", width=40)

# Etiquetas para mostrar las carpetas seleccionadas
imagenes_label = tk.Label(root, text="Carpeta IMAGENES:")
roms_label = tk.Label(root, text="Carpeta ROMS:")
output_label = tk.Label(root, text="Carpeta OUTPUT:")

imagenes_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
roms_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
output_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

imagenes_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
roms_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
output_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Botones para seleccionar las carpetas
imagenes_button = tk.Button(root, text="Seleccionar", command=lambda: seleccionar_carpeta(imagenes_entry, imagenes_var))
roms_button = tk.Button(root, text="Seleccionar", command=lambda: seleccionar_carpeta(roms_entry, roms_var))
output_button = tk.Button(root, text="Seleccionar", command=lambda: seleccionar_carpeta(output_entry, output_var))

imagenes_button.grid(row=1, column=2, padx=5, pady=5, sticky="w")
roms_button.grid(row=2, column=2, padx=5, pady=5, sticky="w")
output_button.grid(row=3, column=2, padx=5, pady=5, sticky="w")

# Combobox para seleccionar la opción
opcion_label = tk.Label(root, text="Seleccionar opción:")
opcion_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

opcion_combobox = ttk.Combobox(root, textvariable=opcion_var, values=["COPIAR IMAGENES", "COPIAR ROMS"], state="readonly")
opcion_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Barra de progreso
progreso = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progreso.grid(row=4, column=0, columnspan=3, pady=10)

# Botón para iniciar el proceso
procesar_button = tk.Button(root, text="Procesar Coincidencias", command=procesar_coincidencias)
procesar_button.grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()
