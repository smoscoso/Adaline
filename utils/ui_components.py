import tkinter as tk
from tkinter import ttk

# Colores refinados de la Universidad de Cundinamarca (manteniendo la paleta original)
COLOR_PRIMARY = "#004d25"       # Verde oscuro del escudo
COLOR_PRIMARY_LIGHT = "#006633" # Verde principal más claro para hover
COLOR_SECONDARY = "#ffd700"     # Amarillo/dorado del escudo
COLOR_ACCENT_RED = "#e60000"    # Rojo del mapa en el centro
COLOR_ACCENT_BLUE = "#66ccff"   # Azul claro del mapa en el centro
COLOR_BG = "#FFFFFF"            # Fondo blanco para contraste
COLOR_TEXT = "#333333"          # Texto oscuro para mejor legibilidad
COLOR_TEXT_SECONDARY = "#666666" # Texto secundario
COLOR_LIGHT_BG = "#f5f5f5"      # Fondo claro para secciones
COLOR_BORDER = "#e0e0e0"        # Color para bordes sutiles
COLOR_SUCCESS = "#28a745"       # Verde para éxito

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        # Crear ventana de tooltip con estilo mejorado
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        frame = tk.Frame(self.tooltip, background=COLOR_PRIMARY, bd=0)
        frame.pack(fill="both", expand=True)
        
        label = tk.Label(frame, text=self.text, justify='left',
                       background=COLOR_PRIMARY, foreground="white",
                       relief="flat", borderwidth=0,
                       font=("Arial", 9), padx=8, pady=4)
        label.pack(ipadx=1)
        
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

# Mantener la clase ModernButton pero ajustar los valores predeterminados para que ocupe menos espacio
class ModernButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        self.hover_bg = kwargs.pop('hover_bg', None)
        self.hover_fg = kwargs.pop('hover_fg', None)
        self.original_bg = kwargs.get('bg', None) or kwargs.get('background', None)
        self.original_fg = kwargs.get('fg', None) or kwargs.get('foreground', None)
        
        # Configurar estilo moderno por defecto con tamaños más compactos
        if 'font' not in kwargs:
            kwargs['font'] = ('Arial', 9)  # Reducir tamaño de fuente
        if 'bd' not in kwargs and 'borderwidth' not in kwargs:
            kwargs['bd'] = 0
        if 'relief' not in kwargs:
            kwargs['relief'] = tk.FLAT
        if 'padx' not in kwargs:
            kwargs['padx'] = 10  # Reducir padding horizontal
        if 'pady' not in kwargs:
            kwargs['pady'] = 5   # Reducir padding vertical
            
        tk.Button.__init__(self, master, **kwargs)
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        
    def _on_enter(self, e):
        if self.hover_bg and self['state'] != 'disabled':
            self.config(bg=self.hover_bg)
        if self.hover_fg and self['state'] != 'disabled':
            self.config(fg=self.hover_fg)
            
    def _on_leave(self, e):
        if self.original_bg and self['state'] != 'disabled':
            self.config(bg=self.original_bg)
        if self.original_fg and self['state'] != 'disabled':
            self.config(fg=self.original_fg)
            
    def _on_press(self, e):
        if self['state'] != 'disabled':
            self.config(relief=tk.SUNKEN)
        
    def _on_release(self, e):
        if self['state'] != 'disabled':
            self.config(relief=tk.FLAT)
            self.after(100, lambda: self.config(relief=tk.FLAT))

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """Crea un rectángulo con esquinas redondeadas en un canvas"""
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    
    return canvas.create_polygon(points, **kwargs, smooth=True)

def setup_styles():
    """Configurar estilos para ttk widgets con apariencia más profesional"""
    style = ttk.Style()
    style.theme_use('default')
    
    # Estilo para pestañas
    style.configure('TNotebook', background=COLOR_BG)
    style.configure('TNotebook.Tab', background=COLOR_BG, foreground=COLOR_TEXT, 
                    padding=[15, 5], font=('Arial', 10, 'bold'))
    style.map('TNotebook.Tab', 
              background=[('selected', COLOR_SECONDARY)], 
              foreground=[('selected', COLOR_PRIMARY)])
    
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

