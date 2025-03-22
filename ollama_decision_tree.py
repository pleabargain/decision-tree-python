#!/usr/bin/env python3
"""
Ollama Decision Tree Generator - A simple terminal-based tool that uses Ollama to generate decision trees.
"""
import sys
import os
import json
import datetime
import argparse
import logging
import re
import ollama  # The Python client for Ollama

# Configure logging
logging.basicConfig(
    filename='ollama_decision_tree.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ollama_decision_tree')

# Default model
DEFAULT_MODEL = "llama3.2"

class OllamaClient:
    """Handles communication with the Ollama service."""
    
    def __init__(self, model=DEFAULT_MODEL):
        """
        Initialize the Ollama client.
        
        Args:
            model: The Ollama model to use
        """
        self.model = model
        self.conversation = []
        logger.info(f"Initialized OllamaClient with model: {model}")
        
    def send_message(self, message):
        """
        Send a message to Ollama and get the response.
        
        Args:
            message: The message to send
            
        Returns:
            The response from Ollama
        """
        try:
            # Add user message to conversation
            self.conversation.append({"role": "user", "content": message})
            logger.info(f"Sending message to Ollama model {self.model}")
            
            # Send to Ollama
            response = ollama.chat(
                model=self.model,
                messages=self.conversation
            )
            
            # Add assistant response to conversation
            assistant_message = response['message']
            self.conversation.append(assistant_message)
            
            logger.info("Received response from Ollama")
            return assistant_message['content']
            
        except Exception as e:
            error_msg = f"Error communicating with Ollama: {str(e)}"
            logger.error(error_msg)
            return f"Error: {str(e)}"
    
    def save_conversation(self, filename=None):
        """
        Save the current conversation to a file.
        
        Args:
            filename: Optional filename, otherwise auto-generated
            
        Returns:
            The filename the conversation was saved to
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if not filename:
            filename = f"ollama_decision_tree_chat_history_{timestamp}.json"
        
        data = {
            "metadata": {
                "timestamp": timestamp,
                "model": self.model,
                "version": "0.1.0"
            },
            "conversation": self.conversation
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved conversation to {filename}")
            return filename
        except Exception as e:
            error_msg = f"Error saving conversation: {str(e)}"
            logger.error(error_msg)
            return None
    
    def extract_decision_tree(self):
        """
        Extract a decision tree structure from the conversation.
        
        This is a simple extraction that looks for patterns in the LLM responses
        that might indicate questions and options.
        
        Returns:
            A dictionary representing the decision tree structure
        """
        tree = {
            "nodes": {},
            "current_id": 1,
            "result_id": 1
        }
        
        # Process each message in the conversation
        for i, msg in enumerate(self.conversation):
            if msg["role"] != "assistant":
                continue
                
            content = msg["content"]
            
            # Look for question patterns
            question_match = re.search(r'(?:QUESTION:|(?:\d+\.\s*)?([^?]+\?))', content)
            if question_match:
                question_text = question_match.group(1) if question_match.group(1) else question_match.group(0)
                question_text = question_text.strip()
                
                # Create a question node
                node_id = f"Q{tree['current_id']}"
                tree["nodes"][node_id] = {
                    "text": question_text,
                    "is_result": False,
                    "answers": []
                }
                
                # Look for options/answers
                options = re.findall(r'(?:OPTION\s*\d+:|(?:\d+\.\s*))([^.?!]+)[.?!]?', content)
                
                for option in options:
                    option_text = option.strip()
                    
                    # For simplicity, create a result node for each option
                    result_id = f"R{tree['result_id']}"
                    tree["nodes"][result_id] = {
                        "text": f"Result for: {option_text}",
                        "is_result": True,
                        "answers": []
                    }
                    
                    # Add the option to the question node
                    tree["nodes"][node_id]["answers"].append({
                        "text": option_text,
                        "next_node_id": result_id
                    })
                    
                    tree["result_id"] += 1
                
                tree["current_id"] += 1
        
        return tree
    
    def save_decision_tree(self, tree=None, filename=None):
        """
        Save the extracted decision tree to a file in the format compatible with decision_tree.py.
        
        Args:
            tree: The decision tree structure (if None, will be extracted)
            filename: Optional filename, otherwise auto-generated
            
        Returns:
            The filename the decision tree was saved to
        """
        if tree is None:
            tree = self.extract_decision_tree()
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if not filename:
            filename = f"ollama_decision_tree_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Write each node
                for node_id, node in tree["nodes"].items():
                    # Write the node text
                    f.write(f"{node_id}: {node['text']}\n")
                    
                    # Write the answers if not a result node
                    if not node["is_result"]:
                        for answer in node["answers"]:
                            f.write(f"A: {answer['text']} -> {answer['next_node_id']}\n")
                    
                    # Add a blank line between nodes
                    f.write("\n")
            
            logger.info(f"Saved decision tree to {filename}")
            return filename
        except Exception as e:
            error_msg = f"Error saving decision tree: {str(e)}"
            logger.error(error_msg)
            return None


def main():
    """Main function to run the Ollama Decision Tree Generator."""
    parser = argparse.ArgumentParser(description="Ollama Decision Tree Generator")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--save", action="store_true", help="Save conversation on exit")
    parser.add_argument("--export-tree", action="store_true", help="Export decision tree on exit")
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("OLLAMA DECISION TREE GENERATOR".center(60))
    print("=" * 60)
    print(f"\nUsing model: {args.model}")
    print("\nThis tool will help you create decision trees using Ollama.")
    print("Type 'exit' to quit, 'save' to save the conversation, 'export' to export as decision tree, or 'help' for more commands.")
    print("=" * 60)
    
    # Initialize Ollama client
    try:
        client = OllamaClient(model=args.model)
    except Exception as e:
        print(f"Error initializing Ollama client: {str(e)}")
        print("Make sure Ollama is installed and running.")
        print("You can install Ollama from: https://ollama.ai/")
        sys.exit(1)
    
    # Initial prompt to guide Ollama
    initial_prompt = """
    You are a decision tree creation assistant. Help me create a decision tree by asking relevant questions and providing options.
    For each step, present a clear question and 2-4 possible answers.
    Let's start by asking what topic or problem the decision tree should address.
    """
    
    # Send initial prompt
    print("\nInitializing conversation with Ollama...")
    response = client.send_message(initial_prompt)
    print("\nAssistant:", response)
    
    # Main conversation loop
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            if args.save:
                filename = client.save_conversation()
                if filename:
                    print(f"\nConversation saved to: {filename}")
            
            if args.export_tree:
                filename = client.save_decision_tree()
                if filename:
                    print(f"\nDecision tree exported to: {filename}")
                    print(f"You can use this file with decision_tree.py: python decision_tree.py {filename}")
            break
        
        elif user_input.lower() == 'save':
            filename = client.save_conversation()
            if filename:
                print(f"\nConversation saved to: {filename}")
            else:
                print("\nError saving conversation.")
            continue
        
        elif user_input.lower() == 'export':
            filename = client.save_decision_tree()
            if filename:
                print(f"\nDecision tree exported to: {filename}")
                print(f"You can use this file with decision_tree.py: python decision_tree.py {filename}")
            else:
                print("\nError exporting decision tree.")
            continue
            
        elif user_input.lower() == 'help':
            print("\nAvailable commands:")
            print("  exit, quit - Exit the program")
            print("  save - Save the current conversation")
            print("  export - Export as decision tree file")
            print("  help - Show this help message")
            continue
            
        response = client.send_message(user_input)
        print("\nAssistant:", response)
    
    print("\nThank you for using the Ollama Decision Tree Generator!")


if __name__ == "__main__":
    main()
