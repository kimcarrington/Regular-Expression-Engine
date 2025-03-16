# Regular-Expression-Engine
This simple regular expression engine accepts and evaluates a regular expression, and compares it to input strings to check for matches. 

## Regular Expression Syntax

| Syntax | Description |
| ------ | ----------- |
| `*` | zero or more occurrences |
| `+` | alternation | 
| `(` | beginning of subexpression |
| `)` | end of subexpression |

> [!Note]
> all other characters will be treated as literals

## Usage
1. Run `main.py`
2. Enter the regular expression when prompted.
3. Enter the number of strings to be tested.
4. Enter test strings when prompted.
5. The results will be printed for each test string.

## Project Details
* `LexicalAnalyzer.py` contains the first stage of regular expression processing. Its purpose is to create a list of tokens. 
* `AbstractSyntaxTree.py` contains the second stage of regular expression processing. An Abstract Syntax Tree is built from the list of tokens.
* `NFA.py` contains the third stage of processing. A Non-Deterministic Finite Automata is built from the Abstract Syntax Tree. The final node is located and marked.
* `DFA.py` contains the fourth stage of processing. A Deterministic Finite Automata is constructed from the Non-Deterministic Finite Automata. The constructed DFA is minimized to remove duplicate states.
* `Matching.py` contains the function used to check for a match between between an input string and the minimized DFA.
* `main.py` handles user interaction, collecting input values and displaying output.
