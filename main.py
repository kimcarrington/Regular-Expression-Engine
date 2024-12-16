from Matching import match
from LexicalAnalyzer import LexicalAnalyzer
from AbstractSyntaxTree import Parser
from NFA import construct_nfa
from DFA import construct_dfa

def main():
    regex = input("\nEnter regular expression: ")
    tokenizer = LexicalAnalyzer(regex)
    ast = Parser(tokenizer.tokens).buildAST()
    nfa = construct_nfa(ast)
    dfa = construct_dfa(nfa)



    no_of_strings = input("\nEnter the number of strings to be tested: ")

    if no_of_strings.isdigit():
        no_of_strings = int(no_of_strings)
        print()
        test_strings = []
        for i in range(no_of_strings):
            test_value = input("Enter test string #" + str(i+1) + ": ")
            test_strings.append(test_value)
        print()
        for string in test_strings:
            if match(dfa, string):
                print(string + " is a match.")
            else:
                print(string + " is not a match.")
        print()
    else: 
        print("Invalid input.")

main()
