import tkinter as tk
from tkinter import ttk
import time
from utils.ui_components import (COLOR_BG, COLOR_PRIMARY, COLOR_TEXT, COLOR_LIGHT_BG, 
                           COLOR_TEXT_SECONDARY, COLOR_BORDER)
from PIL import Image, ImageTk
import os
import sys

class MainView:
  def __init__(self, root):
      self.root = root
      self.root.title("Adaline Interactivo - Universidad de Cundinamarca")
      self.root.geometry("1000x750")
      self.root.configure(bg=COLOR_BG)
      self.root.minsize(900, 700)
      
      # Configurar estilos modernos
      self.style = self.setup_styles()
      
      # Crear interfaz principal
      self.create_main_interface()
      
  def setup_styles(self):
      """Configurar estilos para ttk widgets con apariencia más profesional"""
      style = ttk.Style()
      style.theme_use('default')
      
      # Estilo para pestañas
      style.configure('TNotebook', background=COLOR_BG)
      style.configure('TNotebook.Tab', background=COLOR_BG, foreground=COLOR_TEXT, 
                      padding=[15, 5], font=('Arial', 10, 'bold'))
      style.map('TNotebook.Tab', 
              background=[('selected', COLOR_PRIMARY)], 
              foreground=[('selected', 'white')])
      
      # Estilo para frames
      style.configure('TFrame', background=COLOR_BG)
      
      # Estilo para combobox
      style.configure('TCombobox', 
                      fieldbackground=COLOR_LIGHT_BG,
                      background=COLOR_PRIMARY,
                      foreground=COLOR_TEXT,
                      arrowcolor=COLOR_PRIMARY)
      style.map('TCombobox',
              fieldbackground=[('readonly', COLOR_LIGHT_BG)],
              selectbackground=[('readonly', COLOR_PRIMARY)],
              selectforeground=[('readonly', 'white')])
      
      # Estilo para separadores
      style.configure('TSeparator', background=COLOR_PRIMARY)
      
      # Estilo para barras de progreso
      style.configure("TProgressbar", 
                      troughcolor=COLOR_LIGHT_BG, 
                      background=COLOR_PRIMARY,
                      thickness=8)
      
      # Estilo para scrollbars
      style.configure("TScrollbar",
                      background=COLOR_BG,
                      troughcolor=COLOR_LIGHT_BG,
                      arrowsize=14)
      
      return style
      
  def create_main_interface(self):
      # Crear marco principal con expansión adecuada
      self.main_frame = tk.Frame(self.root, bg=COLOR_BG)
      self.main_frame.pack(fill='both', expand=True, padx=15, pady=15)
      
      # Crear encabezado
      self.create_header()
      
      # Crear pestañas con estilo mejorado
      self.notebook = ttk.Notebook(self.main_frame)
      self.notebook.pack(fill='both', expand=True, padx=5, pady=10)
      
      # Añadir información de autores
      self.add_authors_info()
      
      # Pestaña para configuración y entrenamiento
      self.config_frame = ttk.Frame(self.notebook)
      self.notebook.add(self.config_frame, text="Configuración y Entrenamiento")
      
      # Pestaña para visualización de error
      self.error_frame = ttk.Frame(self.notebook)
      self.notebook.add(self.error_frame, text="Error vs Épocas")
      
      # Pestaña para salidas obtenidas
      self.obtained_frame = ttk.Frame(self.notebook)
      self.notebook.add(self.obtained_frame, text="Salidas Obtenidas")
      
      # Pestaña para pruebas personalizadas
      self.test_frame = ttk.Frame(self.notebook)
      self.notebook.add(self.test_frame, text="Pruebas Personalizadas")
      
      # Pestaña para proceso de cálculo de pesos
      self.weights_frame = ttk.Frame(self.notebook)
      self.notebook.add(self.weights_frame, text="Proceso de Pesos")
      
      # Crear pie de página
      self.create_footer()

  def obtener_ruta_relativa(self, ruta_archivo):
      if getattr(sys, 'frozen', False):  # Si el programa está empaquetado con PyInstaller
          base_path = sys._MEIPASS       # Carpeta temporal donde PyInstaller extrae archivos
      else:
          base_path = os.path.abspath(".")  # Carpeta normal en modo desarrollo

      return os.path.join(base_path, ruta_archivo)

  def create_header(self):
      # Crear un marco para el encabezado con borde inferior sutil
      header_frame = tk.Frame(self.main_frame, bg=COLOR_LIGHT_BG, height=80)  # Reducir altura
      header_frame.pack(fill='x', pady=(0, 10))  # Reducir espacio
      
      # Añadir un borde inferior sutil
      border_frame = tk.Frame(header_frame, bg=COLOR_BORDER, height=1)
      border_frame.pack(side=tk.BOTTOM, fill='x')
      
      try:
          # Tamaños deseados
          logo_with = 60   # Reducir ancho
          logo_height = 80  # Reducir alto

          # Crear un frame para contener la imagen
          logo_frame = tk.Frame(header_frame, width=logo_with, height=logo_height, bg=COLOR_LIGHT_BG)
          logo_frame.pack(side=tk.LEFT, padx=15, pady=5)  # Reducir padding
          
          try:
              # Obtener la ruta de la imagen de manera segura
              image_path = self.obtener_ruta_relativa(os.path.join("utils", "Images", "escudo_udec.png"))
              
              # Cargar y redimensionar la imagen
              image = Image.open(image_path)
              image = image.resize((logo_with, logo_height), Image.LANCZOS)
              logo_img = ImageTk.PhotoImage(image)

              # Crear un Label con la imagen
              logo_label = tk.Label(logo_frame, image=logo_img, bg=COLOR_LIGHT_BG)
              logo_label.image = logo_img  # Mantener referencia para que no se "pierda" la imagen
              logo_label.pack()

          except Exception as e:
              print(f"Error al cargar la imagen: {e}")
              
              # Como respaldo, dibujamos un canvas con un óvalo verde y texto "UDEC"
              logo_canvas = tk.Canvas(
                  logo_frame, 
                  width=logo_with, 
                  height=logo_height, 
                  bg=COLOR_LIGHT_BG, 
                  highlightthickness=0
              )
              logo_canvas.pack()
              
              logo_canvas.create_oval(
                  5, 5, 
                  logo_with - 5, logo_height - 5, 
                  fill=COLOR_PRIMARY, 
                  outline=""
              )
              logo_canvas.create_text(
                  logo_with / 2, logo_height / 2, 
                  text="UDEC", 
                  fill="white", 
                  font=("Arial", 10, "bold")  # Reducir tamaño
              )

      except Exception as e:
          print(f"Error en la creación del logo: {e}")
          
      # Título y subtítulo con mejor tipografía
      title_frame = tk.Frame(header_frame, bg=COLOR_LIGHT_BG)
      title_frame.pack(side=tk.LEFT, padx=8, pady=5)  # Reducir padding
      
      title_label = tk.Label(title_frame, text="ADALINE", 
                           font=("Arial", 20, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)  # Reducir tamaño
      title_label.pack(anchor='w')
      
      subtitle_label = tk.Label(title_frame, text="Universidad de Cundinamarca", 
                              font=("Arial", 12), bg=COLOR_LIGHT_BG, fg=COLOR_TEXT_SECONDARY)  # Reducir tamaño
      subtitle_label.pack(anchor='w')
      
      # Información del proyecto con mejor alineación
      info_frame = tk.Frame(header_frame, bg=COLOR_LIGHT_BG)
      info_frame.pack(side=tk.RIGHT, padx=15, pady=5)  # Reducir padding
      
  def add_authors_info(self):
      # Crear un marco para la información de autores con estilo mejorado
      authors_frame = tk.Frame(self.main_frame, bg=COLOR_LIGHT_BG, padx=10, pady=5)  # Reducir padding
      authors_frame.pack(fill=tk.X, before=self.notebook)
      
      # Añadir un borde superior e inferior sutil
      top_border = tk.Frame(authors_frame, bg=COLOR_BORDER, height=1)
      top_border.pack(side=tk.TOP, fill='x')
      
      bottom_border = tk.Frame(authors_frame, bg=COLOR_BORDER, height=1)
      bottom_border.pack(side=tk.BOTTOM, fill='x')
      
      # Información de los autores con mejor tipografía
      authors_info = tk.Label(
          authors_frame,
          text="Desarrollado por: Sergio Leonardo Moscoso Ramirez - Miguel Ángel Pardo Lopez",
          font=("Arial", 10),  # Reducir tamaño
          bg=COLOR_LIGHT_BG,
          fg=COLOR_TEXT
      )
      authors_info.pack(side=tk.LEFT, padx=5)  # Reducir padding
      
  def create_footer(self):
      # Crear un marco para el pie de página con estilo mejorado
      footer_frame = tk.Frame(self.main_frame, bg=COLOR_PRIMARY, height=30)  # Reducir altura
      footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
      
      # Añadir un borde superior sutil
      top_border = tk.Frame(footer_frame, bg=COLOR_BORDER, height=1)
      top_border.pack(side=tk.TOP, fill='x')
      
      # Texto del pie de página con mejor tipografía
      footer_text = "© Universidad de Cundinamarca - Simulador de Adaline"
      footer_label = tk.Label(footer_frame, text=footer_text, 
                            font=("Arial", 8), bg=COLOR_PRIMARY, fg="white")  # Reducir tamaño
      footer_label.pack(pady=6)  # Reducir padding