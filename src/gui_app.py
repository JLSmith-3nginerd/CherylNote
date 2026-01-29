# src/gui_app.py - Main GUI Implementation

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys

# Add src to path for imports
sys.path.append(os.path.dirname(__file__))

from audio_processor import AudioProcessor
from diarization_manager import DiarizationManager
from transcription_manager import TranscriptionManager
from note_generator import NoteGenerator
from content_classifier import ContentClassifierSimple

class AudioNotesGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Initialize components
        self.audio_processor = AudioProcessor()
        self.diarization_manager = DiarizationManager()
        self.transcription_manager = TranscriptionManager() 
        self.note_generator = NoteGenerator()
        self.content_classifier = ContentClassifierSimple()
        
        # State variables
        self.current_file_path = None
        self.speaker_names = {}
        
        # Create UI elements
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Audio Notes Processor")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # Configure styles
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat")
        
    def create_widgets(self):
        """Create all GUI elements"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Audio Notes Processor", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Audio File", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="File:").grid(row=0, column=0, sticky="w")
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=50)
        file_entry.grid(row=0, column=1, sticky="ew", padx=(5, 5))
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=0, column=2)
        
        # Speaker naming section
        speaker_frame = ttk.LabelFrame(main_frame, text="Speaker Names", padding="10")
        speaker_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        speaker_frame.columnconfigure(1, weight=1)
        
        ttk.Label(speaker_frame, text="Speaker 1:").grid(row=0, column=0, sticky="w")
        self.speaker1_var = tk.StringVar()
        speaker1_entry = ttk.Entry(speaker_frame, textvariable=self.speaker1_var, width=20)
        speaker1_entry.grid(row=0, column=1, sticky="w", padx=(5, 5))
        
        ttk.Label(speaker_frame, text="Speaker 2:").grid(row=0, column=2, sticky="w")
        self.speaker2_var = tk.StringVar()
        speaker2_entry = ttk.Entry(speaker_frame, textvariable=self.speaker2_var, width=20)
        speaker2_entry.grid(row=0, column=3, sticky="w", padx=(5, 5))
        
        ttk.Label(speaker_frame, text="Speaker 3:").grid(row=1, column=0, sticky="w")
        self.speaker3_var = tk.StringVar()
        speaker3_entry = ttk.Entry(speaker_frame, textvariable=self.speaker3_var, width=20)
        speaker3_entry.grid(row=1, column=1, sticky="w", padx=(5, 5))
        
        # Output format selection
        output_frame = ttk.LabelFrame(main_frame, text="Output Format", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Format:").grid(row=0, column=0, sticky="w")
        self.output_format_var = tk.StringVar(value="text")
        format_combo = ttk.Combobox(output_frame, textvariable=self.output_format_var, 
                                   values=["text", "markdown", "pdf"], width=15)
        format_combo.grid(row=0, column=1, sticky="w", padx=(5, 5))
        
        # Processing controls
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        self.process_btn = ttk.Button(control_frame, text="Process Audio", 
                                     command=self.start_processing)
        self.process_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.reset_btn = ttk.Button(control_frame, text="Reset", command=self.reset_all)
        self.reset_btn.pack(side=tk.LEFT)
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=0, sticky="w")
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
        # Output sections
        output_frame = ttk.LabelFrame(main_frame, text="Processing Results", padding="10")
        output_frame.grid(row=7, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # Notebook for different outputs
        self.notebook = ttk.Notebook(output_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        # Create tabs
        self.create_output_tabs()
        
        # Configure grid weights for resize behavior
        main_frame.rowconfigure(7, weight=1)
        
    def create_output_tabs(self):
        """Create tabs for different output views"""
        # Diarization results tab
        diarization_frame = ttk.Frame(self.notebook)
        self.notebook.add(diarization_frame, text="Speaker Diarization")
        
        diarization_text = tk.Text(diarization_frame, height=10)
        diarization_scrollbar = ttk.Scrollbar(diarization_frame, orient="vertical", command=diarization_text.yview)
        diarization_text.configure(yscrollcommand=diarization_scrollbar.set)
        
        diarization_text.pack(side="left", fill="both", expand=True)
        diarization_scrollbar.pack(side="right", fill="y")
        
        self.diarization_output = diarization_text
        
        # Transcription tab
        transcription_frame = ttk.Frame(self.notebook)
        self.notebook.add(transcription_frame, text="Transcription")
        
        transcription_text = tk.Text(transcription_frame, height=10)
        transcription_scrollbar = ttk.Scrollbar(transcription_frame, orient="vertical", command=transcription_text.yview)
        transcription_text.configure(yscrollcommand=transcription_scrollbar.set)
        
        transcription_text.pack(side="left", fill="both", expand=True)
        transcription_scrollbar.pack(side="right", fill="y")
        
        self.transcription_output = transcription_text
        
        # Note generation tab
        notes_frame = ttk.Frame(self.notebook)
        self.notebook.add(notes_frame, text="Generated Notes")
        
        notes_text = tk.Text(notes_frame, height=10)
        notes_scrollbar = ttk.Scrollbar(notes_frame, orient="vertical", command=notes_text.yview)
        notes_text.configure(yscrollcommand=notes_scrollbar.set)
        
        notes_text.pack(side="left", fill="both", expand=True)
        notes_scrollbar.pack(side="right", fill="y")
        
        self.notes_output = notes_text
        
        # Content classification tab
        content_frame = ttk.Frame(self.notebook)
        self.notebook.add(content_frame, text="Content Classification")
        
        content_text = tk.Text(content_frame, height=10)
        content_scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=content_text.yview)
        content_text.configure(yscrollcommand=content_scrollbar.set)
        
        content_text.pack(side="left", fill="both", expand=True)
        content_scrollbar.pack(side="right", fill="y")
        
        self.content_output = content_text
    
    def browse_file(self):
        """Open file dialog to select audio/video file"""
        file_path = filedialog.askopenfilename(
            title="Select Audio/Video File",
            filetypes=[
                ("Audio files", "*.mp3 *.wav *.aac *.flac"),
                ("Video files", "*.mp4 *.mov *.avi *.mkv"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.current_file_path = file_path
            self.file_path_var.set(file_path)
            # Reset previous results when a new file is selected
            self.reset_results()
    
    def start_processing(self):
        """Start processing in a separate thread"""
        if not self.current_file_path:
            messagebox.showerror("Error", "Please select an audio file first")
            return
        
        # Get speaker names from UI
        self.speaker_names = {}
        if self.speaker1_var.get():
            self.speaker_names["1"] = self.speaker1_var.get()
        if self.speaker2_var.get():
            self.speaker_names["2"] = self.speaker2_var.get()
        if self.speaker3_var.get():
            self.speaker_names["3"] = self.speaker3_var.get()
        
        # Disable UI during processing
        self.process_btn.config(state='disabled')
        self.reset_btn.config(state='disabled')
        self.status_var.set("Processing...")
        self.progress.start()
        
        # Start processing in background thread
        process_thread = threading.Thread(target=self.process_audio, args=(self.current_file_path,))
        process_thread.daemon = True
        process_thread.start()
    
    def process_audio(self, file_path):
        """Process audio file in background thread"""
        try:
            # Step 1: Audio preprocessing
            self.update_status("Preparing audio file...")
            processed_audio = self.audio_processor.prepare_file(file_path)
            
            # Step 2: Speaker diarization
            self.update_status("Performing speaker diarization...")
            if self.speaker_names:
                diarization_results = self.diarization_manager.process_with_speaker_names(
                    processed_audio, list(self.speaker_names.values()))
            else:
                diarization_results = self.diarization_manager.process_audio(processed_audio)
            
            # Step 3: Transcription
            self.update_status("Transcribing audio...")
            transcription_results = self.transcription_manager.transcribe_audio(processed_audio)
            
            # Step 4: Content classification
            self.update_status("Classifying content type...")
            content_type = self.content_classifier.classify_content(transcription_results)
            
            # Step 5: Generate notes
            self.update_status("Generating notes...")
            output_format = self.output_format_var.get()
            
            # Generate notes based on selected format
            if output_format == "markdown":
                notes = self.note_generator.generate_markdown_notes(
                    transcription_results, content_type, self.speaker_names)
            elif output_format == "pdf":
                notes = self.note_generator.generate_pdf_notes(
                    transcription_results, content_type, self.speaker_names)
            else:
                notes = self.note_generator.generate_notes(
                    transcription_results, content_type, self.speaker_names)
            
            # Display results
            self.root.after(0, lambda: self.display_results(diarization_results, transcription_results, 
                                                          notes, content_type))
            
            self.update_status("Processing complete!")
            
        except Exception as e:
            error_msg = f"Error during processing: {str(e)}"
            self.update_status(error_msg)
            messagebox.showerror("Processing Error", error_msg)
        finally:
            # Re-enable UI
            self.root.after(0, lambda: self.finish_processing())
    
    def display_results(self, diarization_results, transcription_results, notes, content_type):
        """Display processing results in GUI"""
        # Display diarization
        self.diarization_output.delete(1.0, tk.END)
        for speaker_id, text in diarization_results.items():
            self.diarization_output.insert(tk.END, f"{speaker_id}:\n{text}\n\n")
        
        # Display transcription  
        self.transcription_output.delete(1.0, tk.END)
        for segment in transcription_results:
            self.transcription_output.insert(tk.END, f"[{segment['start']:.1f}s - {segment['end']:.1f}s] {segment['text']}\n")
        
        # Display notes
        self.notes_output.delete(1.0, tk.END)
        self.notes_output.insert(tk.END, notes)
        
        # Display content classification
        self.content_output.delete(1.0, tk.END)
        self.content_output.insert(tk.END, f"Content type: {content_type}\n")
        self.content_output.insert(tk.END, "Classification details:\n")
        
    def update_status(self, message):
        """Update status bar text"""
        self.status_var.set(message)
        
    def reset_results(self):
        """Clear previous results"""
        self.diarization_output.delete(1.0, tk.END)
        self.transcription_output.delete(1.0, tk.END)  
        self.notes_output.delete(1.0, tk.END)
        self.content_output.delete(1.0, tk.END)
        
    def reset_all(self):
        """Reset entire application"""
        self.file_path_var.set("")
        self.current_file_path = None
        self.speaker1_var.set("")
        self.speaker2_var.set("")
        self.speaker3_var.set("")
        self.speaker_names = {}
        self.reset_results()
        self.status_var.set("Ready")
        self.progress.stop()
        self.process_btn.config(state='normal')
        self.reset_btn.config(state='normal')
        
    def finish_processing(self):
        """Finalize processing and re-enable UI"""
        self.progress.stop()
        self.process_btn.config(state='normal')
        self.reset_btn.config(state='normal')

# Entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioNotesGUI(root)
    root.mainloop()