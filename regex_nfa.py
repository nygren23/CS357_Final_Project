
#TODO make parens work
#already have some cases to handle
#can mostly ignore - only changes where e transitions go on '*'
#put in the stack or not?


import re

def main():

    #read input from command line or file
    #USE SET INPUT STRING FOR NOW
    input = "(ab)*"

    #check if input is proper regex form
    #return if not
    try:
        re.compile(input)
    except re.error:
        print("invalid input")
        return -1

    #initialize tuple values
    final_states = []

    #substitute out all modifier characters
    #to manually produce the language
    char_language = re.sub("[|*()+.]", "", input)
    language = (list(set(char_language)))
    language.sort()

    final_transitions = []

    final_start = 0

    final_accepts = []

    #print formal tuple
    parsed = parse_input(input)

    final_states = parsed[0]
    final_transitions = parsed[1]
    final_start = parsed[2]
    final_accepts = parsed[3]

    print("******************")
    print("*Final NFA Tuple:*")
    print("******************\n(")
    print("states: " + str(final_states) + "\nlanguage: " + str(language) + "\ntransition table: " + 
    str(final_transitions) + "\nstart state: " + str(final_start) + "\naccept states: " + str(final_accepts))
    print(")")
    

def parse_input(input):

    #deal separately with: (, ), *, |, concat
    #transition component tuple: (start state, end state, transition character {e, a, b})
    states = []
    stack = []
    transitions = []
    accepts = []
    state_count = 0
    start = 0
    union_starts = None

    #iterate over characters of input string
    print("Shows stack each pass:")
    for index in range(0, len(input)):
        print(stack)
        #if seeing a modifier, pop stack and apply modification to top of stack
        #if character, add new component
        
        #case {*}
        if input[index] == '*':
            last_input = stack.pop()
            stack.append(((last_input[0] + '*'), last_input[1]))

            #state_count-2 --> last_input[1]
            transitions.append((state_count-1, last_input[1], 'e'))
            transitions.append((last_input[1], state_count-1, 'e'))

        elif input[index] == '+':
            last_input = stack.pop()
            stack.append(((last_input[0] + '+'), last_input[1]))

            transitions.append((state_count-1, state_count-2, 'e'))

        #case {union}
        elif input[index] == '|':
            last_input = stack.pop()
            stack.append(last_input)
            
            #keep track of the start of each branch
            union_starts = (last_input[1], state_count)

        #case {character}
        elif input[index] != '(' and input[index] != ')':
            #make new component (2 states) and update state count
            #unless reading '()' --> ignore
            states.append(state_count)
            state_count += 1
            states.append(state_count)
            
            #add to transition table
            #substitute sigma for sigma transition character
            char_output = 'sigma' if input[index] == '.' else input[index]
            transitions.append((state_count-1, state_count, char_output))

            #{concatenate} new component to a previous expression
            if index>0 and input[index-1] != '|':

                last_input = stack.pop()
                stack.append(((last_input[0]+input[index]), last_input[1]))

                if input[index-1] != '(' and input[index-1] != ')':
                    transitions.append((state_count-2, state_count-1, 'e'))
                    accepts.remove(state_count-2)

                accepts.append(state_count)
                
            #add newest component to the stack --> no concatenation
            else:
                stack.append((input[index], state_count-1))
                accepts.append(state_count)

            state_count += 1

        #case {(}
        elif input[index] == '(':
            stack.append((input[index], state_count))
        
        #BASE case {)}
        else:
            last_input = stack.pop()
            stack.append((last_input[0]+')', last_input[1]))
            
            
    if union_starts is not None:
        #add new middle state to connect components
        #update start
        states.append(state_count)

        transitions.append((state_count, union_starts[0], 'e'))
        transitions.append((state_count, union_starts[1], 'e'))

        start = state_count
        

    print(str(stack) + "\n--------------------------------------")
    
    return (states, transitions, start, accepts)
    
    
if __name__ == "__main__":
    main()