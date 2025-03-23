# Decision Tree Navigator

A decision tree implementation that processes structured text files and guides users through a series of questions, displaying the decision path as a tree. Available in both terminal-based and web-based (Streamlit) versions.

## Repository

Original repository: https://github.com/pleabargain/decision-tree-python


# TBD
Currently the decision tree stops as soon as it reaches a 'result', which may be a good thing.

## Motivation

This project began with an exploration of decision trees and their practical applications. The goal was to create a simple, flexible tool that could be used for any type of decision-making process, from food safety evaluation to determining when to use decision trees in data science.

## Rationale for Streamlit Version

The Streamlit version was created to make this tool more accessible to all users, regardless of their technical background. While the terminal-based version is powerful, a web-based interface:

- Eliminates the command-line barrier for non-technical users
- Provides a more intuitive, point-and-click interface
- Makes the visual diagrams interactive and immediately visible
- Allows for easier sharing and deployment
- Enables access from any device with a web browser

By making this tool available as a Streamlit application, we extend its reach to a broader audience, including business users, educators, students, and anyone who needs to navigate decision trees without dealing with command-line interfaces.

## Overview

The Decision Tree Navigator reads a text file containing a decision tree structure and presents questions to the user. As the user answers questions, the application navigates through the tree and displays the decision path visually. This implementation is designed to be simple, flexible, and easy to use for any type of decision tree content.

## Installation

### Terminal Version
No installation is required beyond having Python 3.6+ installed on your system. The script uses only standard library modules.

### Streamlit Version
To run the Streamlit version, you'll need to install Streamlit:

```bash
pip install -r requirements.txt
```

## Usage

### Terminal Version
Run the script with a decision tree file as an argument:

```bash
python decision_tree.py food_safety.txt
```

### Streamlit Version
Run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

Then select a decision tree file from the sidebar to begin.

### Command-line Options (Terminal Version Only)

- `--version`: Show the version information and exit
- `--help`: Show the help message and exit

## Decision Tree File Format

The decision tree file should follow this format:

```
Q1: First question text
A: Answer option 1 -> Q2
A: Answer option 2 -> R1

Q2: Second question text
A: Answer option 1 -> Q3
A: Answer option 2 -> R2

Q3: Third question text
A: Answer option 1 -> R3
A: Answer option 2 -> R4

R1: RESULT: First result text
R2: RESULT: Second result text
R3: RESULT: Third result text
R4: RESULT: Fourth result text
```

### Format Rules:

- Question lines start with `Q` followed by a number and a colon (e.g., `Q1:`)
- Result lines start with `R` followed by a number and a colon (e.g., `R1:`)
- Answer lines start with `A:` and must include an arrow (`->`) pointing to the next question or result ID
- Blank lines are ignored
- IDs must be unique

## Features

### Terminal Version
- Interactive terminal-based navigation
- Colorful visual representation of the decision path as a tree
- Support for going back to previous questions
- Ability to restart the decision tree
- Save decision paths as Markdown files

### Streamlit Version
- Web-based user interface with intuitive controls
- Interactive selection of decision tree files
- Visual representation of the decision path as both text and Mermaid diagram
- Support for going back to previous questions
- Ability to restart the decision tree
- Save and download decision paths as Markdown files

### Common Features
- Simple and flexible file format
- Mermaid diagrams for visual representation of decision paths
- Support for any type of decision tree content

## Interactive Commands

### Terminal Version
During the session, you can use these commands:
- Enter a number to select an answer option
- Type `back` to return to the previous question
- Type `restart` to start over from the beginning
- Type `tree` to display your current decision path
- Type `help` to show available commands
- Type `exit` to quit the application
- Type `save` to save your decision path (available at result screens)

### Streamlit Version
Use the buttons and controls in the interface:
- Click on answer options to select them
- Use the "Back" button to return to the previous question
- Use the "Restart" button to start over
- View your decision path in the main display area
- Use the "Save Path" button to save your decision path
- Use the "Download Decision Path" button to download the saved path

## Example: Food Safety Evaluation

The included `food_safety.txt` file demonstrates a decision tree for evaluating food safety. It guides users through a series of questions about food storage, preparation, and handling to determine if food is safe to consume.

The food safety evaluation includes:
- Initial check for availability of a food thermometer (essential for accurate temperature assessment)
- Storage temperature verification
- Cooking temperature verification
- Spoilage and expiration date checks
- Cross-contamination assessment
- Handling procedures evaluation
- Storage conditions verification
- Allergen considerations

The decision tree incorporates "I don't know" options for cases where the user is uncertain, with appropriate guidance for each scenario.

## Saved Decision Path Format

When you save your decision path, the system creates a Markdown file with the following structure:

1. **Header Information**:
   - Title and generation timestamp
   - Source file information

2. **ASCII Tree Representation**:
   - A text-based tree showing the complete decision path
   - Identical to what's displayed in the terminal/app (without colors)

3. **Mermaid Diagram**:
   - A visual flowchart representation of your decision path
   - Nodes represent questions and results
   - Edges show the answers that connect questions
   - Current path is highlighted with blue nodes
   - Result nodes are highlighted with green

The Mermaid diagram provides several advantages:
- **Visual Clarity**: Makes complex decision paths easier to understand at a glance
- **Shareable Format**: When viewed in GitHub or other Markdown viewers that support Mermaid, the diagram renders as an interactive flowchart
- **Documentation Quality**: Enhances the quality of saved outputs for reporting or sharing
- **Accessibility**: Provides an alternative representation for users who prefer visual formats

### Decision Tree Selection Guide

The included `use-a-decision-tree-yes-or-no.txt` file provides a decision tree to help users determine whether a decision tree is appropriate for their specific problem. This meta-decision tree was created based on the comprehensive guide in `when_to_use_a_decision_tree.md`.

The decision tree selection guide includes:
- Initial assessment of the user's primary goal (data exploration, machine learning, business decision-making)
- Evaluation of specific requirements like interpretability, feature importance, and handling missing data
- Assessment of data characteristics such as dimensionality and complexity
- Consideration of regulatory requirements and stakeholder needs
- Clear recommendations with explanations for when to use decision trees and when to consider alternatives

## Project Files

- `decision_tree.py`: Main Python script for terminal version
- `streamlit_app.py`: Streamlit web application version
- `requirements.txt`: Dependencies for the Streamlit version
- `food_safety.txt`: Sample decision tree for food safety evaluation
- `use-a-decision-tree-yes-or-no.txt`: Decision tree to help determine when to use decision trees
- `college-decision-path.txt`: Sample decision tree for college decision-making
- `when_to_use_a_decision_tree.md`: Comprehensive guide on decision tree applications
- `README.md`: This documentation file
- `food_safety_research.md`: Research on food safety evaluation
- `chat_history.md`: Development history and planning conversation

## GitHub Forking Instructions

To fork this repository and create your own version:

1. **Fork the repository**:
   - Visit the original repository at https://github.com/pleabargain/decision-tree-python
   - Click the "Fork" button in the top-right corner of the page
   - This creates a copy of the repository under your GitHub account

2. **Clone your forked repository**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/decision-tree-python.git
   cd decision-tree-python
   ```

3. **Create a new branch**:
   ```bash
   git checkout -b streamlit-version
   ```

4. **Make your changes**:
   - Add the Streamlit application
   - Update the README.md
   - Make any other desired changes

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add Streamlit version of decision tree navigator"
   ```

6. **Push to GitHub**:
   ```bash
   git push origin streamlit-version
   ```

7. **Create a Pull Request** (optional, if you want to contribute back to the original repository):
   - Go to your fork on GitHub
   - Click "Pull Request"
   - Select your branch and submit the pull request

## License

This project is available under the MIT License.
