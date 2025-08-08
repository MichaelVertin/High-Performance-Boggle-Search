import time
import pdb
startTime = time.time()

import sys
OUTPUT_FILE = "board4_words.txt"
yPos = 0 # rows
xPos = 1 # columns

def loadBoard( fileName ):
    # add all lines from filename into board, excluding whitespace
    return [line.lower().split() for line in open( fileName )]

def possibleMoves(xy_pair, board_object):
    # lists of possible_x and possible_y values:
        # starts with current x and y values
    possible_x = [ xy_pair[ xPos ] ]
    possible_y = [ xy_pair[ yPos ] ]

    # loop over edges
    for test_adjust in (-1,1):
        # test at each x/y for test_adjust
        test_x = xy_pair[xPos] + test_adjust
        test_y = xy_pair[yPos] + test_adjust

        # append position to possible coordinate in range
        if( test_x < len( board_object ) and test_x >= 0 ):
            possible_x.append( test_x )
        if( test_y < len( board_object ) and test_y >= 0):
            possible_y.append( test_y )

    # find all permutations of possible x/y, store in possible_coor
    possible_coor = { (y_coor,x_coor) for x_coor in possible_x \
                                      for y_coor in possible_y }

    # remove original
    possible_coor.remove( xy_pair )

    return possible_coor

def legalMoves( potentialMoves, previousStates ):
    nonRepeating = set() # set to contain non repeating positions

    # iterate over positions in potential moves
    for position in potentialMoves:
        if position not in previousStates:
            # add if not previously included
            nonRepeating.add( position )

    return nonRepeating

def examineState( boggleBoard, nextPosition, currentPositions, myDict ):
    testWord = str() # initialize string for new word

    # iterate over xs and ys in current positions and next position
    for wkgX, wkgY in ( currentPositions + [ nextPosition ] ):
        # add character at x/y to word
        testWord += boggleBoard[ wkgY ][ wkgX ]
    
    inDictState = testWord in myDict
    return testWord, inDictState

def runBoard( boardFile, dictFile ):
    legalWords = set() # initialize legal words as set

    # load boggleBoard
    boardSet = loadBoard( boardFile )

    # board can be 'jumped'
    if False: #len( boardSet ) <= MAX_JUMPABLE_SIZE:
        legalWords = jumpBoggle( dictFile, boardSet )

    # board cannot be 'jumped'
    else:
        # create dictionary
        dictSet, beginsWithObject = readDictionary( dictFile )

        # find start positions as permutations of xs and ys in range of boardSet
        startPositions = [ ( startY, startX ) \
                           for startX in range( len( boardSet ) )\
                           for startY in range( len( boardSet ) ) ]
    
        for startPos in startPositions:
            findWords( boardSet, beginsWithObject, dictSet, [ startPos ], \
                       legalWords )


    # write all legalWords to file
    outputFile = boardFile.replace( ".txt", "_words.txt" )
    writeSetToFile( outputFile, legalWords )




def findWords( boggleBoard, beginsWithObject, dictSet, \
               usedPositions, legalWords ):
    # stop if usedPositions does not generate prefix in beginsWithObject
    if positionsToString( usedPositions, boggleBoard ) not in beginsWithObject:
        return False

    # get next legal moves
    nextMoves = legalMoves( possibleMoves( usedPositions[-1], boggleBoard ), \
                            usedPositions )

    # examine state corresponding to each nextMove
    for nextMove in nextMoves:
        # get word based on nextMove
        testWord, inDictState = examineState( boggleBoard, nextMove, \
                                              usedPositions, dictSet )
        # add to legalWords if found in dictionary
        if inDictState:
            legalWords.add( testWord )
    
    # recurse for each recursive move
    for nextRecursePos in nextMoves:
        nextUsed = usedPositions + [nextRecursePos]
        # recurse with the next recursion position
        findWords( boggleBoard, beginsWithObject, dictSet, nextUsed, \
                   legalWords )

def readDictionary(filename):
    myDict = set()
    beginsWithObject = set()

    # read all words in file
    for word in open(filename):
        # remove whitespace
        word = word.replace("\n", "")

        # add to dict
        myDict.add( word )

        # do not include last letter in word (exclusive)
        rangeMax = len( word )

        # iterate over selected indices
        for endIndex in range( 0, rangeMax ):
            prefix = word[:endIndex]
            beginsWithObject.add( prefix )

    return myDict, beginsWithObject


def positionsToString( positions, boardObj ):
    positionStr = str()
    for xPos,yPos in positions:
        # find characer reference of indices in boardObj
        positionStr += boardObj[yPos][xPos]
    return positionStr

def writeSetToFile( fileName, iterable ):
    # connect with newlines
    toWrite = "\n".join( sorted( iterable ) )
    #toWrite = "\n".join( iterable )
    with open( fileName, 'w' ) as file_object:
        file_object.write( toWrite )




########################## 2x2 board ###############################
def boardToString( boggleBoard ):
    boggleStr = str()
    for line in boggleBoard:
        for char in line:
            boggleStr += char
    return boggleStr

def readDictLimited( limit, filename ):
    # adjust for newline char
    adjustLimit = limit + 1
    
    myDict = set()
    for word in open( filename ):
        # add if less than/equal to limit
        if len( word ) <= adjustLimit:
            myDict.add( word[:-1] )
    return myDict

def findPermutations( remainingList, limit, currentPermutations = set(), \
                      startList = str() ):
    # iterate over all remaining characters
    for char in remainingList:
        # add character for next start
        nextStart = startList + char

        # remove character from remaining
        nextRemaining = remainingList.replace( char, '' )

        # find all permutations using next start and remaining
        currentPermutations = findPermutations( nextRemaining, limit, \
                                                currentPermutations, nextStart )

        # add to currentPermutations if found in limit
        if nextStart in limit:
            currentPermutations.add( nextStart )
    
    return currentPermutations

# boggle game, except any position can be reached from any other position
    # occurs naturally in 1x1 and 2x2 boards
def jumpBoggle( dictFileName, boggleBoard ):
    # convert board into string
    boggleStr = boardToString( boggleBoard )

    # read dictionary, limited to word size = area of board
    myDict = readDictLimited( len( boggleBoard ) ** 2, dictFileName )

    # find all permutations boggleStr that are in myDict
    perm = findPermutations( boggleStr, myDict, set(), str() )

    return perm

 

runBoard( sys.argv[1], sys.argv[2] )

endTime = time.time()
print( f"Total time = {endTime - startTime}" )



