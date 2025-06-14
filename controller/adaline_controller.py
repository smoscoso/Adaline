import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import os
from views.main_view import MainView
from views.config_view import ConfigView
from views.test_view import TestView
from views.visualization_view import VisualizationView
from views.weights_view import WeightsView
from models.adaline_model import AdalineModel

COLOR_LIGHT_BG = "#f0f0f0"
COLOR_TEXT_SECONDARY = "#555555"

class AdalineController:
    def __init__(self, root):
        # Create the main view
        self.main_view = MainView(root)
        
        # Create the config view
        self.config_view = ConfigView(self.main_view.config_frame)
        
        # Create the visualization view
        self.visualization_view = VisualizationView(
            self.main_view.error_frame,
            None,  # Pasamos None en lugar de desired_frame
            self.main_view.obtained_frame
        )
        
        # Create the test view
        self.test_view = TestView(self.main_view.test_frame)
        
        # Create the weights view
        self.weights_view = WeightsView(self.main_view.weights_frame)
        
        # Create models dictionary for multiple cases
        self.models = {
            "Caso 1 (entrada 2)": None,
            "Caso 2 (entrada 3)": None,
            "Caso 3 (entrada 4)": None,
            "Caso 4 (entrada 5)": None
        }
        
        # Dictionary to track which cases have data loaded
        self.data_loaded = {
            "Caso 1 (entrada 2)": False,
            "Caso 2 (entrada 3)": False,
            "Caso 3 (entrada 4)": False,
            "Caso 4 (entrada 5)": False
        }
        
        # Current active model
        self.current_model = None
        
        # Create data directory if it doesn't exist
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        # Create results directory if it doesn't exist
        self.results_dir = "resultados"
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
        
        # Bind events
        self.bind_events()
        
        # Initialize case data
        self.initialize_case_data()
        
        # Set initial case
        self.update_case()
        
        # Deshabilitar el botón de entrenamiento hasta que se carguen datos
        self.config_view.train_button.config(state=tk.DISABLED)
        
        # Guardar los archivos de ejemplo
        self.save_provided_files()
        
    def bind_events(self):
        """Bind UI events to controller methods"""
        # Bind train button
        self.config_view.train_button.config(command=self.train_model)
        
        # Bind case selection
        self.config_view.case_combo.bind("<<ComboboxSelected>>", self.update_case)
        
        # Bind test button
        self.test_view.test_button.config(command=self.test_custom_input)
        
        # Bind test case selection
        self.test_view.test_case_combo.bind("<<ComboboxSelected>>", self.update_test_case)
        
        # Bind load data button
        self.config_view.load_data_button.config(command=self.load_training_data)
        
        # Bind load test data button
        self.test_view.load_test_button.config(command=self.load_test_data)
        
    def initialize_case_data(self):
        """Initialize the data for each case"""
        # Initialize empty data structures
        self.case_data = {
            "Caso 1 (entrada 2)": (None, None),
            "Caso 2 (entrada 3)": (None, None),
            "Caso 3 (entrada 4)": (None, None),
            "Caso 4 (entrada 5)": (None, None)
        }
    
    def load_data_from_file(self, file_path):
        """Load training data from a text file"""
        try:
            # Check if the file has a header (first line contains text)
            with open(file_path, 'r') as f:
                first_line = f.readline().strip()
                has_header = ',' in first_line and any(c.isalpha() for c in first_line)
        
            # Load data with numpy, skipping header if present
            if has_header:
                data = np.loadtxt(file_path, delimiter=',', skiprows=1)
            else:
                # Try with comma delimiter first
                try:
                    data = np.loadtxt(file_path, delimiter=',')
                except:
                    # If that fails, try with space delimiter
                    data = np.loadtxt(file_path)
        
            # The last column is the desired output
            outputs = data[:, -1]
        
            # All other columns are inputs
            inputs = data[:, :-1]
        
            return inputs, outputs
    
        except Exception as e:
            print(f"Error loading file {file_path}: {str(e)}")
            raise e
    
    def load_training_data(self):
        """Load training data automatically based on the selected case"""
        selected_case = self.config_view.case_var.get()
        
        if selected_case == "Todos los casos":
            messagebox.showerror("Error", "Por favor seleccione un caso específico para cargar datos")
            return
        
        # Determine the file path based on the selected case
        file_name = ""
        if selected_case == "Caso 1 (entrada 2)":
            file_name = "Caso1.txt"
        elif selected_case == "Caso 2 (entrada 3)":
            file_name = "Caso2.txt"
        elif selected_case == "Caso 3 (entrada 4)":
            file_name = "Caso3.txt"
        elif selected_case == "Caso 4 (entrada 5)":
            file_name = "Caso4.txt"
        
        file_path = os.path.join(self.data_dir, file_name)
        
        # Check if the file exists
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"No se encontró el archivo {file_name} en la carpeta {self.data_dir}")
            return
        
        try:
            # Load data from the file
            inputs, outputs = self.load_data_from_file(file_path)
            
            # Verify the number of inputs matches the case
            expected_inputs = 0
            if selected_case == "Caso 1 (entrada 2)":
                expected_inputs = 2
            elif selected_case == "Caso 2 (entrada 3)":
                expected_inputs = 3
            elif selected_case == "Caso 3 (entrada 4)":
                expected_inputs = 4
            elif selected_case == "Caso 4 (entrada 5)":
                expected_inputs = 5
            
            if inputs.shape[1] != expected_inputs:
                messagebox.showerror("Error", 
                                f"El archivo contiene {inputs.shape[1]} entradas, pero {selected_case} requiere {expected_inputs} entradas")
                return
            
            # Store the data
            self.case_data[selected_case] = (inputs, outputs)
            
            # Mark this case as having data loaded
            self.data_loaded[selected_case] = True
            
            # Update current inputs/outputs
            self.current_inputs, self.current_outputs = inputs, outputs
            
            # Show success message
            messagebox.showinfo("Datos Cargados", 
                           f"Se cargaron {len(inputs)} patrones de entrenamiento para {selected_case}")
            
            # Update the case reference in the UI
            self.config_view.update_case_reference(selected_case, inputs, outputs)
            
            # Habilitar el botón de entrenamiento
            self.config_view.train_button.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
    
    def load_test_data(self):
        """Load test data automatically based on the selected case"""
        selected_case = self.test_view.test_case_var.get()
        
        if not selected_case:
            messagebox.showerror("Error", "Por favor seleccione un caso para cargar datos de prueba")
            return
        
        # Determine the file path based on the selected case
        file_name = ""
        if selected_case == "Caso 1 (entrada 2)":
            file_name = "Pesos_Caso1.txt"
        elif selected_case == "Caso 2 (entrada 3)":
            file_name = "Pesos_Caso2.txt"
        elif selected_case == "Caso 3 (entrada 4)":
            file_name = "Pesos_Caso3.txt"
        elif selected_case == "Caso 4 (entrada 5)":
            file_name = "Pesos_Caso4.txt"
        
        file_path = os.path.join(self.results_dir, file_name)
        
        # Check if the file exists
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"No se encontró el archivo {file_name} en la carpeta {self.results_dir}")
            return
        
        try:
            # Load data from the file
            data = np.loadtxt(file_path)
            
            # The last value is bias, all others are weights
            weights = data[:-1]
            bias = data[-1]
            
            # Verify the number of weights matches the case
            expected_weights = 0
            if selected_case == "Caso 1 (entrada 2)":
                expected_weights = 2
            elif selected_case == "Caso 2 (entrada 3)":
                expected_weights = 3
            elif selected_case == "Caso 3 (entrada 4)":
                expected_weights = 4
            elif selected_case == "Caso 4 (entrada 5)":
                expected_weights = 5
            
            if len(weights) != expected_weights:
                messagebox.showerror("Error", 
                                f"El archivo contiene {len(weights)} pesos, pero {selected_case} requiere {expected_weights} pesos")
                return
            
            # Create a model with these weights and bias
            model = AdalineModel()
            model.weights = weights
            model.bias = bias
            
            # Store the model
            self.models[selected_case] = model
            self.current_model = model
            
            # Update the test view with the loaded weights and bias
            self.test_view.update_weights_fields(weights, bias)
            
            # Update the test view
            self.update_test_case()
            
            # Show success message
            messagebox.showinfo("Datos de Prueba Cargados", 
                           f"Se cargaron los pesos y sesgo para {selected_case}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo de prueba: {str(e)}")
    
    def update_case(self, event=None):
        """Update the current case based on the selection"""
        selected_case = self.config_view.case_var.get()
        
        if selected_case == "Todos los casos":
            # No specific inputs/outputs to set for all cases
            self.current_inputs = None
            self.current_outputs = None
            # Disable train button for "Todos los casos" until all cases have data
            if all(self.data_loaded.values()):
                self.config_view.train_button.config(state=tk.NORMAL)
            else:
                self.config_view.train_button.config(state=tk.DISABLED)
        else:
            # Set inputs/outputs for the selected case
            self.current_inputs, self.current_outputs = self.case_data[selected_case]
            
            # Update the case reference in the UI
            if self.current_inputs is not None and self.current_outputs is not None:
                self.config_view.update_case_reference(selected_case, self.current_inputs, self.current_outputs)
                # Enable train button if data is loaded for this case
                self.config_view.train_button.config(state=tk.NORMAL)
            else:
                # Disable train button if no data is loaded for this case
                self.config_view.train_button.config(state=tk.DISABLED)
            
    def update_test_case(self, event=None):
        """Update the test view based on the selected test case"""
        selected_case = self.test_view.test_case_var.get()
        
        if not selected_case:
            return
        
        # Update input fields based on the case
        if selected_case == "Caso 1 (entrada 2)":
            input_size = 2
        elif selected_case == "Caso 2 (entrada 3)":
            input_size = 3
        elif selected_case == "Caso 3 (entrada 4)":
            input_size = 4
        elif selected_case == "Caso 4 (entrada 5)":
            input_size = 5
        else:
            input_size = 2  # Default
            
        # Update input fields
        self.test_view.create_input_fields(input_size)
        
        # Create weight fields
        self.test_view.create_weight_fields(input_size)
        
        # Check if the model for this case is trained
        if self.models.get(selected_case) is not None:
            # Set the current model for testing
            self.current_model = self.models[selected_case]
            
            # Update weight fields with current model weights and bias
            self.test_view.update_weights_fields(self.current_model.weights, self.current_model.bias)
        else:
            # Clear weight fields if no model is available
            self.test_view.clear_weights_fields()
        
        # Clear previous test results
        self.test_view.test_result_label.config(text="Los resultados se mostrarán aquí")
        
        # Clear previous visualization
        for widget in self.test_view.process_visualization_frame.winfo_children():
            widget.destroy()
            
        # Create a placeholder message for the visualization
        placeholder = tk.Label(self.test_view.process_visualization_frame, 
                            text=f"Modelo {selected_case} seleccionado. Ingrese valores y presione 'Probar' para ver resultados.", 
                            bg=COLOR_LIGHT_BG, fg=COLOR_TEXT_SECONDARY, font=("Arial", 9))
        placeholder.pack(expand=True, pady=15)
        
    def train_model(self):
        """Train the Adaline model with the current configuration"""
        try:
            # Get learning rate and target error from the UI
            learning_rate = float(self.config_view.lr_var.get())
            target_error = float(self.config_view.error_var.get())
            selected_case = self.config_view.case_var.get()
            
            # Validate inputs
            if learning_rate <= 0 or learning_rate > 1:
                messagebox.showerror("Error", "La tasa de aprendizaje debe estar entre 0 y 1")
                return
                
            if target_error <= 0 or target_error > 1:
                messagebox.showerror("Error", "El error objetivo debe estar entre 0 y 1")
                return
            
            # Train based on the selected case
            if selected_case == "Todos los casos":
                # Train all cases
                self.train_all_cases(learning_rate, target_error)
            else:
                # Train a single case
                self.train_single_case(selected_case, learning_rate, target_error)
                
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los valores de entrada: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el entrenamiento: {str(e)}")
    
    def train_single_case(self, case_name, learning_rate, target_error):
        """Train a single case"""
        # Get the inputs and outputs for this case
        inputs, outputs = self.case_data[case_name]
        
        if inputs is None or outputs is None:
            messagebox.showerror("Error", f"No hay datos de entrenamiento para {case_name}")
            return
        
        # Configure the model
        model = AdalineModel(learning_rate=learning_rate, target_error=target_error)
        
        # Train the model
        epochs, error_history = model.train(inputs, outputs)
        
        # Get the final weights and bias
        weights = model.weights
        bias = model.bias
        
        # Get the final error
        final_error = error_history[-1] if error_history else 1.0
        
        # Store the trained model
        self.models[case_name] = model
        self.current_model = model
        
        # Update the config view with results
        success = final_error <= target_error
        self.config_view.update_results(epochs, final_error, weights, bias, success, case_name)
        
        # Update the visualization view
        self.update_visualizations(case_name)
        
        # Update the weights view
        self.weights_view.update_weights_visualization(model, case_name)
        
        # Update test view dropdown to include this case
        trained_cases = [k for k, v in self.models.items() if v is not None]
        self.test_view.test_case_combo['values'] = trained_cases
        if case_name in trained_cases:
            self.test_view.test_case_combo.current(trained_cases.index(case_name))
            self.update_test_case()
        
        # Save weights and bias to file
        self.save_weights_to_file(case_name, weights, bias)
        
        # Show success message
        if success:
            messagebox.showinfo("Entrenamiento Exitoso", 
                               f"El modelo para {case_name} ha sido entrenado exitosamente en {epochs} épocas con un error final de {final_error:.8f}")
        else:
            messagebox.showwarning("Entrenamiento Incompleto", 
                                  f"El entrenamiento para {case_name} se detuvo después de {epochs} épocas con un error de {final_error:.8f}, que es mayor que el objetivo de {target_error}")
    
    def train_all_cases(self, learning_rate, target_error):
        """Train all cases simultaneously"""
        all_success = True
        total_epochs = 0
        avg_error = 0
        weights_dict = {}
        error_histories = {}
        cases_data_obtained = {}
        trained_cases = []
        
        # Train each case
        for case_name in self.case_data.keys():
            inputs, outputs = self.case_data[case_name]
            
            if inputs is None or outputs is None:
                messagebox.showwarning("Advertencia", f"No hay datos de entrenamiento para {case_name}, se omitirá")
                continue
            
            # Configure the model
            model = AdalineModel(learning_rate=learning_rate, target_error=target_error)
            
            # Train the model
            epochs, error_history = model.train(inputs, outputs)
            
            # Get the final error
            final_error = error_history[-1] if error_history else 1.0
            
            # Store the trained model
            self.models[case_name] = model
            trained_cases.append(case_name)
            
            # Store weights and bias for this case
            weights_dict[case_name] = (model.weights, model.bias)
            
            # Store error history for this case
            error_histories[case_name] = error_history
            
            # Store data for obtained outputs visualization
            predictions = model.predict(inputs)
            cases_data_obtained[case_name] = (inputs, outputs, predictions)
            
            # Save weights and bias to file
            self.save_weights_to_file(case_name, model.weights, model.bias)
            
            # Update statistics
            total_epochs += epochs
            avg_error += final_error
            
            # Check if training was successful
            if final_error > target_error:
                all_success = False
        
        # Calculate average error
        avg_error /= len(cases_data_obtained) if cases_data_obtained else 1
        
        # Set the current model to the first one
        if trained_cases:
            self.current_model = self.models[trained_cases[0]]
        
        # Update the config view with results
        self.config_view.update_results(total_epochs, avg_error, weights_dict, None, all_success, "Todos los casos")
        
        # Update the visualization view for all cases
        if error_histories:
            self.visualization_view.update_error_graphs_multiple(error_histories)
        if cases_data_obtained:
            self.visualization_view.update_obtained_visualizations_multiple(cases_data_obtained)
        
        # Update the weights view for all cases
        self.weights_view.update_weights_visualizations_multiple(self.models)
        
        # Update test view dropdown to include trained cases
        self.test_view.test_case_combo['values'] = trained_cases
        if trained_cases:
            self.test_view.test_case_combo.current(0)
            self.update_test_case()
        
        # Show success message
        if all_success:
            messagebox.showinfo("Entrenamiento Exitoso", 
                               f"Todos los modelos han sido entrenados exitosamente en un total de {total_epochs} épocas con un error promedio de {avg_error:.8f}")
        else:
            messagebox.showwarning("Entrenamiento Incompleto", 
                                  f"El entrenamiento de algunos modelos no alcanzó el error objetivo de {target_error}. Error promedio: {avg_error:.8f}")
    
    def save_weights_to_file(self, case_name, weights, bias):
        """Save weights and bias to a file"""
        # Determine file name based on case
        file_name = ""
        if case_name == "Caso 1 (entrada 2)":
            file_name = "Pesos_Caso1.txt"
        elif case_name == "Caso 2 (entrada 3)":
            file_name = "Pesos_Caso2.txt"
        elif case_name == "Caso 3 (entrada 4)":
            file_name = "Pesos_Caso3.txt"
        elif case_name == "Caso 4 (entrada 5)":
            file_name = "Pesos_Caso4.txt"
        
        file_path = os.path.join(self.results_dir, file_name)
        
        try:
            # Combine weights and bias into a single array
            data = np.append(weights, bias)
            
            # Save to file
            np.savetxt(file_path, data)
            
            print(f"Weights and bias saved to {file_path}")
        except Exception as e:
            print(f"Error saving weights to file: {str(e)}")
            
    def update_visualizations(self, case_name):
        """Update all visualizations after training for a specific case"""
        # Get the model for this case
        model = self.models[case_name]
        
        # Get the inputs and outputs for this case
        inputs, outputs = self.case_data[case_name]
        
        # Get predictions for the training data
        predictions = model.predict(inputs)
        
        # Update error graph
        self.visualization_view.update_error_graph(model.error_history, case_name)
        
        # Update obtained outputs visualization
        self.visualization_view.update_obtained_visualization(inputs, outputs, predictions, case_name)
            
    def test_custom_input(self):
        """Test the model with custom input"""
        try:
            selected_case = self.test_view.test_case_var.get()
            
            if not selected_case:
                messagebox.showerror("Error", "Por favor seleccione un caso para probar")
                return
            
            # Get weights and bias from the UI
            weights, bias = self.test_view.get_weights_and_bias()
            
            # Create or update the model with the current weights and bias
            if self.current_model is None:
                self.current_model = AdalineModel()
            
            self.current_model.weights = weights
            self.current_model.bias = bias
            
            # Store the updated model
            self.models[selected_case] = self.current_model
                
            # Get input values from the UI
            input_values = []
            for var in self.test_view.test_entry_vars:
                try:
                    value = int(var.get())
                    if value not in [0, 1]:
                        messagebox.showerror("Error", "Las entradas deben ser 0 o 1")
                        return
                    input_values.append(value)
                except ValueError:
                    messagebox.showerror("Error", "Las entradas deben ser números enteros (0 o 1)")
                    return
                    
            # Convert to numpy array
            input_array = np.array(input_values)
            
            # Make prediction
            prediction = self.current_model.predict([input_array])[0]
            
            # Update the test result
            self.test_view.update_test_result(input_array, prediction)
            
            # Draw the Adaline visualization
            self.test_view.draw_adaline_visualization(input_array, self.current_model.weights, self.current_model.bias, prediction)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la prueba: {str(e)}")

    def save_provided_files(self):
        """Save the provided files to the data directory"""
        try:
            # Check if files already exist
            caso1_path = os.path.join(self.data_dir, "Caso1.txt")
            caso2_path = os.path.join(self.data_dir, "Caso2.txt")
            caso3_path = os.path.join(self.data_dir, "Caso3.txt")
            caso4_path = os.path.join(self.data_dir, "Caso4.txt")
        
            # Only save if files don't exist
            if not os.path.exists(caso1_path):
                with open(caso1_path, 'w') as f:
                    f.write("x1,x2,Y\n0,0,0\n0,1,1\n1,0,2\n1,1,3")
                print(f"Saved Caso1.txt to {caso1_path}")
            
            if not os.path.exists(caso2_path):
                with open(caso2_path, 'w') as f:
                    f.write("x1,x2,x3,Y\n0,0,0,0\n0,0,1,1\n0,1,0,2\n0,1,1,3\n1,0,0,4\n1,0,1,5\n1,1,0,6\n1,1,1,7")
                print(f"Saved Caso2.txt to {caso2_path}")
            
            if not os.path.exists(caso3_path):
                with open(caso3_path, 'w') as f:
                    f.write("x1,x2,x3,x4,Y\n0,0,0,0,0\n0,0,0,1,1\n0,0,1,0,2\n0,0,1,1,3\n0,1,0,0,4\n0,1,0,1,5\n0,1,1,0,6\n0,1,1,1,7\n1,0,0,0,8\n1,0,0,1,9\n1,0,1,0,10\n1,0,1,1,11\n1,1,0,0,12\n1,1,0,1,13\n1,1,1,0,14\n1,1,1,1,15")
                print(f"Saved Caso3.txt to {caso3_path}")
            
            if not os.path.exists(caso4_path):
                with open(caso4_path, 'w') as f:
                    f.write("x1,x2,x3,x4,x5,Y\n0,0,0,0,0,0\n0,0,0,0,1,1\n0,0,0,1,0,2\n0,0,0,1,1,3\n0,0,1,0,0,4\n0,0,1,0,1,5\n0,0,1,1,0,6\n0,0,1,1,1,7\n0,1,0,0,0,8\n0,1,0,0,1,9\n0,1,0,1,0,10\n0,1,0,1,1,11\n0,1,1,0,0,12\n0,1,1,0,1,13\n0,1,1,1,0,14\n0,1,1,1,1,15\n1,0,0,0,0,16\n1,0,0,0,1,17\n1,0,0,1,0,18\n1,0,0,1,1,19\n1,0,1,0,0,20\n1,0,1,0,1,21\n1,0,1,1,0,22\n1,0,1,1,1,23\n1,1,0,0,0,24\n1,1,0,0,1,25\n1,1,0,1,0,26\n1,1,0,1,1,27\n1,1,1,0,0,28\n1,1,1,0,1,29\n1,1,1,1,0,30\n1,1,1,1,1,31")
                print(f"Saved Caso4.txt to {caso4_path}")
            
        except Exception as e:
            print(f"Error saving provided files: {str(e)}")
