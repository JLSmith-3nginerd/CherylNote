# src/content_classifier.py - Classify content type

import re

class ContentClassifier:
    def __init__(self):
        # Define patterns for different content types
        self.patterns = {
            'meeting': [
                r'meeting', r'discuss', r'agenda', r'responsibility',
                r'action item', r'to do list'
            ],
            'lecture': [
                r'lecture', r'subject', r'chapter', r'lesson',
                r'topic', r'discussion'
            ],
            'interview': [
                r'interview', r'question', r'answer', r'expert',
                r'specialist'
            ],
            'podcast': [
                r'podcast', r'talk show', r'discussion', 
                r'show notes'
            ],
            'speech': [
                r'speech', r'presentation', r'remarks',
                r'main points'
            ]
        }
    
    def classify_content(self, transcription_results):
        """Classify content type based on transcription"""
        # Extract text from all segments
        full_text = " ".join([segment['text'] for segment in transcription_results])
        
        # Count matches for each content type
        scores = {}
        
        for content_type, keywords in self.patterns.items():
            score = 0
            for keyword in keywords:
                # Use regex for case-insensitive matching with word boundaries
                pattern = re.compile(r'\b' + keyword + r'\b', re.IGNORECASE)
                matches = pattern.findall(full_text)
                score += len(matches)
            
            scores[content_type] = score
        
        # Return the content type with highest score
        if max(scores.values()) == 0:
            return "general"
        
        # Fix for the LSP error by ensuring we're using a valid function
        max_score = 0
        best_type = "general"
        for content_type, score in scores.items():
            if score > max_score:
                max_score = score
                best_type = content_type
                
        return best_type

# Create a simplified version that works with the current architecture
class ContentClassifierSimple:
    def __init__(self):
        # For demonstration purposes, we'll use a simple rule-based classifier
        pass
    
    def classify_content(self, transcription_results):
        """Simple content classification based on keywords in the first few segments"""
        # Get text from first 3 segments for initial classification
        sample_text = " ".join([segment['text'][:50] for segment in transcription_results[:3]])
        sample_text_lower = sample_text.lower()
        
        # Check for common meeting keywords
        if any(word in sample_text_lower for word in ['meeting', 'agenda', 'discuss']):
            return "meeting"
        elif any(word in sample_text_lower for word in ['lecture', 'subject', 'chapter']):
            return "lecture"
        elif any(word in sample_text_lower for word in ['interview', 'question']):
            return "interview"
        else:
            # Default to general classification
            return "general"