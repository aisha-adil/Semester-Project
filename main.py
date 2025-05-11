"""
Main application entry point with GUI.

This module implements a GUI for the hybrid encryption application, which combines
columnar transposition with cryptarithmetic-based substitution using genetic algorithms.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time

from encryption import encrypt, decrypt
from finishing_touches import save_to_file, load_from_file, is_valid_keyword, format_puzzle_display


class HybridEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hybrid Encryption Application")
        self.root.geometry("800x600")
        
        # Create tabs
        self.tab_control = ttk.Notebook(root)
        
        self.encrypt_tab = ttk.Frame(self.tab_control)
        self.decrypt_tab = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.encrypt_tab, text='Encrypt')
        self.tab_control.add(self.decrypt_tab, text='Decrypt')
        
        self.tab_control.pack(expand=1, fill="both")
        
        # Setup the encryption tab
        self.setup_encrypt_tab()
        
        # Setup the decryption tab
        self.setup_decrypt_tab()
    
    def setup_encrypt_tab(self):
        # Frame for input
        input_frame = ttk.LabelFrame(self.encrypt_tab, text="Input")
        input_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Plaintext input
        ttk.Label(input_frame, text="Plaintext:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.plaintext_input = tk.Text(input_frame, height=10, width=50)
        self.plaintext_input.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        # Keyword input
        ttk.Label(input_frame, text="Keyword:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.encrypt_keyword_input = ttk.Entry(input_frame, width=20)
        self.encrypt_keyword_input.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, padx=5, pady=10, sticky="w")
        
        self.encrypt_button = ttk.Button(button_frame, text="Encrypt", command=self.perform_encryption)
        self.encrypt_button.pack(side=tk.LEFT, padx=5)
        
        self.load_plaintext_button = ttk.Button(button_frame, text="Load from File", command=self.load_plaintext)
        self.load_plaintext_button.pack(side=tk.LEFT, padx=5)
        
        # Frame for output
        output_frame = ttk.LabelFrame(self.encrypt_tab, text="Output")
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Encrypted output
        ttk.Label(output_frame, text="Encrypted Puzzle:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.encrypted_output = tk.Text(output_frame, height=10, width=50, state="disabled")
        self.encrypted_output.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        # Buttons for output
        output_button_frame = ttk.Frame(output_frame)
        output_button_frame.grid(row=2, column=0, padx=5, pady=10, sticky="w")
        
        self.save_encrypted_button = ttk.Button(output_button_frame, text="Save to File", command=self.save_encrypted)
        self.save_encrypted_button.pack(side=tk.LEFT, padx=5)
        
        # Progress indicator
        self.encrypt_progress = ttk.Progressbar(self.encrypt_tab, orient="horizontal", length=200, mode="indeterminate")
        self.encrypt_progress.pack(padx=10, pady=10, fill="x")
        
        # Status label
        self.encrypt_status = ttk.Label(self.encrypt_tab, text="Ready")
        self.encrypt_status.pack(padx=10, pady=5, anchor="w")