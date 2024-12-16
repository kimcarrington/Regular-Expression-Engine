# DFAState Class
class DFAState:
    def __init__(self, nfa_states):
        self.nfa_states = nfa_states
        self.transitions = {}
        self.is_accept = False
        self.is_final = False

# DFA Class
class DFA:
    def __init__(self, start_state):
        self.start_state = start_state
        self.states = []
        self.state_map = {}

    # Function to add DFA state
    def add_state(self, nfa_states):
        state_key = frozenset(nfa_states)
        # Check if state key is in state map
        if state_key not in self.state_map:
            new_dfa_state = DFAState(nfa_states)
            self.state_map[state_key] = new_dfa_state
            self.states.append(new_dfa_state)
        return self.state_map[state_key]

# Function to return DFA
def construct_dfa(nfa):
  # Build DFA
  dfa = build_dfa(nfa)
  # Minimize DFA
  minimized_dfa = minimize_dfa(dfa)
  return minimized_dfa

# Function to build DFA
def build_dfa(nfa):
    # Find epsilon closure of the NFA start state
    start_closure = epsilon_closure([nfa.start_state])

    # Initialize DFA's start state
    dfa = DFA(start_state=None) 
    dfa_start_state = dfa.add_state(start_closure)
    dfa.start_state = dfa_start_state
    unprocessed_states = [dfa_start_state]

    # Process each DFA State
    while unprocessed_states:
        current_dfa_state = unprocessed_states.pop()

        # Get the unique NFA states for the current DFA
        nfa_states = current_dfa_state.nfa_states

        # Mark corresponding DFA state as accept/final
        if any(state.is_accept for state in nfa_states):
            current_dfa_state.is_accept = True
        if any(state.is_final for state in nfa_states):
            current_dfa_state.is_final = True

        # Collect possible symbols for transitions
        symbols = set()
        for state in nfa_states:
            symbols.update(state.transitions.keys())

        for symbol in symbols:
            # Get the next set of NFA states
            next_nfa_states = move(nfa_states, symbol)
            if not next_nfa_states:
                continue
            # Compute the epsilon closure of the next states
            next_closure = epsilon_closure(next_nfa_states)


            state_key = frozenset(next_closure)
            if state_key not in dfa.state_map:
                #Add to DFA and unprocessed states
                next_dfa_state = dfa.add_state(next_closure)
                unprocessed_states.append(next_dfa_state)
            else:
                #retrieve existing DFA state
                next_dfa_state = dfa.state_map[state_key]

            # Create transition in the current DFA state
            current_dfa_state.transitions[symbol] = next_dfa_state

    return dfa

# Function to find all reachable states
def epsilon_closure(nfa_states):
    closure = set(nfa_states)
    stack = list(nfa_states)

    # Go through the stack
    while stack:
        state = stack.pop()
        for next_state in state.epsilon_transitions:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure

# Function to find next state based on symbol
def move(nfa_states, symbol):
    next_states = set() 
    for state in nfa_states: 
        # Check if symbol is in transitions
        if symbol in state.transitions: 
            next_states.add(state.transitions[symbol])
    return next_states


# Function to get rid of duplicate DFA states  
def minimize_dfa(dfa):
    # Separate states into accepting and non-accepting sets
    accepting_states = {state for state in dfa.states if state.is_accept}
    non_accepting_states = {state for state in dfa.states if not state.is_accept}

    # Initialize partitions
    partitions = [accepting_states, non_accepting_states] if accepting_states else [non_accepting_states]
    worklist = [accepting_states, non_accepting_states] if accepting_states else [non_accepting_states]

    # Refine partitions using Hopcroft's algorithm
    while worklist:
        current_partition = worklist.pop()
        symbol_partitions = {}

        # Classify states by the symbol
        for state in dfa.states:
            for symbol, next_state in state.transitions.items():
                if next_state in current_partition:
                    if symbol not in symbol_partitions:
                        symbol_partitions[symbol] = set()
                    symbol_partitions[symbol].add(state)

        # Refine partitions based on transitions to current_partition
        for symbol, states_with_transition in symbol_partitions.items():
            new_partitions = []
            for partition in partitions:
                # Partition split based on states that transition to current_partition on symbol
                intersection = partition & states_with_transition
                difference = partition - states_with_transition
                if intersection and difference:
                    new_partitions.append(intersection)
                    new_partitions.append(difference)
                    # Add smaller subset to worklist
                    if partition in worklist:
                        worklist.remove(partition)
                        worklist.append(intersection)
                        worklist.append(difference)
                    else:
                        worklist.append(intersection if len(intersection) < len(difference) else difference)
                else:
                    new_partitions.append(partition)
            partitions = new_partitions

    
    # Create minimized DFA
    minimized_dfa = DFA(start_state=None)
    state_map = {}

    for partition in partitions:
        if not partition:
            continue
        # Create a representative for each partition
        repr_state = next(iter(partition))
        minimized_state = DFAState(repr_state.nfa_states)
        minimized_state.is_accept = repr_state.is_accept
        minimized_state.is_final = any(state.is_final for state in partition)
        state_map[repr_state] = minimized_state
        minimized_dfa.states.append(minimized_state)
        
        # Assign start state based on corresponding NFA
        if repr_state.nfa_states == dfa.start_state.nfa_states:
            minimized_dfa.start_state = minimized_state

    # Fallback: Ensure start state assignment if missed
    if not minimized_dfa.start_state:
        for partition in partitions:
            if not partition:
                continue
            if dfa.start_state in partition:
                repr_state = next(iter(partition))
                minimized_dfa.start_state = state_map[repr_state]
                break



    # Recreate transitions for minimized DFA
    for partition in partitions:
        if not partition:
            continue
        repr_state = next(iter(partition)) 
        minimized_state = state_map[repr_state]

        for symbol, next_state in repr_state.transitions.items():
            # Find the partition containing next state
            for target_partition in partitions:
                if next_state in target_partition:
                    # Map the transition to the representative state of the target partition
                    minimized_state.transitions[symbol] = state_map[next(iter(target_partition))]
                    break

    return minimized_dfa
