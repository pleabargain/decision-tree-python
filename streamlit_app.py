#!/usr/bin/env python3
"""
Decision Tree Navigator - A Streamlit-based decision tree implementation.

This script reads a text file containing a decision tree structure and guides
the user through a series of questions, displaying the decision path as a tree.
"""
import os
import re
import datetime
import glob
import logging
import traceback
import streamlit as st
from streamlit.runtime.scriptrunner.exceptions import RerunException
from typing import Dict, List, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    filename='streamlit-errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('decision_tree_app')

# Error handling decorator
def log_exceptions(func):
    """Decorator to catch and log exceptions in functions."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RerunException:
            # Let Streamlit's rerun mechanism work normally
            raise
        except Exception as e:
            error_msg = f"Error in {func.__name__}: {str(e)}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            st.error(error_msg)
            return None
    return wrapper

# Set page configuration
st.set_page_config(
    page_title="Decision Tree Navigator",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
                lines.append(f"{prefix[:-4]}└── {answer}")
            
            if i == len(self.current_path) - 1 and not node.is_result:
                lines.append(f"{prefix}└── {node.text}")
                lines.append(f"{prefix}    └── [Awaiting your answer]")
            else:
                if node.is_result:
                    lines.append(f"{prefix}└── {node.text}")
                else:
                    lines.append(f"{prefix}└── {node.text}")
        
        return "\n".join(lines)


@log_exceptions
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
        st.error(f"Error: File not found: {file_path}")
        raise
    
    if not tree.nodes:
        raise ValueError("No valid nodes found in the file")
    
    return tree


@log_exceptions
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


@log_exceptions
def save_path_to_file(tree: DecisionTree, input_file: str = None) -> str:
    """
    Save the current decision path to a Markdown file with a timestamp.
    
    Args:
        tree: The decision tree with the current path
        input_file: The input file path used to generate the decision tree
    
    Returns:
        The filename the path was saved to
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    
    # Extract base name from input file if provided
    if input_file:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        filename = f"{base_name}_decision_path_{timestamp}.md"
    else:
        filename = f"decision_path_{timestamp}.md"
    
    # Generate Mermaid diagram
    mermaid_diagram = generate_mermaid_diagram(tree)
    
    clean_path_display = tree.get_path_display()
    
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
    
    st.success(f"Decision path saved to: {filename}")
    return filename


@log_exceptions
def get_decision_tree_files():
    """
    Get a list of all decision tree files in the current directory.
    
    Returns:
        List of file paths
    """
    # Look for .txt files that might contain decision trees
    files = glob.glob("*.txt")
    return files


@log_exceptions
def main():
    """Main function to run the Streamlit decision tree navigator."""
    st.title("🌳 Decision Tree Navigator")
    st.markdown("A Streamlit-based decision tree implementation that processes structured text files and guides users through a series of questions.")
    
    # Initialize session state if not already done
    if 'tree' not in st.session_state:
        st.session_state.tree = None
    if 'current_file' not in st.session_state:
        st.session_state.current_file = None
    if 'restart_requested' not in st.session_state:
        st.session_state.restart_requested = False
    if 'back_requested' not in st.session_state:
        st.session_state.back_requested = False
    if 'save_requested' not in st.session_state:
        st.session_state.save_requested = False
    
    # Sidebar for file selection and controls
    with st.sidebar:
        st.header("Controls")
        
        # File selection
        files = get_decision_tree_files()
        if files:
            selected_file = st.selectbox(
                "Select a decision tree file:",
                files,
                index=0 if st.session_state.current_file is None else files.index(st.session_state.current_file) if st.session_state.current_file in files else 0
            )
            
            if st.button("Load Selected File") or (selected_file != st.session_state.current_file and st.session_state.current_file is not None):
                try:
                    # Check if the file is a valid decision tree file
                    tree = parse_file(selected_file)
                    if tree is None:
                        # This happens if parse_file caught an error and returned None
                        valid_files = [f for f in files if f != selected_file and f.endswith('.txt')]
                        suggestions = ""
                        if valid_files:
                            suggestions = f" Try one of these files instead: {', '.join(valid_files)}"
                        st.error(f"The file '{selected_file}' does not appear to be a valid decision tree file. It may be missing the required Q/A format.{suggestions}")
                    else:
                        tree.navigate_to_start()
                        st.session_state.tree = tree
                        st.session_state.current_file = selected_file
                        st.success(f"Loaded: {selected_file}")
                        
                        # Count questions and results
                        question_count = sum(1 for node in tree.nodes.values() if not node.is_result)
                        result_count = sum(1 for node in tree.nodes.values() if node.is_result)
                        st.info(f"Tree contains: {question_count} questions and {result_count} possible outcomes")
                
                except ValueError as e:
                    # More specific error for format issues
                    valid_files = [f for f in files if f != selected_file and f.endswith('.txt')]
                    suggestions = ""
                    if valid_files:
                        suggestions = f" Try one of these files instead: {', '.join(valid_files)}"
                    st.error(f"Format error in '{selected_file}': {str(e)}.{suggestions}")
                
                except Exception as e:
                    # Generic error with suggestions
                    valid_files = [f for f in files if f != selected_file and f.endswith('.txt')]
                    suggestions = ""
                    if valid_files:
                        suggestions = f" Try one of these files instead: {', '.join(valid_files)}"
                    st.error(f"Error loading file '{selected_file}': {str(e)}.{suggestions}")
        else:
            st.warning("No decision tree files found in the current directory.")
        
        # Navigation controls
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⬅️ Back"):
                st.session_state.back_requested = True
        
        with col2:
            if st.button("🔄 Restart"):
                st.session_state.restart_requested = True
        
        if st.session_state.tree and st.session_state.tree.get_current_node().is_result:
            if st.button("💾 Save Path"):
                st.session_state.save_requested = True
    
    # Main content area
    if st.session_state.tree is None:
        st.info("Please select and load a decision tree file from the sidebar to begin.")
        
        # Show available files
        if files:
            st.subheader("Available Decision Tree Files:")
            for file in files:
                st.markdown(f"- `{file}`")
        
        # Instructions
        st.markdown("---")
        st.subheader("How to Use")
        st.markdown("""
        1. Select a decision tree file from the sidebar
        2. Click "Load Selected File" to start
        3. Answer the questions by clicking on the options
        4. Use "Back" to return to the previous question
        5. Use "Restart" to start over
        6. Use "Save Path" to save your decision path when you reach a result
        """)
        
    else:
        # Handle navigation requests
        if st.session_state.back_requested:
            st.session_state.tree.go_back()
            st.session_state.back_requested = False
        
        if st.session_state.restart_requested:
            st.session_state.tree.navigate_to_start()
            st.session_state.restart_requested = False
        
        if st.session_state.save_requested:
            save_path_to_file(st.session_state.tree, st.session_state.current_file)
            st.session_state.save_requested = False
        
        # Get current node
        current_node = st.session_state.tree.get_current_node()
        
        # Display current decision path
        st.subheader("Your Decision Path")
        st.code(st.session_state.tree.get_path_display(), language=None)
        
        # Display Mermaid diagram
        st.subheader("Visual Diagram")
        
        # Generate Mermaid diagram
        mermaid_diagram = generate_mermaid_diagram(st.session_state.tree)
        
        # Try to render the diagram with HTML component, with fallback to markdown
        try:
            mermaid_html = f"""
            <div class="mermaid">
            {mermaid_diagram}
            </div>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>
                mermaid.initialize({{ startOnLoad: true, securityLevel: 'loose' }});
            </script>
            """
            st.components.v1.html(mermaid_html, height=350)
        except Exception as e:
            logger.warning(f"Failed to render Mermaid diagram with HTML component: {str(e)}")
            st.warning("Interactive diagram rendering failed. Showing static version instead.")
            st.markdown(f"```mermaid\n{mermaid_diagram}\n```")
        
        # Also keep the markdown version for reference and copying
        with st.expander("Show Mermaid Code"):
            st.code(mermaid_diagram, language="mermaid")
        
        # Display current question or result
        st.markdown("---")
        if current_node.is_result:
            st.subheader("🏁 FINAL RESULT")
            st.markdown(f"**{current_node.text}**")
            
            # Offer to save or restart
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save This Decision Path"):
                    filename = save_path_to_file(st.session_state.tree, st.session_state.current_file)
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                    st.download_button(
                        label="📥 Download Decision Path",
                        data=content,
                        file_name=filename,
                        mime="text/markdown"
                    )
            
            with col2:
                if st.button("🔄 Start Over"):
                    st.session_state.tree.navigate_to_start()
                    st.rerun()
        else:
            st.subheader("❓ QUESTION")
            st.markdown(f"**{current_node.text}**")
            
            # Display answer options
            st.subheader("Options")
            for i, (answer, _) in enumerate(current_node.answers):
                if st.button(f"{i+1}. {answer}", key=f"answer_{i}"):
                    st.session_state.tree.select_answer(i)
                    st.rerun()


if __name__ == "__main__":
    main()
