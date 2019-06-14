import PIL
from PIL import Image

def assign_color_value(elevation):
    assigned_color = (elevation // 10) - 310
    return assigned_color

with open('elevation_small.txt') as file:
    llist = [[int(x) for x in line.split()] for line in file]

max_elevation = [max(max(num) for num in llist)].pop()
min_elevation = [min(min(num) for num in llist)].pop()

y = 0
x = 0
map = Image.new('RGBA', (600, 600))

while y < 600:
    while x < 600:
        map.putpixel((x, y), (assign_color_value(llist[y][x]), assign_color_value(llist[y][x]), assign_color_value(llist[y][x])))
        x += 1

    y += 1
    x = 0
map.save('map.png')
    






