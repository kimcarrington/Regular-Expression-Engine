#Lexical Analysis: break regular expression down into tokens.
class LexicalAnalyzer:
  def __init__(self, regex):
    self.regex = regex
    self.length = len(regex)
    self.position = 0
    self.tokens = []          #list for storing the tokens

  #while loop to go through the regex and create tokens
  while self.position < self.length:
    
