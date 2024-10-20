""" 
Make ASTNodes for the different types
Literal - done
Concatenation - done
Alternation - done
KleeneStar - done
Optional
Group - unnecessary
"""

# node for literals
class LiteralNode:
  def __init__(self, value):
    self.value = value

#node for kleene star
# @param the operand it is tied to
class KleeneStarNode:
  def __init__(self, operand):
    self.operator = '*'
    self.operand = operand
    
#node for concatenation operator
#@param left operand
# @param right operand
class ConcatNode:
  def __init__(self, left, right):
    self.operator = '-'
    self.left = left
    self.right = right
    
#node for alternation operator
# @param left
# @param right
class AlternationNode:
  def __init__(self, left, right):
    self.operator = '+'
    self.left = left
    self.right = right

#parser class to build the Abstract Syntax Tree
class Parser:
  #initializer
  # @param a list of tokens
  def __init__(self, tokens):
    self.tokens = tokens
    self.position = 0
    self.operand_stack = []
    self.operator_stack = []  #temporary storage for unprocessed operators

  #method to build the abstract syntax tree
  def buildAST(self):
    #while loop to iterate through list of tokens
    while self.position < len(self.tokens):
      token = self.tokens[self.position]
      
      #handles literals
      if token['Type'] == 'literal':
        self.operand_stack.append(LiteralNode(token['Value']))  #pushes literal to stack
      #handles kleene stars
      elif token['Type'] == 'kleeneStar':
        operand = self.operand_stack.pop()  #takes operand off stack
        self.operand_stack.append(KleeneStarNode(operand))  #pushes kleene star and its operand to stack
      #handles alternation 
      elif token['Type'] == 'alternationOperator':
        self.process_operator(token['Value'])  #call process operator function
      #handles concatenation
      elif token['Type'] == 'concat':
        self.process_operator(token['Value'])   #call process operator function
      #handles the beginning of a subexpression
      elif token['Type'] == 'openSubexpression':
        self.operator_stack.append(token) #push token to operator stack
      #handles the end of a subexpression
      elif token['Type'] == 'closeSubexpression':
        self.process_subexpression() #call process subexpression method

      #increment position
      self.position += 1

    #while loop to process remaining operators
    while self.operator_stack:
      self.process_operator_stack()

    # returns the final node in the operand stadck
    if len(self.operand_stack) == 1:
      return self.operand_stack[0]
    else:
      raise ValueError("Invalid Expression")

  #method to process operators in order of precedence
  def process_operator(self,operator):
    #while loop to check operator stack
    while self.operator_stack and self.operator_stack[-1]['Type'] != 'openSubexpression':
      top_operator = self.operator_stack.pop()
      right = self.operand_stack.pop()
      left = self.operand_stack.pop()
      #push node and its operands to the operand stack
      if top_operator['Value'] == '+':
        self.operand_stack.append(AlternationNode(left, right))
      elif top_operator['Value'] == '-':
        self.operand_stack.append(ConcatNode(left, right))

    #push operator to operator stack for temporary storage
    self.operator_stack.append(dict(Value=operator, Type="binaryOperator"))

  #method to process subexpressions
  def process_subexpression(self):
    while self.operator_stack and self.operator_stack[-1]['Type'] != 'openSubexpression':
      self.process_operator_stack()
    #get rid of the openSubexpression token
    if self.operator_stack and self.operator_stack[-1]['Type'] == 'openSubexpression':
      self.operator_stack.pop()

  #method to process the operators left on stack
  def process_operator_stack(self):
    if self.operator_stack:
      top_operator = self.operator_stack.pop()
      right = self.operand_stack.pop()
      left = self.operand_stack.pop()
      if top_operator['Value'] == '+':
        self.operand_stack.append(AlternationNode(left, right))
      elif top_operator['Value'] == '-':
        self.operand_stack.append(ConcatNode(left, right))
