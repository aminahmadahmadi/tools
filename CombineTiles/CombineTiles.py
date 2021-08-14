import sys
from PIL import Image
import os
import math


def combineTiles(Dir, name='', Mode='RGB', automatic_Find=True, folder_min=0, folder_max=0, pic_min=0, pic_max=0, tiles_format='.png'):
    Wsize = os.get_terminal_size()[0]-60
    if Mode == 'RGB':
        colorBack = 'white'
    elif Mode == 'RGBA':
        colorBack = (255, 255, 255, 0)
    print(Dir)
    # automatic find
    auto = automatic_Find
    # pictures
    row_min = pic_min
    row_max = pic_max
    # folders
    col_min = folder_min
    col_max = folder_max
    # tile size
    width = 256
    height = 256

    # list of folders

    if auto:
        col_min, col_max, row_min, row_max = findMinMax(Dir, tiles_format)

    else:
        folders = list(range(col_min, col_max+1))

        for folder in folders:
            try:
                os.mkdir(Dir+'\\'+str(folder))
            except:
                pass

    print(f'col min : {col_min}')
    print(f'col max : {col_max}')
    print(f'row min : {row_min}')
    print(f'row max : {row_max}')

    row_no = row_max - row_min + 1
    col_no = col_max - col_min + 1

    for i in range(col_min, col_max + 1):
        tiles = []
        for j in range(row_min, row_max + 1):
            try:
                tile = Image.open(f'{Dir}\\{i}\\{j}{tiles_format}')
                tiles.append(tile)
            except:
                if Mode == 'RGB':
                    if (i+j) % 2 == 0:
                        c = 'white'
                    else:
                        c = '#eeeeee'
                elif Mode == 'RGBA':
                    c = (255, 255, 255, 0)

                tile = Image.new(Mode, (width, height), color=c)
                tiles.append(tile)

        new_im = Image.new(Mode, (width, row_no * height), colorBack)

        y_offset = 0
        for tile in tiles:
            if Mode == 'RGB':
                new_im.paste(tile, (0, y_offset))
            elif Mode == 'RGBA':
                new_im.paste(tile, (0, y_offset), tile)
            y_offset += height

        new_im.save(f'{Dir}\\{i}\\col.png')
        progressbar('Create Columns', col_min, i, col_max, Wsize)

    cols = [Image.open(f'{Dir}\\{j}\\col.png')
            for j in range(col_min, col_max + 1)]

    print(int(col_no * width), 'x', int(row_no * height))

    final_image = Image.new(
        Mode, (int(col_no * width), int(row_no * height)), colorBack)

    x_offset = 0
    for col in cols:
        final_image.paste(col, (x_offset, 0))
        progressbar('Combine Columns', col_min, col_min +
                    round(x_offset/width), col_max, Wsize)
        x_offset += width

    try:
        os.mkdir(f'{Dir}\\.files\\')
    except OSError:
        print('', end='')

    dir_ = Dir.split('\\')
    final_image.save(
        f'{Dir}\\.files\\{Mode}_{name}-{dir_[-1]}_{row_min}-{row_max+1}_{col_min}-{col_max+1}.png')
    print('File saved.')
    Cleaner(Dir)

    print(
        f'{Mode}_{name}-{dir_[-1]}_{row_min}-{row_max+1}_{col_min}-{col_max+1} Done\n')


def findMinMax(Dir, tiles_format):
    rowset = False
    dirs = os.listdir(Dir)
    try:
        dirs.remove('.files')
    except:
        pass
    dirs = list(map(lambda x: int(x), dirs))
    f_min = min(dirs)
    f_max = max(dirs)
    folders = list(range(f_min, f_max+1))

    col_min = f_min
    col_max = f_max

    for folder in folders:
        try:
            os.mkdir(Dir+'\\'+str(folder))
        except:
            dirs = os.listdir(Dir+'\\'+str(folder))
            try:
                dirs.remove('col.png')
            except:
                pass
            dirs = list(map(lambda x: int(x[:-len(tiles_format)]), dirs))

            if len(dirs) != 0:
                p_min = min(dirs)
                p_max = max(dirs)

                if rowset == False:
                    row_min = p_min
                    row_max = p_max
                    rowset = True

                if p_min < row_min:
                    row_min = p_min
                if p_max > row_max:
                    row_max = p_max

    return col_min, col_max, row_min, row_max


def Cleaner(Dir):
    folders = os.listdir(Dir)
    try:
        folders.remove('.files')
    except:
        pass
    for folder in folders:
        try:
            os.remove(f'{Dir}\\{folder}\\col.png')
        except:
            pass
        try:
            os.rmdir(f'{Dir}\\{folder}')
        except:
            pass


def progressbar(name, Min, no, Max, num):
    if num < 0:
        num = 0
    Min = int(Min)
    Max = int(Max)
    diff = Max-Min
    scl = num/diff

    if no >= Min and no < Max:
        bar = f'> {name:>20}:{round((100/num)*scl*(no-Min)):3}%   '
        for _ in range(round(scl*(no-Min))):
            bar += '█'
        for _ in range(round(scl*(Max-no))):
            bar += '░'
        bar += f'   {no:6}   {(no%10+1)*"#":11}'
        try:
            print(bar, end="\r")
        except:
            print(bar.replace('█', '$').replace('░', '-'), end="\r")
    else:
        print(f'> {name} Done!{100*" "}')


for Dir in [
    # 'CombineTiles\\Z4',
    'D:\\KND\\PMO\\density map\\inbox\\densitymap\\total\\Z9',
]:

    zoomTile = 3  # area of tile like one tile in this zoom
    ratio = 2  # height / width

    # zoom 4 tile numbers
    top = 5
    bottom = 8
    left = 10
    right = 11

    # -----------------------------------------------------------------------------

    zoom = int(Dir.split('\\')[-1][1:])

    if zoom-zoomTile > 7:
        zoomTile = zoom - 7
        ratio = 1

    z = 1/2**(4-zoomTile)
    scl = 2 ** (zoom-zoomTile)

    # tile no
    top = int(math.floor(top*z)*scl)
    bottom = int(math.floor(bottom*z)*scl)
    left = int(math.floor(left*z)*scl)
    right = int(math.floor(right*z)*scl)

    bottom += 1 if top == bottom else 0
    right += 1 if left == right else 0

    name = Dir.split("\\")[-2]
    name = f'{name}_Ztile{zoomTile}'

    for i in range(left, right, int(scl)):
        for j in range(top, bottom, int(ratio*scl)):
            print(i, j)
            combineTiles(f"{Dir}", name, 'RGBA', False, i, i +
                         int(scl)-1, j, j+int(ratio*scl)-1)
