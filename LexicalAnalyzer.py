class LexicalAnalyzer:
  def __init__(self, regex):
    self.regex = regex
    self.length = len(regex)
    self.position = 0
    self.tokens = []           #list of dictionaries

#method to add tokens 
def analyze(self):
  #while loop to go through the regex and create tokens
  while self.position < self.length:
    character = self.regex[self.position]
    #handle unary operators
    if character in '*':
      self.tokens.append(dict(Value = character, Type = "unaryOperator"))
      self.position += 1
    #handle binary operators
    elif character in '+':
      self.tokens.append(dict(Value = character, Type = "binaryOperator"))
      self.position += 1
    #handle escape characters
    elif character == '\\':
      #call method to analyze escape sequence
      self.tokens.append(self.analyzeEscape())
    #handle the beginning of a subexpression
    elif character == '(':
      self.tokens.append(dict(Value = character, Type = "openSubexpression"))
      self.position += 1
    #Handle the end of a subexpression
    elif character == ')':
      self.tokens.append(dict(Value = character, Type = "closeSubexpression"))
    #handle literals
    else:
      self.tokens.append(dict(Value = character, Type = "literal"))

#method to tokenize escape sequence
def analyzeEscape(self):
  #check next character
  self.position += 1
  character = self.regex[self.position]
  #check if next character is supported
  if character in '*+()':
    self.position += 1
    return '\\' + character
  #send error message
  else:
    raise ValueError("Unsupported Escape Sequence.")
