import PIL
from PIL import Image
from random import randint

def assign_color_value(elevation):
    """This math is dirty and confined to this assignment, wouldn't work elsewhere"""
    assigned_color = (elevation // 10) - 310
    return assigned_color

def choose_closest_elevation(x, y):
    """chooses closest elevation change block and stores the amount of change for use
    in determining the ideal path"""
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

class Draw:
    """Drawing object contains different drawing methods"""
    def __init__(self):
        self.y = 0
        self.x = 0

    def mapdraw(self):
        while self.y < 600:
            """prints map"""
            while self.x < 600:
                """prints each line of map"""
                emap.putpixel((self.x, self.y), (assign_color_value(llist[self.y][self.x]), assign_color_value(llist[self.y][self.x]), assign_color_value(llist[self.y][self.x])))
                self.x += 1

            self.y += 1
            self.x = 0

    def pathdraw(self):
        self.y = 0
        self.origin = 0
        self.elevation_change_total = 0
        self.prev_total = 99999
        self.shortest_origin = 0
        emap.putpixel((self.x, self.y), (255, 0, 0))

        while self.origin < 600:
            """prints all the paths"""
            while self.x < 599:
                """prints individual paths and chooses route"""
                self.output = choose_closest_elevation(self.x, self.y)
                self.x += self.output[0]
                self.y += self.output[1]
                self.elevation_change_total += self.output[2]
                emap.putpixel((self.x, self.y), (255, 0, 0))
            if self.elevation_change_total < self.prev_total:
                self.prev_total = self.elevation_change_total
                self.shortest_origin = self.origin
            self.elevation_change_total = 0
            self.origin += 1
            self.y = self.origin
            self.x = 0

    def idealdraw(self):
        self.y = self.shortest_origin
        while self.x < 599:
            """prints the ideal path"""
            self.output = choose_closest_elevation(self.x, self.y)
            self.x += self.output[0]
            self.y += self.output[1]
            emap.putpixel((self.x, self.y), (255, 255, 0))

with open('elevation_small.txt') as file:
    llist = [[int(num) for num in line.split()] for line in file]

emap = Image.new('RGBA', (600, 600))
d = Draw()
d.mapdraw()
d.pathdraw()
d.idealdraw()
emap.save('map.png')