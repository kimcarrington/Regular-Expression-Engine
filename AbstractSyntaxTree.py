""" 
Make ASTNodes for the different types
Literal
Concatenation
Alternation
KleeneStar
Optional
Group
"""

# node for literals
class LiteralNode:
  def __init__(self, value):
    self.value = value

#node for unary operators like kleene star
class UnaryNode:
  def __init__(self, operator, operand):
    self.operator = operator
    self.operand = operand

#node for binary operators like concatenation - or alternation +
class BinaryNode:
  def __init__(self, operator, left, right):
    self.operator = operator
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
    self.operator_stack = []

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
        self.operand_stack.append(UnaryNode('*', operand))  #pushes kleene star and its operator to stack
      #handles alternation 
      elif token['Type'] == 'alternationOperator':
        self.process_operator(token['Value'])
      #handles concatenation
      elif token['Type'] == 'concatenation':
        self.process_operator(token['Value'])
      #handles the beginning of a subexpression
      elif token['Type'] == 'openSubexpression':
        self.operator_stack.append(token)
      #handles the end of a subexpression
      elif token['Type'] == 'closeSubexpression':
        self.process_subExpression()

      #increment position
      self.position += 1

  #method to process operators in order of precedence
  def process_operator(self,operator):
    #while loop to check operator stack
    while self.operator_stack and self.operator_stack[-1]['Type'] != 'openSubexpression':
      top_operator = self.operator_stack.pop()
      right = self.operand_stack.pop()
      left = self.operand_stack.pop()
      #push binary node and its operands to the operand stack
      self.operand_stack.append(BinaryNode(top_operator['Value'], left, right))
    #push operator to operator stack
    self.operator_stack.append(dict(Value=operator, Type="binaryOperator"))
