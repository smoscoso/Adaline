import tkinter as tk
from controller.adaline_controller import AdalineController
from utils.ui_components import setup_styles

def main():
    # Create the root window
    root = tk.Tk()
    
    # Set up styles
    style = setup_styles()
    
    # Create the controller
    controller = AdalineController(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()

