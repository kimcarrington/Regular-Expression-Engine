# Literal Node Class
class LiteralNode:
  def __init__(self, value):
    self.value = value

# Kleene Star Node Class
class KleeneStarNode:
  def __init__(self, operand):
    self.operator = '*'
    self.operand = operand
    
# Concat Node Class
class ConcatNode:
  def __init__(self, left, right):
    self.operator = '-'
    self.left = left
    self.right = right
    
# Alternation Node Class
class AlternationNode:
  def __init__(self, left, right):
    self.operator = '+'
    self.left = left
    self.right = right

# Parser Class to build the Abstract Syntax Tree from a list of tokens
class Parser:

  def __init__(self, tokens):
    self.tokens = tokens
    self.position = 0
    self.operand_stack = []
    self.operator_stack = []  #temporary storage for unprocessed operators

  # Function to build the AST
  def buildAST(self):

    # Iterate through list of tokens
    while self.position < len(self.tokens):
      token = self.tokens[self.position]
      
      # Handle literal
      if token['Type'] == "literal":
        self.operand_stack.append(LiteralNode(token['Value'])) 

      # Handle kleene star 
      elif token['Type'] == "kleeneStar":
        operand = self.operand_stack.pop() 
        self.operand_stack.append(KleeneStarNode(operand))

      # Handle binary operators
      elif token['Type'] == "alternationOperator" or token['Type'] == "concat":
        self.process_operator(token['Value'])   

      # Handle subexpressions
      elif token['Type'] == "openSubexpression":
        self.operator_stack.append(token) 
      elif token['Type'] == "closeSubexpression":
        self.process_subexpression()  

      # Increment position
      self.position += 1

    # Process remaining operators
    while self.operator_stack:
      self.process_operator_stack()

    # Return final node
    if len(self.operand_stack) == 1:
      return self.operand_stack[0]
    else:
      raise ValueError("Invalid Expression")

  # Helper Function to Process Operators
  def process_operator(self,operator):

    # Check operator stack
    while self.operator_stack and self.operator_stack[-1]['Type'] != "openSubexpression":
      
      top_operator = self.operator_stack.pop()
      right = self.operand_stack.pop()
      left = self.operand_stack.pop()

      # Push node and its operands to operand stack
      if top_operator['Value'] == '+':
        self.operand_stack.append(AlternationNode(left, right))
      elif top_operator['Value'] == '-':
        self.operand_stack.append(ConcatNode(left, right))          

    # Push operator to operator stack
    self.operator_stack.append(dict(Value=operator, Type="binaryOperator"))


  # Helper Function to Process Subexpressions
  def process_subexpression(self):
    while self.operator_stack and self.operator_stack[-1]['Type'] != "openSubexpression":
      self.process_operator_stack()
    # Remove openSubexpression token
    if self.operator_stack and self.operator_stack[-1]['Type'] == "openSubexpression":
      self.operator_stack.pop()


  # Helper Function to process operator stack
  def process_operator_stack(self):
    if self.operator_stack:

      top_operator = self.operator_stack.pop()
      right = self.operand_stack.pop()
      left = self.operand_stack.pop()

      if top_operator['Value'] == '+':
        self.operand_stack.append(AlternationNode(left, right))
      elif top_operator['Value'] == '-':
        self.operand_stack.append(ConcatNode(left, right))
