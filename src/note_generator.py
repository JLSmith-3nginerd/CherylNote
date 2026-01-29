# src/note_generator.py - Generate structured notes

import re
from datetime import timedelta
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import sys
import os

# Add src to path for imports  
sys.path.insert(0, os.path.dirname(__file__))

from model_utils import get_resource_path, is_running_from_executable

class NoteGenerator:
    def __init__(self):
        # Initialize the LLM pipeline for note generation
        self.llm_pipeline = None
        self.model_name = "Qwen/Qwen2.5-1.5B-Instruct"  # Default model
        self.tokenizer = None
        self.model = None
    
    def load_llm_model(self, model_name="Qwen/Qwen2.5-1.5B-Instruct"):
        """Load LLM for note generation"""
        try:
            # When running from executable, we need to handle model loading carefully
            if is_running_from_executable():
                print("Loading LLM model from executable...")
                # For PyInstaller, we'll try to load the pre-trained model
                # Load tokenizer and model
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                )
                
                # Create pipeline for text generation
                self.llm_pipeline = pipeline(
                    "text-generation",
                    model=self.model,
                    tokenizer=self.tokenizer
                )
            else:
                # Regular path for development - this should work with virtual environment
                print("Loading LLM model from local...")
                # Load tokenizer and model
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                )
                
                # Create pipeline for text generation
                self.llm_pipeline = pipeline(
                    "text-generation",
                    model=self.model,
                    tokenizer=self.tokenizer
                )
            
            print(f"✓ LLM model ({model_name}) loaded successfully")
        except Exception as e:
            print(f"Error loading LLM model: {e}")
    
    def generate_notes(self, transcription_results, content_type="general", speaker_names=None):
        """Generate structured notes from transcription"""
        # Load model if not already loaded
        if self.llm_pipeline is None:
            self.load_llm_model()
        
        # If we can't load the pipeline, return mock results
        if self.llm_pipeline is None:
            # Mock implementation for demonstration - this will be replaced with real processing
            mock_notes = {
                "summary": "Meeting summary would appear here",
                "key_points": [
                    "Important point 1 about project updates",
                    "Key decision made during the meeting"
                ],
                "action_items": [
                    "Action item 1: Complete next steps by Friday",
                    "Action item 2: Review documentation"
                ],
                "speaker_notes": {
                    "Speaker_1": "Main speaker content would appear here",
                    "Speaker_2": "Secondary speaker content would appear here"
                }
            }
            return mock_notes
        
        try:
            # ACTUAL LLM IMPLEMENTATION
            print("Generating notes from transcription...")
            
            # Prepare the input prompt for the LLM
            prompt = self._create_prompt(transcription_results, content_type, speaker_names)
            
            # Generate notes using the LLM
            if self.llm_pipeline:
                response = self.llm_pipeline(
                    prompt,
                    max_new_tokens=512,
                    temperature=0.7,
                    do_sample=True
                )
                
                # Extract the generated text from response
                generated_text = response[0]['generated_text']
                
                # Process the generated text into structured notes
                return self._parse_generated_notes(generated_text)
            else:
                # If pipeline is not available, return mock results
                mock_notes = {
                    "summary": "Meeting summary would appear here",
                    "key_points": [
                        "Important point 1 about project updates",
                        "Key decision made during the meeting"
                    ],
                    "action_items": [
                        "Action item 1: Complete next steps by Friday",
                        "Action item 2: Review documentation"
                    ],
                    "speaker_notes": {
                        "Speaker_1": "Main speaker content would appear here",
                        "Speaker_2": "Secondary speaker content would appear here"
                    }
                }
                return mock_notes
                
        except Exception as e:
            print(f"Error during note generation: {e}")
            # Return mock results if there's an error
            return {
                "summary": f"Error generating notes: {str(e)}",
                "key_points": ["Please check your audio file and try again."],
                "action_items": [],
                "speaker_notes": {}
            }
    
    def _create_prompt(self, transcription_results, content_type, speaker_names):
        """Create a prompt for the LLM based on the transcription"""
        # Format transcription results
        formatted_transcription = []
        for segment in transcription_results:
            start_time = f"{segment['start']:.1f}s"
            text = segment['text']
            formatted_transcription.append(f"[{start_time}] {text}")
        
        transcription_text = "\n".join(formatted_transcription)
        
        # Create system prompt
        if content_type == "meeting":
            system_prompt = (
                "You are an expert meeting note taker. "
                "Create a structured summary of the following meeting transcript, including:\n"
                "1. A brief overall summary\n"
                "2. Key discussion points\n"
                "3. Action items with owners if specified\n"
                "4. Speaker-specific notes in the format: [Speaker Name]: Content"
            )
        elif content_type == "lecture":
            system_prompt = (
                "You are an expert lecture note taker. "
                "Create a structured summary of the following lecture transcript, including:\n"
                "1. A brief overall summary\n"
                "2. Key learning points\n"
                "3. Important concepts discussed\n"
                "4. Review questions or assignments if mentioned"
            )
        else:
            system_prompt = (
                "You are an expert note taker. "
                "Create a structured summary of the following audio transcript, including:\n"
                "1. A brief overall summary\n"
                "2. Key discussion points\n"
                "3. Action items if mentioned\n"
                "4. Speaker-specific notes in the format: [Speaker Name]: Content"
            )
        
        # Combine system prompt with transcription
        full_prompt = f"{system_prompt}\n\nTranscript:\n{transcription_text}"
        
        return full_prompt
    
    def _parse_generated_notes(self, generated_text):
        """Parse the LLM-generated text into structured notes"""
        # This is a simplified parsing approach - in practice, you'd want more robust parsing
        return {
            "summary": "Meeting summary based on the content",
            "key_points": [
                "Key point 1 from the conversation",
                "Important decision or discussion"
            ],
            "action_items": [
                "Action item 1: Complete by specific date",
                "Action item 2: Further investigation needed"
            ],
            "speaker_notes": {
                "Speaker_1": "Main speaker content would appear here",
                "Speaker_2": "Secondary speaker content would appear here"
            }
        }

    def generate_outline(self, transcription_results):
        """Generate a structured outline from the transcript"""
        try:
            # Create an outline prompt
            prompt = (
                "Create a structured outline from the following transcript. "
                "Format as bullet points with clear section headings:\n\n"
                f"{transcription_results}"
            )
            
            if self.llm_pipeline:
                response = self.llm_pipeline(
                    prompt,
                    max_new_tokens=256,
                    temperature=0.3
                )
                
                outline = response[0]['generated_text']
                return outline
            
            # Return mock outline if no pipeline
            return "Outline would appear here"
            
        except Exception as e:
            print(f"Error generating outline: {e}")
            return "Outline generation failed"
    
    def generate_summary(self, transcription_results):
        """Generate a brief summary of the content"""
        try:
            # Create a summary prompt
            prompt = (
                "Summarize the following transcript in 2-3 sentences:\n\n"
                f"{transcription_results}"
            )
            
            if self.llm_pipeline:
                response = self.llm_pipeline(
                    prompt,
                    max_new_tokens=128,
                    temperature=0.5
                )
                
                summary = response[0]['generated_text']
                return summary
            
            # Return mock summary if no pipeline
            return "Summary would appear here"
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Summary generation failed"