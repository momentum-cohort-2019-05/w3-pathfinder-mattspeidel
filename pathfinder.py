import PIL
from PIL import Image
from random import randint

def assign_color_value(elevation):
    """This math is dirty and confined to this assignment, wouldn't work elsewhere"""
    assigned_color = (elevation // 10) - 310
    return assigned_color

with open('elevation_small.txt') as file:
    llist = [[int(num) for num in line.split()] for line in file]

y = 0
x = 0

def choose_closest_elevation(x, y):
    while True:  
        try:
            top = llist[y - 1][x + 1]
        except IndexError:
            top = 0
        try:
            middle = llist[y][x + 1]
        except IndexError:
            middle = 0
        try:
            bottom = llist[y + 1][x + 1]
        except IndexError:
            bottom = 0
        output = []
        closest = min(top, middle, bottom, key=lambda delta:abs(delta - llist[y][x]))
        if closest == middle:
            output = [1, 0, abs(llist[y][x]-closest)]
            return output

        elif closest == top and closest == bottom:
            coinflip = randint(0, 1)
            if coinflip == 0:
                output = [1, -1, abs(llist[y][x]-closest)]
                return output
            else:
                output = [1, 1, abs(llist[y][x]-closest)]
                return output

        elif closest == bottom:
            output = [1, 1, abs(llist[y][x]-closest)]
            return output

        elif closest == top:
            output = [1, -1, abs(llist[y][x]-closest)]
            return output

emap = Image.new('RGBA', (600, 600))

while y < 600:
    """prints map"""
    while x < 600:
        """prints each line of map"""
        emap.putpixel((x, y), (assign_color_value(llist[y][x]), assign_color_value(llist[y][x]), assign_color_value(llist[y][x])))
        x += 1

    y += 1
    x = 0

y = 0
origin = 0
elevation_change_total = 0
prev_total = 99999
shortest_origin = 0
emap.putpixel((x, y), (255, 0, 0))

while origin < 600:
    """prints all the paths"""
    while x < 599:
        """prints individual paths and chooses route"""
        output = choose_closest_elevation(x, y)
        x += output[0]
        y += output[1]
        elevation_change_total += output[2]
        emap.putpixel((x, y), (255, 0, 0))
    if elevation_change_total < prev_total:
        prev_total = elevation_change_total
        shortest_origin = origin
    elevation_change_total = 0
    origin += 1
    y = origin
    x = 0

y = shortest_origin
while x < 599:
    output = choose_closest_elevation(x, y)
    x += output[0]
    y += output[1]
    emap.putpixel((x, y), (255, 255, 0))

emap.save('map.png')