backtracks = 0
btracks = 0

# The primary function that solves the SudokuBoard bo
def solveSudoku(bo, i = 0, j = 0):
    global backtracks
    i, j = find_empty(bo)
    if i == -1:
        return True # Meaning we did not find any other element, SOLVED SUDOKU
    for num in range(1, 10):
        if isValid(bo, i, j, num): # are we allowed to place num here?
            bo[i][j] = num # YES

            # Now we try to recursively finish the board by calling SolveSudoku
            # on the new updated board with the new board
            # We keep trying and trying untill we either SOLVED SUDOKU
            if(solveSudoku(bo, i, j)):
                return True

            # The last element we added is incorrect therfore get back
            backtracks+=1 # a counter to keep track how many times we went back
            bo[i][j] = 0 # reset this value and check back again!

    return False # or we tried all numbers and none of them is valid



# A WAY TO MAKE IMPROVEMENTS BY MAKING IMPLICATIONS!

# What we can do is, make some implication i.e. a prior decision that okay at
# some particular position I will enter this number ( the human way) and then
# do my recursive steps. Now this implication made can be good or bad. Yes it
# was made keeing in mind the three prime constraints of Sudoku, but when further
# updations are being made into the Sudoku board there will be moments when it is
# needed to undo all the changes that were made after the implication was made.
#
# This can greatly reduce the number of backtracks innvolved if done correctly.
# It is a more 'Human way' of approaching the problem to Optimize it greatly.
# We can make repetitive implications till we run out of implications to get the
# best results.


sectors = [ [0, 3, 0, 3], [3, 6, 0, 3], [6, 9, 0, 3],
            [0, 3, 3, 6], [3, 6, 3, 6], [6, 9, 3, 6],
            [0, 3, 6, 9], [3, 6, 6, 9], [6, 9, 6, 9] ]
#This gives grid indices for each of the sectors
#example in the 3rd sector(talking index wise)i.e. 1st row and 0th column
#Column can go from 0 to 3 --> 0 OR 1 OR 2 Along X (left to right direction)
#Row can go from 3 to 6 -----> 3 OR 4 OR 5 Along Y (downward direction)


# This procedure fills in the missing squares of a Sudoku puzzle
#obeying the Sudoku rules by guessing when it has to and performing
#implications when it can
def solveSudokuOpt(bo, i = 0, j = 0):

    global btracks

    #find the next empty cell to fill
    i, j = find_empty(bo)
    if i == -1:
        return True


    for e in range(1, 10):
        #Try different values in i, j location
        if isValid(bo, i, j, e):

            impl = makeImplications(bo, i, j, e) # REPETITVE IMPLICATIONS MADE
            # It is necessary to store the implications made at i,j
            # bo[i][j] = e is remember in impl so that it can be reversed
            if solveSudokuOpt(bo, i, j):
                return True
            # Undo the current cell for backtracking
            btracks += 1
            undoImplications(bo, impl) # The implication made was INCORRECT!

    return False


#This procedure makes implications based on existing numbers on squares
def makeImplications(grid, i, j, e):

    global sectors

    grid[i][j] = e # We have implied this number onto the location
    impl = [(i, j, e)] # A list of 3 tuples represeting grid[i][j] = e

    done = False

    #Keep going till you stop finding implications
    while not done:
        done = True

        for k in range(len(sectors)): # For each sector

            sectinfo = [] # this is going to be maintained for each sect
            # it is a3 element tuple (x coord, y coord, set)

            #find missing elements in ith sector
            vset = {1, 2, 3, 4, 5, 6, 7, 8, 9} # a set of possible values

            # going through the elements in the sector and
            # remove these elements from vset using the remove function
            for x in range(sectors[k][0], sectors[k][1]):
                for y in range(sectors[k][2], sectors[k][3]):
                    if grid[x][y] != 0:
                        vset.remove(grid[x][y])

            # THE TWO FOR LOOPS ARE USED TO ITERATE OVER A SECTOR
            # MAKING USE OF THE INDICES THAT WE SPECIFIED
            # For example k = 3 from the sectors variable...
            # range(sectors[k][0], sectors[k][1]) is --> range(0, 3) X
            # range(sectors[k][2], sectors[k][3]) is --> range(3, 6) Y

            # attach copy of vset to each missing square in ith sector
            # saying that one of these is values is going to be your final
            # value ( iff we reduce to a singleton)
            for x in range(sectors[k][0], sectors[k][1]):
                for y in range(sectors[k][2], sectors[k][3]):
                    if grid[x][y] == 0:
                        sectinfo.append([x, y, vset.copy()])

            for m in range(len(sectinfo)):
                sin = sectinfo[m] # sin is also a 3 element tuple
                # it contains the info for the current sector
                # say for sector[0] it has the info for all squares
                # and there corresponding set possiblities grid[x][y] = {set}
                # as--> [x, y, set]

                #find the set of elements on the row corresponding to m and remove them
                rowv = set()
                for y in range(9):
                    rowv.add(grid[sin[0]][y])

                # remove from the corresponding set the elements in the rows of
                # the current sector
                left = sin[2].difference(rowv)

                #find the set of elements on the column corresponding to m and remove them
                colv = set()
                for x in range(9):
                    colv.add(grid[x][sin[1]])
                left = left.difference(colv)

                #check if the vset is a singleton
                if len(left) == 1:
                    val = left.pop() # we take the implication as final

                    if isValid(grid, sin[0], sin[1], val):
                        grid[sin[0]][sin[1]] = val
                        impl.append((sin[0], sin[1], val))
                        done = False

    return impl

#This procedure undoes all the implications
def undoImplications(grid, impl):
    for i in range(len(impl)):
        grid[impl[i][0]][impl[i][1]] = 0
    return



# It take the partially filled in Sudoku board as an input and checks
# whether putting s num at the pos is allowed or not
def isValid(bo, i, j, num):
    rowOk = all([num!= bo[i][x]  for x in range(9)])
    #all will Return True if all elements of the iterable are true
    if rowOk:
        columnOk = all([num!= bo[x][j]  for x in range(9)])
        if columnOk:
            secTopX, secTopY = 3 *(i//3), 3 * (j//3)
            for x in range(secTopX, secTopX+3):
                for y in range(secTopY, secTopY + 3):
                    if(bo[x][y] == num):
                        return False
            return True
    return False

#A simple printing function that prints the Sudoku board

def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


#the function is used to find the next empty cell in the given grid
def find_empty(bo):
    for i in range(0,9):
        for j in range(0,9):
            if bo[i][j] == 0:
                return i, j # the first encountered empty row and the column
    return -1, -1

diff  = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

print(solveSudoku(diff))
print_board(diff)
print ('Backtracks = ', backtracks)
