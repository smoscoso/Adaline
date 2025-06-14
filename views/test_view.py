import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.ui_components import (COLOR_BG, COLOR_LIGHT_BG, COLOR_PRIMARY, COLOR_TEXT, 
                         COLOR_SECONDARY, COLOR_ACCENT_RED, COLOR_TEXT_SECONDARY, COLOR_BORDER, ModernButton)
import pandas as pd

class TestView:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.setup_test_tab()
        
    def setup_test_tab(self):
        """Set up the custom testing tab with improved style"""
        self.test_container = tk.Frame(self.parent, bg=COLOR_BG)
        self.test_container.pack(fill='both', expand=True, padx=5, pady=5)  # Reducido padding
        
        # Create a scrollable frame for the content with improved style
        self.test_scroll_frame = tk.Frame(self.test_container, bg=COLOR_BG)
        self.test_scroll_frame.pack(fill='both', expand=True)
        
        # Add vertical scrollbar with improved style
        y_scrollbar = ttk.Scrollbar(self.test_scroll_frame, orient="vertical")
        y_scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # Create a canvas for scrolling with improved style
        self.test_canvas = tk.Canvas(self.test_scroll_frame, bg=COLOR_BG,
                           yscrollcommand=y_scrollbar.set,
                           highlightthickness=0)
        self.test_canvas.pack(side=tk.LEFT, fill='both', expand=True)
        
        # Configure the scrollbar
        y_scrollbar.config(command=self.test_canvas.yview)
        
        # Create a frame inside the canvas for the content
        self.test_content_frame = tk.Frame(self.test_canvas, bg=COLOR_BG)
        self.test_canvas.create_window((0, 0), window=self.test_content_frame, anchor='nw')
        
        # Title with improved style
        title_label = tk.Label(self.test_content_frame, text="Pruebas Personalizadas", 
                         font=("Arial", 12, "bold"), bg=COLOR_BG, fg=COLOR_PRIMARY)  # Reducido tamaño
        title_label.pack(pady=(0, 5))  # Reducido padding
        
        # Input card with improved style
        self.test_input_card = tk.Frame(self.test_content_frame, bg=COLOR_LIGHT_BG, bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
        self.test_input_card.pack(fill='x', pady=3)  # Reducido padding
        
        # Card header with improved style
        test_input_header = tk.Frame(self.test_input_card, bg=COLOR_PRIMARY, height=25)  # Reducido altura
        test_input_header.pack(fill='x')
        
        test_input_title = tk.Label(test_input_header, text="Entradas Personalizadas", 
                                font=("Arial", 10, "bold"), bg=COLOR_PRIMARY, fg="white", padx=8, pady=3)  # Reducido tamaño y padding
        test_input_title.pack(anchor='w')
        
        # Card content with improved style
        test_input_content = tk.Frame(self.test_input_card, bg=COLOR_LIGHT_BG, padx=10, pady=5)  # Reducido padding
        test_input_content.pack(fill='x')
        
        # Message with improved style
        message_label = tk.Label(test_input_content, 
                           text="Entrene el modelo primero, luego seleccione un caso para probar", 
                           bg=COLOR_LIGHT_BG, fg=COLOR_TEXT_SECONDARY, font=("Arial", 8))  # Reducido tamaño
        message_label.pack(pady=2)  # Reducido padding
        
        # Add case selection dropdown
        case_frame = tk.Frame(test_input_content, bg=COLOR_LIGHT_BG)
        case_frame.pack(fill='x', pady=3)  # Reducido padding
        
        case_label = tk.Label(case_frame, text="Seleccionar caso:", 
                         bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY, font=("Arial", 9))  # Reducido tamaño
        case_label.pack(side=tk.LEFT, padx=3)  # Reducido padding
        
        self.test_case_var = tk.StringVar()
        self.test_case_combo = ttk.Combobox(case_frame, textvariable=self.test_case_var, state="readonly", 
                                       font=("Arial", 9), width=18)  # Reducido tamaño y ancho
        self.test_case_combo['values'] = []  # Inicialmente vacío, se llenará con casos entrenados
        self.test_case_combo.pack(side=tk.LEFT, padx=3)  # Reducido padding
        
        # Add a button to load test data with weights
        load_test_frame = tk.Frame(test_input_content, bg=COLOR_LIGHT_BG)
        load_test_frame.pack(fill='x', pady=3)
        
        self.load_test_button = ModernButton(
            load_test_frame, 
            text="Cargar Datos de Prueba", 
            bg=COLOR_SECONDARY, 
            fg=COLOR_PRIMARY, 
            font=("Arial", 9, "bold"),
            hover_bg=COLOR_PRIMARY,
            hover_fg="white",
            padx=10,
            pady=3,
            bd=0,
            relief=tk.FLAT
        )
        self.load_test_button.pack(anchor='w')
        
        # Weights card with improved style
        self.weights_card = tk.Frame(self.test_content_frame, bg=COLOR_LIGHT_BG, bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
        self.weights_card.pack(fill='x', pady=3)  # Reducido padding
        
        # Card header with improved style
        weights_header = tk.Frame(self.weights_card, bg=COLOR_PRIMARY, height=25)  # Reducido altura
        weights_header.pack(fill='x')
        
        weights_title = tk.Label(weights_header, text="Pesos y Sesgo", 
                            font=("Arial", 10, "bold"), bg=COLOR_PRIMARY, fg="white", padx=8, pady=3)  # Reducido tamaño y padding
        weights_title.pack(anchor='w')
        
        # Card content with improved style
        weights_content = tk.Frame(self.weights_card, bg=COLOR_LIGHT_BG, padx=10, pady=5)  # Reducido padding
        weights_content.pack(fill='x')
        
        # Frame for weight fields
        self.weights_frame = tk.Frame(weights_content, bg=COLOR_LIGHT_BG)
        self.weights_frame.pack(fill='x', pady=3)
        
        # Initial placeholder
        self.weights_placeholder = tk.Label(self.weights_frame, 
                                     text="Seleccione un caso para ver y modificar los pesos", 
                                     bg=COLOR_LIGHT_BG, fg=COLOR_TEXT_SECONDARY, font=("Arial", 8))
        self.weights_placeholder.pack(pady=3)
        
        # Dynamically created input fields (will be updated after case selection)
        self.test_entries_frame = tk.Frame(test_input_content, bg=COLOR_LIGHT_BG)
        self.test_entries_frame.pack(fill='x', pady=3)  # Reducido padding
        
        # Initial placeholder with improved style
        self.test_placeholder = tk.Label(self.test_entries_frame, 
                                   text="Seleccione un caso y entrene el modelo para habilitar las pruebas", 
                                   bg=COLOR_LIGHT_BG, fg=COLOR_TEXT_SECONDARY, font=("Arial", 8))  # Reducido tamaño
        self.test_placeholder.pack(pady=3)  # Reducido padding
        
        # Test button with improved style
        self.test_button = ModernButton(
            test_input_content, 
            text="Probar", 
            bg=COLOR_PRIMARY, 
            fg="white", 
            state=tk.DISABLED,
            hover_bg=COLOR_SECONDARY,
            hover_fg=COLOR_PRIMARY,
            font=("Arial", 9, "bold"),  # Reducido tamaño
            padx=10,  # Reducido padding
            pady=3    # Reducido padding
        )
        self.test_button.pack(pady=3)  # Reducido padding
        
        # Results card with improved style
        self.test_results_card = tk.Frame(self.test_content_frame, bg=COLOR_LIGHT_BG, bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
        self.test_results_card.pack(fill='x', pady=3)  # Reducido padding
        
        # Card header with improved style
        test_results_header = tk.Frame(self.test_results_card, bg=COLOR_PRIMARY, height=25)  # Reducido altura
        test_results_header.pack(fill='x')
        
        test_results_title = tk.Label(test_results_header, text="Resultados", 
                                  font=("Arial", 10, "bold"), bg=COLOR_PRIMARY, fg="white", padx=8, pady=3)  # Reducido tamaño y padding
        test_results_title.pack(anchor='w')
        
        # Card content with improved style
        test_results_content = tk.Frame(self.test_results_card, bg=COLOR_LIGHT_BG, padx=10, pady=5)  # Reducido padding
        test_results_content.pack(fill='x')
        
        # Result label with improved style
        self.test_result_label = tk.Label(test_results_content, 
                                    text="Los resultados se mostrarán aquí", 
                                    bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, font=("Arial", 8))  # Reducido tamaño
        self.test_result_label.pack(pady=3)  # Reducido padding
        
        # Visualization card with improved style
        self.visualization_card = tk.Frame(self.test_content_frame, bg=COLOR_LIGHT_BG, bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
        self.visualization_card.pack(fill='x', pady=3, expand=True)  # Reducido padding
        
        # Card header with improved style
        visualization_header = tk.Frame(self.visualization_card, bg=COLOR_PRIMARY, height=25)  # Reducido altura
        visualization_header.pack(fill='x')
        
        visualization_title = tk.Label(visualization_header, text="Visualización del Proceso", 
                                   font=("Arial", 10, "bold"), bg=COLOR_PRIMARY, fg="white", padx=8, pady=3)  # Reducido tamaño y padding
        visualization_title.pack(anchor='w')
        
        # Card content with improved style
        visualization_content = tk.Frame(self.visualization_card, bg=COLOR_LIGHT_BG, padx=10, pady=5)  # Reducido padding
        visualization_content.pack(fill='x')
        
        # Create a frame for the visualization with improved style
        self.process_visualization_frame = tk.Frame(visualization_content, bg=COLOR_LIGHT_BG)
        self.process_visualization_frame.pack(fill='both', expand=True, padx=2, pady=2)  # Reducido padding
        
        # Update the scroll region when the frame size changes
        self.test_content_frame.bind("<Configure>", 
                               lambda e: self.test_canvas.configure(
                                   scrollregion=self.test_canvas.bbox("all")))
        
        # Add mousewheel scrolling
        self.test_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Initialize variables
        self.test_entry_vars = []
        self.weight_vars = []
        self.bias_var = None

    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        self.test_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_input_fields(self, input_size):
        """Create input fields based on the selected case with improved style"""
        # Clear existing entries
        for widget in self.test_entries_frame.winfo_children():
            widget.destroy()
        
        # Create entry variables
        self.test_entry_vars = []
        
        # Create input fields with improved style
        for i in range(input_size):
            entry_frame = tk.Frame(self.test_entries_frame, bg=COLOR_LIGHT_BG)
            entry_frame.pack(fill='x', pady=2)  # Reducido padding
            
            label = tk.Label(entry_frame, text=f"Entrada {i+1}:", 
                       bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY, width=8, anchor='w',  # Reducido ancho
                       font=("Arial", 9))  # Reducido tamaño
            label.pack(side=tk.LEFT, padx=3)  # Reducido padding
            
            var = tk.StringVar(value="0")
            entry = tk.Entry(entry_frame, textvariable=var, width=8, font=("Arial", 9),  # Reducido tamaño y ancho
                       bd=1, relief=tk.SOLID)
            entry.pack(side=tk.LEFT, padx=3)  # Reducido padding
            
            self.test_entry_vars.append(var)
        
        # Enable the test button
        self.test_button.config(state=tk.NORMAL)
    
    def create_weight_fields(self, input_size):
        """Create weight fields based on the selected case"""
        # Clear existing weight fields
        for widget in self.weights_frame.winfo_children():
            widget.destroy()
        
        # Create weight variables
        self.weight_vars = []
        
        # Create weight fields
        for i in range(input_size):
            weight_frame = tk.Frame(self.weights_frame, bg=COLOR_LIGHT_BG)
            weight_frame.pack(fill='x', pady=2)
            
            label = tk.Label(weight_frame, text=f"Peso {i+1}:", 
                       bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY, width=8, anchor='w',
                       font=("Arial", 9))
            label.pack(side=tk.LEFT, padx=3)
            
            var = tk.StringVar(value="0.0")
            entry = tk.Entry(weight_frame, textvariable=var, width=10, font=("Arial", 9),
                       bd=1, relief=tk.SOLID)
            entry.pack(side=tk.LEFT, padx=3)
            
            self.weight_vars.append(var)
        
        # Create bias field
        bias_frame = tk.Frame(self.weights_frame, bg=COLOR_LIGHT_BG)
        bias_frame.pack(fill='x', pady=2)
        
        bias_label = tk.Label(bias_frame, text="Sesgo:", 
                        bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY, width=8, anchor='w',
                        font=("Arial", 9))
        bias_label.pack(side=tk.LEFT, padx=3)
        
        self.bias_var = tk.StringVar(value="0.0")
        bias_entry = tk.Entry(bias_frame, textvariable=self.bias_var, width=10, font=("Arial", 9),
                        bd=1, relief=tk.SOLID)
        bias_entry.pack(side=tk.LEFT, padx=3)
        
        # Add a note about modifying weights
        note_frame = tk.Frame(self.weights_frame, bg=COLOR_LIGHT_BG)
        note_frame.pack(fill='x', pady=5)
        
        note_label = tk.Label(note_frame, 
                        text="Puede modificar los pesos y el sesgo manualmente o cargar desde un archivo", 
                        bg=COLOR_LIGHT_BG, fg=COLOR_TEXT_SECONDARY, font=("Arial", 8), wraplength=300)
        note_label.pack(pady=2)
    
    def update_weights_fields(self, weights, bias):
        """Update weight fields with the given weights and bias"""
        if len(self.weight_vars) != len(weights):
            return
        
        # Update weight values
        for i, weight in enumerate(weights):
            self.weight_vars[i].set(f"{weight:.6f}")
        
        # Update bias value
        self.bias_var.set(f"{bias:.6f}")
    
    def clear_weights_fields(self):
        """Clear all weight fields"""
        # Set default values for weights
        for var in self.weight_vars:
            var.set("0.0")
        
        # Set default value for bias
        if self.bias_var:
            self.bias_var.set("0.0")
    
    def get_weights_and_bias(self):
        """Get the current weights and bias from the UI"""
        weights = []
        for var in self.weight_vars:
            try:
                weight = float(var.get())
                weights.append(weight)
            except ValueError:
                raise ValueError("Los pesos deben ser números decimales")
        
        try:
            bias = float(self.bias_var.get())
        except ValueError:
            raise ValueError("El sesgo debe ser un número decimal")
        
        return np.array(weights), bias
        
    def update_test_result(self, input_values, prediction):
        """Update the test result display with improved style"""
        input_str = ", ".join([str(int(v)) for v in input_values])
        self.test_result_label.config(text=f"Entrada: [{input_str}] → Salida: {prediction:.4f}")
        
    def draw_adaline_visualization(self, inputs, weights, bias, prediction):
        """Draw an interactive visualization of the Adaline process with improved professional design"""
        # Clear existing visualization
        for widget in self.process_visualization_frame.winfo_children():
            widget.destroy()
        
        # Create a figure for the visualization
        fig = Figure(figsize=(7, 4), dpi=100, facecolor=COLOR_LIGHT_BG)  # Reducido tamaño
        ax = fig.add_subplot(111)
        
        # Number of inputs
        n_inputs = len(inputs)
        
        # Create positions for the visualization elements
        input_x = 0.2
        neuron_x = 0.6
        output_x = 0.9
        
        # Calculate vertical positions
        input_positions = np.linspace(0.2, 0.8, n_inputs)
        
        # Draw a professional background
        ax.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=True, color='#f8f9fa', alpha=0.5, zorder=1))
        
        # Add title
        ax.text(0.5, 0.95, "Modelo Adaline - Flujo de Procesamiento", 
              ha='center', va='center', fontsize=11, fontweight='bold', color=COLOR_PRIMARY,  # Reducido tamaño
              bbox=dict(facecolor=COLOR_LIGHT_BG, alpha=0.9, boxstyle='round,pad=0.3', edgecolor=COLOR_BORDER))  # Reducido padding
        
        # Draw inputs with improved style
        for i, (pos, val) in enumerate(zip(input_positions, inputs)):
            # Input node with gradient fill
            circle = plt.Circle((input_x, pos), 0.04, color=COLOR_LIGHT_BG, ec=COLOR_PRIMARY, lw=1.5, zorder=10)  # Reducido tamaño y grosor
            ax.add_patch(circle)
            
            # Input label with better styling
            ax.text(input_x - 0.08, pos, f"X{i+1} = {val}", ha='right', va='center', 
                  fontsize=9, color=COLOR_TEXT, fontweight='bold',  # Reducido tamaño
                  bbox=dict(facecolor=COLOR_LIGHT_BG, alpha=0.7, boxstyle='round,pad=0.2', edgecolor=COLOR_BORDER))  # Reducido padding
            
            # Connection line to neuron with gradient
            ax.plot([input_x + 0.04, neuron_x - 0.06], [pos, 0.5], 
                  color=COLOR_PRIMARY, lw=1.5, zorder=5, alpha=0.8)  # Reducido grosor
            
            # Weight label with improved styling
            midx = (input_x + 0.04 + neuron_x - 0.06) / 2
            midy = (pos + 0.5) / 2
            ax.text(midx, midy + 0.02, f"w{i+1} = {weights[i]:.4f}", 
                  ha='center', va='center', fontsize=8, color=COLOR_TEXT,  # Reducido tamaño
                  bbox=dict(facecolor=COLOR_LIGHT_BG, alpha=0.9, boxstyle='round,pad=0.2', edgecolor=COLOR_BORDER))  # Reducido padding
        
        # Draw bias with improved styling
        bias_y = 0.9
        ax.text(neuron_x - 0.12, bias_y, f"Bias = {bias:.4f}", ha='right', va='center', 
              fontsize=9, color=COLOR_TEXT, fontweight='bold',  # Reducido tamaño
              bbox=dict(facecolor=COLOR_LIGHT_BG, alpha=0.7, boxstyle='round,pad=0.2', edgecolor=COLOR_BORDER))  # Reducido padding
        
        ax.plot([neuron_x - 0.12, neuron_x - 0.06], [bias_y, 0.5], 
              color=COLOR_PRIMARY, lw=1.5, zorder=5, alpha=0.8)  # Reducido grosor
        
        # Draw neuron with improved styling
        neuron_circle = plt.Circle((neuron_x, 0.5), 0.06, color=COLOR_LIGHT_BG, ec=COLOR_PRIMARY, lw=2, zorder=10)  # Reducido tamaño
        ax.add_patch(neuron_circle)
        ax.text(neuron_x, 0.5, "Σ", ha='center', va='center', fontsize=14, color=COLOR_PRIMARY, fontweight='bold')  # Reducido tamaño
        
        # Add a subtle glow effect around the neuron
        for r in np.linspace(0.07, 0.09, 2):  # Reducido tamaño y número
            glow_circle = plt.Circle((neuron_x, 0.5), r, color=COLOR_PRIMARY, alpha=0.1, zorder=9)
            ax.add_patch(glow_circle)
        
        # Draw output with improved styling
        ax.plot([neuron_x + 0.06, output_x - 0.04], [0.5, 0.5], 
              color=COLOR_PRIMARY, lw=1.5, zorder=5, alpha=0.8)  # Reducido grosor
        
        output_circle = plt.Circle((output_x, 0.5), 0.04, color=COLOR_PRIMARY, ec=COLOR_PRIMARY, lw=1.5, zorder=10)  # Reducido tamaño y grosor
        ax.add_patch(output_circle)
        
        # Add a subtle glow effect around the output
        for r in np.linspace(0.05, 0.07, 2):  # Reducido tamaño y número
            glow_circle = plt.Circle((output_x, 0.5), r, color=COLOR_PRIMARY, alpha=0.1, zorder=9)
            ax.add_patch(glow_circle)
        
        ax.text(output_x, 0.5, f"{prediction:.2f}", ha='center', va='center', fontsize=8, color='white', fontweight='bold')  # Reducido tamaño
        ax.text(output_x + 0.08, 0.5, "Salida", ha='left', va='center', fontsize=9, color=COLOR_TEXT, fontweight='bold')  # Reducido tamaño
        
        # Calculate and display the weighted sum with improved styling
        weighted_sum = np.dot(inputs, weights) + bias
        sum_text = f"Σ = "
        for i, (input_val, weight) in enumerate(zip(inputs, weights)):
            if i > 0:
                sum_text += " + "
            sum_text += f"({input_val} × {weight:.4f})"
        sum_text += f" + {bias:.4f} = {weighted_sum:.4f}"
        
        ax.text(0.5, 0.15, sum_text, ha='center', va='center', fontsize=9, color=COLOR_TEXT,  # Reducido tamaño
              bbox=dict(facecolor=COLOR_LIGHT_BG, alpha=0.9, boxstyle='round,pad=0.3', edgecolor=COLOR_BORDER))  # Reducido padding
        
        # Add a formula explanation
        formula = "y = f(Σ wi·xi + b)"
        ax.text(0.5, 0.05, formula, ha='center', va='center', fontsize=10, color=COLOR_PRIMARY, fontweight='bold')  # Reducido tamaño
        
        # Set axis properties
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Add the plot to the frame
        canvas = FigureCanvasTkAgg(fig, master=self.process_visualization_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill='both', expand=True)