import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
from PIL import Image, ImageTk
import os

class PippidonCustomizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pippidon Customizer")
        
        # Directorios
        self.base_path = "resources/base/"
        self.face_path = "resources/face/"
        
        # Cargar imágenes base
        self.base_images = {}
        self.modified_images = {}  # Para almacenar imágenes modificadas
        self.load_base_images()
        
        # Marco izquierdo (Vista previa)
        self.preview_frame = tk.Frame(root)
        self.preview_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.preview_frame, width=380, height=380, bg="white")
        self.canvas.pack()
        
        # Marco derecho (Opciones)
        self.options_frame = tk.Frame(root)
        self.options_frame.pack(side=tk.RIGHT, padx=10, pady=10, anchor="n")
        
        self.notebook = ttk.Notebook(self.options_frame)
        self.notebook.pack(side=tk.TOP, fill=tk.X)
        
        # Crear pestañas para personalización
        self.tabs = {}
        for category in ["Cuerpo", "Cara", "Borde", "Sombrero", "Disfraz Adelante", "Disfraz Atrás", "Accesorio"]:
            frame = tk.Frame(self.notebook)
            self.notebook.add(frame, text=category)
            self.tabs[category] = frame
        
        # Controles de color para el cuerpo, cara y borde en la misma pestaña
        self.body_color = "#6ac1c1"
        self.face_color = "#fc4729"
        self.border_color = "#faf1d9"
        
        if "Cuerpo" in self.tabs:
            tk.Label(self.tabs["Cuerpo"], text="Color del Cuerpo:").pack()
            self.body_color_button = tk.Button(self.tabs["Cuerpo"], bg=self.body_color, width=10, command=self.change_body_color)
            self.body_color_button.pack()
            
            tk.Label(self.tabs["Cuerpo"], text="Color de la Cara:").pack()
            self.face_color_button = tk.Button(self.tabs["Cuerpo"], bg=self.face_color, width=10, command=self.change_face_color)
            self.face_color_button.pack()
            
            tk.Label(self.tabs["Cuerpo"], text="Color del Borde:").pack()
            self.border_color_button = tk.Button(self.tabs["Cuerpo"], bg=self.border_color, width=10, command=self.change_border_color)
            self.border_color_button.pack()
        
        # Mostrar miniaturas en la pestaña "Cara"
        self.face_images = {}
        self.selected_face = None
        self.display_face_options()
        
        # Botón de guardar
        self.save_button = tk.Button(self.options_frame, text="Guardar", command=self.save_customized_sprites)
        self.save_button.pack(pady=10)
        
        # Imagen actual
        self.update_preview()
    
    def apply_color_change(self, image, target_color, new_color):
        image = image.convert("RGBA")
        data = image.getdata()
        new_data = []
        
        target_color = tuple(int(target_color[i:i+2], 16) for i in (1, 3, 5))
        new_color = tuple(int(new_color[i:i+2], 16) for i in (1, 3, 5))
        
        for item in data:
            if abs(item[0] - target_color[0]) < 30 and abs(item[1] - target_color[1]) < 30 and abs(item[2] - target_color[2]) < 30:
                new_data.append(new_color + (item[3],))
            else:
                new_data.append(item)
        
        image.putdata(new_data)
        return image
    
    def change_body_color(self):
        color = colorchooser.askcolor(title="Selecciona el color del cuerpo")[1]
        if color:
            self.body_color = color
            self.body_color_button.config(bg=color)
            self.update_preview()
    
    def change_face_color(self):
        color = colorchooser.askcolor(title="Selecciona el color de la cara")[1]
        if color:
            self.face_color = color
            self.face_color_button.config(bg=color)
            self.update_preview()
    
    def change_border_color(self):
        color = colorchooser.askcolor(title="Selecciona el color del borde")[1]
        if color:
            self.border_color = color
            self.border_color_button.config(bg=color)
            self.update_preview()
    
    def display_face_options(self):
        for file in os.listdir(self.face_path):
            if file.endswith(".png"):
                path = os.path.join(self.face_path, file)
                img = Image.open(path).resize((50, 50))
                img_tk = ImageTk.PhotoImage(img)
                self.face_images[file] = img
                btn = tk.Button(self.tabs["Cara"], image=img_tk, command=lambda f=file: self.select_face(f))
                btn.image = img_tk
                btn.pack(side=tk.LEFT, padx=5)
    
    def select_face(self, face_file):
        self.selected_face = self.face_images.get(face_file)
        self.update_preview()
    
    def load_base_images(self):
        for file in os.listdir(self.base_path):
            if file.endswith(".png"):
                path = os.path.join(self.base_path, file)
                self.base_images[file] = Image.open(path).convert("RGBA")
    
    def update_preview(self):
        # Parámetros predeterminados para los accesorios en el apartado "cara"
        accessory_params = {
            "pippidonidle0.png": {"position": (100, 10), "size": (300, 300), "rotation": 0},
            "pippidonidle1.png": {"position": (12, 12), "size": (50, 50), "rotation": 5},
            "pippidonidle2.png": {"position": (14, 14), "size": (50, 50), "rotation": -5},
            "pippidonidle3.png": {"position": (10, 10), "size": (50, 50), "rotation": 0},
            "pippidonidle4.png": {"position": (12, 12), "size": (50, 50), "rotation": 5},
            "pippidonidle5.png": {"position": (14, 14), "size": (50, 50), "rotation": -5},
            "pippidonkiai0.png": {"position": (20, 20), "size": (60, 60), "rotation": 0},
            "pippidonkiai1.png": {"position": (22, 22), "size": (60, 60), "rotation": 10},
            "pippidonkiai2.png": {"position": (24, 24), "size": (60, 60), "rotation": -10},
            "pippidonkiai3.png": {"position": (20, 20), "size": (60, 60), "rotation": 0},
            "pippidonfail0.png": {"position": (15, 15), "size": (55, 55), "rotation": 0},
            "pippidonfail1.png": {"position": (17, 17), "size": (55, 55), "rotation": 5},
            "pippidonclear0.png": {"position": (10, 10), "size": (50, 50), "rotation": 0},
            "pippidonclear1.png": {"position": (12, 12), "size": (50, 50), "rotation": 5},
            "pippidonclear2.png": {"position": (14, 14), "size": (50, 50), "rotation": -5},
            "pippidonclear3.png": {"position": (10, 10), "size": (50, 50), "rotation": 0},
            "pippidonclear4.png": {"position": (12, 12), "size": (50, 50), "rotation": 5},
            "pippidonclear5.png": {"position": (14, 14), "size": (50, 50), "rotation": -5},
            "pippidonclear6.png": {"position": (16, 16), "size": (50, 50), "rotation": 0},
        }

        for filename, img in self.base_images.items():
            modified_img = img.copy()
            modified_img = self.apply_color_change(modified_img, "#6ac1c1", self.body_color)
            modified_img = self.apply_color_change(modified_img, "#fc4729", self.face_color)
            modified_img = self.apply_color_change(modified_img, "#faf1d9", self.border_color)
            
            if self.selected_face:
                # Obtener parámetros del accesorio
                params = accessory_params.get(filename, {"position": (0, 0), "size": (50, 50), "rotation": 0})
                position = params["position"]
                size = params["size"]
                rotation = params["rotation"]

                # Modificar el accesorio según los parámetros
                accessory = self.selected_face.resize(size).rotate(rotation, expand=True)
                modified_img.paste(accessory, position, accessory)

            self.modified_images[filename] = modified_img
        
        img_tk = ImageTk.PhotoImage(self.modified_images["pippidonidle0.png"])
        self.canvas.create_image(190, 190, image=img_tk)
        self.canvas.image = img_tk
    
    def save_customized_sprites(self):
        folder_selected = filedialog.askdirectory()
        if not folder_selected:
            return
        for filename, image in self.modified_images.items():
            image.save(os.path.join(folder_selected, filename))

if __name__ == "__main__":
    root = tk.Tk()
    app = PippidonCustomizer(root)
    root.mainloop()
