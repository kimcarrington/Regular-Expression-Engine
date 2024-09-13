""" 
Regular Expression Engine
Input:
  regular expression
  valid character set
  input string
Output:
  match found (boolean)
"""

#Check if input is a string, else return error message

#Check if input has valid characters, if not return error message

#Read and interpret regular expression
#handles Kleene Closure(*), Or + 

#iterator to keep track of position in string
"""
* 0 or more (0)
{} exact number (1)
() grouping (0)
+ or (0)
^ starts with (2)
$ ends with (2)
\escape character(2)
"""
#class definition
class RegExParser:
  #initializes self 
  def __init__(self, regex):
    self.index = 0
    self.pattern = regex
    self.length = len(regex)
    self.tokens = []

  #parser method to tokenize the regular expression
  def parse(self):
    #while loop to interate through input
    while self.position < self.length:
      character = self.regex[self.position]
      #operators
      if char in '*+()':
        self.tokens.append(char)
      #literals
      else:
        self.tokens.append(char)
      self.position += 1
      
      

