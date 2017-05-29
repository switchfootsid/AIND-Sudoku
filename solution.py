assignments = []
values = []
rows = 'ABCDEFGHI'
cols = '123456789'
total_digits = cols


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]

square_units = [cross(row_set, cols_set) for row_set in ('ABC', 'DEF', 'GHI') for cols_set in ('123', '456', '789')]
diag_units = [[x + y for x, y in zip(rows, cols)],  [x + y for x, y in zip(rows, reversed(cols))]]

unitlist = row_units + col_units + square_units + diag_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for box in values.keys():
        for peer in peers[box]:
            if values[box] == values[peer] and len(values[box]) == 2 and len(values[peer]) == 2:
                for box_units in units[box]:
                    if box_units in units[peer]:
                        for x in box_units:
                            if x != box and x != peer:
                                values[x] = values[x].replace(values[box][0], '')
                                values[x] = values[x].replace(values[box][1], '')

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    buff = []
    nums = '123456789'

    if len(grid) != 81:
        raise ValueError("Grid error, must be 81 units")

    for c in grid:
        if c == '.':
            buff.append(nums)
        elif c in nums:
            buff.append(c)

    values = dict(zip(boxes, buff))
    return values


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    print 'disp values',values
    width = 1 + max([len(values[each_box]) for each_box in boxes])
    line = '+'.join(['-' * (width * 3)] * 3)
    for each_row in rows:
        print(''.join(values[each_row + each_col].center(width) + ('|' if each_col in '36' else '') for each_col in cols))
        
        if each_row in 'CF':
            print(line)
    return

def eliminate(values):
    """
    Find all solved boxes
    Args:
        values(dict): The sudoku in dictionary form

    """
    solved_boxes = []
    for box in values.keys():
        if len(values[box]) == 1:
            solved_boxes.append(box)

    for each_box in solved_boxes:
        solution = values[each_box]
        for peer in peers[each_box]:
            values[peer] = values[peer].replace(solution, '')

    return values

def only_choice(values):
    """
    Find each unit that contains a value fitting only ONE box and assign
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        modified (after applying operation) sudoku in dictionary form 
    """

    for each_unit in unitlist:
        for each_digit in total_digits:
            solutions = [each_box for each_box in each_unit if each_digit in values[each_box]]
            if len(solutions) == 1:
                values[solutions[0]] = each_digit
    return values


def reduce_puzzle(values):
    """
    Args:
        values(dict): The sudoku in dictionary form
    This is an iterative calls (steps) to multiple functions defined earlier until there is no further reduction possible.
    First, this function finds all the solved boxes
    Second, call the eliminate() function and prune the possibilities from each of the peers
    Third, it calls the naked_twins and only_choice functions for reduction.  

    """

    solved = [box for box in values.keys() if len(values[box])]
    counter = False
    
    while not counter:
        values_before = [] #list containing values before
        for box in values.keys():
            if len(values[box]) == 1:
                values_before.append(box)
        solved_before = len(values_before)
        
        #Eliminate choices, implement strategy and pick the best choice 
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)

        values_after = []
        for box in values.keys():
            if len(values[box]) == 1:
                values_after.append(box)
        solved_after = len(values_after)

        counter = solved_before == solved_after
        
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Recursive search for solving sudoku
    """
    values = reduce_puzzle(values)

    if values is False:
        return False

    if all(len(values[s]) == 1 for s in boxes):
        return values  
    
    #find the correct square 
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    print 'n,s', n,s

    for value in values[s]:
        nu_sudoku = values.copy()
        nu_sudoku[s] = value
        attempt = search(nu_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solution = search(values)
    #print 'solution',solution
    return solution

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
