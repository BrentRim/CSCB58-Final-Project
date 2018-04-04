
import sys
import csv
import random

X = 256
Y = 128
WIDTH = 3

# format for the initial.mif file
START_TEXT = """
WIDTH={};
DEPTH={};

ADDRESS_RADIX=UNS;
DATA_RADIX=UNS;

CONTENT BEGIN
	[0..{}]		:	0;
""".format(WIDTH, X * Y, X * Y - 1)

END_TEXT = """
END;
"""

EASINESS_FACTOR = 30 # increase for less stuff on the screen (more black)

def generate_tank_map(csv_path=None, outpath="initial.mif"):
    ''' (.csv file) -> set of int
    Takes in a .csv file, and returns an initial.mif file which is the
    map of the tank game. If no .csv file is used, then it will create a 
    random map. The map will consist of green, turquoise/teal, and
    yellow squares. Green and turquoise represent blocks which the tank
    cannot move through. The tank can shoot green blocks and destroy them,
    but the turquoise blocks cannot be destroyed. Yellow represents mines
    which will kill the tank if they step on it.
    Note: if a random map is to be generated, the map will look very
    maze-like, and it will create blocks of size 2x2 in order to look
    nicer and for better gameplay.
    '''
    tank_map = {}
    exception_message = "Non-empty cells can only contain 2, 3, or 6."
    if csv_path == None:
        #for index in range(X * Y):
        
        # for loop is designed like this to create blocks that are 2x2
        # this is so the game looks nicer, and it's cleaner to work with
        for i in range(0, Y, 2):
            for j in range(0, X, 2):
                if (i,j) in [(0,0), (118,158)]: # skip these starting blocks
                    continue
                value = random.randrange(EASINESS_FACTOR)
                for index in [j * Y + i, j * Y + i + 1, (j + 1) * Y + i, 
                              (j + 1) * Y + i + 1]:
                    if value in [0, 1]:
                        tank_map[index] = "3" # turquoise/teal block
                        
                    elif value in [2, 3, 4, 5, 6]:
                        tank_map[index] = "2" # green block
                    elif value in [7]:
                        tank_map[index] = "6" # yellow mine
                    # if it reached here, no blocks/mines drawn (black)

    # does the same thing as above, except it reads from a .csv file 
    # you drew out on excel                
    else: 
        reader = csv.reader(open(csv_path))
        i = 0
        for row in reader:
            j = 0
            for value in row:
                index = j * Y + i
                if len(value) > 0:
                    if value not in ["2", "3", "6"]:
                        raise Exception(exception_message)
                    tank_map[index] = value
                j += 1
            i += 1
    outfile = open(outpath, "w")
    outfile.write(START_TEXT)
    for index, value in tank_map.items():
        if index < X * Y:
            outfile.write("	{}  	:	{};\n".format(index, value))
    outfile.write(END_TEXT)
    outfile.close()

if __name__ == "__main__":
    # COMMENT AND UNCOMMENT THE ONES YOU WANT

    # this one uses a map you've drawn
    generate_tank_map("source.csv")

    # this one generates a random map
    #generate_tank_map()
