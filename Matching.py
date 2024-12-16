# Matching Algorithm
def match(dfa, input_string):
    # Start from the DFA's start state
    current_state = dfa.start_state
    # Process each character in the input string
    for symbol in input_string:
        
        # Check if there's a transition for the current symbol
        if symbol in current_state.transitions:
            # Move to the next state in the DFA
            current_state = current_state.transitions[symbol]
        else:
            return False

    # Check if the final state was reached
    return current_state.is_final
