
import re

if __name__ == "__main__":
    from sys import argv
    filename = argv[1]
    pattern = pattern = re.compile(r'\S+')
    columns = []
    total = 0

    last_line_tokens = None
    
    with open(filename) as f:
        for line in f:
            tokens = pattern.findall(line)

            # Initialize columns on first line
            if not columns:
                columns = [[] for _ in tokens]

            # Try to convert to int, skip if it fails (operators)
            for i, token in enumerate(tokens):
                columns[i].append(token)
        
    # Now process each column
    for column in columns:
        operator = column[-1]  # Last item is the operator
        numbers = [int(x) for x in column[:-1]]  # Convert all but last to ints
        
        if operator == '+':
            result = sum(numbers)
        elif operator == '*':
            result = 1
            for num in numbers:
                result *= num
        
        total += result
        
    print(total)