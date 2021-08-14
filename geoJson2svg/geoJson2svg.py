# from os import close
import latlon2pixel
import geojson
from svg import Svg

# ------------------------------------------------
zoom = 7  # zoom DPI
# ------------------------------------------------
zoomTile = 3  # size of artboard
scl = 2  # height / width

# top left tile in zoomTile
folder = 5 
pic = 2
top = 2
bottom = 3
left = 5
right = 5
# ------------------------------------------------


Dir = 'geoJson2svg\\World_Countries.geojson'

with open(Dir) as f:
    gj = geojson.load(f)
features = gj['features']


mySvg = Svg('geoJson2svg', 256*2**(zoom-zoomTile), scl*256*2**(zoom-zoomTile))
mySvg.addStyle(
    'country', f'fill:white;stroke:#ddd;stroke-width:{2**(zoom-7)};stroke-linecap:round;stroke-linejoin:round;')
mySvg.addStyle('country:hover', 'fill:#eee;')
mySvg.addStyle(
    'sea', f'fill:#00f;stroke:#ddd;stroke-width:{2**(zoom-7)};stroke-linecap:round;stroke-linejoin:round;')
mySvg.addStyle('tile0', f'fill:#00f;stroke:#00f;stroke-width:{2**(zoom-7)}')
mySvg.addStyle('tile1', 'fill:#00e;')


mySvg.openGroup()
for i in range(0, mySvg.width, 256):
    for j in range(0, mySvg.height, 256):
        mySvg.addRect(i, j, 256, 256, class_=f'tile{int((i+j)/256)%2}')
mySvg.closeGroup()

mySvg.openGroup()

for feature in features:
    for country in feature['geometry']['coordinates']:
        mySvg.openGroup()
        for path in country:
            points = path
            # list(map(lambda x, y: int(x), int, points))
            # for p in points:
            #     print(p)
            points = list(
                map(lambda p: latlon2pixel.latlon2pixeltile(p[1], p[0], zoom, folder, pic, zoomTile), points))

            show = False
            for p in points:
                if p[0] > -256 and p[0] < mySvg.width+256 and p[1] > -256 and p[1] < mySvg.height+256:
                    show = True
            if show:
                print(feature['properties']['COUNTRYAFF'])
                # for p in points:
                # print(p)
                # mySvg.addCloseCurve(points, class_='country')
                mySvg.addPolygon(points, class_='country')

        mySvg.closeGroup()
        if mySvg.objects[-2] == '<g>':
            mySvg.objects = mySvg.objects[:-2]

mySvg.closeGroup()

Dir = 'geoJson2svg\\North_WGS84.json'

with open(Dir) as f:
    gj = geojson.load(f)
features = gj['features']

# for feature in features:
feature = features[0]
shape = feature['geometry']['coordinates'][1]
mySvg.openGroup()
for path in shape:
    points = path
    points = list(
        map(lambda p: latlon2pixel.latlon2pixeltile(p[1], p[0], zoom, folder, pic, zoomTile), points))

    show = False
    for p in points:
        if p[0] > 0 and p[0] < mySvg.width and p[1] > 0 and p[1] < mySvg.height:
            show = True
    if show:
        # print(feature['properties']['COUNTRYAFF'])
        mySvg.addPolygon(points, class_='sea')
mySvg.closeGroup()
if mySvg.objects[-2] == '<g>':
    mySvg.objects = mySvg.objects[:-2]

mySvg.save('geoJson2svg')
