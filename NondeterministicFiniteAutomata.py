from AbstractSyntaxTree import LiteralNode
from AbstractSyntaxTree import KleeneStarNode
from AbstractSyntaxTree import ConcatNode
from AbstractSyntaxTree import AlternationNode

# NFA State Class
class NFAState:
  def __init__(self):
    self.transitions = {}
    self.epsilon_transitions = []
    self.is_accept = False
    self.is_final = False
    
# NFA Class
class NFA:
  def __init__(self):
    self.start_state = NFAState()
    self.accept_state = NFAState()

# Function to return NFA with updated final states
def construct_nfa(ast):
  # Build NFA
  nfa, nfa_map = build_nfa(ast)
  # Mark final states
  mark_final_states(nfa_map, ast)
  return nfa

# Function to build the NFA
def build_nfa(ast):
  # Store AST to NFA state mapping
  nfa_map = {}

  # Literal
  if isinstance(ast, LiteralNode):
    nfa = NFA()
    connect(nfa.start_state, ast.value, nfa.accept_state)
    mark_accept_state(nfa.accept_state)
    nfa_map[ast] = nfa.accept_state
    return nfa, nfa_map
  
  # Kleene Star
  elif isinstance(ast, KleeneStarNode):
    nfa = NFA()
    # Recursive call to child
    sub_nfa, sub_nfa_map = build_nfa(ast.operand) 
    # Add epsilon transitions
    add_epsilon_transition(nfa.start_state, nfa.accept_state)          # Skip  
    add_epsilon_transition(nfa.start_state, sub_nfa.start_state)       # To sub nfa
    add_epsilon_transition(sub_nfa.accept_state, nfa.accept_state)     # To accept state
    add_epsilon_transition(sub_nfa.accept_state, sub_nfa.start_state)  # Loop back
    mark_accept_state(nfa.accept_state)
    nfa_map.update(sub_nfa_map)
    return nfa, nfa_map
    
  # Concatenation
  elif isinstance(ast, ConcatNode):
    nfa = NFA()
    left_nfa, left_map = build_nfa(ast.left)
    right_nfa, right_map = build_nfa(ast.right)
    add_epsilon_transition(left_nfa.accept_state, right_nfa.start_state)   
    nfa.start_state = left_nfa.start_state
    nfa.accept_state = right_nfa.accept_state
    mark_accept_state(nfa.accept_state)
    nfa_map.update(left_map)
    nfa_map.update(right_map)
    return nfa, nfa_map
    
  # Alternation
  elif isinstance(ast, AlternationNode):
    nfa = NFA()
    left_nfa, left_map = build_nfa(ast.left)
    right_nfa, right_map = build_nfa(ast.right)
    add_epsilon_transition(nfa.start_state, left_nfa.start_state)       # To left start state
    add_epsilon_transition(nfa.start_state, right_nfa.start_state)      # To right start state
    add_epsilon_transition(left_nfa.accept_state, nfa.accept_state)     # From left accept state
    add_epsilon_transition(right_nfa.accept_state, nfa.accept_state)    # From right accept state
    mark_accept_state(nfa.accept_state)
    nfa_map.update(left_map)
    nfa_map.update(right_map)
    return nfa, nfa_map
  
  # Error Handling
  else:
    raise ValueError("Unknown AST Node Type")

# Helper function to connect states
def connect(start_state, symbol, next_state):
    start_state.transitions[symbol] = next_state
  
# Helper function to add epsilon transitions
def add_epsilon_transition(first_nfa_state, second_nfa_state):
  first_nfa_state.epsilon_transitions.append(second_nfa_state)

# Function to mark accept state
def mark_accept_state(nfa_state):
  nfa_state.is_accept = True
  
# Function to mark true final states in the NFA
def mark_final_states( nfa_map, ast):
    final_nodes = find_final_nodes(ast)
    
    for node in final_nodes:
        if node in nfa_map:
            nfa_map[node].is_final = True

# Function to find the last node(s) recursively
def find_final_nodes(ast):
  if isinstance(ast, LiteralNode):
    return {ast}
  elif isinstance(ast, KleeneStarNode):
    return find_final_nodes(ast.operand)
  elif isinstance(ast, ConcatNode):
    # Recursive call to right child
    return find_final_nodes(ast.right)
  elif isinstance(ast, AlternationNode):
    left_last_nodes = find_final_nodes(ast.left)
    right_last_nodes = find_final_nodes(ast.right)
    # Combine sets
    return left_last_nodes.union(right_last_nodes)
  else:
    return set()
