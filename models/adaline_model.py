import numpy as np

class AdalineModel:
    def __init__(self, learning_rate=0.01, target_error=0.01, max_epochs=100000):
        self.learning_rate = learning_rate
        self.target_error = target_error
        self.max_epochs = max_epochs
        self.weights = None
        self.bias = None
        self.epochs_trained = 0
        self.error_history = []
        self.inputs = None
        self.desired_outputs = None
        
    def initialize_weights(self, input_size):
        """Initialize weights and bias with small random values"""
        self.weights = np.random.randn(input_size) * 0.1
        self.bias = np.random.randn() * 0.1
        
    def activation(self, x):
        """Linear activation function"""
        return x
    
    def train(self, inputs, desired_outputs):
        """Train the Adaline model"""
        self.inputs = inputs
        self.desired_outputs = desired_outputs
        
        # Initialize weights if not already done
        if self.weights is None:
            self.initialize_weights(inputs.shape[1])
        
        # Reset error history
        self.error_history = []
        self.epochs_trained = 0
        
        # Training loop
        current_error = float('inf')
        while current_error > self.target_error and self.epochs_trained < self.max_epochs:
            total_error = 0
            
            # Process each training sample
            for i in range(len(inputs)):
                # Calculate net input
                net_input = np.dot(inputs[i], self.weights) + self.bias
                
                # Apply activation function
                output = self.activation(net_input)
                
                # Calculate error
                error = desired_outputs[i] - output
                
                # Update weights and bias
                self.weights += self.learning_rate * error * inputs[i]
                self.bias += self.learning_rate * error
                
                # Add squared error to total error
                total_error += error ** 2
                
            # Calculate MSE for this epoch
            current_error = total_error / len(inputs)
            self.error_history.append(current_error)
            self.epochs_trained += 1
            
            # Optional: Add a callback for UI updates if needed
            if self.epochs_trained % 1000 == 0:
                print(f"Epoch {self.epochs_trained}, Error: {current_error}")
        
        return self.epochs_trained, self.error_history
    
    def predict(self, inputs):
        """Make predictions with the trained model"""
        if self.weights is None:
            raise ValueError("Model has not been trained yet")
        
        predictions = []
        for input_vector in inputs:
            net_input = np.dot(input_vector, self.weights) + self.bias
            output = self.activation(net_input)
            predictions.append(output)
            
        return np.array(predictions)

