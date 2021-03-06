import readsketchup
import eplusgeom



def makeidf(txt):
    """make idff file from the file generated by sketchup"""
    dct = readsketchup.readsketchup(txt)
    dct = readsketchup.duplicatewindows(dct)
    dct = readsketchup.inch2meters(dct)
    zonestxt = eplusgeom.makezones(dct)
    wallstxt = eplusgeom.makewalls(dct)
    windowstxt = eplusgeom.makewindows(dct)

    snippet1 = """
VERSION,
    1.3;                     !- Version Identifier

!-   ===========  ALL OBJECTS IN CLASS: BUILDING ===========

BUILDING,
    Building,                !- Building Name
    0.,                      !- North Axis {deg}
    City,                    !- Terrain
    0.04,                    !- Loads Convergence Tolerance Value {W}
    0.4,                     !- Temperature Convergence Tolerance Value {deltaC}
    FullExterior,            !- Solar Distribution
    25;                      !- Maximum Number of Warmup Days


"""
    snippet2 = """
!-   ===========  ALL OBJECTS IN CLASS: SURFACEGEOMETRY ===========

SurfaceGeometry,
    UpperLeftCorner,         !- SurfaceStartingPosition
    CCW,        !- VertexEntry
    WCS;                     !- CoordinateSystem


"""


    eplustxt = snippet1 + zonestxt + snippet2 + wallstxt + windowstxt
    eplustxt = eplustxt.replace('\n', '\r\n')
    return eplustxt



if __name__ == '__main__':
    txt = open('e.txt', 'r').read()
    eplustxt = makeidf(txt)
    open('ee.idf', 'wb').write(eplustxt)
