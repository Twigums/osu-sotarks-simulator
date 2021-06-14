import numpy as np

# Reads the files based on the path and returns the first 3 values which are [x, y, offset]
def read(path):
    with open(path, "r") as f:
        doc = f.readlines()

    lines = np.size(doc)
    numbers = np.zeros([lines, 3])

    for i in range(lines):
        line = doc[i].replace(",", " ")
        line.replace(":", " ")
        numbers[i, :] = line.split()[:3]

    return numbers

# Connects the x and y values to the original file so it can be easily c+p into the osu map file
def join(i, path, x, y):

    with open(path, "r") as f:
        doc = f.readlines()

    [useless, useless2, rest] = doc[i].split(sep = ",", maxsplit = 2)
    final = ",".join([x, y, rest])

    return final

# Given the previous two points and the offsets of the 2nd and newly generated point, will it fit these params and if it does, returns the [x, y]
def check(p1, p2, off1, off2, diff):

    boundCheck = False # boundary check to ensure the points are in the frame (redundant/should always return true)
    dotCheck = False # checks to see if the angle between p1 -> p2 -> [x, y] are acute
    distCheck = False # checks the distance between the two points (helpful for specific cases as defined below)

    while boundCheck == False or dotCheck == False or distCheck == False:
        boundCheck = False
        dotCheck = False
        distCheck = False

        x = np.random.randint(0, 512)
        y = np.random.randint(0, 384)

        distance = np.sqrt((x - p2[0]) ** 2 + (y - p2[1]) ** 2)

        if y > 0 and y < 384 and x > 0 and x < 512:
            boundCheck = True

        if np.dot(p1 - p2, [x, y] - p2) > 0:
            dotCheck = True

        if abs(off1 - off2) > diff * 0.90 and abs(off1 - off2) < diff * 2.15: # case of regular jumps

            if distance > 100:
                distCheck = True

        elif abs(off1 - off2) < diff * 0.75: # case of streams

            if distance < 40:
                distCheck = True

        else: # other cases
            distCheck = True

    return [x, y]

f = read("input.txt") # defines the file to read
row = np.size(f, 0) # gets the number of rows

diff = 10883 - 10725
p1 = f[0, :2]
p2 = f[1, :2]
arr = []

for i in range(row - 1): # since it makes a new [x, y], we need to read until row - 1
    off1 = f[i, 2]
    off2 = f[i + 1, 2]
    [x, y] = check(p1, p2, off1, off2, diff)

    arr.append(x)
    arr.append(y)
    p1 = p2
    p2 = np.array([x, y])

for i in range(np.size(arr) // 2): # uses the array from the previous for loop to input and print out the finished line to c+p
    final = join(i, "input.txt", str(arr[2 * i - 2]), str(arr[2 * i - 1]))
    print(final)
