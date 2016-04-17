import random

map = []

def first(y):
    det = random.randint(1, 100)                
    if det >= 80:
        map[y].append(4)
    if det >= 50 and det < 80:
        map[y].append(1)
    if det >= 20 and det < 50:
        map[y].append(2)
    if det < 20:
        map[y].append(3)

def generateBy1(y):
    det = random.randint(1,100)
    if det >= 90:
        map[y].append(4)
    if det >= 40 and det < 90:
        map[y].append(1)
    if det >= 15 and det < 40:
        map[y].append(2)
    if det < 15:
        map[y].append(3)

def generateBy2(y):
    det = random.randint(1,100)
    if det >= 90:
        map[y].append(4)
    if det >= 65 and det < 90:
        map[y].append(1)
    if det >= 15 and det < 65:
        map[y].append(2)
    if det < 15:
        map[y].append(3)

def generateBy3(y):
    det = random.randint(1,100)
    if det >= 90:
        map[y].append(4)
    if det >= 70 and det < 90:
        map[y].append(1)
    if det >= 50 and det < 70:
        map[y].append(2)
    if det < 50:
        map[y].append(3)

def generateBy4(y):
    det = random.randint(1,100)
    if det >= 70:
        map[y].append(4)
    if det >= 40 and det < 70:
        map[y].append(1)
    if det >= 10 and det < 40:
        map[y].append(2)
    if det < 10:
        map[y].append(3)

def GenerateMap(MaxX, MaxY):
    for y in range(MaxY):
        map.append([])
        for x in range(MaxX):
            if map == [[]]:
                first(y)
            else:
                if y == 0:
                    ## first line ##
                    if map[y][x-1] == 1:
                        generateBy1(y)
                    elif map[y][x-1] == 2:
                        generateBy2(y)
                    elif map[y][x-1] == 3:
                        generateBy3(y)
                    elif map[y][x-1] == 4:
                        generateBy4(y)
                elif x-1 < 0:
                    if map[y-1][x] == 1:
                        generateBy1(y)
                    elif map[y-1][x] == 2:
                        generateBy2(y)
                    elif map[y-1][x] == 3:
                        generateBy3(y)
                    elif map[y-1][x] == 4:
                        generateBy4(y)
                else:
                    if map[y][x-1] == 1:
                        generateBy1(y)
                    elif map[y][x-1] == 2:
                        generateBy2(y)
                    elif map[y][x-1] == 3:
                        generateBy3(y)
                    elif map[y][x-1] == 4:
                        generateBy4(y)

GenerateMap(15, 5)
print(map)
