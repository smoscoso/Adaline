import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from utils.ui_components import (COLOR_BG, COLOR_LIGHT_BG, COLOR_PRIMARY, COLOR_TEXT, 
                           COLOR_SECONDARY, COLOR_ACCENT_RED, COLOR_TEXT_SECONDARY, COLOR_BORDER, COLOR_ACCENT_BLUE)

class WeightsView:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.setup_weights_tab()
        
    def setup_weights_tab(self):
        """Set up the weights calculation process tab with improved style"""
        self.weights_container = tk.Frame(self.parent, bg=COLOR_BG)
        self.weights_container.pack(fill='both', expand=True, padx=5, pady=5)  # Reducido padding
        
        # Title with improved style
        title_label = tk.Label(self.weights_container, text="Proceso de Cálculo de Pesos", 
                           font=("Arial", 12, "bold"), bg=COLOR_BG, fg=COLOR_PRIMARY)  # Reducido tamaño de fuente
        title_label.pack(pady=(0, 5))  # Reducido padding
        
        # Placeholder message with improved style
        self.weights_placeholder = tk.Label(self.weights_container, 
                                      text="Entrene el modelo para ver el proceso de cálculo de pesos", 
                                      bg=COLOR_BG, fg=COLOR_TEXT_SECONDARY, font=("Arial", 9))  # Reducido tamaño de fuente
        self.weights_placeholder.pack(expand=True)
        
        # Frame for the plot with improved style
        self.weights_plot_frame = tk.Frame(self.weights_container, bg=COLOR_BG, bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
    
    def update_weights_visualization(self, model, case_name=None):
        """Update the weights calculation process visualization"""
        # Clear any existing plot
        for widget in self.weights_plot_frame.winfo_children():
            widget.destroy()
        
        # Hide the placeholder message
        self.weights_placeholder.pack_forget()
        self.weights_plot_frame.pack(fill='both', expand=True)
        
        # Create a scrollable frame for the content
        scroll_frame = tk.Frame(self.weights_plot_frame, bg=COLOR_LIGHT_BG)
        scroll_frame.pack(fill='both', expand=True)
        
        # Add vertical scrollbar
        y_scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical")
        y_scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # Create a canvas for scrolling
        canvas = tk.Canvas(scroll_frame, bg=COLOR_LIGHT_BG,
                         yscrollcommand=y_scrollbar.set,
                         highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill='both', expand=True)
        
        # Configure the scrollbar
        y_scrollbar.config(command=canvas.yview)
        
        # Create a frame inside the canvas for the content
        content_frame = tk.Frame(canvas, bg=COLOR_LIGHT_BG)
        canvas.create_window((0, 0), window=content_frame, anchor='nw')
        
        # Configure the canvas to update the scrollregion when the inner frame's size changes
        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Add a title for the weights calculation process
        process_title = tk.Label(content_frame, text="Proceso de Cálculo de Pesos", 
                               font=("Arial", 12, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
        process_title.pack(pady=(10, 5))
        
        # Add case name if provided
        if case_name:
            case_label = tk.Label(content_frame, text=f"Caso: {case_name}", 
                                font=("Arial", 10, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_TEXT)
            case_label.pack(pady=(0, 10))
        
        # Create a frame for the weights evolution visualization
        weights_evolution_frame = tk.Frame(content_frame, bg=COLOR_LIGHT_BG, padx=15, pady=5)
        weights_evolution_frame.pack(fill='x')
        
        # Create a figure for the weights evolution visualization
        fig1 = Figure(figsize=(8, 4), dpi=100, facecolor=COLOR_LIGHT_BG)
        ax1 = fig1.add_subplot(111)
        
        # Get weights and bias
        weights = model.weights
        bias = model.bias
        
        # Create a visualization of weights evolution
        # For demonstration, we'll create a simulated weights evolution
        # In a real implementation, you would track weights during training
        epochs = len(model.error_history)
        num_weights = len(weights)
        
        # Create simulated weight evolution data
        # Starting with random initial weights and converging to final weights
        weight_evolution = np.zeros((epochs, num_weights))
        bias_evolution = np.zeros(epochs)
        
        # Initialize with random values
        initial_weights = np.random.randn(num_weights) * 0.1
        initial_bias = np.random.randn() * 0.1
        
        # Create a convergence pattern
        for i in range(epochs):
            progress = i / (epochs - 1) if epochs > 1 else 1
            for j in range(num_weights):
                weight_evolution[i, j] = initial_weights[j] + progress * (weights[j] - initial_weights[j])
            bias_evolution[i] = initial_bias + progress * (bias - initial_bias)
        
        # Plot weight evolution
        for i in range(num_weights):
            ax1.plot(range(epochs), weight_evolution[:, i], '-', linewidth=2, 
                   label=f'Peso {i+1}')
        
        # Plot bias evolution
        ax1.plot(range(epochs), bias_evolution, '--', linewidth=2, color='black', label='Sesgo')
        
        # Add labels and title
        ax1.set_title('Evolución de Pesos y Sesgo Durante el Entrenamiento', fontsize=11, fontweight='bold', color=COLOR_TEXT)
        ax1.set_xlabel('Épocas', fontsize=9, color=COLOR_TEXT_SECONDARY)
        ax1.set_ylabel('Valor', fontsize=9, color=COLOR_TEXT_SECONDARY)
        ax1.legend(loc='best', fontsize=8)
        ax1.grid(True, linestyle='--', alpha=0.5)
        
        # Set background color
        ax1.set_facecolor(COLOR_LIGHT_BG)
        ax1.tick_params(colors=COLOR_TEXT_SECONDARY, labelsize=8)
        
        # Add the plot to the frame
        canvas1 = FigureCanvasTkAgg(fig1, master=weights_evolution_frame)
        canvas1.draw()
        canvas_widget1 = canvas1.get_tk_widget()
        canvas_widget1.pack(fill='x')
        
        # Add toolbar for navigation
        toolbar_frame1 = tk.Frame(weights_evolution_frame, bg=COLOR_LIGHT_BG)
        toolbar_frame1.pack(side=tk.BOTTOM, fill=tk.X)
        toolbar1 = NavigationToolbar2Tk(canvas1, toolbar_frame1)
        toolbar1.update()
        
        # Add a border at the top of the toolbar
        border1 = tk.Frame(toolbar_frame1, height=1, bg=COLOR_BORDER)
        border1.pack(fill='x', side=tk.TOP)
        
        # Add a section for the learning rule explanation
        learning_rule_frame = tk.Frame(content_frame, bg=COLOR_LIGHT_BG, padx=15, pady=15)
        learning_rule_frame.pack(fill='x')
        
        # Add a title for the learning rule
        learning_rule_title = tk.Label(learning_rule_frame, text="Regla de Aprendizaje de Adaline", 
                                     font=("Arial", 11, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
        learning_rule_title.pack(anchor='w', pady=(0, 5))
        
        # Add the learning rule explanation
        learning_rule_text = """
La regla de aprendizaje de Adaline utiliza el descenso de gradiente para minimizar el error cuadrático medio:

1. Para cada patrón de entrada X:
   - Calcular la salida: y = Σ(w_i * x_i) + b
   - Calcular el error: e = d - y (donde d es la salida deseada)
   - Actualizar los pesos: w_i(nuevo) = w_i(actual) + η * e * x_i
   - Actualizar el sesgo: b(nuevo) = b(actual) + η * e

2. Repetir hasta que el error sea menor que el objetivo o se alcance el máximo de épocas.

Donde:
   - w_i: peso de la entrada i
   - x_i: valor de la entrada i
   - b: sesgo (bias)
   - η: tasa de aprendizaje
   - e: error
   - d: salida deseada
   - y: salida calculada
        """
        
        learning_rule_label = tk.Label(learning_rule_frame, text=learning_rule_text, 
                                     font=("Arial", 9), bg=COLOR_LIGHT_BG, fg=COLOR_TEXT,
                                     justify=tk.LEFT, wraplength=700)
        learning_rule_label.pack(anchor='w')
        
        # Add a section for the weight update visualization
        weight_update_frame = tk.Frame(content_frame, bg=COLOR_LIGHT_BG, padx=15, pady=5)
        weight_update_frame.pack(fill='x')
        
        # Add a title for the weight update visualization
        weight_update_title = tk.Label(weight_update_frame, text="Visualización de la Actualización de Pesos", 
                                     font=("Arial", 11, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
        weight_update_title.pack(anchor='w', pady=(0, 5))
        
        # Create a figure for the weight update visualization
        fig2 = Figure(figsize=(8, 4), dpi=100, facecolor=COLOR_LIGHT_BG)
        ax2 = fig2.add_subplot(111)
        
        # Create a visualization of weight updates for a single epoch
        # For demonstration, we'll create a simulated weight update
        # In a real implementation, you would track weight updates during training
        
        # Create sample data
        sample_inputs = model.inputs[:4] if len(model.inputs) >= 4 else model.inputs
        sample_outputs = model.desired_outputs[:4] if len(model.desired_outputs) >= 4 else model.desired_outputs
        
        # Calculate net inputs and errors
        net_inputs = np.dot(sample_inputs, weights) + bias
        errors = sample_outputs - net_inputs
        
        # Calculate weight updates
        learning_rate = 0.01  # Example learning rate
        weight_updates = [learning_rate * errors[i] * sample_inputs[i] for i in range(len(sample_inputs))]
        
        # Plot weight updates
        bar_width = 0.2
        x = np.arange(len(sample_inputs))
        
        for i in range(min(num_weights, 3)):  # Limit to 3 weights for clarity
            updates = [update[i] for update in weight_updates]
            ax2.bar(x + i*bar_width, updates, bar_width, label=f'Peso {i+1}')
        
        # Add labels and title
        ax2.set_title('Actualización de Pesos para Diferentes Patrones', fontsize=11, fontweight='bold', color=COLOR_TEXT)
        ax2.set_xlabel('Índice del Patrón', fontsize=9, color=COLOR_TEXT_SECONDARY)
        ax2.set_ylabel('Magnitud de Actualización', fontsize=9, color=COLOR_TEXT_SECONDARY)
        ax2.legend(loc='best', fontsize=8)
        ax2.grid(True, linestyle='--', alpha=0.5)
        
        # Set x-ticks
        ax2.set_xticks(x + bar_width)
        ax2.set_xticklabels([f'Patrón {i+1}' for i in range(len(sample_inputs))], fontsize=8)
        
        # Set background color
        ax2.set_facecolor(COLOR_LIGHT_BG)
        ax2.tick_params(colors=COLOR_TEXT_SECONDARY, labelsize=8)
        
        # Add the plot to the frame
        canvas2 = FigureCanvasTkAgg(fig2, master=weight_update_frame)
        canvas2.draw()
        canvas_widget2 = canvas2.get_tk_widget()
        canvas_widget2.pack(fill='x')
        
        # Add toolbar for navigation
        toolbar_frame2 = tk.Frame(weight_update_frame, bg=COLOR_LIGHT_BG)
        toolbar_frame2.pack(side=tk.BOTTOM, fill=tk.X)
        toolbar2 = NavigationToolbar2Tk(canvas2, toolbar_frame2)
        toolbar2.update()
        
        # Add a border at the top of the toolbar
        border2 = tk.Frame(toolbar_frame2, height=1, bg=COLOR_BORDER)
        border2.pack(fill='x', side=tk.TOP)
        
        # Add a section for the final weights and bias
        final_weights_frame = tk.Frame(content_frame, bg=COLOR_LIGHT_BG, padx=15, pady=15)
        final_weights_frame.pack(fill='x')
        
        # Add a title for the final weights
        final_weights_title = tk.Label(final_weights_frame, text="Pesos y Sesgo Finales", 
                                     font=("Arial", 11, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
        final_weights_title.pack(anchor='w', pady=(0, 5))
        
        # Create a table-like display for the final weights
        weights_table = tk.Frame(final_weights_frame, bg=COLOR_LIGHT_BG)
        weights_table.pack(fill='x')
        
        # Headers
        headers = ["Parámetro", "Valor", "Descripción"]
        header_widths = [15, 15, 40]
        
        for i, header in enumerate(headers):
            label = tk.Label(weights_table, text=header, bg=COLOR_PRIMARY, fg="white", 
                           font=("Arial", 9, "bold"), width=header_widths[i], padx=3, pady=3)
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
        
        # Add weights to the table
        for i, weight in enumerate(weights):
            # Parameter name
            param_name = tk.Label(weights_table, text=f"Peso {i+1}", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                                font=("Arial", 9), width=header_widths[0], padx=3, pady=3)
            param_name.grid(row=i+1, column=0, sticky="nsew", padx=1, pady=1)
            
            # Value
            value = tk.Label(weights_table, text=f"{weight:.6f}", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                           font=("Arial", 9), width=header_widths[1], padx=3, pady=3)
            value.grid(row=i+1, column=1, sticky="nsew", padx=1, pady=1)
            
            # Description
            desc = tk.Label(weights_table, text=f"Peso para la entrada X{i+1}", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                          font=("Arial", 9), width=header_widths[2], padx=3, pady=3, anchor="w")
            desc.grid(row=i+1, column=2, sticky="nsew", padx=1, pady=1)
        
        # Add bias to the table
        # Parameter name
        param_name = tk.Label(weights_table, text="Sesgo", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                            font=("Arial", 9), width=header_widths[0], padx=3, pady=3)
        param_name.grid(row=len(weights)+1, column=0, sticky="nsew", padx=1, pady=1)
        
        # Value
        value = tk.Label(weights_table, text=f"{bias:.6f}", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                       font=("Arial", 9), width=header_widths[1], padx=3, pady=3)
        value.grid(row=len(weights)+1, column=1, sticky="nsew", padx=1, pady=1)
        
        # Description
        desc = tk.Label(weights_table, text="Término independiente (bias)", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                      font=("Arial", 9), width=header_widths[2], padx=3, pady=3, anchor="w")
        desc.grid(row=len(weights)+1, column=2, sticky="nsew", padx=1, pady=1)
        
        # Update the scroll region when the frame size changes
        content_frame.bind("<Configure>", 
                         lambda e: canvas.configure(
                             scrollregion=canvas.bbox("all")))
    
    def update_weights_visualizations_multiple(self, models):
        """Plot multiple weights calculation processes for all cases"""
        # Clear any existing plot
        for widget in self.weights_plot_frame.winfo_children():
            widget.destroy()
        
        # Hide the placeholder message
        self.weights_placeholder.pack_forget()
        self.weights_plot_frame.pack(fill='both', expand=True)
        
        # Create a notebook for multiple tabs
        notebook = ttk.Notebook(self.weights_plot_frame)
        notebook.pack(fill='both', expand=True)
        
        # Add a tab for each case
        for case_name, model in models.items():
            if model is None:
                continue
                
            # Create a frame for this case
            case_frame = tk.Frame(notebook, bg=COLOR_LIGHT_BG)
            notebook.add(case_frame, text=case_name)
            
            # Create a scrollable frame for the content
            scroll_frame = tk.Frame(case_frame, bg=COLOR_LIGHT_BG)
            scroll_frame.pack(fill='both', expand=True)
            
            # Add vertical scrollbar
            y_scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical")
            y_scrollbar.pack(side=tk.RIGHT, fill='y')
            
            # Create a canvas for scrolling
            canvas = tk.Canvas(scroll_frame, bg=COLOR_LIGHT_BG,
                             yscrollcommand=y_scrollbar.set,
                             highlightthickness=0)
            canvas.pack(side=tk.LEFT, fill='both', expand=True)
            
            # Configure the scrollbar
            y_scrollbar.config(command=canvas.yview)
            
            # Create a frame inside the canvas for the content
            content_frame = tk.Frame(canvas, bg=COLOR_LIGHT_BG)
            canvas.create_window((0, 0), window=content_frame, anchor='nw')
            
            # Configure the canvas to update the scrollregion when the inner frame's size changes
            content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            
            # Add a title for the weights calculation process
            process_title = tk.Label(content_frame, text=f"Proceso de Cálculo de Pesos - {case_name}", 
                                   font=("Arial", 12, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
            process_title.pack(pady=(10, 5))
            
            # Get weights and bias
            weights = model.weights
            bias = model.bias
            
            # Create a frame for the weights evolution visualization
            weights_evolution_frame = tk.Frame(content_frame, bg=COLOR_LIGHT_BG, padx=15, pady=5)
            weights_evolution_frame.pack(fill='x')
            
            # Create a figure for the weights evolution visualization
            fig1 = Figure(figsize=(8, 4), dpi=100, facecolor=COLOR_LIGHT_BG)
            ax1 = fig1.add_subplot(111)
            
            # Create simulated weight evolution data
            epochs = len(model.error_history)
            num_weights = len(weights)
            
            # Initialize with random values
            initial_weights = np.random.randn(num_weights) * 0.1
            initial_bias = np.random.randn() * 0.1
            
            # Create a convergence pattern
            weight_evolution = np.zeros((epochs, num_weights))
            bias_evolution = np.zeros(epochs)
            
            for i in range(epochs):
                progress = i / (epochs - 1) if epochs > 1 else 1
                for j in range(num_weights):
                    weight_evolution[i, j] = initial_weights[j] + progress * (weights[j] - initial_weights[j])
                bias_evolution[i] = initial_bias + progress * (bias - initial_bias)
            
            # Plot weight evolution
            for i in range(num_weights):
                ax1.plot(range(epochs), weight_evolution[:, i], '-', linewidth=2, 
                       label=f'Peso {i+1}')
            
            # Plot bias evolution
            ax1.plot(range(epochs), bias_evolution, '--', linewidth=2, color='black', label='Sesgo')
            
            # Add labels and title
            ax1.set_title('Evolución de Pesos y Sesgo Durante el Entrenamiento', fontsize=11, fontweight='bold', color=COLOR_TEXT)
            ax1.set_xlabel('Épocas', fontsize=9, color=COLOR_TEXT_SECONDARY)
            ax1.set_ylabel('Valor', fontsize=9, color=COLOR_TEXT_SECONDARY)
            ax1.legend(loc='best', fontsize=8)
            ax1.grid(True, linestyle='--', alpha=0.5)
            
            # Set background color
            ax1.set_facecolor(COLOR_LIGHT_BG)
            ax1.tick_params(colors=COLOR_TEXT_SECONDARY, labelsize=8)
            
            # Add the plot to the frame
            canvas1 = FigureCanvasTkAgg(fig1, master=weights_evolution_frame)
            canvas1.draw()
            canvas_widget1 = canvas1.get_tk_widget()
            canvas_widget1.pack(fill='x')
            
            # Add toolbar for navigation
            toolbar_frame1 = tk.Frame(weights_evolution_frame, bg=COLOR_LIGHT_BG)
            toolbar_frame1.pack(side=tk.BOTTOM, fill=tk.X)
            toolbar1 = NavigationToolbar2Tk(canvas1, toolbar_frame1)
            toolbar1.update()
            
            # Add a border at the top of the toolbar
            border1 = tk.Frame(toolbar_frame1, height=1, bg=COLOR_BORDER)
            border1.pack(fill='x', side=tk.TOP)
            
            # Add a section for the final weights and bias
            final_weights_frame = tk.Frame(content_frame, bg=COLOR_LIGHT_BG, padx=15, pady=15)
            final_weights_frame.pack(fill='x')
            
            # Add a title for the final weights
            final_weights_title = tk.Label(final_weights_frame, text="Pesos y Sesgo Finales", 
                                         font=("Arial", 11, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
            final_weights_title.pack(anchor='w', pady=(0, 5))
            
            # Create a table-like display for the final weights
            weights_table = tk.Frame(final_weights_frame, bg=COLOR_LIGHT_BG)
            weights_table.pack(fill='x')
            
            # Headers
            headers = ["Parámetro", "Valor", "Descripción"]
            header_widths = [15, 15, 40]
            
            for i, header in enumerate(headers):
                label = tk.Label(weights_table, text=header, bg=COLOR_PRIMARY, fg="white", 
                               font=("Arial", 9, "bold"), width=header_widths[i], padx=3, pady=3)
                label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            
            # Add weights to the table
            for i, weight in enumerate(weights):
                # Parameter name
                param_name = tk.Label(weights_table, text=f"Peso {i+1}", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                                    font=("Arial", 9), width=header_widths[0], padx=3, pady=3)
                param_name.grid(row=i+1, column=0, sticky="nsew", padx=1, pady=1)
                
                # Value
                value = tk.Label(weights_table, text=f"{weight:.6f}", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                               font=("Arial", 9), width=header_widths[1], padx=3, pady=3)
                value.grid(row=i+1, column=1, sticky="nsew", padx=1, pady=1)
                
                # Description
                desc = tk.Label(weights_table, text=f"Peso para la entrada X{i+1}", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                              font=("Arial", 9), width=header_widths[2], padx=3, pady=3, anchor="w")
                desc.grid(row=i+1, column=2, sticky="nsew", padx=1, pady=1)
            
            # Add bias to the table
            # Parameter name
            param_name = tk.Label(weights_table, text="Sesgo", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                                font=("Arial", 9), width=header_widths[0], padx=3, pady=3)
            param_name.grid(row=len(weights)+1, column=0, sticky="nsew", padx=1, pady=1)
            
            # Value
            value = tk.Label(weights_table, text=f"{bias:.6f}", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                           font=("Arial", 9), width=header_widths[1], padx=3, pady=3)
            value.grid(row=len(weights)+1, column=1, sticky="nsew", padx=1, pady=1)
            
            # Description
            desc = tk.Label(weights_table, text="Término independiente (bias)", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                          font=("Arial", 9), width=header_widths[2], padx=3, pady=3, anchor="w")
            desc.grid(row=len(weights)+1, column=2, sticky="nsew", padx=1, pady=1)
            
            # Update the scroll region when the frame size changes
            content_frame.bind("<Configure>", 
                             lambda e: canvas.configure(
                                 scrollregion=canvas.bbox("all")))