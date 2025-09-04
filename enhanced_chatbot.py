#!/usr/bin/env python3
"""
Enhanced Chatbot with Memory
A more sophisticated chatbot that remembers conversation context and user information.
"""

import re
import random
import json
from datetime import datetime
from typing import Dict, List, Any

class EnhancedChatBot:
    def __init__(self):
        self.name = "Enhanced ChatBot"
        self.user_name = None
        self.conversation_history = []
        self.user_info = {}
        self.session_start = datetime.now()
        
        self.responses = {
            'greetings': [
                "Hello{name}! How can I help you today?",
                "Hi there{name}! What's on your mind?",
                "Hey{name}! Nice to see you!",
                "Hello{name}! I'm here to chat with you."
            ],
            'how_are_you': [
                "I'm doing great, thank you for asking! How are you feeling today?",
                "I'm fantastic! How has your day been so far?",
                "I'm doing well. How about you? Anything interesting happening?",
                "All good here! Thanks for asking. What's new with you?"
            ],
            'name_questions': [
                f"My name is {self.name}. What's yours?",
                f"I'm {self.name}! What should I call you?",
                f"You can call me {self.name}. I'd love to know your name!"
            ],
            'name_provided': [
                "Nice to meet you, {user_name}! I'll remember that.",
                "Great to meet you, {user_name}! How are you doing today?",
                "Hello {user_name}! That's a lovely name. I'm glad to know you!"
            ],
            'help': [
                "I can chat with you about various topics! I also remember our conversation, so feel free to reference things we've talked about before.",
                "I'm here to have a conversation with you. I can remember what we discuss, so our chat can be more natural!",
                "I can help with conversations and I'll remember what we talk about. What interests you?"
            ],
            'goodbye': [
                "Goodbye{name}! It was wonderful chatting with you!",
                "See you later{name}! Have a great day!",
                "Bye{name}! Thanks for the great conversation!",
                "Farewell{name}! I've enjoyed our chat!"
            ],
            'weather': [
                "I don't have access to real weather data, but I hope it's nice where you are! How's the weather on your end?",
                "I can't check the weather, but I hope you're having a beautiful day! What's it like outside?",
                "Weather-wise, I'm not connected to any weather services, but I'm curious - how's the weather where you are?"
            ],
            'memory_reference': [
                "Yes, I remember we talked about that! {context}",
                "Right, you mentioned that earlier. {context}",
                "I recall our conversation about that. {context}"
            ],
            'default': [
                "That's interesting{name}! Tell me more about that.",
                "I see{name}. What else would you like to talk about?",
                "Hmm{name}, I'm not sure how to respond to that. Can you elaborate?",
                "That's a good point{name}. What's your take on it?",
                "I'd love to hear more about that{name}!",
                "Could you tell me more about that{name}?"
            ]
        }
        
        # Compile regex patterns
        self.patterns = {
            'greetings': re.compile(r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b', re.IGNORECASE),
            'how_are_you': re.compile(r'\b(how are you|how\'re you|how do you feel|what\'s up)\b', re.IGNORECASE),
            'name_questions': re.compile(r'\b(what\'s your name|your name|who are you|what are you called)\b', re.IGNORECASE),
            'name_response': re.compile(r'\b(my name is|i\'m|call me|i am)\s+(\w+)', re.IGNORECASE),
            'help': re.compile(r'\b(help|what can you do|commands|assist)\b', re.IGNORECASE),
            'goodbye': re.compile(r'\b(bye|goodbye|see you|farewell|exit|quit)\b', re.IGNORECASE),
            'weather': re.compile(r'\b(weather|temperature|sunny|rainy|cloudy|hot|cold)\b', re.IGNORECASE),
            'remember': re.compile(r'\b(remember|recall|you said|we talked|earlier|before)\b', re.IGNORECASE)
        }

    def extract_name(self, user_input: str) -> str:
        """Extract user's name from their input."""
        match = self.patterns['name_response'].search(user_input)
        if match:
            return match.group(2).capitalize()
        return None

    def format_response(self, response: str) -> str:
        """Format response with user's name if available."""
        name_part = f" {self.user_name}" if self.user_name else ""
        return response.format(name=name_part, user_name=self.user_name)

    def add_to_history(self, user_input: str, bot_response: str):
        """Add interaction to conversation history."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation_history.append({
            'timestamp': timestamp,
            'user': user_input,
            'bot': bot_response
        })

    def search_context(self, query: str) -> str:
        """Search conversation history for relevant context."""
        query_words = query.lower().split()
        relevant_context = []
        
        for entry in self.conversation_history[-10:]:  # Look at last 10 interactions
            user_text = entry['user'].lower()
            if any(word in user_text for word in query_words):
                relevant_context.append(f"You said: '{entry['user']}'")
        
        if relevant_context:
            return " ".join(relevant_context[:2])  # Return up to 2 most relevant
        return "something we discussed earlier"

    def get_response(self, user_input: str) -> str:
        """Generate a response based on user input and conversation context."""
        user_input = user_input.strip()
        
        # Check if user is providing their name
        if not self.user_name:
            name = self.extract_name(user_input)
            if name:
                self.user_name = name
                self.user_info['name'] = name
                response = random.choice(self.responses['name_provided'])
                return self.format_response(response)
        
        # Check for memory references
        if self.patterns['remember'].search(user_input) and self.conversation_history:
            context = self.search_context(user_input)
            response = random.choice(self.responses['memory_reference'])
            return self.format_response(response.format(context=context))
        
        # Check other patterns
        for intent, pattern in self.patterns.items():
            if intent in ['name_response', 'remember']:  # Skip already handled patterns
                continue
            if pattern.search(user_input):
                response = random.choice(self.responses[intent])
                return self.format_response(response)
        
        # Default response
        response = random.choice(self.responses['default'])
        return self.format_response(response)

    def get_stats(self) -> Dict[str, Any]:
        """Get conversation statistics."""
        duration = datetime.now() - self.session_start
        return {
            'session_duration': str(duration).split('.')[0],  # Remove microseconds
            'messages_exchanged': len(self.conversation_history),
            'user_name': self.user_name or "Unknown"
        }

    def save_conversation(self, filename: str = None):
        """Save conversation history to a JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/Users/pratyushpandey/python-chatbot/conversation_{timestamp}.json"
        
        conversation_data = {
            'session_info': {
                'start_time': self.session_start.isoformat(),
                'end_time': datetime.now().isoformat(),
                'user_name': self.user_name
            },
            'conversation': self.conversation_history,
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
        """Main chat loop with enhanced features."""
        print(f"🤖 {self.name}: Hello! I'm an enhanced chatbot with memory.")
        print("   I can remember our conversation and get to know you better!")
        print("   Type 'quit', 'bye', or 'stats' for statistics, or just start chatting!")
        print("=" * 70)
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() == 'stats':
                    stats = self.get_stats()
                    print(f"📊 Session Stats:")
                    print(f"   Duration: {stats['session_duration']}")
                    print(f"   Messages: {stats['messages_exchanged']}")
                    print(f"   Your name: {stats['user_name']}")
                    continue
                
                # Check for exit commands
                if re.search(r'\b(quit|exit|bye|goodbye)\b', user_input, re.IGNORECASE):
                    response = random.choice(self.responses['goodbye'])
                    response = self.format_response(response)
                    print(f"🤖 {self.name}: {response}")
                    
                    # Save conversation
                    filename = self.save_conversation()
                    if filename:
                        print(f"💾 Conversation saved to: {filename}")
                    
                    stats = self.get_stats()
                    print(f"📊 Final Stats: {stats['messages_exchanged']} messages in {stats['session_duration']}")
                    break
                
                # Get and display response
                response = self.get_response(user_input)
                print(f"🤖 {self.name}: {response}")
                
                # Add to conversation history
                self.add_to_history(user_input, response)
                
            except KeyboardInterrupt:
                print(f"\n🤖 {self.name}: Goodbye! Thanks for chatting!")
                filename = self.save_conversation()
                if filename:
                    print(f"💾 Conversation saved to: {filename}")
                break
            except Exception as e:
                print(f"🤖 {self.name}: Sorry, I encountered an error: {e}")

def main():
    """Main function to run the enhanced chatbot."""
    chatbot = EnhancedChatBot()
    chatbot.chat()

if __name__ == "__main__":
    main()
