#!/usr/bin/env python3
"""
Decision Tree Navigator - A simple terminal-based decision tree implementation.

This script reads a text file containing a decision tree structure and guides
the user through a series of questions, displaying the decision path as a tree.
"""
import sys
import os
import re
import argparse
import datetime
from typing import Dict, List, Optional, Tuple, Union

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Node:
    """Represents a node (question or result) in the decision tree."""
    
    def __init__(self, node_id: str, text: str, is_result: bool = False):
        """
        Initialize a node in the decision tree.
        
        Args:
            node_id: Unique identifier for the node
            text: Text content of the node (question or result)
            is_result: Whether this node is a result node
        """
        self.id = node_id
        self.text = text
        self.is_result = is_result
        self.answers = []  # List of (answer_text, next_node_id) tuples
    
    def add_answer(self, text: str, next_node_id: str):
        """
        Add an answer option to this node.
        
        Args:
            text: The answer text
            next_node_id: ID of the node to go to if this answer is selected
        """
        self.answers.append((text, next_node_id))
    
    def __str__(self) -> str:
        """Return a string representation of the node."""
        if self.is_result:
            return f"RESULT: {self.text}"
        return f"{self.id}: {self.text}"


class DecisionTree:
    """Manages the decision tree structure and navigation."""
    
    def __init__(self):
        """Initialize an empty decision tree."""
        self.nodes: Dict[str, Node] = {}
        self.start_node_id: Optional[str] = None
        self.current_path: List[Tuple[Node, Optional[str]]] = []  # List of (node, answer) tuples
    
    def add_node(self, node: Node):
        """
        Add a node to the decision tree.
        
        Args:
            node: The node to add
        """
        self.nodes[node.id] = node
        # Set the first non-result node as the start node if not already set
        if self.start_node_id is None and not node.is_result:
            self.start_node_id = node.id
    
    def navigate_to_start(self):
        """Reset navigation to the start of the tree."""
        if self.start_node_id is None:
            raise ValueError("Decision tree has no start node")
        self.current_path = [(self.nodes[self.start_node_id], None)]
    
    def get_current_node(self) -> Node:
        """Get the current node in the navigation."""
        if not self.current_path:
            self.navigate_to_start()
        return self.current_path[-1][0]
    
    def select_answer(self, answer_index: int) -> bool:
        """
        Select an answer and move to the next node.
        
        Args:
            answer_index: Index of the answer to select (0-based)
        
        Returns:
            True if navigation continues, False if a result node is reached
        """
        current_node = self.get_current_node()
        
        if current_node.is_result:
            return False
        
        if answer_index < 0 or answer_index >= len(current_node.answers):
            raise ValueError(f"Invalid answer index: {answer_index}")
        
        answer_text, next_node_id = current_node.answers[answer_index]
        next_node = self.nodes.get(next_node_id)
        
        if next_node is None:
            raise ValueError(f"Node not found: {next_node_id}")
        
        self.current_path.append((next_node, answer_text))
        return not next_node.is_result
    
    def go_back(self) -> bool:
        """
        Go back to the previous question.
        
        Returns:
            True if successful, False if already at the start
        """
        if len(self.current_path) <= 1:
            return False
        
        self.current_path.pop()
        return True
    
    def get_path_display(self) -> str:
        """
        Get a string representation of the current decision path as a tree.
        
        Returns:
            ASCII tree representation of the path
        """
        if not self.current_path:
            return "Empty path"
        
        lines = []
        for i, (node, answer) in enumerate(self.current_path):
            prefix = "    " * i
            if i > 0:
                lines.append(f"{prefix[:-4]}└── {Colors.YELLOW}{answer}{Colors.ENDC}")
            
            if i == len(self.current_path) - 1 and not node.is_result:
                lines.append(f"{prefix}└── {Colors.CYAN}{node.text}{Colors.ENDC}")
                lines.append(f"{prefix}    └── {Colors.BOLD}[Awaiting your answer]{Colors.ENDC}")
            else:
                if node.is_result:
                    lines.append(f"{prefix}└── {Colors.GREEN}{node.text}{Colors.ENDC}")
                else:
                    lines.append(f"{prefix}└── {Colors.CYAN}{node.text}{Colors.ENDC}")
        
        return "\n".join(lines)


def parse_file(file_path: str) -> DecisionTree:
    """
    Parse the decision tree file and build the tree structure.
    
    Args:
        file_path: Path to the decision tree file
    
    Returns:
        Populated DecisionTree object
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format is invalid
    """
    tree = DecisionTree()
    current_node = None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                
                # Parse question line
                question_match = re.match(r'^([QR]\d+[a-z]*):\s+(.+)$', line)
                if question_match:
                    node_id, text = question_match.groups()
                    is_result = node_id.startswith('R')
                    current_node = Node(node_id, text, is_result)
                    tree.add_node(current_node)
                    continue
                
                # Parse answer line
                answer_match = re.match(r'^A:\s+(.+?)\s+->\s+([QR]\d+[a-z]*)$', line)
                if answer_match and current_node and not current_node.is_result:
                    answer_text, next_node_id = answer_match.groups()
                    current_node.add_answer(answer_text, next_node_id)
                    continue
                
                # If we get here, the line format is invalid
                raise ValueError(f"Invalid line format at line {line_num}: {line}")
    
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        raise
    
    if not tree.nodes:
        raise ValueError("No valid nodes found in the file")
    
    return tree


def display_options(node: Node):
    """
    Display the answer options for a node.
    
    Args:
        node: The node to display options for
    """
    if node.is_result:
        print(f"\n{Colors.BOLD}{Colors.GREEN}FINAL RESULT:{Colors.ENDC}")
        print(f"{Colors.GREEN}{node.text}{Colors.ENDC}")
        return
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}QUESTION:{Colors.ENDC} {Colors.CYAN}{node.text}{Colors.ENDC}")
    print(f"\n{Colors.BOLD}Options:{Colors.ENDC}")
    for i, (answer, _) in enumerate(node.answers, 1):
        print(f"{Colors.YELLOW}{i}.{Colors.ENDC} {answer}")


def get_user_input(options_count: int) -> Union[int, str]:
    """
    Get and validate user input for the given options.
    
    Args:
        options_count: Number of available options
    
    Returns:
        Option index (0-based) or command string
    """
    while True:
        try:
            prompt = f"\n{Colors.BOLD}Enter your choice ({Colors.YELLOW}1-{options_count}{Colors.ENDC}{Colors.BOLD}) or type '{Colors.CYAN}back{Colors.ENDC}{Colors.BOLD}', '{Colors.CYAN}restart{Colors.ENDC}{Colors.BOLD}', '{Colors.CYAN}tree{Colors.ENDC}{Colors.BOLD}', '{Colors.CYAN}exit{Colors.ENDC}{Colors.BOLD}':{Colors.ENDC} "
            user_input = input(prompt).strip().lower()
            
            if user_input in ['back', 'restart', 'tree', 'exit', 'help']:
                return user_input
            
            choice = int(user_input)
            if 1 <= choice <= options_count:
                return choice - 1  # Convert to 0-based index
            
            print(f"{Colors.RED}Please enter a number between 1 and {options_count}{Colors.ENDC}")
        
        except ValueError:
            print(f"{Colors.RED}Please enter a valid number or command{Colors.ENDC}")


import datetime
import os

def generate_mermaid_diagram(tree: DecisionTree) -> str:
    """
    Generate a Mermaid flowchart diagram from the decision path.
    
    Args:
        tree: The decision tree with the current path
    
    Returns:
        Mermaid diagram code as a string
    """
    if not tree.current_path:
        return "graph TD\n    A[No decision path]"
    
    # Start with the graph definition
    mermaid_code = ["graph TD"]
    
    # Define node IDs and labels
    node_definitions = []
    connections = []
    current_nodes = []
    result_nodes = []
    
    # Create a sanitized ID for each node
    def sanitize_id(text):
        return "".join(c if c.isalnum() else "_" for c in text)
    
    # Process each node in the path
    prev_node_id = None
    for i, (node, answer) in enumerate(tree.current_path):
        # Create a unique ID for this node
        node_id = f"node_{sanitize_id(node.id)}"
        
        # Add to current nodes list
        current_nodes.append(node_id)
        
        # If it's a result node, add to result nodes list
        if node.is_result:
            result_nodes.append(node_id)
        
        # Define the node with its text
        node_text = node.text.replace('"', "'")
        node_definitions.append(f'    {node_id}["{node_text}"]')
        
        # If there's a previous node and an answer, create a connection
        if prev_node_id and answer:
            answer_text = answer.replace('"', "'")
            connections.append(f'    {prev_node_id} -->|"{answer_text}"| {node_id}')
        
        prev_node_id = node_id
    
    # Add node definitions and connections to the diagram
    mermaid_code.extend(node_definitions)
    mermaid_code.extend(connections)
    
    # Add styling
    mermaid_code.append("")
    mermaid_code.append("    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;")
    mermaid_code.append("    classDef current fill:#d4f4ff,stroke:#0077b6,stroke-width:2px;")
    mermaid_code.append("    classDef result fill:#d8f3dc,stroke:#2d6a4f,stroke-width:2px;")
    
    # Apply styles
    if current_nodes:
        mermaid_code.append(f"    class {','.join(current_nodes)} current;")
    if result_nodes:
        mermaid_code.append(f"    class {','.join(result_nodes)} result;")
    
    return "\n".join(mermaid_code)

def save_path_to_file(tree: DecisionTree, input_file: str = None, filename: str = None) -> str:
    """
    Save the current decision path to a Markdown file with a timestamp.
    
    Args:
        tree: The decision tree with the current path
        input_file: The input file path used to generate the decision tree
        filename: Optional filename to save to
    
    Returns:
        The filename the path was saved to
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Extract base name from input file if provided
    if input_file:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        if filename is None:
            filename = f"{base_name}_decision_path_{timestamp}.md"
    else:
        if filename is None:
            filename = f"decision_path_{timestamp}.md"
    
    # Generate Mermaid diagram
    mermaid_diagram = generate_mermaid_diagram(tree)
    
    # Remove ANSI color codes for file output
    def strip_ansi_codes(text):
        return text.replace(Colors.YELLOW, '').replace(Colors.CYAN, '').replace(Colors.GREEN, '')\
                  .replace(Colors.BLUE, '').replace(Colors.RED, '').replace(Colors.HEADER, '')\
                  .replace(Colors.BOLD, '').replace(Colors.UNDERLINE, '').replace(Colors.ENDC, '')
    
    clean_path_display = strip_ansi_codes(tree.get_path_display())
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("# Decision Path Analysis\n\n")
        if input_file:
            file.write(f"Generated from: `{input_file}`  \n")
        file.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        file.write("## Decision Path Tree\n\n")
        file.write("```\n")
        file.write(clean_path_display)
        file.write("\n```\n\n")
        
        file.write("## Visual Diagram\n\n")
        file.write("```mermaid\n")
        file.write(mermaid_diagram)
        file.write("\n```\n")
    
    print(f"\nDecision path saved to: {filename}")
    return filename


def display_help():
    """Display help information for the user."""
    print(f"\n{Colors.BOLD}{Colors.HEADER}Available commands:{Colors.ENDC}")
    print(f"- Enter a {Colors.YELLOW}number{Colors.ENDC} to select an option")
    print(f"- '{Colors.CYAN}back{Colors.ENDC}' - Return to the previous question")
    print(f"- '{Colors.CYAN}restart{Colors.ENDC}' - Start the decision tree from the beginning")
    print(f"- '{Colors.CYAN}tree{Colors.ENDC}' - Display the current decision path as a tree")
    print(f"- '{Colors.CYAN}exit{Colors.ENDC}' - Quit the application")
    print(f"- '{Colors.CYAN}help{Colors.ENDC}' - Show this help message")


def main():
    """Main function to run the decision tree navigator."""
    parser = argparse.ArgumentParser(description="Decision Tree Navigator")
    parser.add_argument("file", help="Path to the decision tree file")
    parser.add_argument("--version", action="version", version="Decision Tree Navigator v0.1.0")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    
    try:
        tree = parse_file(args.file)
    except (FileNotFoundError, ValueError) as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.ENDC}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print(f"{Colors.BOLD}{Colors.HEADER}{'DECISION TREE NAVIGATOR'.center(60)}{Colors.ENDC}")
    print("=" * 60)
    print(f"\n{Colors.BOLD}Loaded:{Colors.ENDC} {Colors.CYAN}{args.file}{Colors.ENDC}")
    print(f"{Colors.BOLD}Tree contains:{Colors.ENDC} {Colors.YELLOW}{sum(1 for node in tree.nodes.values() if not node.is_result)}{Colors.ENDC} questions and "
          f"{Colors.YELLOW}{sum(1 for node in tree.nodes.values() if node.is_result)}{Colors.ENDC} possible outcomes")
    print(f"\n{Colors.BOLD}This interactive tool will guide you through a series of questions.{Colors.ENDC}")
    print(f"Your answers will determine the path through the decision tree.")
    print(f"\n{Colors.BOLD}At any point, you can:{Colors.ENDC}")
    print(f"- Type '{Colors.CYAN}back{Colors.ENDC}' to return to the previous question")
    print(f"- Type '{Colors.CYAN}restart{Colors.ENDC}' to start over")
    print(f"- Type '{Colors.CYAN}tree{Colors.ENDC}' to see your current path")
    print(f"- Type '{Colors.CYAN}exit{Colors.ENDC}' to quit")
    print(f"- Type '{Colors.CYAN}help{Colors.ENDC}' for more commands")
    print(f"\n{Colors.BOLD}{Colors.GREEN}Let's begin!{Colors.ENDC}")
    print("=" * 60)
    
    tree.navigate_to_start()
    
    while True:
        current_node = tree.get_current_node()
        display_options(current_node)
        
        if current_node.is_result:
            print(f"\n{Colors.BOLD}{Colors.BLUE}Your complete decision path:{Colors.ENDC}")
            print(tree.get_path_display())
            
            choice = input(f"\n{Colors.BOLD}What would you like to do next? ({Colors.CYAN}save{Colors.ENDC}{Colors.BOLD}/{Colors.CYAN}restart{Colors.ENDC}{Colors.BOLD}/{Colors.CYAN}exit{Colors.ENDC}{Colors.BOLD}):{Colors.ENDC} ").strip().lower()
            if choice == 'restart':
                tree.navigate_to_start()
                continue
            elif choice == 'save':
                save_path_to_file(tree, args.file)
                choice = input(f"\n{Colors.BOLD}What would you like to do next? ({Colors.CYAN}restart{Colors.ENDC}{Colors.BOLD}/{Colors.CYAN}exit{Colors.ENDC}{Colors.BOLD}):{Colors.ENDC} ").strip().lower()
                if choice == 'restart':
                    tree.navigate_to_start()
                    continue
                else:
                    break
            else:
                break
        
        user_input = get_user_input(len(current_node.answers))
        
        if isinstance(user_input, int):
            tree.select_answer(user_input)
        elif user_input == 'back':
            if not tree.go_back():
                print("Already at the first question")
        elif user_input == 'restart':
            tree.navigate_to_start()
        elif user_input == 'tree':
            print("\nYour current decision path:")
            print(tree.get_path_display())
        elif user_input == 'help':
            display_help()
        elif user_input == 'exit':
            break
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}Thank you for using the Decision Tree Navigator!{Colors.ENDC}")


if __name__ == "__main__":
    main()
