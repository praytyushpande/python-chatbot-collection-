#!/usr/bin/env python3
"""
Simple Rule-Based Chatbot
A basic chatbot that responds to user input using pattern matching.
"""

import re
import random

class SimpleChatBot:
    def __init__(self):
        self.name = "ChatBot"
        self.responses = {
            'greetings': [
                "Hello! How can I help you today?",
                "Hi there! What's on your mind?",
                "Hey! Nice to meet you!",
                "Hello! I'm here to chat with you."
            ],
            'how_are_you': [
                "I'm doing great, thank you for asking!",
                "I'm fantastic! How are you?",
                "I'm doing well. How about you?",
                "All good here! Thanks for asking."
            ],
            'name_questions': [
                f"My name is {self.name}. What's yours?",
                f"I'm {self.name}! Nice to meet you!",
                f"You can call me {self.name}. What should I call you?"
            ],
            'help': [
                "I can chat with you about various topics! Try asking me about myself, the weather, or just say hello!",
                "I'm here to have a conversation with you. Ask me anything!",
                "I can help with basic conversations. What would you like to talk about?"
            ],
            'goodbye': [
                "Goodbye! It was nice chatting with you!",
                "See you later! Have a great day!",
                "Bye! Come back anytime for another chat!",
                "Farewell! Take care!"
            ],
            'weather': [
                "I don't have access to real weather data, but I hope it's nice where you are!",
                "I can't check the weather, but I hope you're having a beautiful day!",
                "Weather-wise, I'm not connected to any weather services, but I hope it's pleasant!"
            ],
            'default': [
                "That's interesting! Tell me more.",
                "I see. What else would you like to talk about?",
                "Hmm, I'm not sure how to respond to that. Can you rephrase?",
                "That's a good point. What do you think about it?",
                "I'd love to hear more about that!",
                "Could you elaborate on that?"
            ]
        }
        
        # Compile regex patterns for better performance
        self.patterns = {
            'greetings': re.compile(r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b', re.IGNORECASE),
            'how_are_you': re.compile(r'\b(how are you|how\'re you|how do you feel|what\'s up)\b', re.IGNORECASE),
            'name_questions': re.compile(r'\b(what\'s your name|your name|who are you|what are you called)\b', re.IGNORECASE),
            'help': re.compile(r'\b(help|what can you do|commands|assist)\b', re.IGNORECASE),
            'goodbye': re.compile(r'\b(bye|goodbye|see you|farewell|exit|quit)\b', re.IGNORECASE),
            'weather': re.compile(r'\b(weather|temperature|sunny|rainy|cloudy|hot|cold)\b', re.IGNORECASE)
        }

    def get_response(self, user_input):
        """Generate a response based on user input using pattern matching."""
        user_input = user_input.strip()
        
        # Check each pattern
        for intent, pattern in self.patterns.items():
            if pattern.search(user_input):
                return random.choice(self.responses[intent])
        
        # Default response if no pattern matches
        return random.choice(self.responses['default'])

    def chat(self):
        """Main chat loop."""
        print(f"🤖 {self.name}: Hello! I'm a simple chatbot. Type 'quit' or 'bye' to exit.")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if re.search(r'\b(quit|exit|bye|goodbye)\b', user_input, re.IGNORECASE):
                    print(f"🤖 {self.name}: {random.choice(self.responses['goodbye'])}")
                    break
                
                # Get and display response
                response = self.get_response(user_input)
                print(f"🤖 {self.name}: {response}")
                
            except KeyboardInterrupt:
                print(f"\n🤖 {self.name}: Goodbye! Thanks for chatting!")
                break
            except Exception as e:
                print(f"🤖 {self.name}: Sorry, I encountered an error: {e}")

def main():
    """Main function to run the chatbot."""
    chatbot = SimpleChatBot()
    chatbot.chat()

if __name__ == "__main__":
    main()
