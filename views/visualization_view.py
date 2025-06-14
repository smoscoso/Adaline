import tkinter as tk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from utils.ui_components import COLOR_BG, COLOR_PRIMARY, COLOR_TEXT, COLOR_LIGHT_BG, COLOR_TEXT_SECONDARY, COLOR_BORDER, COLOR_SECONDARY, COLOR_ACCENT_BLUE
from tkinter import ttk

class VisualizationView:
    def __init__(self, error_frame, desired_frame, obtained_frame):
        self.error_frame = error_frame
        self.desired_frame = desired_frame
        self.obtained_frame = obtained_frame
        
        # Initialize the frames with placeholders
        self.setup_error_frame()
        if self.desired_frame:  # Solo inicializar si existe
            self.setup_desired_frame()
        self.setup_obtained_frame()
        
    def setup_error_frame(self):
        """Set up the error visualization tab with improved style"""
        self.error_container = tk.Frame(self.error_frame, bg=COLOR_BG)
        self.error_container.pack(fill='both', expand=True, padx=5, pady=5)  # Reducido padding
        
        # Title with improved style
        title_label = tk.Label(self.error_container, text="Gráfica de Error vs Épocas", 
                           font=("Arial", 12, "bold"), bg=COLOR_BG, fg=COLOR_PRIMARY)  # Reducido tamaño de fuente
        title_label.pack(pady=(0, 5))  # Reducido padding
        
        # Placeholder message with improved style
        self.error_placeholder = tk.Label(self.error_container, 
                                      text="Entrene el modelo para ver la gráfica de error", 
                                      bg=COLOR_BG, fg=COLOR_TEXT_SECONDARY, font=("Arial", 9))  # Reducido tamaño de fuente
        self.error_placeholder.pack(expand=True)
        
        # Frame for the plot with improved style
        self.error_plot_frame = tk.Frame(self.error_container, bg=COLOR_BG, bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
    
    def update_error_graph(self, error_history, case_name=None):
        """Plot the error vs epochs graph after training with improved style"""
        # Clear any existing plot
        for widget in self.error_plot_frame.winfo_children():
            widget.destroy()
        
        # Hide the placeholder message
        self.error_placeholder.pack_forget()
        self.error_plot_frame.pack(fill='both', expand=True)
        
        # Create a new figure and plot with improved style
        fig = Figure(figsize=(8, 4), dpi=100, facecolor=COLOR_LIGHT_BG)  # Reducido tamaño
        ax = fig.add_subplot(111)
        
        # Plot the error history with improved style
        ax.plot(error_history, color=COLOR_PRIMARY, linewidth=2)
        
        # Set title based on case name
        title = f'Error vs Épocas - {case_name}' if case_name else 'Error vs Épocas'
        ax.set_title(title, fontsize=12, fontweight='bold', color=COLOR_TEXT)  # Reducido tamaño de fuente
        
        ax.set_xlabel('Épocas', fontsize=10, color=COLOR_TEXT_SECONDARY)  # Reducido tamaño de fuente
        ax.set_ylabel('Error Cuadrático Medio', fontsize=10, color=COLOR_TEXT_SECONDARY)  # Reducido tamaño de fuente
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.tick_params(colors=COLOR_TEXT_SECONDARY, labelsize=8)  # Reducido tamaño de fuente
        
        # Set background color
        ax.set_facecolor(COLOR_LIGHT_BG)
        
        # Add the plot to the frame with proper expansion
        canvas = FigureCanvasTkAgg(fig, master=self.error_plot_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill='both', expand=True)
        
        # Add toolbar for navigation with improved style
        toolbar_frame = tk.Frame(self.error_plot_frame, bg=COLOR_LIGHT_BG)
        toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        
        # Add a border at the top of the toolbar
        border = tk.Frame(toolbar_frame, height=1, bg=COLOR_BORDER)
        border.pack(fill='x', side=tk.TOP)
    
    def update_error_graphs_multiple(self, error_histories):
        """Plot multiple error graphs for all cases"""
        # Clear any existing plot
        for widget in self.error_plot_frame.winfo_children():
            widget.destroy()
        
        # Hide the placeholder message
        self.error_placeholder.pack_forget()
        self.error_plot_frame.pack(fill='both', expand=True)
        
        # Create a notebook for multiple tabs
        notebook = ttk.Notebook(self.error_plot_frame)
        notebook.pack(fill='both', expand=True)
        
        # Add a tab for each case
        for case_name, error_history in error_histories.items():
            # Create a frame for this case
            case_frame = tk.Frame(notebook, bg=COLOR_LIGHT_BG)
            notebook.add(case_frame, text=case_name)
            
            # Create a figure for this case
            fig = Figure(figsize=(8, 4), dpi=100, facecolor=COLOR_LIGHT_BG)  # Reducido tamaño
            ax = fig.add_subplot(111)
            
            # Plot the error history
            ax.plot(error_history, color=COLOR_PRIMARY, linewidth=2)
            ax.set_title(f'Error vs Épocas - {case_name}', fontsize=12, fontweight='bold', color=COLOR_TEXT)  # Reducido tamaño de fuente
            ax.set_xlabel('Épocas', fontsize=10, color=COLOR_TEXT_SECONDARY)  # Reducido tamaño de fuente
            ax.set_ylabel('Error Cuadrático Medio', fontsize=10, color=COLOR_TEXT_SECONDARY)  # Reducido tamaño de fuente
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.tick_params(colors=COLOR_TEXT_SECONDARY, labelsize=8)  # Reducido tamaño de fuente
            
            # Set background color
            ax.set_facecolor(COLOR_LIGHT_BG)
            
            # Add the plot to the frame with proper expansion
            canvas = FigureCanvasTkAgg(fig, master=case_frame)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill='both', expand=True)
            
            # Add toolbar for navigation with improved style
            toolbar_frame = tk.Frame(case_frame, bg=COLOR_LIGHT_BG)
            toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            
            # Add a border at the top of the toolbar
            border = tk.Frame(toolbar_frame, height=1, bg=COLOR_BORDER)
            border.pack(fill='x', side=tk.TOP)
        
        # Add a tab for combined view
        combined_frame = tk.Frame(notebook, bg=COLOR_LIGHT_BG)
        notebook.add(combined_frame, text="Vista Combinada")
        
        # Create a figure for combined view
        fig_combined = Figure(figsize=(8, 4), dpi=100, facecolor=COLOR_LIGHT_BG)  # Reducido tamaño
        ax_combined = fig_combined.add_subplot(111)
        
        # Plot all error histories
        colors = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT_BLUE, '#FF6B6B', '#6BCB77']
        for i, (case_name, error_history) in enumerate(error_histories.items()):
            ax_combined.plot(error_history, label=case_name, color=colors[i % len(colors)], linewidth=2)
        
        ax_combined.set_title('Comparación de Error vs Épocas', fontsize=12, fontweight='bold', color=COLOR_TEXT)  # Reducido tamaño de fuente
        ax_combined.set_xlabel('Épocas', fontsize=10, color=COLOR_TEXT_SECONDARY)  # Reducido tamaño de fuente
        ax_combined.set_ylabel('Error Cuadrático Medio', fontsize=10, color=COLOR_TEXT_SECONDARY)  # Reducido tamaño de fuente
        ax_combined.grid(True, linestyle='--', alpha=0.7)
        ax_combined.tick_params(colors=COLOR_TEXT_SECONDARY, labelsize=8)  # Reducido tamaño de fuente
        ax_combined.legend(loc='best', fontsize=8)  # Reducido tamaño de fuente
        
        # Set background color
        ax_combined.set_facecolor(COLOR_LIGHT_BG)
        
        # Add the plot to the frame with proper expansion
        canvas_combined = FigureCanvasTkAgg(fig_combined, master=combined_frame)
        canvas_combined.draw()
        canvas_widget_combined = canvas_combined.get_tk_widget()
        canvas_widget_combined.pack(fill='both', expand=True)
        
        # Add toolbar for navigation with improved style
        toolbar_frame_combined = tk.Frame(combined_frame, bg=COLOR_LIGHT_BG)
        toolbar_frame_combined.pack(side=tk.BOTTOM, fill=tk.X)
        toolbar_combined = NavigationToolbar2Tk(canvas_combined, toolbar_frame_combined)
        toolbar_combined.update()
        
        # Add a border at the top of the toolbar
        border_combined = tk.Frame(toolbar_frame_combined, height=1, bg=COLOR_BORDER)
        border_combined.pack(fill='x', side=tk.TOP)

    def setup_desired_frame(self):
        """Set up the desired outputs tab with improved visualization"""
        # Esta función ya no se usará, pero la mantenemos por compatibilidad
        if not self.desired_frame:
            return
            
        self.desired_container = tk.Frame(self.desired_frame, bg=COLOR_BG)
        self.desired_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Title with improved style
        title_label = tk.Label(self.desired_container, text="Descenso de Gradiente", 
                           font=("Arial", 12, "bold"), bg=COLOR_BG, fg=COLOR_PRIMARY)
        title_label.pack(pady=(0, 5))
        
        # Placeholder message with improved style
        self.desired_placeholder = tk.Label(self.desired_container, 
                                    text="Entrene el modelo para ver la visualización del descenso de gradiente", 
                                    bg=COLOR_BG, fg=COLOR_TEXT_SECONDARY, font=("Arial", 9))
        self.desired_placeholder.pack(expand=True, pady=15)
        
        # Frame for the plot with improved style
        self.desired_plot_frame = tk.Frame(self.desired_container, bg=COLOR_BG, bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
    
    def update_desired_visualization(self, inputs, outputs, weights, bias, case_name=None):
        """Update the desired outputs visualization with gradient descent visualization"""
        # Clear any existing plot
        for widget in self.desired_plot_frame.winfo_children():
            widget.destroy()
        
        # Hide the placeholder message
        self.desired_placeholder.pack_forget()
        self.desired_plot_frame.pack(fill='both', expand=True)
        
        # Create a new figure with improved style
        fig = Figure(figsize=(10, 6), dpi=100, facecolor=COLOR_LIGHT_BG)
        
        # Create a 2x1 subplot layout
        gs = fig.add_gridspec(2, 1, height_ratios=[2, 1], hspace=0.3)
        
        # Top subplot: Gradient descent visualization
        ax1 = fig.add_subplot(gs[0], projection='3d')
        
        # Create a simple gradient descent visualization
        # We'll create a simple error surface for visualization
        x = np.linspace(-2, 2, 30)
        y = np.linspace(-2, 2, 30)
        X, Y = np.meshgrid(x, y)
        Z = X**2 + Y**2  # Simple paraboloid as error surface
        
        # Plot the error surface
        surf = ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
        
        # Plot a path representing gradient descent
        # We'll create a simple spiral path towards the minimum
        t = np.linspace(0, 10, 100)
        radius = 2 * np.exp(-0.3 * t)
        x_path = radius * np.cos(t)
        y_path = radius * np.sin(t)
        z_path = x_path**2 + y_path**2
        
        ax1.plot(x_path, y_path, z_path, color='red', linewidth=2, marker='o', markersize=3)
        
        # Mark the minimum point
        ax1.scatter([0], [0], [0], color='red', s=100, marker='*')
        
        # Set labels and title
        title = f'Visualización de Descenso de Gradiente - {case_name}' if case_name else 'Visualización de Descenso de Gradiente'
        ax1.set_title(title, fontsize=14, fontweight='bold', color=COLOR_TEXT)
        ax1.set_xlabel('Peso 1', fontsize=10, color=COLOR_TEXT_SECONDARY)
        ax1.set_ylabel('Peso 2', fontsize=10, color=COLOR_TEXT_SECONDARY)
        ax1.set_zlabel('Error', fontsize=10, color=COLOR_TEXT_SECONDARY)
        
        # Bottom subplot: Desired outputs
        ax2 = fig.add_subplot(gs[1])
        
        # Create bar chart of outputs
        bars = ax2.bar(range(len(outputs)), outputs, color=COLOR_PRIMARY, alpha=0.7)
        
        # Add a trend line
        ax2.plot(range(len(outputs)), outputs, 'o-', color=COLOR_SECONDARY, linewidth=2)
        
        # Add labels and title with improved style
        ax2.set_title('Salidas Deseadas por Patrón de Entrada', fontsize=12, fontweight='bold', color=COLOR_TEXT)
        ax2.set_xlabel('Índice del Patrón', fontsize=10, color=COLOR_TEXT_SECONDARY)
        ax2.set_ylabel('Salida Deseada', fontsize=10, color=COLOR_TEXT_SECONDARY)
        
        # Add value labels on top of bars
        for bar, output in zip(bars, outputs):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                  f'{output:.1f}', ha='center', va='bottom', 
                  color=COLOR_TEXT_SECONDARY, fontsize=9)
        
        # Set background color
        ax2.set_facecolor(COLOR_LIGHT_BG)
        ax2.grid(True, linestyle='--', alpha=0.3)
        
        # Add the plot to the frame with proper expansion
        canvas = FigureCanvasTkAgg(fig, master=self.desired_plot_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill='both', expand=True)
        
        # Add toolbar for navigation with improved style
        toolbar_frame = tk.Frame(self.desired_plot_frame, bg=COLOR_LIGHT_BG)
        toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        
        # Add a border at the top of the toolbar
        border = tk.Frame(toolbar_frame, height=1, bg=COLOR_BORDER)
        border.pack(fill='x', side=tk.TOP)
    
    def update_desired_visualizations_multiple(self, cases_data):
        """Plot multiple gradient descent visualizations for all cases"""
        # Clear any existing plot
        for widget in self.desired_plot_frame.winfo_children():
            widget.destroy()
        
        # Hide the placeholder message
        self.desired_placeholder.pack_forget()
        self.desired_plot_frame.pack(fill='both', expand=True)
        
        # Create a notebook for multiple tabs
        notebook = ttk.Notebook(self.desired_plot_frame)
        notebook.pack(fill='both', expand=True)
        
        # Add a tab for each case
        for case_name, (inputs, outputs, weights, bias) in cases_data.items():
            # Create a frame for this case
            case_frame = tk.Frame(notebook, bg=COLOR_LIGHT_BG)
            notebook.add(case_frame, text=case_name)
            
            # Create a figure for this case
            fig = Figure(figsize=(10, 6), dpi=100, facecolor=COLOR_LIGHT_BG)
            
            # Create a 2x1 subplot layout
            gs = fig.add_gridspec(2, 1, height_ratios=[2, 1], hspace=0.3)
            
            # Top subplot: Gradient descent visualization
            ax1 = fig.add_subplot(gs[0], projection='3d')
            
            # Create a simple gradient descent visualization
            x = np.linspace(-2, 2, 30)
            y = np.linspace(-2, 2, 30)
            X, Y = np.meshgrid(x, y)
            Z = X**2 + Y**2  # Simple paraboloid as error surface
            
            # Plot the error surface
            surf = ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
            
            # Plot a path representing gradient descent
            t = np.linspace(0, 10, 100)
            radius = 2 * np.exp(-0.3 * t)
            x_path = radius * np.cos(t)
            y_path = radius * np.sin(t)
            z_path = x_path**2 + y_path**2
            
            ax1.plot(x_path, y_path, z_path, color='red', linewidth=2, marker='o', markersize=3)
            
            # Mark the minimum point
            ax1.scatter([0], [0], [0], color='red', s=100, marker='*')
            
            # Set labels and title
            ax1.set_title(f'Visualización de Descenso de Gradiente - {case_name}', fontsize=14, fontweight='bold', color=COLOR_TEXT)
            ax1.set_xlabel('Peso 1', fontsize=10, color=COLOR_TEXT_SECONDARY)
            ax1.set_ylabel('Peso 2', fontsize=10, color=COLOR_TEXT_SECONDARY)
            ax1.set_zlabel('Error', fontsize=10, color=COLOR_TEXT_SECONDARY)
            
            # Bottom subplot: Desired outputs
            ax2 = fig.add_subplot(gs[1])
            
            # Create bar chart of outputs
            bars = ax2.bar(range(len(outputs)), outputs, color=COLOR_PRIMARY, alpha=0.7)
            
            # Add a trend line
            ax2.plot(range(len(outputs)), outputs, 'o-', color=COLOR_SECONDARY, linewidth=2)
            
            # Add labels and title with improved style
            ax2.set_title('Salidas Deseadas por Patrón de Entrada', fontsize=12, fontweight='bold', color=COLOR_TEXT)
            ax2.set_xlabel('Índice del Patrón', fontsize=10, color=COLOR_TEXT_SECONDARY)
            ax2.set_ylabel('Salida Deseada', fontsize=10, color=COLOR_TEXT_SECONDARY)
            
            # Add value labels on top of bars
            for bar, output in zip(bars, outputs):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                      f'{output:.1f}', ha='center', va='bottom', 
                      color=COLOR_TEXT_SECONDARY, fontsize=9)
            
            # Set background color
            ax2.set_facecolor(COLOR_LIGHT_BG)
            ax2.grid(True, linestyle='--', alpha=0.3)
            
            # Add the plot to the frame with proper expansion
            canvas = FigureCanvasTkAgg(fig, master=case_frame)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill='both', expand=True)
            
            # Add toolbar for navigation with improved style
            toolbar_frame = tk.Frame(case_frame, bg=COLOR_LIGHT_BG)
            toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            
            # Add a border at the top of the toolbar
            border = tk.Frame(toolbar_frame, height=1, bg=COLOR_BORDER)
            border.pack(fill='x', side=tk.TOP)
    
    def setup_obtained_frame(self):
        """Set up the obtained outputs tab with improved style"""
        self.obtained_container = tk.Frame(self.obtained_frame, bg=COLOR_BG)
        self.obtained_container.pack(fill='both', expand=True, padx=5, pady=5)  # Reducido padding
        
        # Title with improved style
        title_label = tk.Label(self.obtained_container, text="Comparación de Salidas", 
                             font=("Arial", 12, "bold"), bg=COLOR_BG, fg=COLOR_PRIMARY)  # Reducido tamaño de fuente
        title_label.pack(pady=(0, 5))  # Reducido padding
        
        # Placeholder message with improved style
        self.obtained_placeholder = tk.Label(self.obtained_container, 
                                       text="Entrene el modelo para ver la comparación de salidas", 
                                       bg=COLOR_BG, fg=COLOR_TEXT_SECONDARY, font=("Arial", 9))  # Reducido tamaño de fuente
        self.obtained_placeholder.pack(expand=True, pady=15)  # Reducido padding
        
        # Frame for the plot with improved style
        self.obtained_plot_frame = tk.Frame(self.obtained_container, bg=COLOR_BG, bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
    
    def update_obtained_visualization(self, inputs, desired_outputs, predictions, case_name=None):
        """Update the obtained outputs visualization with comparison charts"""
        # Clear any existing plot
        for widget in self.obtained_plot_frame.winfo_children():
            widget.destroy()
        
        # Hide the placeholder message
        self.obtained_placeholder.pack_forget()
        self.obtained_plot_frame.pack(fill='both', expand=True)
        
        # Create a new figure with improved style
        fig = Figure(figsize=(8, 4), dpi=100, facecolor=COLOR_LIGHT_BG)  # Reducido tamaño
        
        # Create a 2x1 subplot layout
        gs = fig.add_gridspec(2, 1, height_ratios=[2, 1], hspace=0.2)  # Reducido espacio
        
        # Top subplot: Comparison of desired vs obtained outputs
        ax1 = fig.add_subplot(gs[0])
        
        # Plot desired and obtained outputs
        x = range(len(desired_outputs))
        ax1.plot(x, desired_outputs, 'o-', color=COLOR_PRIMARY, linewidth=2, label='Salida Deseada')
        ax1.plot(x, predictions, 's--', color=COLOR_SECONDARY, linewidth=2, label='Salida Obtenida')
        
        # Add labels and title with improved style
        title = f'Comparación de Salidas - {case_name}' if case_name else 'Comparación de Salidas Deseadas vs Obtenidas'
        ax1.set_title(title, fontsize=11, fontweight='bold', color=COLOR_TEXT)  # Reducido tamaño de fuente
        ax1.set_xlabel('Índice del Patrón', fontsize=9, color=COLOR_TEXT_SECONDARY)  # Reducido tamaño de fuente
        ax1.set_ylabel('Valor de Salida', fontsize=9, color=COLOR_TEXT_SECONDARY)  # Reducido tamaño de fuente
        ax1.legend(loc='best', fontsize=8)  # Reducido tamaño de fuente
        ax1.grid(True, linestyle='--', alpha=0.5)
        
        # Set background color
        ax1.set_facecolor(COLOR_LIGHT_BG)
        
        # Bottom subplot: Error for each pattern
        ax2 = fig.add_subplot(gs[1])
        
        # Calculate error for each pattern
        errors = np.abs(desired_outputs - predictions)
        
        # Create bar chart of errors
        bars = ax2.bar(x, errors, color=COLOR_ACCENT_BLUE, alpha=0.7)
        
        # Add a horizontal line for average error
        avg_error = np.mean(errors)
        ax2.axhline(y=avg_error, color='red', linestyle='--', linewidth=1.5, 
                  label=f'Error Promedio: {avg_error:.4f}')
        
        # Add labels and title with improved style
        ax2.set_title('Error Absoluto por Patrón', fontsize=10, fontweight='bold', color=COLOR_TEXT)  # Reducido tamaño de fuente
        ax2.set_xlabel('Índice del Patrón', fontsize=8, color=COLOR_TEXT_SECONDARY)  # Reducido tamaño de fuente
        ax2.set_ylabel('Error Absoluto', fontsize=8, color=COLOR_TEXT_SECONDARY)  # Reducido tamaño de fuente
        ax2.legend(loc='best', fontsize=7)  # Reducido tamaño de fuente
        
        # Set background color
        ax2.set_facecolor(COLOR_LIGHT_BG)
        ax2.grid(True, linestyle='--', alpha=0.3)
        
        # Add the plot to the frame with proper expansion
        canvas = FigureCanvasTkAgg(fig, master=self.obtained_plot_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill='both', expand=True)
        
        # Add toolbar for navigation with improved style
        toolbar_frame = tk.Frame(self.obtained_plot_frame, bg=COLOR_LIGHT_BG)
        toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        
        # Add a border at the top of the toolbar
        border = tk.Frame(toolbar_frame, height=1, bg=COLOR_BORDER)
        border.pack(fill='x', side=tk.TOP)
    
    def update_obtained_visualizations_multiple(self, cases_data):
        """Plot multiple output comparisons for all cases"""
        # Clear any existing plot
        for widget in self.obtained_plot_frame.winfo_children():
            widget.destroy()
        
        # Hide the placeholder message
        self.obtained_placeholder.pack_forget()
        self.obtained_plot_frame.pack(fill='both', expand=True)
        
        # Create a notebook for multiple tabs
        notebook = ttk.Notebook(self.obtained_plot_frame)
        notebook.pack(fill='both', expand=True)
        
        # Add a tab for each case
        for case_name, (inputs, desired_outputs, predictions) in cases_data.items():
            # Create a frame for this case
            case_frame = tk.Frame(notebook, bg=COLOR_LIGHT_BG)
            notebook.add(case_frame, text=case_name)
            
            # Create a figure for this case
            fig = Figure(figsize=(8, 4), dpi=100, facecolor=COLOR_LIGHT_BG)  # Reducido tamaño
            
            # Create a 2x1 subplot layout
            gs = fig.add_gridspec(2, 1, height_ratios=[2, 1], hspace=0.2)  # Reducido espacio
            
            # Top subplot: Comparison of desired vs obtained outputs
            ax1 = fig.add_subplot(gs[0])
            
            # Plot desired and obtained outputs
            x = range(len(desired_outputs))
            ax1.plot(x, desired_outputs, 'o-', color=COLOR_PRIMARY, linewidth=2, label='Salida Deseada')
            ax1.plot(x, predictions, 's--', color=COLOR_SECONDARY, linewidth=2, label='Salida Obtenida')
            
            # Add labels and title with improved style
            ax1.set_title(f'Comparación de Salidas - {case_name}', fontsize=11, fontweight='bold', color=COLOR_TEXT)  # Reducido tamaño de fuente
            ax1.set_xlabel('Índice del Patrón', fontsize=9, color=COLOR_TEXT_SECONDARY)  # Reducido tamaño de fuente
            ax1.set_ylabel('Valor de Salida', fontsize=9, color=COLOR_TEXT_SECONDARY)  # Reducido tamaño de fuente
            ax1.legend(loc='best', fontsize=8)  # Reducido tamaño de fuente
            ax1.grid(True, linestyle='--', alpha=0.5)
            
            # Set background color
            ax1.set_facecolor(COLOR_LIGHT_BG)
            
            # Bottom subplot: Error for each pattern
            ax2 = fig.add_subplot(gs[1])
            
            # Calculate error for each pattern
            errors = np.abs(desired_outputs - predictions)
            
            # Create bar chart of errors
            bars = ax2.bar(x, errors, color=COLOR_ACCENT_BLUE, alpha=0.7)
            
            # Add a horizontal line for average error
            avg_error = np.mean(errors)
            ax2.axhline(y=avg_error, color='red', linestyle='--', linewidth=1.5, 
                      label=f'Error Promedio: {avg_error:.4f}')
            
            # Add labels and title with improved style
            ax2.set_title('Error Absoluto por Patrón', fontsize=10, fontweight='bold', color=COLOR_TEXT)  # Reducido tamaño de fuente
            ax2.set_xlabel('Índice del Patrón', fontsize=8, color=COLOR_TEXT_SECONDARY)  # Reducido tamaño de fuente
            ax2.set_ylabel('Error Absoluto', fontsize=8, color=COLOR_TEXT_SECONDARY)  # Reducido tamaño de fuente
            ax2.legend(loc='best', fontsize=7)  # Reducido tamaño de fuente
            
            # Set background color
            ax2.set_facecolor(COLOR_LIGHT_BG)
            ax2.grid(True, linestyle='--', alpha=0.3)
            
            # Add the plot to the frame with proper expansion
            canvas = FigureCanvasTkAgg(fig, master=case_frame)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill='both', expand=True)
            
            # Add toolbar for navigation with improved style
            toolbar_frame = tk.Frame(case_frame, bg=COLOR_LIGHT_BG)
            toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            
            # Add a border at the top of the toolbar
            border = tk.Frame(toolbar_frame, height=1, bg=COLOR_BORDER)
            border.pack(fill='x', side=tk.TOP)
    
    def setup_decision_frame(self):
        """Set up the decision line tab with improved visualization"""
        self.decision_container = tk.Frame(self.decision_frame, bg=COLOR_BG)
        self.decision_container.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Title with improved style
        title_label = tk.Label(self.decision_container, text="Pesos y Sesgos del Modelo", 
                             font=("Arial", 14, "bold"), bg=COLOR_BG, fg=COLOR_PRIMARY)
        title_label.pack(pady=(0, 10))
        
        # Placeholder message with improved style
        self.decision_placeholder = tk.Label(self.decision_container, 
                                       text="Entrene el modelo para ver los pesos y sesgos", 
                                       bg=COLOR_BG, fg=COLOR_TEXT_SECONDARY, font=("Arial", 10))
        self.decision_placeholder.pack(expand=True, pady=30)
        
        # Frame for the plot with improved style
        self.decision_plot_frame = tk.Frame(self.decision_container, bg=COLOR_BG, bd=1, relief=tk.SOLID, highlightbackground=COLOR_BORDER, highlightthickness=1)
    
    def update_decision_visualization(self, inputs, outputs, weights, bias):
        """Update the decision visualization with weights and bias visualization"""
        # Clear any existing plot
        for widget in self.decision_plot_frame.winfo_children():
            widget.destroy()
        
        # Hide the placeholder message
        self.decision_placeholder.pack_forget()
        self.decision_plot_frame.pack(fill='both', expand=True)
        
        # Create a scrollable frame for the content
        scroll_frame = tk.Frame(self.decision_plot_frame, bg=COLOR_LIGHT_BG)
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
        
        # Add a title for the weights section
        weights_title = tk.Label(content_frame, text="Pesos del Modelo", 
                               font=("Arial", 12, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
        weights_title.pack(pady=(10, 5))
        
        # Create a frame for the weights visualization
        weights_frame = tk.Frame(content_frame, bg=COLOR_LIGHT_BG, padx=15, pady=5)
        weights_frame.pack(fill='x')
        
        # Create a figure for the weights visualization
        fig1 = Figure(figsize=(8, 3), dpi=100, facecolor=COLOR_LIGHT_BG)
        ax1 = fig1.add_subplot(111)
        
        # Create bar chart of weights
        x = np.arange(len(weights))
        bars = ax1.bar(x, weights, color=COLOR_PRIMARY, alpha=0.7)
        
        # Add labels and title
        ax1.set_title('Pesos del Modelo', fontsize=11, fontweight='bold', color=COLOR_TEXT)
        ax1.set_xlabel('Índice del Peso', fontsize=9, color=COLOR_TEXT_SECONDARY)
        ax1.set_ylabel('Valor', fontsize=9, color=COLOR_TEXT_SECONDARY)
        
        # Add x-tick labels
        labels = [f'w{i+1}' for i in range(len(weights))]
        ax1.set_xticks(x)
        ax1.set_xticklabels(labels, fontsize=8)
        
        # Add value labels on top of bars
        for bar, val in zip(bars, weights):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02 if height >= 0 else height - 0.08,
                   f'{val:.4f}', ha='center', va='bottom' if height >= 0 else 'top', 
                   color=COLOR_TEXT_SECONDARY, fontsize=8)
        
        # Set background color
        ax1.set_facecolor(COLOR_LIGHT_BG)
        ax1.grid(True, linestyle='--', alpha=0.3)
        ax1.tick_params(colors=COLOR_TEXT_SECONDARY, labelsize=8)
        
        # Add the plot to the frame
        canvas1 = FigureCanvasTkAgg(fig1, master=weights_frame)
        canvas1.draw()
        canvas_widget1 = canvas1.get_tk_widget()
        canvas_widget1.pack(fill='x')
        
        # Add a title for the bias section
        bias_title = tk.Label(content_frame, text="Sesgo del Modelo", 
                            font=("Arial", 12, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
        bias_title.pack(pady=(15, 5))
        
        # Create a frame for the bias visualization
        bias_frame = tk.Frame(content_frame, bg=COLOR_LIGHT_BG, padx=15, pady=5)
        bias_frame.pack(fill='x')
        
        # Create a figure for the bias visualization
        fig2 = Figure(figsize=(8, 1.5), dpi=100, facecolor=COLOR_LIGHT_BG)
        ax2 = fig2.add_subplot(111)
        
        # Create bar chart for bias
        bias_bar = ax2.bar(0, bias, color=COLOR_SECONDARY, alpha=0.7, width=0.5)
        
        # Add labels and title
        ax2.set_title('Sesgo del Modelo', fontsize=11, fontweight='bold', color=COLOR_TEXT)
        ax2.set_xlabel('', fontsize=9, color=COLOR_TEXT_SECONDARY)
        ax2.set_ylabel('Valor', fontsize=9, color=COLOR_TEXT_SECONDARY)
        
        # Add x-tick label
        ax2.set_xticks([0])
        ax2.set_xticklabels(['bias'], fontsize=8)
        
        # Add value label on top of bar
        ax2.text(0, bias + 0.02 if bias >= 0 else bias - 0.08,
               f'{bias:.4f}', ha='center', va='bottom' if bias >= 0 else 'top', 
               color=COLOR_TEXT_SECONDARY, fontsize=8)
        
        # Set background color
        ax2.set_facecolor(COLOR_LIGHT_BG)
        ax2.grid(True, linestyle='--', alpha=0.3)
        ax2.tick_params(colors=COLOR_TEXT_SECONDARY, labelsize=8)
        
        # Add the plot to the frame
        canvas2 = FigureCanvasTkAgg(fig2, master=bias_frame)
        canvas2.draw()
        canvas_widget2 = canvas2.get_tk_widget()
        canvas_widget2.pack(fill='x')
        
        # Add a title for the weights-inputs correspondence section
        corr_title = tk.Label(content_frame, text="Correspondencia entre Pesos y Entradas", 
                            font=("Arial", 12, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
        corr_title.pack(pady=(15, 5))
        
        # Create a frame for the correspondence table
        corr_frame = tk.Frame(content_frame, bg=COLOR_LIGHT_BG, padx=15, pady=5)
        corr_frame.pack(fill='x', padx=20, pady=10)
        
        # Create a table-like display for the correspondence
        headers = ["Peso", "Valor", "Entrada", "Descripción"]
        header_widths = [8, 12, 12, 25]
        
        # Create headers
        for i, header in enumerate(headers):
            label = tk.Label(corr_frame, text=header, bg=COLOR_PRIMARY, fg="white", 
                           font=("Arial", 9, "bold"), width=header_widths[i], padx=3, pady=3)
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
        
        # Fill the table with data
        for i, weight in enumerate(weights):
            # Weight name
            weight_name = tk.Label(corr_frame, text=f"w{i+1}", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                                 font=("Arial", 9), width=header_widths[0], padx=3, pady=3)
            weight_name.grid(row=i+1, column=0, sticky="nsew", padx=1, pady=1)
            
            # Weight value
            weight_val = tk.Label(corr_frame, text=f"{weight:.6f}", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                                font=("Arial", 9), width=header_widths[1], padx=3, pady=3)
            weight_val.grid(row=i+1, column=1, sticky="nsew", padx=1, pady=1)
            
            # Input name
            input_name = tk.Label(corr_frame, text=f"X{i+1}", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                                font=("Arial", 9), width=header_widths[2], padx=3, pady=3)
            input_name.grid(row=i+1, column=2, sticky="nsew", padx=1, pady=1)
            
            # Description
            desc = tk.Label(corr_frame, text=f"Peso para la entrada {i+1}", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                          font=("Arial", 9), width=header_widths[3], padx=3, pady=3, anchor="w")
            desc.grid(row=i+1, column=3, sticky="nsew", padx=1, pady=1)
        
        # Add bias to the table
        bias_name = tk.Label(corr_frame, text="bias", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                           font=("Arial", 9), width=header_widths[0], padx=3, pady=3)
        bias_name.grid(row=len(weights)+1, column=0, sticky="nsew", padx=1, pady=1)
        
        bias_val = tk.Label(corr_frame, text=f"{bias:.6f}", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                          font=("Arial", 9), width=header_widths[1], padx=3, pady=3)
        bias_val.grid(row=len(weights)+1, column=1, sticky="nsew", padx=1, pady=1)
        
        bias_input = tk.Label(corr_frame, text="1", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                            font=("Arial", 9), width=header_widths[2], padx=3, pady=3)
        bias_input.grid(row=len(weights)+1, column=2, sticky="nsew", padx=1, pady=1)
        
        bias_desc = tk.Label(corr_frame, text="Sesgo (término independiente)", bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                           font=("Arial", 9), width=header_widths[3], padx=3, pady=3, anchor="w")
        bias_desc.grid(row=len(weights)+1, column=3, sticky="nsew", padx=1, pady=1)
        
        # Add the equation of the model
        eq_title = tk.Label(content_frame, text="Ecuación del Modelo", 
                          font=("Arial", 12, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
        eq_title.pack(pady=(15, 5))
        
        # Create the equation string
        eq_str = "y = "
        for i, w in enumerate(weights):
            if i > 0:
                eq_str += " + " if w >= 0 else " - "
                eq_str += f"{abs(w):.4f}·X{i+1}"
            else:
                eq_str += f"{w:.4f}·X{i+1}"
        
        if bias >= 0:
            eq_str += f" + {bias:.4f}"
        else:
            eq_str += f" - {abs(bias):.4f}"
        
        # Display the equation
        eq_label = tk.Label(content_frame, text=eq_str, bg=COLOR_LIGHT_BG, fg=COLOR_TEXT, 
                          font=("Arial", 10), padx=15, pady=10)
        eq_label.pack(pady=(0, 15))
        
        # Update the scroll region when the frame size changes
        content_frame.bind("<Configure>", 
                         lambda e: canvas.configure(
                             scrollregion=canvas.bbox("all")))