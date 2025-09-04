#!/usr/bin/env python3
"""
Chatbot Launcher
Easy way to run different versions of the chatbot.
"""

import sys
import os

def print_menu():
    """Display the chatbot selection menu."""
    print("🤖 Python Chatbot Collection")
    print("=" * 40)
    print("Choose a chatbot to run:")
    print()
    print("1. Simple Chatbot")
    print("   - Basic rule-based responses")
    print("   - Pattern matching")
    print("   - No dependencies required")
    print()
    print("2. Enhanced Chatbot")
    print("   - Conversation memory")
    print("   - User recognition")
    print("   - Session statistics")
    print("   - Conversation saving")
    print()
    print("3. NLP Chatbot")
    print("   - Sentiment analysis")
    print("   - Emotion detection")
    print("   - Intent recognition")
    print("   - Advanced NLP features")
    print("   - Requires: nltk, textblob")
    print()
    print("0. Exit")
    print("=" * 40)

def run_chatbot(choice):
    """Run the selected chatbot."""
    chatbot_files = {
        '1': 'simple_chatbot.py',
        '2': 'enhanced_chatbot.py', 
        '3': 'nlp_chatbot.py'
    }
    
    if choice in chatbot_files:
        filename = chatbot_files[choice]
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        if os.path.exists(filepath):
            print(f"\n🚀 Starting {filename}...")
            print("-" * 40)
            
            # Import and run the selected chatbot
            try:
                if choice == '1':
                    from simple_chatbot import main
                elif choice == '2':
                    from enhanced_chatbot import main
                elif choice == '3':
                    from nlp_chatbot import main
                
                main()
            except ImportError as e:
                print(f"❌ Error importing {filename}: {e}")
                if choice == '3':
                    print("💡 Tip: Install NLP dependencies with: pip install nltk textblob")
            except Exception as e:
                print(f"❌ Error running {filename}: {e}")
        else:
            print(f"❌ File {filename} not found!")
    else:
        print("❌ Invalid choice!")

def main():
    """Main launcher function."""
    try:
        while True:
            print_menu()
            choice = input("👤 Enter your choice (0-3): ").strip()
            
            if choice == '0':
                print("👋 Goodbye! Thanks for using the chatbot collection!")
                break
            elif choice in ['1', '2', '3']:
                run_chatbot(choice)
                
                # Ask if user wants to try another chatbot
                print("\n" + "=" * 40)
                while True:
                    again = input("🔄 Would you like to try another chatbot? (y/n): ").strip().lower()
                    if again in ['y', 'yes']:
                        print()
                        break
                    elif again in ['n', 'no']:
                        print("👋 Thanks for using the chatbot collection!")
                        return
                    else:
                        print("Please enter 'y' for yes or 'n' for no.")
            else:
                print("❌ Please enter a number between 0 and 3.")
                print()
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Thanks for using the chatbot collection!")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
