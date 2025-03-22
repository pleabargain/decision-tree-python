# Decision Tree Navigator

A simple terminal-based decision tree implementation that processes structured text files and guides users through a series of questions, displaying the decision path as a tree.

## Overview

The Decision Tree Navigator is a Python script that reads a text file containing a decision tree structure and presents questions to the user in the terminal. As the user answers questions, the script navigates through the tree and displays the decision path visually. This implementation is designed to be simple, flexible, and easy to use for any type of decision tree content.

## Installation

No installation is required beyond having Python 3.6+ installed on your system. The script uses only standard library modules.

### Requirements
- Python 3.6 or higher

## Usage

Run the script with a decision tree file as an argument:

```bash
python decision_tree.py food_safety.txt
```

### Command-line Options

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

- Interactive terminal-based navigation
- Colorful visual representation of the decision path as a tree
- Support for going back to previous questions
- Ability to restart the decision tree
- Save decision paths as Markdown files with:
  - Input file name included in the output filename
  - Timestamp for easy tracking
  - ASCII tree representation of the decision path
  - Mermaid diagram for visual representation
- Simple and flexible file format
- No external dependencies

## Interactive Commands

During the session, you can use these commands:

- Enter a number to select an answer option
- Type `back` to return to the previous question
- Type `restart` to start over from the beginning
- Type `tree` to display your current decision path
- Type `help` to show available commands
- Type `exit` to quit the application
- Type `save` to save your decision path (available at result screens)

## Examples

### Food Safety Evaluation

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

Example session (note: actual terminal output includes colors):

```
============================================================
                DECISION TREE NAVIGATOR
============================================================

Loaded: food_safety.txt
Tree contains: 15 questions and 10 possible outcomes

This interactive tool will guide you through a series of questions.
Your answers will determine the path through the decision tree.

At any point, you can:
- Type 'back' to return to the previous question
- Type 'restart' to start over
- Type 'tree' to see your current path
- Type 'exit' to quit
- Type 'help' for more commands

Let's begin!
============================================================

QUESTION: Do you have a food thermometer available for temperature checks?

Options:
1. Yes
2. No

Enter your choice (1-2) or type 'back', 'restart', 'tree', 'exit': 1

QUESTION: Is the food stored at the proper temperature (below 40°F for refrigerated items, below 0°F for frozen items)?

Options:
1. Yes
2. No
3. Not sure

Enter your choice (1-3) or type 'back', 'restart', 'tree', 'exit': 1

QUESTION: Has the food been cooked to the appropriate internal temperature?

Options:
1. Yes
2. No
3. Not sure
4. It's a ready-to-eat food that doesn't require cooking

Enter your choice (1-4) or type 'back', 'restart', 'tree', 'exit': 1

QUESTION: Are there any visible signs of spoilage (unusual color, texture, or odor)?

Options:
1. Yes
2. No

Enter your choice (1-2) or type 'back', 'restart', 'tree', 'exit': 2

FINAL RESULT:
The food is SAFE. All critical safety checks have passed. The food has been properly stored, handled, and shows no signs of spoilage or contamination.

Your complete decision path:
└── Do you have a food thermometer available for temperature checks?
    └── Yes
        └── Is the food stored at the proper temperature (below 40°F for refrigerated items, below 0°F for frozen items)?
            └── Yes
                └── Has the food been cooked to the appropriate internal temperature?
                    └── Yes
                        └── Are there any visible signs of spoilage (unusual color, texture, or odor)?
                            └── No
                                └── The food is SAFE. All critical safety checks have passed. The food has been properly stored, handled, and shows no signs of spoilage or contamination.

What would you like to do next? (save/restart/exit): save

Decision path saved to: food_safety_decision_path_2025-03-22_11-41-00.md

What would you like to do next? (restart/exit): exit

Thank you for using the Decision Tree Navigator!
```

## Saved Decision Path Format

When you save your decision path, the system creates a Markdown file with the following structure:

1. **Header Information**:
   - Title and generation timestamp
   - Source file information

2. **ASCII Tree Representation**:
   - A text-based tree showing the complete decision path
   - Identical to what's displayed in the terminal (without colors)

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

Example of a saved Markdown file when viewed in a compatible viewer:

![Mermaid Diagram Example](https://mermaid.ink/img/pako:eNp1kMFqwzAMhl9F-NRBXsA9bGxQKOwwGIPtVnwwsZpYOLZxnMFKeffJTrqyXXSS_n_6JR1hbwNBCQfXvw-Oe-fJfnUfH-1bS_ZIjVt3Hs_Oe-qo8XYgCnTqvKHWDVTBKVhFe2qcpVNHtbOWrKcKPv_xX8nS8JQsU7aK2TJZpWwO5XNMljFbxTGLWZKwNGFpzNKYJQlLWZqyNGVJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJTFLYpbELIlZErMkZknMkpglMUtilsQsiVkSsyRmScySmCUxS2KWxCyJWRKzJGZJzJKYJT
# Decision Tree Navigator

A simple terminal-based decision tree implementation that processes structured text files and guides users through a series of questions, displaying the decision path as a tree.

## Overview

The Decision Tree Navigator is a Python script that reads a text file containing a decision tree structure and presents questions to the user in the terminal. As the user answers questions, the script navigates through the tree and displays the decision path visually. This implementation is designed to be simple, flexible, and easy to use for any type of decision tree content.

## Installation

No installation is required beyond having Python 3.6+ installed on your system. The script uses only standard library modules.

### Requirements
- Python 3.6 or higher

## Usage

Run the script with a decision tree file as an argument:

```bash
python decision_tree.py food_safety.txt
```

### Command-line Options

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

- Interactive terminal-based navigation
- Colorful visual representation of the decision path as a tree
- Support for going back to previous questions
- Ability to restart the decision tree
- Save decision paths as Markdown files with:
  - Input file name included in the output filename
  - Timestamp for easy tracking
  - ASCII tree representation of the decision path
  - Mermaid diagram for visual representation
- Simple and flexible file format
- No external dependencies

## Interactive Commands

During the session, you can use these commands:

- Enter a number to select an answer option
- Type `back` to return to the previous question
- Type `restart` to start over from the beginning
- Type `tree` to display your current decision path
- Type `help` to show available commands
- Type `exit` to quit the application
- Type `save` to save your decision path (available at result screens)

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

Example session (note: actual terminal output includes colors):

```
============================================================
                DECISION TREE NAVIGATOR
============================================================

Loaded: food_safety.txt
Tree contains: 15 questions and 10 possible outcomes

This interactive tool will guide you through a series of questions.
Your answers will determine the path through the decision tree.

At any point, you can:
- Type 'back' to return to the previous question
- Type 'restart' to start over
- Type 'tree' to see your current path
- Type 'exit' to quit
- Type 'help' for more commands

Let's begin!
============================================================

QUESTION: Do you have a food thermometer available for temperature checks?

Options:
1. Yes
2. No

Enter your choice (1-2) or type 'back', 'restart', 'tree', 'exit': 1

QUESTION: Is the food stored at the proper temperature (below 40°F for refrigerated items, below 0°F for frozen items)?

Options:
1. Yes
2. No
3. Not sure

Enter your choice (1-3) or type 'back', 'restart', 'tree', 'exit': 1

QUESTION: Has the food been cooked to the appropriate internal temperature?

Options:
1. Yes
2. No
3. Not sure
4. It's a ready-to-eat food that doesn't require cooking

Enter your choice (1-4) or type 'back', 'restart', 'tree', 'exit': 1

QUESTION: Are there any visible signs of spoilage (unusual color, texture, or odor)?

Options:
1. Yes
2. No

Enter your choice (1-2) or type 'back', 'restart', 'tree', 'exit': 2

FINAL RESULT:
The food is SAFE. All critical safety checks have passed. The food has been properly stored, handled, and shows no signs of spoilage or contamination.

Your complete decision path:
└── Do you have a food thermometer available for temperature checks?
    └── Yes
        └── Is the food stored at the proper temperature (below 40°F for refrigerated items, below 0°F for frozen items)?
            └── Yes
                └── Has the food been cooked to the appropriate internal temperature?
                    └── Yes
                        └── Are there any visible signs of spoilage (unusual color, texture, or odor)?
                            └── No
                                └── The food is SAFE. All critical safety checks have passed. The food has been properly stored, handled, and shows no signs of spoilage or contamination.

What would you like to do next? (save/restart/exit): save

Decision path saved to: food_safety_decision_path_2025-03-22_11-41-00.md

What would you like to do next? (restart/exit): exit

Thank you for using the Decision Tree Navigator!
```

## Saved Decision Path Format

When you save your decision path, the system creates a Markdown file with the following structure:

1. **Header Information**:
   - Title and generation timestamp
   - Source file information

2. **ASCII Tree Representation**:
   - A text-based tree showing the complete decision path
   - Identical to what's displayed in the terminal (without colors)

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

To use this guide:
```bash
python decision_tree.py use-a-decision-tree-yes-or-no.txt
```

This interactive tool will help data scientists, analysts, and business users make informed choices about whether decision trees are the right approach for their specific problems.

## Project Files

- `decision_tree.py`: Main Python script
- `food_safety.txt`: Sample decision tree for food safety evaluation
- `use-a-decision-tree-yes-or-no.txt`: Decision tree to help determine when to use decision trees
- `when_to_use_a_decision_tree.md`: Comprehensive guide on decision tree applications
- `README.md`: This documentation file
- `food_safety_research.md`: Research on food safety evaluation
- `chat_history.md`: Development history and planning conversation

## License

This project is available under the MIT License.
