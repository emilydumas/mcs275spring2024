# MCS 275 Spring 2024 Project 2 Starter Pack
# David Dumas
"""
Class library for working with labyrinths---maze-like structures
with walls, open spaces, and various kinds of obstacles.
"""

__version__ = "1.0"

import random
import json
import warnings
import functools
import gzip
import base64
from plane import Point2, Vector2

# Attempt to import PIL but recover gracefully if missing
try:
    import PIL.Image
    import PIL.ImageDraw

    _PIL_available = True
except ImportError:
    warnings.warn(
        "Bitmap image (PNG) features will not work because PIL/Pillow was not found."
        + "Try `python3 -m pip install pillow` if such support is needed."
    )
    _PIL_available = False


# Check for patched equality in plane
try:
    assert Point2(1, 1) != "a non-point object"
except Exception as e:
    raise RuntimeError(
        "You need a newer version of plane.py (see starter pack or github)"
    ) from e


def requiresPIL(func):
    "Decorator that makes a method/function fail unless PIL/Pillow is available"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        assert _PIL_available, "This feature requires PIL/Pillow."
        return func(*args, **kwargs)

    return wrapper


# Cell type constants
CT_WALL = 0  # wall: cell cannot be occupied
CT_START = 1
CT_GOAL = 2
CT_EMPTY = 3  # empty: cell can always be occupied
CT_PIT = 20  # pit: need to have a plank to occupy safely
CT_LOCK = 30  # lock: uses up a key to occupy this space
CT_SPRING = 40  # spring trap: occupying initiates flight (perhaps deadly)

CELL_TYPES = [CT_WALL, CT_START, CT_GOAL, CT_EMPTY, CT_PIT, CT_LOCK, CT_SPRING]
CELL_TYPE_NAMES = ["Wall", "Start", "Goal", "Empty", "Pit", "Lock", "Spring trap"]


class CellRenderer:
    """
    Utility class that decides how to display labyrinth cells
    in text or bitmap graphics
    """

    cell_chars = {
        CT_WALL: "\u2588",
        CT_EMPTY: " ",
        CT_PIT: "o",
        CT_LOCK: "?",
        CT_SPRING: "^",
        CT_START: "S",
        CT_GOAL: "G",
    }
    _cell_img_cache = {}

    @classmethod
    def char(cls, k):
        "Text graphics character for a cell type"
        return cls.cell_chars[k]

    @classmethod
    def svg_fragment(cls, k):
        "SVG fragment to render a cell type (planned future feature)"
        raise NotImplementedError

    @classmethod
    @requiresPIL
    def img(cls, k, scale=10, highlight=False):
        "PIL.Image object representing a cell type at a given scale"
        if (k, scale, highlight) in cls._cell_img_cache:
            return cls._cell_img_cache[(k, scale, highlight)]

        if k == CT_WALL:
            bg = (50, 50, 50)
        elif highlight:
            bg = (150, 150, 240)
        else:
            bg = (255, 255, 255)

        im = PIL.Image.new("RGB", (scale, scale), bg)
        if k in [CT_WALL, CT_EMPTY]:
            cls._cell_img_cache[(k, scale, highlight)] = im
            return im
        d = PIL.ImageDraw.Draw(im)
        inset = 1 + int(0.15 * scale)
        if k == CT_START:
            d.rectangle(
                [(inset, inset), (scale - 1 - inset, scale - 1 - inset)],
                fill=(200, 138, 75),
            )
        elif k == CT_GOAL:
            d.rectangle(
                [(inset, inset), (scale - 1 - inset, scale - 1 - inset)],
                fill=(68, 187, 68),
            )
        elif k == CT_PIT:
            w = scale - 2 * inset
            h = max(2, int(0.6 * w))
            d.ellipse(
                [
                    (inset, (scale - h) // 2),
                    (scale - 1 - inset, scale - 1 - ((scale - h) // 2)),
                ],
                fill=(220, 57, 57),
            )
        elif k == CT_LOCK:
            inset = 1 + int(0.20 * scale)
            r = max(1, (scale - 2 * inset) // 3)
            w = max(1, int(1.5 * r))
            d.ellipse(
                [(scale // 2 - r, inset), (scale // 2 + r, inset + 2 * r)],
                fill=(30, 30, 190),
            )
            d.rectangle(
                [
                    (scale // 2 - (w // 2), inset + r),
                    (scale // 2 + (w // 2), scale - 1 - inset),
                ],
                fill=(30, 30, 190),
            )
        elif k == CT_SPRING:
            x = (scale - 1 - inset) - scale // 2
            w = max(2, x // 4)
            d.polygon(
                [
                    (scale // 2, inset),
                    (scale - 1 - inset, inset + x),
                    (inset, inset + x),
                ],
                fill=(179, 60, 190),
            )
            d.rectangle(
                [(scale // 2 - w, inset + x), (scale // 2 + w, scale - 1 - inset)],
                fill=(179, 60, 190),
            )
        cls._cell_img_cache[(k, scale, highlight)] = im
        return im


class Labyrinth:
    """
    Rectangular grid of cells each of which can contain a
    wall, an obstacle, or empty space.
    """

    neighbor_disps = [Vector2(-1, 0), Vector2(0, -1), Vector2(1, 0), Vector2(0, 1)]

    def __init__(self, xsize, ysize, start=None, goal=None):
        """
        Initialize new labyrinth with every cell filled with a wall
        """
        self.xsize = xsize
        self.ysize = ysize
        self.start = start
        self.goal = goal

        self._grid = [[CT_WALL] * self.xsize for _ in range(self.ysize)]

    def __str__(self):
        """Crude text graphics of the maze"""
        rowstrs = []
        for y in range(self.ysize):
            row_ct_list = []
            for x in range(self.xsize):
                row_ct_list.append(self.get_cell(Point2(x, y)))
            rowstrs.append("".join(CellRenderer.char(k) for k in row_ct_list))
        return "\n".join(rowstrs)

    def __repr__(self):
        """Default to using str() for everything"""
        return str(self)

    def is_valid(self, p):
        """Does Point2 object `p` lie within this maze?"""
        if not isinstance(p, Point2):
            raise ValueError("Location must be specified as Point2 instance")
        if p.x < 0 or p.x >= self.xsize:
            return False
        if p.y < 0 or p.y >= self.ysize:
            return False
        return True

    def insist_valid(self, p):
        """Raise exception if Point2 object `p` is not within the maze"""
        if not self.is_valid(p):
            raise ValueError(
                "Position {} invalid for this maze with (xsize,ysize)=({},{})".format(
                    p, self.xsize, self.ysize
                )
            )

    def get_cell(self, p):
        """Return the type of object at cell `p` (a Point2)"""
        self.insist_valid(p)
        if p == self.start:
            return CT_START
        if p == self.goal:
            return CT_GOAL
        return self._grid[p.y][p.x]

    def is_wall(self, p):
        "Is `Point2` object `p` a wall?"
        return self.get_cell(p) == CT_WALL

    def is_empty(self, p):
        "Is `Point2` object `p` empty?"
        return self.get_cell(p) == CT_EMPTY

    def is_start(self, p):
        "Is `Point2` object `p` the start?"
        return self.get_cell(p) == CT_START

    def is_goal(self, p):
        "Is `Point2` object `p` the goal?"
        return self.get_cell(p) == CT_GOAL

    def is_pit(self, p):
        "Is `Point2` object `p` a pit?"
        return self.get_cell(p) == CT_PIT

    def is_lock(self, p):
        "Is `Point2` object `p` a lock?"
        return self.get_cell(p) == CT_LOCK

    def is_spring(self, p):
        "Is `Point2` object `p` a spring trap?"
        return self.get_cell(p) == CT_SPRING

    def set_wall(self, p):
        "Make `Point2` object `p` a wall"
        self.set_cell(p, CT_WALL)

    def set_empty(self, p):
        "Make `Point2` object `p` empty"
        self.set_cell(p, CT_EMPTY)

    def set_start(self, p):
        "Make `Point2` object `p` the starting point"
        self.start = p

    def set_goal(self, p):
        "Make `Point2` object `p` the goal"
        self.goal = p

    def set_pit(self, p):
        "Make `Point2` object `p` a pit"
        self.set_cell(p, CT_PIT)

    def set_lock(self, p):
        "Make `Point2` object `p` a lock"
        self.set_cell(p, CT_LOCK)

    def set_spring(self, p):
        "Make `Point2` object `p` a spring trap"
        self.set_cell(p, CT_SPRING)

    def set_cell(self, p, k):
        """Make the cell at Point2 `p` have type `k` (integer)"""
        assert k in CELL_TYPES
        if k == CT_START:
            raise ValueError(
                "Must set .start attribute rather than using set_cell with CT_START"
            )
        if k == CT_GOAL:
            raise ValueError(
                "Must set .goal attribute rather than using set_cell with CT_GOAL"
            )
        self._grid[p.y][p.x] = k

    def non_wall_neighbors(self, p):
        """Return list of x/y neighbors of Point2 `p` that
        are not walls"""
        nbrs = []
        for v in self.neighbor_disps:
            try:
                if not self.is_wall(p + v):
                    nbrs.append(p + v)
            except ValueError:
                continue
        return nbrs

    def apply_empty_interior(self):
        """
        Make all points not on the edges empty
        """
        self._grid[0] = [CT_WALL] * self.xsize
        self._grid[-1] = [CT_WALL] * self.xsize
        for y in range(1, self.ysize - 1):
            for x in range(1, self.xsize - 1):
                self._grid[y][x] = CT_EMPTY

    def num_locks(self):
        "Number of cells that are locks"
        n = 0
        for r in self._grid:
            n += r.count(CT_LOCK)
        return n

    def num_pits(self):
        "Number of cells that are pits"
        n = 0
        for r in self._grid:
            n += r.count(CT_PIT)
        return n

    def num_springs(self):
        "Number of cells that are spring traps"
        n = 0
        for r in self._grid:
            n += r.count(CT_SPRING)
        return n

    def _serobj(self):
        """
        Private method to make a dict that represents this object
        for serialization (file I/O)
        """
        so = {
            "xsize": self.xsize,
            "ysize": self.ysize,
            "start": [self.start.x, self.start.y] if self.start else None,
            "goal": [self.goal.x, self.goal.y] if self.goal else None,
            "non_walls": [],
        }
        for y in range(self.ysize):
            for x in range(self.xsize):
                k = self._grid[y][x]
                if k != CT_WALL:
                    so["non_walls"].append([x, y, k])
        return so

    @classmethod
    def load(cls, fp):
        """
        Make an instance by loading from a file object (must be open for reading)
        """
        return cls._from_serobj(json.load(fp))

    def save(self, fp):
        """
        Save to a file object (must be open for writing)
        """
        json.dump(self._serobj(), fp)

    @classmethod
    def _from_serobj(cls, so):
        non_walls = so["non_walls"]
        socopy = {k: so[k] for k in so if k != "non_walls"}
        socopy["start"] = Point2(*so["start"]) if so["start"] else None
        socopy["goal"] = Point2(*so["goal"]) if so["goal"] else None
        M = cls(**socopy)
        for x, y, k in non_walls:
            p = Point2(x, y)
            M.set_cell(p, k)
        return M

    @requiresPIL
    def as_image(self, scale=None, highlight=[]):
        "Return a PIL.Image bitmap representing this labyrinth"
        if scale is None:
            scale = max(5, 500 // max(self.xsize, self.ysize))
        img = PIL.Image.new("RGB", (scale * self.xsize, scale * self.ysize))
        for x in range(self.xsize):
            for y in range(self.ysize):
                p = Point2(x, y)
                k = self.get_cell(p)
                tile = CellRenderer.img(k, scale, p in highlight)
                img.paste(tile, (x * scale, y * scale))
        return img

    @requiresPIL
    def save_png(self, fn, scale=None, highlight=[]):
        """
        Save a PNG bitmap representing this labyrinth to new file
        with name given by `fn`
        """
        img = self.as_image(scale=scale, highlight=highlight)
        img.save(fn)


class RandomLabyrinth(Labyrinth):
    """
    Randomly generated labyrinth without any obstacles
    other than walls.  Uses Prim's algorithm.
    """

    frontier_disps = [Vector2(-2, 0), Vector2(0, -2), Vector2(2, 0), Vector2(0, 2)]

    def __init__(self, xsize, ysize):
        """Create a new random maze of size (xsize,ysize).
        Both dimensions must be odd."""
        super().__init__(xsize, ysize)
        if self.xsize % 2 == 0 or self.ysize % 2 == 0:
            raise ValueError("xsize and ysize must be odd")
        if min(self.xsize, self.ysize) < 5:
            raise ValueError("xsize and ysize must be at least 5")
        self.choose_start()
        self.generate_free_space()
        self.choose_goal()

    def choose_start(self):
        "Decide on a good starting point near the middle"
        sx = 2 * (self.xsize // 4) + 1
        sy = 2 * (self.ysize // 4) + 1
        dx = self.xsize // 8
        sx += 2 * random.randint(-dx, dx)
        dy = self.ysize // 8
        sy += 2 * random.randint(-dy, dy)
        s = Point2(sx, sy)
        self.set_start(s)

    def _edge_free_pairs(self):
        """
        Generate pairs p,q where p is on the border, q is empty,
        and q is adjacent to p
        """
        for x in range(1, self.xsize - 1):
            pedge = Point2(x, 0)
            pin = Point2(x, 1)
            if self.is_empty(pin):
                yield pedge, pin
        for x in range(1, self.xsize - 1):
            pedge = Point2(x, self.ysize - 1)
            pin = Point2(x, self.ysize - 2)
            if self.is_empty(pin):
                yield pedge, pin
        for y in range(1, self.ysize - 1):
            pedge = Point2(0, y)
            pin = Point2(1, y)
            if self.is_empty(pin):
                yield pedge, pin
        for y in range(1, self.ysize - 1):
            pedge = Point2(self.xsize - 1, y)
            pin = Point2(self.xsize - 2, y)
            if self.is_empty(pin):
                yield pedge, pin

    def choose_goal(self):
        "Decide on a good goal along an edge"
        L = list(
            (p, q, len(self.non_wall_neighbors(q))) for p, q in self._edge_free_pairs()
        )
        m = min(n for p, q, n in L)
        p, _ = random.choice(list((p, q) for p, q, n in L if n == m))
        self.set_goal(p)

    def generate_free_space(self):
        """Make the maze using Prim's algorithm"""
        sx = 2 * (self.xsize // 4) + 1
        sy = 2 * (self.ysize // 4) + 1
        dx = self.xsize // 8
        sx += 2 * random.randint(-dx, dx)
        dy = self.ysize // 8
        sy += 2 * random.randint(-dy, dy)
        s = Point2(sx, sy)
        self.set_start(s)
        frontier = self.cell_frontier(s)
        while frontier:
            p = frontier.pop(random.randrange(len(frontier)))
            nbrs2 = self.cell_neighbors2(p)
            if nbrs2:
                p2 = random.choice(nbrs2)
                qx = (p.x + p2.x) // 2
                qy = (p.y + p2.y) // 2
                q = Point2(qx, qy)
                self.set_empty(p)
                self.set_empty(q)
                nf = self.cell_frontier(p)
                for r in nf:
                    if r not in frontier:
                        frontier.append(r)

    def cell_frontier(self, p):
        """Return cells at +-2 in x or y that are blocked"""
        F = []
        for v in self.frontier_disps:
            q = p + v
            if self.is_valid(q) and self.is_wall(q):
                F.append(q)
        return F

    def cell_neighbors2(self, p):
        """Return cells at +-2 in x or y that are free"""
        F = []
        for v in self.frontier_disps:
            q = p + v
            if self.is_valid(q) and not self.is_wall(q):
                F.append(q)
        return F


class SampleLabyrinth(Labyrinth):
    "Labyrinth examples with additional info"
    _sampledata = []

    def __init__(self, *args, **kwargs):
        self.info = kwargs.pop("info")
        super().__init__(*args, **kwargs)

    @classmethod
    def load_by_id(cls, n):
        "Get sample labyrinth with index `n` in the sample list"
        if not isinstance(n, int):
            raise TypeError("sample id `n` must be an integer")
        if not cls._sampledata:
            cls._load_sampledata()
        if n < 0 or n >= len(cls._sampledata):
            raise ValueError(
                "bad sample id `n`; allowed range is 0<=n<{}".format(
                    len(cls._sampledata)
                )
            )
        data = cls._sampledata[n]
        return cls._from_serobj(data)

    @classmethod
    def _load_sampledata(cls):
        """
        Decompress the b85-encoded gzipped json blob at the end of this file
        """
        try:
            cls._sampledata = json.loads(
                gzip.decompress(
                    base64.b85decode(_sample_labyrinths_datablock.replace("\n", ""))
                )
            )
        except Exception as e:
            raise RuntimeError("Decompressing the sample labyrinth data failed.") from e


def sample_labyrinth(n):
    """
    Create and return an instance of one of the sample labyrinths.
    The returned object has an .info attribute with a description.
    """
    return SampleLabyrinth.load_by_id(n)


# This is a bunch of compressed data about the sample labyrinths.
# It is decompressed as needed by `sample_labyrinth`.
_sample_labyrinths_datablock = r"""
ABzY8sjJFm0{_ih+iu%P68)8ipPWDwbXAjV(r>eu!7ebH0F&9Lcn~laV{0Rm8c9y<8RXxG
7nyZh?3SoYf&~JkX^PbsHtU=^RsHVIi^tXMkK*D=8Jehzr_BY$^~GwPFW2?OJFaiVztw-a
t@3&MhisyB^M|r3-+#&H^HuZLclFQef2O|ij-_d&8A&siW+F{1%~YD1G)Y4n`XlI&phto(
3Hl`Hl%Q9FZVCEjoEz9@u*qPP!6t)E&YXo|Sq+9+G0cQvlnkR`7!AW{7)H=PTmLUF#z_B0
`Zw|ljJyIPufV_n4Ghr0@)}rP0|Pg(yatxnz=ZlX43WV;N6?1880<5SbD|=dUL+HVU|<mp
CW1~Q=qQ4YBIqcRj$&ETSoV4>-N&-mV_E1}1{K2wk71=_*x)g&dJG#phBpwy8;D_|F--Ki
&CnNveFpmsHW}<Rn>vQYh-EPnnRX%*Okh$8OeBGUC9oY57)$~KNTAb1I<@i!th@m$L$UG(
th@m$1GF$e3j?&Ux)xT~!s=Ss-xelhVL}!rWMNNRSZNCrwJ=ebT`D6^VU#J1CWW3-u%3d&
RF*Ci*N{m+nJir<OP9&gW#T0=8B+$Un8Du7V5}LeXa*~q!5lJJ(F|5JgT0%<>Si$K4Cb7H
bIxFOGgymE)}s0Rdd$%X1R9Y*qx;wB^EKE)1Vji#3`FEZ=tJyt0M9`=2j(1{bAZl4ItS_;
taHH5K|6x|N)Glpfaf5d19=3?!mum=fPLFSJA*di!-P*0K0^2m<1>uUFm}m~fw~PCNdS_4
JAt-^b_Q)iLoGo;*d)YFLf|AsPC~dO#7jbuBt%9+Xq1Z-FM4YYjhmGptD3=G{PQutU(5@o
uhh@^ho|MNT;Hkcqna0=i@73oSyrn0Q1il@d9iwNT^f3%SS^;bd$r8VX?3se^FInTEmpJJ
QeDno6|dB6rE;}i7DfI0f91`^Lpl5Xp-`)8{;-}^W!FJ@TX)rb)XU;FUruZLtLDb1;%PNe
i+Nstny8QS+3nr>ecjb<aa}Hp-ydenV)efJ^OgE3pRe%m?Nj}q?`P%v&8_MC#_W~S7hfkz
7;v*5!hj7j;QFm3NPye7N&jCA7^t5#fgDC&x|v852xBVE3}~bd&{QwI1iIFGMIU_xLM6?}
OWYD^0uM`phG}S%m!9!)^ei1g&w!XnGxCz5M4G^7QlK+BK$n0N97l7Ip6CGO0iGbuNSZ(-
5@`bMNP%5wXwyE{K{~)65M-fkpdCRQK{<go;&U3pdW{zpKy*G3-IGI+UVCBR=c{R?uO{<I
rt{BVX7x|!)w=bt#r<Oaq*jakrcj-SzR%02-aFUcxAtyok=OoseYdP0Ztv7(G%+u}fdjVS
e=WM-W&zOsCL2BCEY9~x$GJDAj=bTu-{p<=QNA6(2kn4eFaO84>h&A-_RY`#{q^5(UZ3L)
zkIpOXRBhRipQH`(QK%fFWr~kFcCpr_qCfX-ARvo@2rnQ-R`*n?2Zwe;sZq`9T1rKc(IB6
$c;i0ZsN=@9?`fR-7Q!G?fvS}kP389I#N<}CRs@bBqkG(l5i>;U8%c3xyS63kTwqoG$g-P
6mQdxzSDzbp`jGCS=urB4~@`*qJS=x_%$M+F2>7*?11OUUPxdjUX3W;M~ntiP-pxQl9cV_
OEOrmMl?nj(kEy{iC-@Qnq|DKEemimRE}t%9Bn4Mtr7KW>QROcm4l*yG&DvILPp8Q%RzB~
F1kz*i6`09#G!Lh$-VSZcIz0~=-Vqr{f6=iLiQlxXXA8_7kh*<_|zVc!m}B@4(dI}NIdC2
y+^=hx8Ngd3z0NI{7e`r6T%rGp7j@uKWqEPtOx<T5#SpElO+H<f_R$%`3MpsgwRKVW!Oba
#4syDh<}8+5W-{#AsP}wAR+D%f}IS3(H!^YeAL`{sX435#jGLV<@~AU<(xf|Z6z`Y&xln%
ofcEo{Bpl?Mrj?L<!g1btX2)(u0yrjT=(o)7XRz=VN{sLm?>^AddA+skdr9Zn?IZ-QafjM
c(a>!r-y|;?W6MKjT~b?86T11rG07I<Qy5>5X~Mzt>bMu4ta9#en#g-cP2yS%ReF;>Y>1?
pAM6sm?F=#C+8eTlgqQ_AN`!r22zOWH%$);a-K*I<<0J6hZGP8!whe8XVXPCKC##H;S(}@
yf4kS8P=(JK0@+za5ipS0`8P#T8d;QI}_7_S86<bDD!Y5V9s80<nV?e1L__RQJ^60@ev&u
3A(%h?Qxh+>R51ks@o8!6F5P_N)19cNEnk7I7R9MW9}|`yWk@UoFsvlBnZa|T&5V!;06(1
U>AgT2@MlkrW7w6({&p>CP5fY;64chX}Q2(wPwMcQikgT9+fZ#%|K8iaHRyklrV2X=u8Q{
DWN+h^rwUlm9P?nF!m;NuY~@!yYLa;XcY0KM<ypFQ7vkkTTXj@x+AcE&r9{8rM;hPLfrne
rL5|5Rw`z-S{IAe3so)Kd)34G`S$(8O=GpZEtcORU(tjG0qMGxa2@Ts{mOPyVI-#Co&bNB
@<=}|&H@5-psMkROp894BJ0rwjvEgelA<#h!5IBH8)U7;$w$wID8`FGt)f4PWPk<7`_kJR
Haz6p25%f%a+sb+ejbz-N?fq3h)^G(5Sudy#CkyDIiwaxr?Y!KkdE0eBZtU72*Z>O6<|Fo
3W#<D1U-)VWMO?m#h}F~V95MM6Wk{ZpD6l<%L7j-0vu5eFbEIA3a(eQ)dSUbj2asb0^(7H
cTVZr9`&_PFcM}Mw*!P><=seGHVQ@#K3R4va_Bw$h^jmjQeT~z;#s5ByA{_x;RZ$+vVL3P
hLGuPnKc}I7#)^bbui%Y=&X9b=<4H?v6oYt4X5mA<ISh0(t+bfQQabz*X1u8qPL-k%@g^$
Hj}T`Dr!p&)w=3v=5_hEnntz{#|^Q(ua-q;exh=<x~rD!VktuGO~+6lR>kxTdTaFE%3^kr
%?%sVP#B|y$n{T#OJg)JHob$V`AcHVzJkF0bZ2D!Ofq_3*+;vpe&%hxbMg<h#o0&oR6VG>
{Bu$7mTtGb`9(I{`b*Vrw*zAmb@`#V$?HwlT5tAT({A_etgM5eeEPy4w)h|H#`XN<j;fsY
!Z{5_j>_M73w^%2oI#W$&dL|sj48m$z>crdMh{ADqCnY=^`76dLv>$+yf1p4SL@FLr@8FG
1v!VL282Ct2RnLn-Oca_mt-in3Tz?`6*hx|Tjc%l<3L5P8F7e<4m;3wzThboJM9dec30>`
dJrRxIHF~C71|8XU)d31)bn91y?q+%r1+{Qc6$OW!T^f{S(4}*pV-=6ffMPi9E($7GbZi|
o!PR3q>MiANi7`+wxVI0<&<++)}NL!p?d5%SZiaxXL(I}bZ8cxCt1VViP}y*qIE>AO&qMQ
IrQ|DJv?q>jJifdar&52n;jvY?&*U6*i|&@3>IO8X9DFpZb^<eLUdA4PPizwtGnXG-c4;+
=t%nVu>90{Yi~GMh!c6La<=MlB#Ra4?KGB?tBT=*F$u<Yn9?%GWVA5X^qgIiy0JskST>Zb
VuQ9ha<0$>TW1gl=d~~sMmCh>;^${%0I9Pvx3Xd8q-2;rF&hSjK!>Kouvd0dd)O1>d>A`o
?1-@=b~>80CnNhvL!+47-svHlQIup9B^k?78K9B@Dj8!NfJX*+WPnEoNMwXWMo45#Lownb
W8}u<%mg8k5fT|8kx|tY3yeK6_QW_H#`&;y#!z24nuinMIfp42Yf;!qXE}!}7;OVaGGHV_
6vu#<3~?L-b~0ioBX%-|b&P1qh?b1_$Owsy$0*of7{UmGjJU^mmVyxk89<N$_ZV@H5$YI&
x#lA3gAfLAV{rQnf)4|PF+doj<jII<jCjTvv@wDkBe*ew8zZ<ef*T{aF@hT-p0QJ9%7|_Z
c`#0JXF^ttA>xxCWpINCFDzc*&lrEkXt}uofXD!djE5{3P>><AW31(11VKg+WQ^z-5s~{i
t6hKVe0_p$DL#f>wc8ovJjUD^BdRhU!eER68G}GZfbA}PLZkHxjZr5wPI`H{oT}BL{?V;k
FZ0E!s}SaFub%zm>wgR-#`dqBxCr9*e;PTvz1@g`_xYznJuKA6YN^_T_nY6h2kj@Scy;^g
y8QF{qV4AT;;Ip@C)XFPf_ZVpb<;VSe{n_WS9O=Kyhr@`KvTLiRaU*V9R^I;fUjs;dj!}{
l^?Cuv#Xn?Ae*LpwEE;g$rQ!<NQ-DHNgk-Y<=$I@0y&iK<!c2y40a6IF%URxi~3qb$Ox)0
B2@S_Nc>u)zDSG6-_I+8@kD@|G1$RCCWi5BNp`)R80;iqCxP`zz)k|=Nnl<{=mSrW{lL@5
)J-f@i=yoE3X|?Uc7Krfy8LPLb#6A|1kzdUCtbDYZ1ee!??ey36VrVr`Iyfv{P^oP{^#5L
#ZCkEYje=N`qB*HbFqBtl5FzX{_unP-@|HsU9KB%Rh30s_NAuPmr`9;W#il0HGR=8#O-`G
E!6t1sF$hshV_az?JxP$tI?nQ&N8sy{sPY-$q_nF000
"""
