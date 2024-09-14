#Lexical Analysis: break regular expression down into tokens.
class LexicalAnalyzer:
  def __init__(self, regex):
    self.regex = regex
    self.length = len(regex)
    self.position = 0
    self.tokens = []          #list for storing the tokens

  #method to add tokens
  def analyze(self):
    #while loop to go through the regex and create tokens
    while self.position < self.length:
      character = self.regex[self.position]
      #handle operators
      if character in '*+().?':
        self.tokens.append(character)
        self.position += 1
      #handle escapes
      elif character == "\\":
        #call method to handle this case
        self.tokens.append(self.analyzeEscape())
      #handle literals
      else:
        self.tokens.append(character)
        self.position += 1

    #method to tokenize escape sequence
    def analyzeEscape(self):
      #check next character
      self.positon += 1
      character = self.regex[self.position]
      #check if next character is supported
      if character in '*+().?':
        self.position += 1
        return '\\' + character
      #error handling
      else:
        raise ValueError("Unsupported Escape Sequence.")
  
