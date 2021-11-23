
import re, sys

def main():

    #TEST CASES
    input = [
        "(a|b)|a", 
        "a*b*a+a",
        "a|.*b+",
        "ab*(a*|b*)a*",
        "b*b(ba)b+"    
    ]

    #stdout change
    original = sys.stdout
    sys.stdout = open('output.txt', 'w')
    
    #print formal tuple
    for single_input in input:
        #check if input is proper regex form
        #return if not
        try:
            re.compile(single_input)
        except re.error:
            print("invalid input")
            return -1
            #initialize tuple values
        final_states = []

        #substitute out all modifier characters
        #to manually produce the language
        char_language = re.sub("[|*()+.]", "", single_input)
        language = (list(set(char_language)))
        language.sort()

        final_transitions = []

        final_start = 0

        final_accepts = []

        parsed = parse_input(single_input)

        final_states = parsed[0]
        final_transitions = parsed[1]
        final_start = parsed[2]
        final_accepts = parsed[3]
        
        print("*********************")
        print("*Final NFA Tuple for: " + str(single_input))
        print("*********************\n(")
        print("states: " + str(final_states) + "\nlanguage: " + str(language) + "\ntransition table: " + 
        str(final_transitions) + "\nstart state: " + str(final_start) + "\naccept states: " + str(final_accepts))
        print(")")
        print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$\n")

    #stdout change back
    sys.stdout = original

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
    #print("Shows stack each pass:")
    for index in range(0, len(input)):
     #   print(stack)
        #if seeing a modifier, pop stack and apply modification to top of stack
        #if character, add new component
        
        #case {*}
        #TODO handle whether in parens or not
        if input[index] == '*':
            last_input = stack.pop()
            stack.append(((last_input[0] + '*'), last_input[1]))

            #state_count-2 if in not parens 
            #last_input[1] if in parens
            transition_to = state_count-2 if '(' not in last_input[0] else last_input[1]
            transitions.append((state_count-1, transition_to, 'e'))
            transitions.append((transition_to, state_count-1, 'e'))

        #case {+}
        #TODO handle whether in parens or not
        elif input[index] == '+':
            last_input = stack.pop()
            stack.append(((last_input[0] + '+'), last_input[1]))

            transition_to = state_count-2 if '(' not in last_input[0] else last_input[1]
            transitions.append((state_count-1, transition_to, 'e'))

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
            new_start = last_input[1]
            
            if union_starts is not None:
                #add new middle state to connect components
                #update start
                states.append(state_count)

                transitions.append((state_count, union_starts[0], 'e'))
                transitions.append((state_count, union_starts[1], 'e'))

                start = state_count 
                new_start = state_count

                state_count += 1

                union_starts = None
            
            stack.append((last_input[0]+')', new_start))
            
            
    if union_starts is not None:
        #add new middle state to connect components
        #update start
        states.append(state_count)

        transitions.append((state_count, union_starts[0], 'e'))
        transitions.append((state_count, union_starts[1], 'e'))

        start = state_count
    
    return (states, transitions, start, accepts)
    
    
if __name__ == "__main__":
    main()