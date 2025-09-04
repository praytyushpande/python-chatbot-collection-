#!/usr/bin/env python3
"""
NLP-Powered Advanced Chatbot
A sophisticated chatbot using natural language processing libraries for better understanding.
"""

import re
import random
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Check for optional NLP libraries
try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.sentiment import SentimentIntensityAnalyzer
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

class NLPChatBot:
    def __init__(self):
        self.name = "NLP ChatBot"
        self.user_name = None
        self.conversation_history = []
        self.user_info = {}
        self.session_start = datetime.now()
        self.mood_history = []
        
        # Initialize NLP components if available
        if NLTK_AVAILABLE:
            try:
                # Download required NLTK data
                self._setup_nltk()
                self.lemmatizer = WordNetLemmatizer()
                self.sentiment_analyzer = SentimentIntensityAnalyzer()
                self.stop_words = set(stopwords.words('english'))
                self.nlp_enabled = True
            except Exception as e:
                print(f"Warning: NLTK setup failed: {e}")
                self.nlp_enabled = False
        else:
            self.nlp_enabled = False
        
        # Extended response patterns with sentiment-aware responses
        self.responses = {
            'greetings': {
                'positive': [
                    "Hello{name}! You seem to be in a great mood! How can I help you today?",
                    "Hi there{name}! I can sense your positive energy. What's making you happy?",
                    "Hey{name}! Your enthusiasm is contagious! What's on your mind?"
                ],
                'neutral': [
                    "Hello{name}! How can I help you today?",
                    "Hi there{name}! What's on your mind?",
                    "Hey{name}! Nice to see you!"
                ],
                'negative': [
                    "Hello{name}. I sense you might be having a tough time. I'm here to listen.",
                    "Hi{name}. How are you feeling? Sometimes it helps to talk.",
                    "Hey{name}. I'm here for you. What's troubling you?"
                ]
            },
            'how_are_you': {
                'positive': [
                    "I'm doing fantastic! It's wonderful to chat with someone so upbeat!",
                    "I'm great! Your positive attitude is really brightening my day!",
                    "I'm doing excellent! How has your day been treating you?"
                ],
                'neutral': [
                    "I'm doing well, thank you for asking! How are you?",
                    "I'm good! How about you? How's your day going?",
                    "I'm fine, thanks! What's been happening with you?"
                ],
                'negative': [
                    "I'm doing okay. More importantly, how are you holding up?",
                    "I'm alright. I'm sorry if you're going through a difficult time.",
                    "I'm here and ready to listen. How can I support you today?"
                ]
            },
            'compliments': [
                "Thank you so much{name}! That's very kind of you to say.",
                "That's really sweet{name}! You've made my day brighter.",
                "I appreciate that{name}! You're pretty awesome yourself!"
            ],
            'questions': [
                "That's a thoughtful question{name}! Let me think about that...",
                "Interesting question{name}! I'd love to explore that with you.",
                "Great question{name}! What's your take on it?"
            ],
            'emotions': {
                'joy': [
                    "That's wonderful{name}! I'm so happy to hear that!",
                    "How exciting{name}! I love your enthusiasm!",
                    "That's fantastic{name}! Your joy is infectious!"
                ],
                'sadness': [
                    "I'm sorry you're feeling this way{name}. It's okay to feel sad sometimes.",
                    "That sounds difficult{name}. Would you like to talk about it?",
                    "I understand{name}. Sometimes life can be challenging."
                ],
                'anger': [
                    "I can sense your frustration{name}. Take a deep breath.",
                    "That sounds really frustrating{name}. What's bothering you?",
                    "I understand you're upset{name}. Let's work through this together."
                ],
                'fear': [
                    "It's natural to feel scared sometimes{name}. You're not alone.",
                    "I understand your concerns{name}. What's making you anxious?",
                    "Fear can be overwhelming{name}. What can I do to help?"
                ]
            },
            'goodbye': [
                "Goodbye{name}! It's been wonderful chatting with you!",
                "Take care{name}! I've really enjoyed our conversation!",
                "Farewell{name}! Thanks for the great chat!"
            ],
            'default': [
                "That's interesting{name}! Tell me more about your thoughts on that.",
                "I see{name}. What's your perspective on this?",
                "Fascinating{name}! I'd love to hear more about your experience."
            ]
        }
        
        # Intent patterns with improved NLP
        self.intent_patterns = {
            'greeting': [r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b'],
            'how_are_you': [r'\b(how are you|how\'re you|how do you feel|what\'s up)\b'],
            'name_question': [r'\b(what\'s your name|your name|who are you|what are you called)\b'],
            'name_response': [r'\b(my name is|i\'m|call me|i am)\s+(\w+)'],
            'compliment': [r'\b(good|great|awesome|amazing|wonderful|fantastic|nice|excellent)\b.*\b(bot|chatbot|you)\b'],
            'question': [r'\?'],
            'goodbye': [r'\b(bye|goodbye|see you|farewell|exit|quit)\b'],
            'help': [r'\b(help|what can you do|commands|assist)\b'],
        }

    def _setup_nltk(self):
        """Setup NLTK by downloading required data."""
        required_data = ['punkt', 'stopwords', 'wordnet', 'vader_lexicon']
        for data in required_data:
            try:
                nltk.data.find(f'tokenizers/{data}' if data == 'punkt' else f'corpora/{data}' if data in ['stopwords', 'wordnet'] else f'vader_lexicon/{data}')
            except LookupError:
                print(f"Downloading NLTK data: {data}")
                nltk.download(data, quiet=True)

    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """Analyze the sentiment of the input text."""
        if not self.nlp_enabled:
            return 'neutral', 0.0
        
        try:
            # Use NLTK's VADER sentiment analyzer
            scores = self.sentiment_analyzer.polarity_scores(text)
            compound_score = scores['compound']
            
            if compound_score >= 0.05:
                return 'positive', compound_score
            elif compound_score <= -0.05:
                return 'negative', compound_score
            else:
                return 'neutral', compound_score
        except Exception:
            # Fallback to TextBlob if available
            if TEXTBLOB_AVAILABLE:
                try:
                    blob = TextBlob(text)
                    polarity = blob.sentiment.polarity
                    if polarity > 0.1:
                        return 'positive', polarity
                    elif polarity < -0.1:
                        return 'negative', polarity
                    else:
                        return 'neutral', polarity
                except Exception:
                    pass
            return 'neutral', 0.0

    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text using NLP techniques."""
        if not self.nlp_enabled:
            return text.split()
        
        try:
            tokens = word_tokenize(text.lower())
            # Remove stopwords and punctuation
            keywords = [self.lemmatizer.lemmatize(token) for token in tokens 
                       if token.isalnum() and token not in self.stop_words and len(token) > 2]
            return keywords[:5]  # Return top 5 keywords
        except Exception:
            return text.split()

    def detect_intent(self, text: str) -> str:
        """Detect user intent from input text."""
        text = text.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return intent
        
        return 'general'

    def detect_emotions(self, text: str) -> List[str]:
        """Detect emotional keywords in text."""
        emotion_keywords = {
            'joy': ['happy', 'excited', 'glad', 'thrilled', 'delighted', 'cheerful'],
            'sadness': ['sad', 'depressed', 'upset', 'disappointed', 'down', 'blue'],
            'anger': ['angry', 'mad', 'furious', 'annoyed', 'frustrated', 'irritated'],
            'fear': ['scared', 'afraid', 'worried', 'anxious', 'nervous', 'frightened']
        }
        
        text_lower = text.lower()
        detected_emotions = []
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_emotions.append(emotion)
        
        return detected_emotions

    def extract_name(self, text: str) -> str:
        """Extract user's name from their input."""
        pattern = re.search(r'\b(my name is|i\'m|call me|i am)\s+(\w+)', text, re.IGNORECASE)
        if pattern:
            return pattern.group(2).capitalize()
        return None

    def format_response(self, response: str, sentiment: str = 'neutral') -> str:
        """Format response with user's name and sentiment awareness."""
        name_part = f" {self.user_name}" if self.user_name else ""
        return response.format(name=name_part, user_name=self.user_name)

    def get_response(self, user_input: str) -> str:
        """Generate an intelligent response using NLP analysis."""
        user_input = user_input.strip()
        
        # Analyze sentiment
        sentiment, sentiment_score = self.analyze_sentiment(user_input)
        
        # Track mood
        self.mood_history.append({
            'timestamp': datetime.now().isoformat(),
            'sentiment': sentiment,
            'score': sentiment_score
        })
        
        # Extract name if provided
        if not self.user_name:
            name = self.extract_name(user_input)
            if name:
                self.user_name = name
                response = f"Nice to meet you, {name}! I'll remember that."
                return response
        
        # Detect intent
        intent = self.detect_intent(user_input)
        
        # Detect emotions
        emotions = self.detect_emotions(user_input)
        
        # Generate response based on intent and sentiment
        if intent == 'greeting' and 'greetings' in self.responses:
            responses = self.responses['greetings'].get(sentiment, self.responses['greetings']['neutral'])
            response = random.choice(responses)
        elif intent == 'how_are_you' and 'how_are_you' in self.responses:
            responses = self.responses['how_are_you'].get(sentiment, self.responses['how_are_you']['neutral'])
            response = random.choice(responses)
        elif intent == 'compliment':
            response = random.choice(self.responses['compliments'])
        elif intent == 'question':
            response = random.choice(self.responses['questions'])
        elif emotions:
            # Respond to detected emotions
            emotion = emotions[0]  # Use the first detected emotion
            if emotion in self.responses['emotions']:
                response = random.choice(self.responses['emotions'][emotion])
            else:
                response = random.choice(self.responses['default'])
        elif intent == 'goodbye':
            response = random.choice(self.responses['goodbye'])
        else:
            response = random.choice(self.responses['default'])
        
        return self.format_response(response, sentiment)

    def add_to_history(self, user_input: str, bot_response: str, sentiment: str, keywords: List[str]):
        """Add interaction to conversation history with NLP analysis."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation_history.append({
            'timestamp': timestamp,
            'user': user_input,
            'bot': bot_response,
            'sentiment': sentiment,
            'keywords': keywords,
            'intent': self.detect_intent(user_input)
        })

    def get_mood_analysis(self) -> Dict[str, Any]:
        """Get analysis of user's mood throughout the conversation."""
        if not self.mood_history:
            return {'average_sentiment': 'neutral', 'mood_trend': 'stable'}
        
        sentiments = [entry['score'] for entry in self.mood_history]
        avg_sentiment = sum(sentiments) / len(sentiments)
        
        if avg_sentiment >= 0.1:
            avg_mood = 'positive'
        elif avg_sentiment <= -0.1:
            avg_mood = 'negative'
        else:
            avg_mood = 'neutral'
        
        # Simple trend analysis
        if len(sentiments) >= 3:
            recent_trend = sum(sentiments[-3:]) / 3
            earlier_trend = sum(sentiments[:-3]) / max(1, len(sentiments) - 3)
            
            if recent_trend > earlier_trend + 0.1:
                trend = 'improving'
            elif recent_trend < earlier_trend - 0.1:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient_data'
        
        return {
            'average_sentiment': avg_mood,
            'mood_trend': trend,
            'sentiment_score': avg_sentiment
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive conversation statistics."""
        duration = datetime.now() - self.session_start
        mood_analysis = self.get_mood_analysis()
        
        return {
            'session_duration': str(duration).split('.')[0],
            'messages_exchanged': len(self.conversation_history),
            'user_name': self.user_name or "Unknown",
            'nlp_enabled': self.nlp_enabled,
            'average_mood': mood_analysis['average_sentiment'],
            'mood_trend': mood_analysis['mood_trend'],
            'total_keywords': len(set([kw for entry in self.conversation_history for kw in entry.get('keywords', [])]))
        }

    def save_conversation(self, filename: str = None):
        """Save detailed conversation with NLP analysis."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/Users/pratyushpandey/python-chatbot/nlp_conversation_{timestamp}.json"
        
        conversation_data = {
            'session_info': {
                'start_time': self.session_start.isoformat(),
                'end_time': datetime.now().isoformat(),
                'user_name': self.user_name,
                'nlp_enabled': self.nlp_enabled
            },
            'conversation': self.conversation_history,
            'mood_analysis': self.get_mood_analysis(),
            'stats': self.get_stats()
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            return filename
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return None

    def chat(self):
        """Main chat loop with NLP features."""
        nlp_status = "✅ Enabled" if self.nlp_enabled else "❌ Disabled (install nltk/textblob)"
        
        print(f"🤖 {self.name}: Hello! I'm an advanced NLP-powered chatbot.")
        print(f"   🧠 Natural Language Processing: {nlp_status}")
        print("   I can analyze sentiment, detect emotions, and understand context!")
        print("   Commands: 'quit', 'bye', 'stats', 'mood' for mood analysis")
        print("=" * 80)
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() == 'stats':
                    stats = self.get_stats()
                    print(f"📊 Advanced Stats:")
                    print(f"   Duration: {stats['session_duration']}")
                    print(f"   Messages: {stats['messages_exchanged']}")
                    print(f"   Your name: {stats['user_name']}")
                    print(f"   NLP Features: {'Active' if stats['nlp_enabled'] else 'Inactive'}")
                    print(f"   Average Mood: {stats['average_mood']}")
                    print(f"   Mood Trend: {stats['mood_trend']}")
                    print(f"   Unique Keywords: {stats['total_keywords']}")
                    continue
                
                if user_input.lower() == 'mood':
                    mood_analysis = self.get_mood_analysis()
                    print(f"🎭 Mood Analysis:")
                    print(f"   Overall Sentiment: {mood_analysis['average_sentiment']}")
                    print(f"   Mood Trend: {mood_analysis['mood_trend']}")
                    if 'sentiment_score' in mood_analysis:
                        print(f"   Sentiment Score: {mood_analysis['sentiment_score']:.3f}")
                    continue
                
                # Check for exit commands
                if re.search(r'\b(quit|exit|bye|goodbye)\b', user_input, re.IGNORECASE):
                    sentiment, _ = self.analyze_sentiment(user_input)
                    response = self.get_response(user_input)
                    print(f"🤖 {self.name}: {response}")
                    
                    # Save conversation
                    filename = self.save_conversation()
                    if filename:
                        print(f"💾 Conversation with NLP analysis saved to: {filename}")
                    
                    stats = self.get_stats()
                    print(f"📊 Final Stats: {stats['messages_exchanged']} messages, {stats['average_mood']} mood")
                    break
                
                # Analyze input and generate response
                sentiment, _ = self.analyze_sentiment(user_input)
                keywords = self.extract_keywords(user_input)
                response = self.get_response(user_input)
                
                # Display sentiment indicator if NLP is enabled
                if self.nlp_enabled:
                    mood_emoji = {'positive': '😊', 'negative': '😔', 'neutral': '😐'}
                    print(f"🤖 {self.name}: {response} {mood_emoji.get(sentiment, '')}")
                else:
                    print(f"🤖 {self.name}: {response}")
                
                # Add to conversation history
                self.add_to_history(user_input, response, sentiment, keywords)
                
            except KeyboardInterrupt:
                print(f"\n🤖 {self.name}: Goodbye! Thanks for the enlightening conversation!")
                filename = self.save_conversation()
                if filename:
                    print(f"💾 Conversation saved to: {filename}")
                break
            except Exception as e:
                print(f"🤖 {self.name}: Sorry, I encountered an error: {e}")

def main():
    """Main function to run the NLP chatbot."""
    if not NLTK_AVAILABLE and not TEXTBLOB_AVAILABLE:
        print("⚠️  Warning: Neither NLTK nor TextBlob is installed.")
        print("   The chatbot will run in basic mode without NLP features.")
        print("   Install with: pip install nltk textblob")
        print()
    
    chatbot = NLPChatBot()
    chatbot.chat()

if __name__ == "__main__":
    main()
