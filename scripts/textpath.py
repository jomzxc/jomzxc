"""Turn text into SVG path data using a static instance of a variable font.

GitHub serves README images through a proxy that blocks web fonts, so text in
the banner and section headers is drawn as outlines instead.
"""
import os
from functools import lru_cache
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")


@lru_cache(maxsize=None)
def font(name, **axes):
    f = TTFont(os.path.join(FONT_DIR, f"{name}.ttf"))
    return instancer.instantiateVariableFont(f, axes)


def _kern_pairs(f):
    """Pair kerning from GPOS PairPos format 1 (enough for short strings)."""
    pairs = {}
    if "GPOS" not in f:
        return pairs
    for lookup in f["GPOS"].table.LookupList.Lookup:
        for st in lookup.SubTable:
            if lookup.LookupType == 9:
                st = st.ExtSubTable
            if getattr(st, "LookupType", 2) != 2 or st.Format != 1:
                continue
            for i, first in enumerate(st.Coverage.glyphs):
                for rec in st.PairSet[i].PairValueRecord:
                    v = rec.Value1
                    if v is not None and getattr(v, "XAdvance", 0):
                        pairs.setdefault((first, rec.SecondGlyph), v.XAdvance)
    return pairs


@lru_cache(maxsize=None)
def kerning(name, **axes):
    return _kern_pairs(font(name, **axes))


def text_path(text, name, size, x=0.0, y=0.0, tracking_em=0.0, **axes):
    """Return (path_d, width) for text with its baseline at y."""
    f = font(name, **axes)
    upm = f["head"].unitsPerEm
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    kern = kerning(name, **axes)
    scale = size / upm
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}")
    cursor = 0.0
    names = [cmap.get(ord(c), ".notdef") for c in text]
    for i, g in enumerate(names):
        tp = TransformPen(pen, (scale, 0, 0, -scale, x + cursor * scale, y))
        gs[g].draw(tp)
        adv = gs[g].width + tracking_em * upm
        if i + 1 < len(names):
            adv += kern.get((g, names[i + 1]), 0)
        cursor += adv
    width = (cursor - tracking_em * upm) * scale
    return pen.getCommands(), width


def text_width(text, name, size, tracking_em=0.0, **axes):
    return text_path(text, name, size, 0, 0, tracking_em, **axes)[1]


FRAUNCES = dict(wght=600, SOFT=100, WONK=0)


def fraunces(text, size, x=0, y=0, tracking_em=-0.055):
    return text_path(text, "Fraunces", size, x, y, tracking_em, opsz=min(144, max(9, size)), **FRAUNCES)


def onest(text, size, x=0, y=0, weight=400, tracking_em=0.0):
    return text_path(text, "Onest", size, x, y, tracking_em, wght=weight)
