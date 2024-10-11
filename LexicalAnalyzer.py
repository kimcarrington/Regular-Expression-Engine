class LexicalAnalyzer:
  def __init__(self, regex):
    self.regex = regex
    self.length = len(regex)
    self.position = 0
    #self.previousIndex = 0
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

  #send error message if end of sequence is reached
  if self.position >= self.length:
    raise ValueError("Incomplete Escape Sequence at End of Input.")
  character = self.regex[self.position]
  #check if next character is supported
  if character in '*+()':
    self.position += 1
    return '\\' + character
  #send error message
  else:
    raise ValueError("Unsupported Escape Sequence.")

#method to add concatenation to tokens
def concatenate(self):
  #check length of tokens
  if len(self.tokens) >= 2:
    self.position = 1
    #while loop to iterate through tokens
    while self.position < len(self.tokens):
      #update current and previous
      current = self.tokens[self.position]
      previous = self.tokens[self.position - 1]
      #conditionals
      if (
        (previous['Type'] == "literal" and (current['Type'] == "literal" or current['Type'] == "openSubexpression")) or 
        (current['Type'] == "literal" and (previous['Type'] == "closeSubexpression" or previous['Type'] == "unaryOperator"))
         ):
           #append and update position
           self.tokens.insert(self.position, dict(Value = "-", Type = "concat"))
           self.position += 1
      #increment position
      self.position += 1
  
