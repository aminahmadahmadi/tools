import math

# https://wikimedia.org/api/rest_v1/media/math/render/svg/f4b1a0904e2e946949995880e64e8baf9ac0afe7
latmax = math.degrees(2*math.atan(math.e**math.pi)-math.pi/2)
# print(latmax)


def latlon2pixel(lat, lon, zoom):
    # https://wikimedia.org/api/rest_v1/media/math/render/svg/996310dc648c9bbfec7a98fcc03224798042c74d
    # https://en.wikipedia.org/wiki/Web_Mercator_projection

    lat = latmax if lat > latmax else lat
    lat = -latmax if lat < -latmax else lat

    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    n = math.pow(2.0, zoom)

    pX = int(math.floor(128*n*(math.pi+lon_rad)/math.pi))
    pY = int(math.floor(
        128*n*(math.pi-math.log(math.tan((math.pi+2*lat_rad)/4)))/math.pi))

    return (pX, pY)


def tileNolatlon(tileFolderNo, tilePicNo, zoom):
    lon = tileFolderNo * 360 / 2**zoom - 180
    lat = latmax - tilePicNo * 2 * latmax / 2**zoom
    return (lat, lon)


def latlon2pixeltile(lat, lon, zoom, tileFolderNo, tilePicNo, zoomTile):
    x, y = latlon2pixel(lat, lon, zoom+1)
    lattop, lonleft = tileNolatlon(tileFolderNo, tilePicNo, zoomTile)
    xleft, ytop = latlon2pixel(lattop, lonleft, zoom)
    x = (x - xleft)/2
    y = (y - ytop)/2

    return (x, y)
