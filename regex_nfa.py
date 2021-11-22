import re

def main():
    #read input from command line or file
    #USE SET INPUT STRING FOR NOW
    input = "a*b*|bba"

    #check if input is proper regex form
    #return if not
    try:
        re.compile(input)
    except re.error:
        print("invalid input")
        return -1

    #initialize tuple values
    final_states = []
    language = ['a', 'b']
    final_transitions = []
    final_start = 0
    final_accepts = []

    #print formal tuple
    parsed = parse_input(input)

    final_states = parsed[0]
    final_transitions = parsed[1]
    final_start = parsed[2]
    final_accepts = parsed[3]

    print("Final NFA Tuple:")
    print("states: " + str(final_states) + "\nlanguage: " + str(language) + "\ntransition table: " + 
    str(final_transitions) + "\nstart state: " + str(final_start) + "\naccept states: " + str(final_accepts))
    

def parse_input(input):

    #deal separately with: (, ), *, |, concat
    #transition component tuple: (start state, end state, transition character {e, a, b})

    states = []
    stack = []
    transitions = []
    accepts = []
    state_count = 0
    start = 0
    union_starts = ()
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

            transitions.append((state_count-1, state_count-2, 'e'))
            transitions.append((state_count-2, state_count-1, 'e'))

        #case {union}
        elif input[index] == '|':
            last_input = stack.pop()
            stack.append(last_input)
            
            #keep track of the start of each branch
            union_starts = (last_input[1], state_count)

        #case {character}
        else:
            #make new component (2 states) and update state count
            states.append(state_count)
            state_count += 1
            states.append(state_count)
            
            #add to transition table
            transitions.append((state_count-1, state_count, input[index]))

            #concat makes new component
            if index>0 and input[index-1] != '|' and input != '(' and input != ')':
                last_input = stack.pop()
                stack.append(((str(last_input[0]) + str(input[index])), last_input[1]))
                transitions.append((state_count-2, state_count-1, 'e'))
                accepts.remove(state_count-2)
                accepts.append(state_count)
            else:
            #add newest component to the stack
                stack.append((input[index], state_count-1))
                accepts.append(state_count)
            state_count += 1
            
        
    
    if union_starts != None:
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