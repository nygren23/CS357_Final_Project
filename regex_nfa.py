import re

def main():
    #read input from command line or file
    #USE SET INPUT STRING FOR NOW
    input = "a*b"

    #check if input is proper regex form
    #return if not
    try:
        re.compile(input)
    except re.error:
        print("invalid input")
        return -1

    #initialize tuple values
    states = []
    language = ['a', 'b']
    transitions = []
    start = 0
    accepts = []

    #print formal tuple
    print(parse_input(input))


def parse_input(input):

    #iterate over characters of input string
    for index in range(0, len(input)):
        print(input[index])

    return "DONE"
    #return formal tuple
    #return (states, language, transitions, start, accepts)
    
    
    

if __name__ == "__main__":
    main()