#nfa state class
class NFAState:
  def __init__(self):
    self.transitions = {}  #dictionary
    self.epsilon_transitions = []  #list
    
#nfa class
class NFA:
  def __init__(self):
    self.start_state = NFAState()
    self.accept_state = NFAState()

#helper function to connect states
def connect(start_state, symbol, next_state):
  start_state.transitions[symbol] = next_state

def build_nfa(ast):
  #literal
  if isinstance(ast, LiteralNode):
    nfa = NFA()
    connect(nfa.start_state, ast.value, nfa.accept_state)
    return nfa
  #kleene star
  elif isinstance(ast, KleeneStarNode):
    nfa = NFA()
    sub_nfa = build_nfa(ast.operand)
    connect(nfa.start_state, None, nfa.start_state) #skip kleene star
    connect(nfa.start_state, None, sub_nfa.start_state)  #epsilon transition
    connect(sub_nfa.start_state, None, nfa.start_state)
    connect(sub_nfa.start_state, None, sub_nfa.start_state) #loop back
    return nfa
    
  #concat
  elif isinstance(ast, ConcatNode):
    nfa = NFA()
    left_nfa = build_nfa(ast.left)
    right_nfa = build_nfa(ast.right)
    connect(left_nfa.accept_state, None, right_nfa.start_state)
    nfa.start_state = left_nfa.start_state
    nfa.accept_state = right_nfa.accept_state
    return nfa
    
  #alternation
  elif isinstance(ast, AlternationNode):
    nfa = NFA()
    left_nfa = build_nfa(ast.left)
    right_nfa = build_nfa(ast.right)
    connect(nfa.start_state, None, left_nfa.start_state)  #epsilon
    connect(nfa.start_state, None, right_nfa.start_state)  #epsilon
    connect(left_nfa.accept_state, None, nfa.accept_state)
    connect(right_nfa.accept_state, None, nfa.accept_state)
    return nfa
  #else
  else:
    raise ValueError("Unknown AST Node Type")
