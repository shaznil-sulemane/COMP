import copy, re, sys
from xml.sax.saxutils import escape
from lxml import etree
from pptx import Presentation

NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')

INK, MUTED, TINT, LINE, WHITE, SOFT = "151B21", "4F5861", "F6F7F8", "D4D9DE", "FFFFFF", "6B7580"
SANS, MONO = "Liberation Sans", "Consolas"
L, RIGHT_END = 566928, 11539728


class S:
    """Builder for one slide's shapes."""
    def __init__(self):
        self.items, self.nid = [], 100

    def id(self):
        self.nid += 1
        return self.nid

    # ---- primitives ----
    def rect(self, x, y, w, h, fill=TINT, line=LINE, geom="rect", eff=0, adj=7000):
        av = f'<a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst>' if geom == "roundRect" else "<a:avLst/>"
        ln = f'<a:ln w="10160"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>' if line else "<a:ln><a:noFill/></a:ln>"
        i = self.id()
        self.items.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Shape {i}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="{geom}">{av}</a:prstGeom><a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>{ln}</p:spPr>'
            f'<p:style><a:lnRef idx="1"><a:schemeClr val="accent1"/></a:lnRef><a:fillRef idx="3"><a:schemeClr val="accent1"/></a:fillRef>'
            f'<a:effectRef idx="{eff}"><a:schemeClr val="accent1"/></a:effectRef><a:fontRef idx="minor"><a:schemeClr val="lt1"/></a:fontRef></p:style>'
            f'<p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/><a:p><a:pPr algn="ctr"/><a:endParaRPr lang="pt-PT"/></a:p></p:txBody></p:sp>')

    def line(self, x, y, w, h, color=LINE, wd=10160):
        i = self.id()
        self.items.append(
            f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{i}" name="Line {i}"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="line"><a:avLst/></a:prstGeom><a:ln w="{wd}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:ln></p:spPr></p:cxnSp>')

    def text(self, x, y, w, h, paras, anchor="t", algn="l", aft=0, ins=22860):
        """paras: list of paragraphs; paragraph = str | list of runs; run = (text, dict)."""
        body = ""
        for p in paras:
            runs = p if isinstance(p, list) else [(p, {})]
            rx = ""
            for t, o in runs:
                sz = o.get("sz", 1400); b = 1 if o.get("b") else 0; it = 1 if o.get("i") else 0
                col = o.get("c", INK); font = o.get("f", SANS)
                sp = ' xml:space="preserve"' if t != t.strip() or "  " in t else ""
                rx += (f'<a:r><a:rPr lang="pt-PT" sz="{sz}" b="{b}" i="{it}" dirty="0"><a:solidFill><a:srgbClr val="{col}"/></a:solidFill>'
                       f'<a:latin typeface="{font}"/><a:cs typeface="{font}"/></a:rPr><a:t{sp}>{escape(t)}</a:t></a:r>')
            a = runs[0][1].get("algn", algn) if runs else algn
            body += (f'<a:p><a:pPr algn="{a}"><a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPts val="{aft}"/></a:spcAft></a:pPr>{rx}</a:p>')
        i = self.id()
        self.items.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="TextBox {i}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="{ins}" rIns="{ins}" tIns="{ins}" bIns="{ins}" anchor="{anchor}"><a:noAutofit/></a:bodyPr><a:lstStyle/>{body}</p:txBody></p:sp>')

    # ---- composites in the deck's visual language ----
    def frame(self, label, title):
        self.text(530352, 201168, 6400800, 219456, [[(label, dict(sz=1000, b=1, c=MUTED))]])
        self.text(530352, 594360, 11109960, 502920, [[(title, dict(sz=2650, b=1))]])
        self.line(530352, 1179576, 11128248, 0, INK, 13970)
        self.line(530352, 6519672, 11128248, 0, LINE, 10160)
        self.text(530352, 6574536, 6400800, 155448, [[("ISUTC  /  COMPILADORES  /  LECC31", dict(sz=900, c=MUTED))]])
        self.text(10972800, 6574536, 685800, 155448, [[("00  /  00", dict(sz=900, b=1, c=MUTED, algn="r"))]])

    def bar(self, x, y, w, label):
        self.rect(x, y, w, 310896)
        self.text(x + 118872, y + 67665, w - 160000, 201168, [[(label, dict(sz=1100, b=1, c=MUTED))]])

    def code(self, x, y, w, h, lines, sz=1050, fill=TINT):
        self.rect(x, y, w, h, fill=fill, geom="roundRect", eff=2, adj=4000)
        paras = []
        for ln in lines:
            if "//" in ln:
                k = ln.index("//")
                runs = [(ln[:k], dict(sz=sz, f=MONO)), (ln[k:], dict(sz=sz, f=MONO, c=SOFT, i=True))]
                if not ln[:k]: runs = runs[1:]
            else:
                runs = [(ln if ln else " ", dict(sz=sz, f=MONO))]
            paras.append(runs)
        self.text(x + 150000, y + 120000, w - 260000, h - 200000, paras)

    def table(self, x, y, cols, header, rows, rh=380000, hh=390000, sz=1100, hsz=1050, mono_cols=(), algn="l"):
        w = sum(cols)
        self.rect(x, y, w, hh, fill=INK)
        cx = x
        for c, hd in zip(cols, header):
            self.text(cx + 60000, y, c - 80000, hh, [[(hd, dict(sz=hsz, b=1, c=WHITE, algn=algn))]], anchor="ctr")
            cx += c
        yy = y + hh
        for r_i, row in enumerate(rows):
            self.rect(x, yy, w, rh, fill=TINT if r_i % 2 == 0 else WHITE)
            cx = x
            for c_i, (c, val) in enumerate(zip(cols, row)):
                o = dict(sz=sz, algn=algn)
                if c_i in mono_cols: o["f"] = MONO
                if isinstance(val, tuple): val, extra = val; o.update(extra)
                paras = [[(v, dict(o))] for v in val.split("\n")]
                self.text(cx + 60000, yy, c - 80000, rh, paras, anchor="ctr")
                cx += c
            yy += rh
        return yy

    def card(self, x, y, w, h, fill=WHITE):
        self.rect(x, y, w, h, fill=fill, geom="roundRect", eff=2, adj=7000)

    def xml(self):
        return [etree.fromstring(f'<root {NS}>{s}</root>')[0] for s in self.items]




# ---------------- extra helpers for v2 (inches-based) ----------------
EMU = 914400
def I(v): return int(round(v * EMU))
RED, GREEN = "B42318", "1F7A4D"


def _ellipse(s, x, y, w, h, fill=WHITE, line=INK, lw=19050):
    i = s.id()
    s.items.append(
        f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Oval {i}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm>'
        f'<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
        f'<a:ln w="{lw}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/><a:p><a:pPr algn="ctr"/><a:endParaRPr lang="pt-PT"/></a:p></p:txBody></p:sp>')
S.ellipse = _ellipse


def _state(s, cx, cy, d, name, terminal=False, sz=1200, fill=WHITE):
    """Estado: círculo; terminal = círculo duplo. Coordenadas em polegadas."""
    s.ellipse(I(cx - d / 2), I(cy - d / 2), I(d), I(d), fill=fill)
    if terminal:
        g = 0.06
        s.ellipse(I(cx - d / 2 + g), I(cy - d / 2 + g), I(d - 2 * g), I(d - 2 * g), fill=fill, lw=12700)
    s.text(I(cx - d / 2), I(cy - d / 2), I(d), I(d), [[(name, dict(sz=sz, b=1, algn="ctr"))]], anchor="ctr", ins=0)
S.state = _state


def _arrow(s, x1, y1, x2, y2, color=INK, wd=15875, head=True, dash=False):
    """Seta de (x1,y1) para (x2,y2), em polegadas."""
    fh = ' flipH="1"' if x2 < x1 else ""
    fv = ' flipV="1"' if y2 < y1 else ""
    ox, oy = min(x1, x2), min(y1, y2)
    tail = '<a:tailEnd type="triangle" w="med" len="med"/>' if head else ""
    ds = '<a:prstDash val="dash"/>' if dash else ""
    i = s.id()
    s.items.append(
        f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{i}" name="Arrow {i}"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>'
        f'<p:spPr><a:xfrm{fh}{fv}><a:off x="{I(ox)}" y="{I(oy)}"/><a:ext cx="{I(abs(x2-x1))}" cy="{I(abs(y2-y1))}"/></a:xfrm>'
        f'<a:prstGeom prst="line"><a:avLst/></a:prstGeom><a:ln w="{wd}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>{ds}{tail}</a:ln></p:spPr></p:cxnSp>')
S.arrow = _arrow


def _box(s, x, y, w, h, text, fill=TINT, color=INK, sz=1200, b=False, f=SANS, line=LINE, geom="roundRect", algn="ctr", adj=12000, eff=0):
    """Caixa com texto centrado (polegadas). text pode ser str ou lista de parágrafos."""
    s.rect(I(x), I(y), I(w), I(h), fill=fill, line=line, geom=geom, eff=eff, adj=adj)
    paras = text if isinstance(text, list) else [[(text, dict(sz=sz, b=b, c=color, f=f, algn=algn))]]
    s.text(I(x), I(y), I(w), I(h), paras, anchor="ctr", ins=45720)
S.box = _box


def _t(s, x, y, w, h, paras, **kw):
    """text() em polegadas."""
    s.text(I(x), I(y), I(w), I(h), paras, **kw)
S.t = _t


def _bar(s, x, y, w, label):
    s.bar(I(x), I(y), I(w), label)
S.ibar = _bar


def _code(s, x, y, w, h, lines, sz=1050, fill=TINT):
    s.code(I(x), I(y), I(w), I(h), lines, sz=sz, fill=fill)
S.icode = _code


def _card(s, x, y, w, h, fill=WHITE):
    s.card(I(x), I(y), I(w), I(h), fill=fill)
S.icard = _card


def R(text, **o):
    """run helper"""
    return (text, o)
