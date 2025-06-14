import tkinter as tk
from tkinter import ttk, messagebox
from utils.ui_components import COLOR_BG, COLOR_LIGHT_BG, COLOR_PRIMARY, COLOR_TEXT, COLOR_ACCENT_RED, COLOR_SECONDARY, COLOR_TEXT_SECONDARY, COLOR_SUCCESS, COLOR_BORDER, ModernButton

class ConfigView:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.setup_config_tab()
        
    def setup_config_tab(self):
        """Set up the configuration and training tab with improved UI"""
        # Create a scrollable frame for the content
        self.config_scroll_frame = tk.Frame(self.parent, bg=COLOR_BG)
        self.config_scroll_frame.pack(fill='both', expand=True)
        
        # Add vertical scrollbar with improved style
        y_scrollbar = ttk.Scrollbar(self.config_scroll_frame, orient="vertical")
        y_scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # Create a canvas for scrolling
        self.config_canvas = tk.Canvas(self.config_scroll_frame, bg=COLOR_BG,
                                     yscrollcommand=y_scrollbar.set,
                                     highlightthickness=0)
        self.config_canvas.pack(side=tk.LEFT, fill='both', expand=True)
        
        # Configure the scrollbar
        y_scrollbar.config(command=self.config_canvas.yview)
        
        # Create a frame inside the canvas for the content
        main_container = tk.Frame(self.config_canvas, bg=COLOR_BG)
        self.config_canvas.create_window((0, 0), window=main_container, anchor='nw')
        
        # Update the scroll region when the frame size changes
        main_container.bind("<Configure>", 
                          lambda e: self.config_canvas.configure(
                              scrollregion=self.config_canvas.bbox("all")))
        
        # Add mousewheel scrolling
        self.config_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Main container with padding
        main_container.pack(fill='both', expand=True)
        main_container_inner = tk.Frame(main_container, bg=COLOR_BG)
        main_container_inner.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Header section with title and description
        header_frame = tk.Frame(main_container_inner, bg=COLOR_BG)
        header_frame.pack(fill='x', pady=(0, 10))
        
        title_label = tk.Label(header_frame, text="Configuración del Adaline", 
                             font=("Arial", 16, "bold"), bg=COLOR_BG, fg=COLOR_PRIMARY)
        title_label.pack(anchor='w')
        
        description_label = tk.Label(header_frame, 
                                   text="Configure los parámetros y seleccione el conjunto de datos para entrenar la red neuronal Adaline", 
                                   font=("Arial", 10), bg=COLOR_BG, fg=COLOR_TEXT_SECONDARY)
        description_label.pack(anchor='w', pady=(2, 0))
        
        # Create a horizontal separator with improved style
        separator = ttk.Separator(main_container_inner, orient='horizontal')
        separator.pack(fill='x', pady=8)
        
        # Create two-column layout
        content_frame = tk.Frame(main_container_inner, bg=COLOR_BG)
        content_frame.pack(fill='both', expand=True)
        
        # Left column for configuration
        left_column = tk.Frame(content_frame, bg=COLOR_BG)
        left_column.pack(side=tk.LEFT, fill='both', expand=True, padx=(0, 5))
        
        # Right column for results
        right_column = tk.Frame(content_frame, bg=COLOR_BG)
        right_column.pack(side=tk.RIGHT, fill='both', expand=True, padx=(5, 0))
        
        # ===== LEFT COLUMN: CONFIGURATION =====
        
        # Parameters card with improved style
        params_card = tk.Frame(left_column, bg=COLOR_LIGHT_BG, bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
        params_card.pack(fill='x', pady=(0, 8), ipady=5)
        
        # Card header with improved style
        params_header = tk.Frame(params_card, bg=COLOR_PRIMARY, height=30)
        params_header.pack(fill='x')
        
        params_title = tk.Label(params_header, text="Parámetros de Entrenamiento", 
                              font=("Arial", 11, "bold"), bg=COLOR_PRIMARY, fg="white", padx=10, pady=5)
        params_title.pack(anchor='w')
        
        # Card content with improved style
        params_content = tk.Frame(params_card, bg=COLOR_LIGHT_BG, padx=15, pady=8)
        params_content.pack(fill='x')
        
        # Learning rate with improved layout
        lr_frame = tk.Frame(params_content, bg=COLOR_LIGHT_BG)
        lr_frame.pack(fill='x', pady=4)
        
        lr_label = tk.Label(lr_frame, text="Tasa de Aprendizaje:", 
                          font=("Arial", 10), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY, width=18, anchor='w')
        lr_label.pack(side=tk.LEFT)
        
        self.lr_var = tk.StringVar(value="0.01")
        lr_entry = tk.Entry(lr_frame, textvariable=self.lr_var, width=8, 
                          font=("Arial", 10), bd=1, relief=tk.SOLID)
        lr_entry.pack(side=tk.LEFT, padx=5)
        
        lr_info = tk.Label(lr_frame, text="Valor recomendado: 0.01 - 0.1", 
                         font=("Arial", 8, "italic"), bg=COLOR_LIGHT_BG, fg=COLOR_TEXT_SECONDARY)
        lr_info.pack(side=tk.LEFT, padx=5)
        
        # Target error with improved layout
        error_frame = tk.Frame(params_content, bg=COLOR_LIGHT_BG)
        error_frame.pack(fill='x', pady=4)
        
        error_label = tk.Label(error_frame, text="Error Objetivo:", 
                             font=("Arial", 10), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY, width=18, anchor='w')
        error_label.pack(side=tk.LEFT)
        
        self.error_var = tk.StringVar(value="0.01")
        error_entry = tk.Entry(error_frame, textvariable=self.error_var, width=8, 
                             font=("Arial", 10), bd=1, relief=tk.SOLID)
        error_entry.pack(side=tk.LEFT, padx=5)
        
        error_info = tk.Label(error_frame, text="Valor recomendado: 0.01 - 0.001", 
                            font=("Arial", 8, "italic"), bg=COLOR_LIGHT_BG, fg=COLOR_TEXT_SECONDARY)
        error_info.pack(side=tk.LEFT, padx=5)
        
        # Case selection card with improved style
        case_card = tk.Frame(left_column, bg=COLOR_LIGHT_BG, bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
        case_card.pack(fill='x', pady=(0, 8), ipady=5)
        
        # Card header with improved style
        case_header = tk.Frame(case_card, bg=COLOR_PRIMARY, height=30)
        case_header.pack(fill='x')
        
        case_title = tk.Label(case_header, text="Conjunto de Datos", 
                            font=("Arial", 11, "bold"), bg=COLOR_PRIMARY, fg="white", padx=10, pady=5)
        case_title.pack(anchor='w')
        
        # Card content with improved style
        case_content = tk.Frame(case_card, bg=COLOR_LIGHT_BG, padx=15, pady=8)
        case_content.pack(fill='x')
        
        case_label = tk.Label(case_content, text="Seleccione un caso:", 
                            font=("Arial", 10), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
        case_label.pack(anchor='w', pady=(0, 5))
        
        # Create a frame for the combobox with improved style
        combo_frame = tk.Frame(case_content, bg=COLOR_LIGHT_BG)
        combo_frame.pack(fill='x', pady=2)
        
        self.case_var = tk.StringVar(value="Caso 1 (entrada 2)")
        self.case_combo = ttk.Combobox(combo_frame, textvariable=self.case_var, state="readonly", 
                                     font=("Arial", 10), width=25)
        self.case_combo['values'] = [
            "Caso 1 (entrada 2)",
            "Caso 2 (entrada 3)",
            "Caso 3 (entrada 4)",
            "Caso 4 (entrada 5)",
            "Todos los casos"
        ]
        self.case_combo.current(0)  # Set default selection to first item
        self.case_combo.pack(anchor='w')
        
        # Add a description for the selected case with improved style
        self.case_description_frame = tk.Frame(case_content, bg=COLOR_LIGHT_BG, pady=5)
        self.case_description_frame.pack(fill='x')
        
        # Referencia del caso (se actualizará dinámicamente)
        self.case_reference_frame = tk.Frame(case_content, bg=COLOR_LIGHT_BG, pady=5, bd=1, relief=tk.SOLID)
        self.case_reference_frame.pack(fill='x', pady=5)
        
        self.case_reference_label = tk.Label(self.case_reference_frame, 
                                          text="Caso 1: Entradas [00,01,10,11], Salidas [0,1,2,3]", 
                                          font=("Arial", 9, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY,
                                          justify=tk.LEFT, padx=10, pady=5)
        self.case_reference_label.pack(anchor='w')
        
        # Add a button to load training data
        load_data_frame = tk.Frame(case_content, bg=COLOR_LIGHT_BG)
        load_data_frame.pack(fill='x', pady=5)
        
        self.load_data_button = ModernButton(
            load_data_frame, 
            text="Cargar Datos de Entrenamiento", 
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
        self.load_data_button.pack(anchor='w')
        
        # Bind the combobox selection to update the description and reference
        self.case_combo.bind("<<ComboboxSelected>>", self.update_case_info)
        
        # Training button card with improved style
        train_card = tk.Frame(left_column, bg=COLOR_LIGHT_BG, bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
        train_card.pack(fill='x', ipady=5)
        
        # Card content with centered button and improved style
        train_content = tk.Frame(train_card, bg=COLOR_LIGHT_BG, padx=15, pady=8)
        train_content.pack(fill='x')
        
        button_frame = tk.Frame(train_content, bg=COLOR_LIGHT_BG)
        button_frame.pack(pady=5)
        
        # Asegurar que el botón de entrenar sea visible y tenga un tamaño adecuado
        self.train_button = ModernButton(
            button_frame, 
            text="Entrenar Adaline", 
            bg=COLOR_PRIMARY, 
            fg="white", 
            font=("Arial", 12, "bold"),
            hover_bg=COLOR_SECONDARY,
            hover_fg=COLOR_PRIMARY,
            padx=15,
            pady=8,
            bd=0,
            relief=tk.FLAT
        )
        self.train_button.pack()
        
        # ===== RIGHT COLUMN: RESULTS =====
        
        # Results card with improved style
        results_card = tk.Frame(right_column, bg=COLOR_LIGHT_BG, bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
        results_card.pack(fill='both', expand=True)
        
        # Card header with improved style
        results_header = tk.Frame(results_card, bg=COLOR_PRIMARY, height=30)
        results_header.pack(fill='x')
        
        results_title = tk.Label(results_header, text="Resultados del Entrenamiento", 
                               font=("Arial", 11, "bold"), bg=COLOR_PRIMARY, fg="white", padx=10, pady=5)
        results_title.pack(anchor='w')
        
        # Card content with improved style
        results_content = tk.Frame(results_card, bg=COLOR_LIGHT_BG, padx=15, pady=8)
        results_content.pack(fill='both', expand=True)
        
        # Status indicator at the top with improved style
        self.status_frame = tk.Frame(results_content, bg=COLOR_LIGHT_BG)
        self.status_frame.pack(fill='x', pady=(0, 8))
        
        self.status_indicator = tk.Canvas(self.status_frame, width=15, height=15, 
                                        bg=COLOR_LIGHT_BG, highlightthickness=0)
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        self.status_indicator.create_oval(2, 2, 13, 13, fill=COLOR_ACCENT_RED, outline="")
        
        self.status_label = tk.Label(self.status_frame, text="Estado: No entrenado", 
                                   font=("Arial", 10, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_ACCENT_RED)
        self.status_label.pack(side=tk.LEFT)
        
        # Results in a nice table-like format with improved style
        results_table = tk.Frame(results_content, bg=COLOR_LIGHT_BG, bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
        results_table.pack(fill='x', pady=5)
        
        table_inner = tk.Frame(results_table, bg=COLOR_LIGHT_BG, padx=8, pady=5)
        table_inner.pack(fill='x')
        
        # Epochs row with improved style
        epochs_row = tk.Frame(table_inner, bg=COLOR_LIGHT_BG)
        epochs_row.pack(fill='x', pady=2)
        
        epochs_label = tk.Label(epochs_row, text="Épocas:", 
                              font=("Arial", 10, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY, 
                              width=15, anchor='w')
        epochs_label.pack(side=tk.LEFT)
        
        self.epochs_value = tk.Label(epochs_row, text="-", 
                                   font=("Arial", 10), bg=COLOR_LIGHT_BG, fg=COLOR_TEXT)
        self.epochs_value.pack(side=tk.LEFT, padx=5)
        
        # Error row with improved style
        error_row = tk.Frame(table_inner, bg=COLOR_LIGHT_BG)
        error_row.pack(fill='x', pady=2)
        
        error_label = tk.Label(error_row, text="Error Final:", 
                             font=("Arial", 10, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY, 
                             width=15, anchor='w')
        error_label.pack(side=tk.LEFT)
        
        self.error_value = tk.Label(error_row, text="-", 
                                 font=("Arial", 10), bg=COLOR_LIGHT_BG, fg=COLOR_TEXT)
        self.error_value.pack(side=tk.LEFT, padx=5)
        
        # Case row with improved style
        case_row = tk.Frame(table_inner, bg=COLOR_LIGHT_BG)
        case_row.pack(fill='x', pady=2)
        
        case_label = tk.Label(case_row, text="Caso Entrenado:", 
                            font=("Arial", 10, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY, 
                            width=15, anchor='w')
        case_label.pack(side=tk.LEFT)
        
        self.case_value = tk.Label(case_row, text="-", 
                                 font=("Arial", 10), bg=COLOR_LIGHT_BG, fg=COLOR_TEXT)
        self.case_value.pack(side=tk.LEFT, padx=5)
        
        # Weights section with improved style
        weights_section = tk.Frame(results_content, bg=COLOR_LIGHT_BG)
        weights_section.pack(fill='x', pady=5)
        
        weights_header = tk.Label(weights_section, text="Pesos Finales:", 
                                font=("Arial", 10, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
        weights_header.pack(anchor='w', pady=(0, 2))
        
        # Weights display in a scrollable text area with improved style
        weights_frame = tk.Frame(weights_section, bg="white", bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
        weights_frame.pack(fill='both', expand=True, pady=2)
        
        self.weights_text = tk.Text(weights_frame, height=6, width=40, font=("Consolas", 9),
                                  bg="white", fg=COLOR_TEXT, bd=0, padx=8, pady=5,
                                  wrap=tk.WORD)
        self.weights_text.pack(side=tk.LEFT, fill='both', expand=True)
        self.weights_text.insert(tk.END, "Los pesos se mostrarán aquí después del entrenamiento.")
        self.weights_text.config(state=tk.DISABLED)
        
        weights_scrollbar = ttk.Scrollbar(weights_frame, orient="vertical", command=self.weights_text.yview)
        weights_scrollbar.pack(side=tk.RIGHT, fill='y')
        self.weights_text.config(yscrollcommand=weights_scrollbar.set)
        
        # Training progress visualization with improved style
        progress_frame = tk.Frame(results_content, bg=COLOR_LIGHT_BG)
        progress_frame.pack(fill='x', pady=5)
        
        progress_label = tk.Label(progress_frame, text="Progreso de Entrenamiento:", 
                                font=("Arial", 10, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
        progress_label.pack(anchor='w', pady=(0, 2))
        
        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", 
                                          length=100, mode="determinate", style="TProgressbar")
        self.progress_bar.pack(fill='x')
        
        # Inicializar la referencia del caso
        self.update_case_info()
        
    def update_case_info(self, event=None):
        """Update the case description and reference based on the selected case"""
        selected_case = self.case_var.get()
        
        # Actualizar la descripción
        if selected_case == "Caso 1 (entrada 2)":
            description = "Caso 1: Entradas [00,01,10,11], Salidas [0,1,2,3]"
            reference = "Caso 1: Entradas [00,01,10,11], Salidas [0,1,2,3]"
            # Mostrar el frame de referencia
            self.case_reference_frame.pack(fill='x', pady=5)
            self.case_reference_label.config(text=reference)
        elif selected_case == "Caso 2 (entrada 3)":
            description = "Caso 2: Entradas [000,001,010,011,100,101,110,111], Salidas [0,1,2,3,4,5,6,7]"
            reference = "Caso 2: Entradas [000,001,...,111], Salidas [0,1,...,7]"
            # Mostrar el frame de referencia
            self.case_reference_frame.pack(fill='x', pady=5)
            self.case_reference_label.config(text=reference)
        elif selected_case == "Caso 3 (entrada 4)":
            description = "Caso 3: Entradas [0000,...,1111], Salidas [0,1,2,3,...,15]"
            reference = "Caso 3: Entradas [0000,...,1111], Salidas [0,1,...,15]"
            # Mostrar el frame de referencia
            self.case_reference_frame.pack(fill='x', pady=5)
            self.case_reference_label.config(text=reference)
        elif selected_case == "Caso 4 (entrada 5)":
            description = "Caso 4: Entradas [00000,...,11111], Salidas [0,1,2,3,...,31]"
            reference = "Caso 4: Entradas [00000,...,11111], Salidas [0,1,...,31]"
            # Mostrar el frame de referencia
            self.case_reference_frame.pack(fill='x', pady=5)
            self.case_reference_label.config(text=reference)
        elif selected_case == "Todos los casos":
            description = "Todos los casos: Entrena los cuatro casos simultáneamente"
            # Ocultar el frame de referencia cuando se seleccionan todos los casos
            self.case_reference_frame.pack_forget()
            self.case_description_label.config(text=description)
        else:
            description = "Seleccione un caso para ver su descripción"
            self.case_reference_frame.pack_forget()
    
    def update_case_reference(self, case_name, inputs, outputs):
        """Update the case reference with actual data loaded from file"""
        if inputs is None or outputs is None:
            return
            
        # Create a summary of the data
        num_patterns = len(inputs)
        input_size = inputs.shape[1]
        
        # Create a sample of the data (first few patterns)
        sample_size = min(3, num_patterns)
        input_samples = []
        output_samples = []
        
        for i in range(sample_size):
            input_str = ''.join([str(int(x)) for x in inputs[i]])
            input_samples.append(input_str)
            output_samples.append(str(int(outputs[i])))
        
        # Create the reference text
        if num_patterns > sample_size:
            input_text = f"[{','.join(input_samples)},...] ({num_patterns} patrones)"
            output_text = f"[{','.join(output_samples)},...] ({num_patterns} valores)"
        else:
            input_text = f"[{','.join(input_samples)}] ({num_patterns} patrones)"
            output_text = f"[{','.join(output_samples)}] ({num_patterns} valores)"
        
        reference = f"{case_name}: Entradas {input_text}, Salidas {output_text}"
        
        # Update the reference label
        self.case_reference_label.config(text=reference)
        self.case_reference_frame.pack(fill='x', pady=5)
        
    def update_results(self, epochs, final_error, weights, bias, success=False, case=""):
        """Update the results display after training"""
        # Update epochs and error
        self.epochs_value.config(text=str(epochs))
        self.error_value.config(text=f"{final_error:.8f}")
        self.case_value.config(text=case)
        
        # Update weights text
        self.weights_text.config(state=tk.NORMAL)
        self.weights_text.delete(1.0, tk.END)
        
        # Format the weights for display
        if isinstance(weights, dict):
            # Multiple cases
            weights_info = "Pesos por caso:\n\n"
            for case_name, case_weights in weights.items():
                weights_info += f"{case_name}:\n"
                weights_info += "Pesos: " + ", ".join([f"{w:.4f}" for w in case_weights[0]]) + "\n"
                weights_info += f"Sesgo: {case_weights[1]:.4f}\n\n"
        else:
            # Single case
            weights_str = ", ".join([f"{w:.4f}" for w in weights])
            bias_str = f"{bias:.4f}"
            weights_info = f"Pesos:\n{weights_str}\n\nSesgo:\n{bias_str}"
        
        self.weights_text.insert(tk.END, weights_info)
        self.weights_text.config(state=tk.DISABLED)
        
        # Update status indicator
        if success:
            self.status_indicator.delete("all")
            self.status_indicator.create_oval(2, 2, 18, 18, fill=COLOR_SUCCESS, outline="")
            self.status_label.config(text="Estado: Entrenamiento exitoso", fg=COLOR_SUCCESS)
            self.progress_bar['value'] = 100
        else:
            self.status_indicator.delete("all")
            self.status_indicator.create_oval(2, 2, 18, 18, fill=COLOR_ACCENT_RED, outline="")
            self.status_label.config(text="Estado: Entrenamiento incompleto", fg=COLOR_ACCENT_RED)
            self.progress_bar['value'] = int((final_error / 0.01) * 100)  # Approximate progress

    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        self.config_canvas.yview_scroll(int(-1*(event.delta/120)), "units")