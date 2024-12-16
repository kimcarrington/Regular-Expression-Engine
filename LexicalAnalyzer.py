class LexicalAnalyzer:
  def __init__(self, regex):
    self.regex = regex
    self.length = len(regex)
    self.position = 0
    self.tokens = []      
    
    self.analyze()
    self.concatenate()
  
  # Function to add tokens 
  def analyze(self):

    # Iterate through regex
    while self.position < self.length:
      character = self.regex[self.position]

      # Handle kleene star
      if character in '*':
        self.tokens.append(dict(Value = character, Type = "kleeneStar"))
      # Handle alternation
      elif character in '+':
        self.tokens.append(dict(Value = character, Type = "alternationOperator"))
      # Handle subexpressions
      elif character == '(':
        self.tokens.append(dict(Value = character, Type = "openSubexpression"))
      elif character == ')':
        self.tokens.append(dict(Value = character, Type = "closeSubexpression"))
      # Handle literals
      else:
        self.tokens.append(dict(Value = character, Type = "literal"))
        
      # Increment position
      self.position += 1

  # Function to add concat nodes
  def concatenate(self):
    # Check for two or more tokens
    if len(self.tokens) >= 2:
      self.position = 1

      while self.position < len(self.tokens):
        current = self.tokens[self.position]
        previous = self.tokens[self.position - 1]

        # Check if previous and current should be concatenated
        if (
          (previous['Type'] == "literal" and (current['Type'] == "literal" or current['Type'] == "openSubexpression")) or 
          (current['Type'] == "literal" and (previous['Type'] == "closeSubexpression" or previous['Type'] == "kleeneStar")) or
          (previous['Type'] == "closeSubexpression" and current['Type'] == "openSubexpression")):
            # Add concat node
            self.tokens.insert(self.position, dict(Value = "-", Type = "concat"))
            self.position += 1

        self.position += 1
