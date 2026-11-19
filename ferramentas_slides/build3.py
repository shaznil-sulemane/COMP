import copy, math, re, sys
sys.path.insert(0, ".")
from helpers import *
from pptx import Presentation

SRC, OUT = sys.argv[1], sys.argv[2]
LBL = "00  /  NA PRÁTICA"


# ---------------------------------------------------------------------
# componentes reutilizáveis
# ---------------------------------------------------------------------
def loop(s, cx, top, w=0.6, h=0.45):
    """laço (self-loop) rectangular por cima de um estado; seta a entrar pela direita"""
    xl, xr, yt = cx - w / 2, cx + w / 2, top - h
    s.line(I(xl), I(yt), 0, I(h), INK, 15875)
    s.line(I(xl), I(yt), I(w), 0, INK, 15875)
    s.arrow(xr, yt, xr, top - 0.02)


def film(s, cols, y0=2.0, base_y=4.55, top_lbl="lê", elem_w=0.9, elem_h=0.4, fsz=1300, mono=True):
    """
    Tira de fotogramas: cada coluna = um passo.
    col = dict(chip=símbolo no topo ou None, chiplbl='lê'/'espreita', stack=[topo,...,base],
               act='push (', state='ok'|'err'|'acc', marks=set(índices de marcadores))
    """
    n = len(cols)
    cw = 12.0 / n
    for k, c in enumerate(cols):
        cx = 0.62 + k * cw + cw / 2
        s.t(cx - cw / 2, y0, cw, 0.25, [[R(c.get("title", f"passo {k}"), sz=900, c=MUTED, algn="ctr")]])
        if c.get("chip"):
            chw = 0.6 if len(c["chip"]) <= 2 else min(cw - 0.15, 0.25 + 0.17 * len(c["chip"]))
            redchip = c.get("state") == "err" and c.get("keeptop")
            s.box(cx - chw / 2, y0 + 0.28, chw, 0.48, c["chip"], fill=WHITE, line=RED if redchip else INK, color=RED if redchip else INK, sz=1500 if len(c["chip"]) <= 2 else 1300, f=MONO, b=True)
            s.t(cx - cw / 2, y0 + 0.77, cw, 0.22, [[R(c.get("chiplbl", top_lbl), sz=850, c=MUTED, algn="ctr")]])
        st = c["stack"]
        marks = c.get("marks", set())
        err = c.get("state") == "err" and not c.get("keeptop")
        for j, sym in enumerate(reversed(st)):
            idx = len(st) - 1 - j          # índice na lista (0 = topo)
            top = idx == 0
            ew = min(elem_w, cw - 0.15)
            if idx in marks:
                fill, col, ln = TINT, MUTED, LINE
            elif top:
                fill, col, ln = (RED if err else INK), WHITE, None
            else:
                fill, col, ln = WHITE, INK, INK
            s.box(cx - ew / 2, base_y - (j + 1) * (elem_h + 0.03), ew, elem_h, sym, fill=fill, color=col, line=ln,
                  sz=fsz if len(sym) < 3 else fsz - 250, f=MONO if mono else SANS, b=True, geom="rect")
        if not st:
            s.t(cx - cw / 2, base_y - 0.45, cw, 0.4, [[R("vazia", sz=1000, c=MUTED, algn="ctr", i=True)]], anchor="ctr")
        s.line(I(cx - min(elem_w, cw - 0.15) / 2 - 0.08), I(base_y + 0.03), I(min(elem_w, cw - 0.15) + 0.16), 0, INK, 19050)
        color = RED if c.get("state") == "err" else (GREEN if c.get("state") == "acc" else INK)
        s.t(cx - cw / 2, base_y + 0.1, cw, 0.6, [[R(c["act"], sz=1100, b=True, c=color, algn="ctr", f=MONO)]])
        if k < n - 1:
            s.arrow(cx + cw / 2 - 0.12, y0 + 0.52, cx + cw / 2 + 0.12, y0 + 0.52, color=LINE, wd=12700)


def terminal(s, x, y, w, h, lines, sz=1000):
    s.rect(I(x), I(y), I(w), I(h), fill=INK, line=None, geom="roundRect", eff=2, adj=4000)
    paras = []
    for l in lines:
        c = "E6E8EB"
        if any(k in l for k in ("ERRO", "Erro", "REJEITA", "false", "variável")): c = "F28B82"
        if any(k in l for k in ("ACEITE", "ACEITA", "true")): c = "81C995"
        if l.startswith(">"): c = "9AA0A6"
        paras.append([R(l if l else " ", sz=sz, f=MONO, c=c)])
    s.t(x + 0.18, y + 0.12, w - 0.3, h - 0.2, paras)


def verdict(s, y, ok, text, sub=""):
    s.box(0.62, y, 2.2, 0.55, "ACEITA ✔" if ok else "REJEITA ✘", fill=GREEN if ok else RED, color=WHITE, line=None, sz=1400, b=True)
    s.t(3.0, y - 0.02, 9.6, 0.6, [[R(text, sz=1250, b=True)]] + ([[R(sub, sz=1050, c=MUTED)]] if sub else []), anchor="ctr")


# =====================================================================
# P1 — classes da aula
# =====================================================================
def p1():
    s = S(); s.frame(LBL, "Ponto de partida: as classes da aula")
    s.ibar(0.62, 1.51, 5.6, "EXEMPLO DA AULA  ·  palavras terminadas em 0")
    s.icard(0.62, 1.95, 5.6, 1.85)
    s.t(0.7, 2.55, 0.6, 0.3, [[R("início", sz=1000, c=MUTED)]])
    s.arrow(0.78, 3.0, 1.23, 3.0)
    s.state(1.65, 3.0, 0.8, "q1")
    s.state(4.45, 3.0, 0.8, "q2", terminal=True)
    s.arrow(2.02, 2.83, 4.07, 2.83)
    s.t(2.85, 2.45, 0.4, 0.35, [[R("0", sz=1400, b=1, f=MONO, algn="ctr")]])
    s.arrow(4.07, 3.17, 2.02, 3.17)
    s.t(2.85, 3.2, 0.4, 0.35, [[R("1", sz=1400, b=1, f=MONO, algn="ctr")]])
    loop(s, 1.65, 2.6, 0.5, 0.42); s.t(1.95, 2.05, 0.4, 0.3, [[R("1", sz=1300, b=1, f=MONO)]])
    loop(s, 4.45, 2.6, 0.5, 0.42); s.t(4.75, 2.05, 0.4, 0.3, [[R("0", sz=1300, b=1, f=MONO)]])
    s.icode(0.62, 3.95, 5.6, 2.05, [
        "Estado q1 = new Estado();",
        "Estado q2 = new Estado(true);",
        "q1.transicoes.add(new Transicao('1', q1));",
        "q1.transicoes.add(new Transicao('0', q2));",
        "q2.transicoes.add(new Transicao('0', q2));",
        "q2.transicoes.add(new Transicao('1', q1));",
        "Automato automato = new Automato(q1);",
    ], sz=1150)
    s.box(0.62, 6.15, 2.7, 0.5, [[R('procurarPalavra("00")  ', sz=1050, f=MONO, c=WHITE), R("true", sz=1100, b=1, f=MONO, c=WHITE)]], fill=INK, line=None)
    s.box(3.52, 6.15, 2.7, 0.5, [[R('procurarPalavra("01")  ', sz=1050, f=MONO), R("false", sz=1100, b=1, f=MONO)]], fill=WHITE)

    x0 = 6.55
    s.ibar(x0, 1.51, 6.07, "O QUE O PROJECTO REUTILIZA E ACRESCENTA")
    rows = [("Transicao", "igual à da aula", WHITE),
            ("Estado", "+ nome  (ex.: \"ID\", \"LAMBDA\")", WHITE),
            ("Automato", "+ maiorPrefixo()  (lê o maior pedaço)", WHITE),
            ("TransicaoPilha", "Transicao + topo + empilhar", TINT),
            ("AutomatoPilha", "o mesmo ciclo, com uma Stack", TINT),
            ("Automatos", "constrói os 3 autómatos", TINT)]
    for k, (n, d, fill) in enumerate(rows):
        y = 2.0 + k * 0.62
        s.box(x0, y, 2.15, 0.5, n, fill=fill, line=INK if fill == WHITE else LINE, sz=1100, f=MONO, b=True)
        s.t(x0 + 2.3, y, 3.8, 0.5, [[R(d, sz=1150)]], anchor="ctr")
    s.box(x0, 5.85, 0.3, 0.3, "", fill=WHITE, line=INK)
    s.t(x0 + 0.38, 5.82, 2.2, 0.36, [[R("da aula", sz=1100)]], anchor="ctr")
    s.box(x0 + 2.2, 5.85, 0.3, 0.3, "", fill=TINT, line=LINE)
    s.t(x0 + 2.58, 5.82, 3.0, 0.36, [[R("novo, no mesmo estilo", sz=1100)]], anchor="ctr")
    return s


# =====================================================================
# P2 — AFD léxico: diagrama + código
# =====================================================================
def p2():
    s = S(); s.frame(LBL, "Autómato 1 — AFD que reconhece os tokens")
    s.ibar(0.62, 1.51, 6.35, "DIAGRAMA  ·  o nome do estado final é o tipo do token")
    q0x, q0y, d0 = 1.35, 4.05, 0.78
    s.t(0.6, 3.55, 0.7, 0.3, [[R("início", sz=1000, c=MUTED)]])
    s.arrow(0.62, 4.05, q0x - d0 / 2, 4.05)
    s.state(q0x, q0y, d0, "q0", sz=1300)
    tx, td = 4.2, 0.62
    targets = [("ID", "letra _", "↻ letra · dígito · _"), ("LAMBDA", "λ  \\", ""), ("DOT", ".", ""),
               ("LPAREN", "(", ""), ("RPAREN", ")", ""), ("EQUALS", "=", ""), ("ESPACO", "espaço", "↻ espaço · ignorado")]
    for k, (nm, lab, note) in enumerate(targets):
        ty = 2.2 + k * 0.63
        dx, dy = tx - q0x, ty - q0y
        dist = math.hypot(dx, dy); ux, uy = dx / dist, dy / dist
        x1, y1 = q0x + ux * d0 / 2, q0y + uy * d0 / 2
        x2, y2 = tx - ux * td / 2, ty - uy * td / 2
        s.arrow(x1, y1, x2, y2, wd=12700)
        ly = y2 - 0.3 if k <= 3 else y2 + 0.04
        s.t(x2 - 1.1, ly, 0.95, 0.26, [[R(lab, sz=950, f=MONO, b=True, algn="r")]], anchor="ctr", ins=0)
        s.state(tx, ty, td, nm, terminal=True, sz=750)
        if note:
            s.t(tx + 0.4, ty - 0.17, 2.6, 0.34, [[R(note, sz=1000, c=MUTED, f=MONO)]], anchor="ctr")

    x0, w0 = 7.15, 5.47
    s.ibar(x0, 1.51, w0, "Automatos.criarAFDLexico()")
    s.icode(x0, 1.95, w0, 3.45, [
        "Estado q0      = new Estado(\"q0\", false);",
        "Estado qID     = new Estado(\"ID\", true);",
        "Estado qLambda = new Estado(\"LAMBDA\", true);",
        "Estado qPonto  = new Estado(\"DOT\", true);",
        "// ... LPAREN, RPAREN, EQUALS, ESPACO",
        "",
        "ligar(q0, LETRAS, qID);",
        "ligar(qID, LETRAS + DIGITOS, qID); // laço",
        "q0.transicoes.add(new Transicao('λ', qLambda));",
        "q0.transicoes.add(new Transicao('.', qPonto));",
        "// ... ( ) = espaço",
        "",
        "return new Automato(q0);",
    ], sz=1080)
    terminal(s, x0, 5.55, w0, 1.3, [
        "> new AnalisadorLexico().tokenizar(\"λx.x y\")",
        "[LAMBDA, ID(x), DOT, ID(x), ID(y), EOF]",
        "> tokenizar(\"lambda @. x\")",
        "Erro léxico [1:8]: carácter '@' não reconhecido"], sz=1000)
    return s


# =====================================================================
# P3 — AFD passo a passo
# =====================================================================
def chain(s, y, word, final_lbl, final_tok, highlight):
    """q0 -c-> ID -c-> ID ... em linha"""
    n = len(word) + 1
    gap = min(1.45, 8.0 / n)
    x = 0.95
    d = 0.6
    for k in range(n):
        cx = x + k * gap
        nm = "q0" if k == 0 else "ID"
        s.state(cx, y, d, nm, terminal=k > 0, sz=1000)
        if k < n - 1:
            s.arrow(cx + d / 2, y, cx + gap - d / 2, y, wd=12700)
            s.box(cx + gap / 2 - 0.2, y - 0.5, 0.4, 0.36, word[k], fill=TINT, sz=1300, f=MONO, b=True)
    end = x + (n - 1) * gap + d / 2
    s.arrow(end + 0.1, y, end + 0.5, y, color=MUTED)
    s.box(end + 0.6, y - 0.28, 1.5, 0.56, f'"{word}"', fill=WHITE, line=INK, sz=1200, f=MONO, b=True)
    s.arrow(end + 2.15, y, end + 2.5, y, color=MUTED)
    s.t(end + 2.0, y + 0.3, 1.9, 0.3, [[R("palavraReservada()", sz=900, f=MONO, c=MUTED, algn="ctr")]])
    s.box(end + 2.55, y - 0.28, 1.25, 0.56, final_tok, fill=INK if highlight else TINT, color=WHITE if highlight else INK,
          line=None if highlight else LINE, sz=1300, b=True)


def p3():
    s = S(); s.frame(LBL, "AFD passo a passo — let  vs  letter")
    s.ibar(0.62, 1.51, 12.0, "afd.maiorPrefixo(texto, 0)   ·   saída real com mostrarPassos = true")
    s.t(0.62, 2.0, 4.0, 0.35, [[R("Entrada  let", sz=1300, b=True)]])
    chain(s, 3.0, "let", "", "LET", True)
    s.t(0.62, 3.75, 4.0, 0.35, [[R("Entrada  letter", sz=1300, b=True)]])
    chain(s, 4.75, "letter", "", "ID", False)
    s.icard(0.62, 5.55, 12.0, 1.3, fill=TINT)
    s.t(0.85, 5.62, 11.6, 1.2, [
        [R("O AFD só pára quando não há transição. ", sz=1250, b=True),
         R("Por isso lê  letter  inteiro e nunca corta em  LET + ter.", sz=1250)],
        [R("Só depois de ler o nome inteiro é que se vê se é palavra reservada (lambda, let, in).", sz=1150, c=MUTED)],
    ], anchor="ctr", aft=400)
    return s


# =====================================================================
# P4 — tokens → palavra
# =====================================================================
def p4():
    s = S(); s.frame(LBL, "Do texto aos tokens, dos tokens à palavra")
    s.ibar(0.62, 1.51, 12.0, "1 · AnalisadorLexico.tokenizar()  corta o texto com o AFD")
    src = "let id = λx.x in id y"
    bw, gap = 0.5, 0.04
    x0 = 0.62 + (12.0 - len(src) * (bw + gap)) / 2
    for k, c in enumerate(src):
        x = x0 + k * (bw + gap)
        if c == " ":
            s.box(x, 2.0, bw, 0.5, "␣", fill=WHITE, color=LINE, sz=1100, f=MONO)
        else:
            s.box(x, 2.0, bw, 0.5, c, fill=TINT, sz=1500, f=MONO, b=True)
    groups = [(0, 2, "LET"), (4, 5, "ID"), (7, 7, "="), (9, 9, "λ"), (10, 10, "ID"), (11, 11, "."),
              (12, 12, "ID"), (14, 15, "IN"), (17, 18, "ID"), (20, 20, "ID")]
    for a, b, tok in groups:
        xa = x0 + a * (bw + gap); xb = x0 + b * (bw + gap) + bw
        s.line(I(xa + 0.04), I(2.6), I(xb - xa - 0.08), 0, INK, 15875)
        s.box(xa + 0.02, 2.7, xb - xa - 0.04, 0.34, tok, fill=INK, color=WHITE, line=None, sz=900, b=True)

    s.ibar(0.62, 3.3, 12.0, "2 · cada token vira uma letra  →  a PALAVRA que os autómatos de pilha vão ler")
    word = [("l", "LET"), ("i", "ID"), ("=", "EQUALS"), ("λ", "LAMBDA"), ("i", "ID"), (".", "DOT"),
            ("i", "ID"), ("n", "IN"), ("i", "ID"), ("i", "ID"), ("#", "EOF")]
    cw, cg = 0.66, 0.12
    cx0 = 0.62 + (12.0 - len(word) * (cw + cg)) / 2
    for k, (c, t) in enumerate(word):
        x = cx0 + k * (cw + cg)
        s.box(x, 3.85, cw, 0.62, c, fill=WHITE, line=INK, sz=2000, f=MONO, b=True)
        s.t(x - 0.1, 4.5, cw + 0.2, 0.25, [[R(t, sz=800, c=MUTED, algn="ctr")]])
    s.icode(0.62, 5.0, 7.3, 1.85, [
        "int fim = afd.maiorPrefixo(texto, i);",
        "String tipo = afd.ultimoEstado.nome;   // \"ID\", \"DOT\", ...",
        "if (tipo.equals(\"ID\")) tipo = palavraReservada(lexema);",
        "if (!tipo.equals(\"ESPACO\"))",
        "    tokens.add(new Token(tipo, lexema, linha, coluna));",
    ], sz=1150)
    s.icard(8.15, 5.0, 4.47, 1.85, fill=WHITE)
    s.t(8.35, 5.08, 4.1, 1.7, [
        [R("Porquê uma palavra?", sz=1300, b=True)],
        [R("Os AP usam  procurarPalavra(\"li=λi.inii#\"),  tal como o AFD da aula usa  procurarPalavra(\"00\").", sz=1150)],
    ], aft=500)
    return s


# =====================================================================
# P5 — AP parênteses: diagrama + código
# =====================================================================
def p5():
    s = S(); s.frame(LBL, "Autómato 2 — AP que verifica os parênteses")
    s.ibar(0.62, 1.51, 6.0, "DIAGRAMA  ·  rótulo:  lê , topo  /  empilha")
    s.icard(0.62, 1.95, 6.0, 3.0)
    s.t(0.7, 3.75, 0.6, 0.3, [[R("início", sz=1000, c=MUTED)]])
    s.arrow(0.78, 4.15, 1.4, 4.15)
    s.state(1.85, 4.15, 0.85, "q0", sz=1300)
    s.state(5.0, 4.15, 0.85, "qf", terminal=True, sz=1300)
    s.arrow(2.3, 4.15, 4.55, 4.15)
    s.t(2.4, 3.78, 2.1, 0.35, [[R("# , B / ε", sz=1150, f=MONO, b=True, algn="ctr")]])
    s.t(2.4, 4.2, 2.1, 0.3, [[R("fim com a base: aceita", sz=900, c=MUTED, algn="ctr")]])
    loop(s, 1.85, 3.72, 0.55, 0.55)
    s.box(0.85, 2.05, 3.5, 1.08, [
        [R("( , B / (B      push", sz=1050, f=MONO)],
        [R("( , ( / ((      push", sz=1050, f=MONO)],
        [R(") , ( / ε       pop", sz=1050, f=MONO)],
        [R("outro , X / X   igual", sz=1050, f=MONO)]], fill=WHITE, line=LINE, algn="l")
    s.t(0.62, 5.1, 6.0, 1.0, [
        [R("A pilha conta os  (  abertos.", sz=1250, b=True)],
        [R("Um AFD não consegue: teria de ter um estado para cada nível de parênteses.", sz=1150, c=MUTED)],
    ], aft=300)
    x0, w0 = 6.9, 5.72
    s.ibar(x0, 1.51, w0, "Automatos.criarAPParenteses()")
    s.icode(x0, 1.95, w0, 3.45, [
        "Estado q0 = new Estado(\"q0\", false);",
        "Estado qf = new Estado(\"qf\", true);",
        "",
        "//                     lê   topo põe  vai  avança",
        "new TransicaoPilha('(', 'B', \"(B\", q0, true)",
        "new TransicaoPilha('(', '(', \"((\", q0, true)",
        "new TransicaoPilha(')', '(', \"\",   q0, true)",
        "new TransicaoPilha('#', 'B', \"\",   qf, true)",
        "// + os outros símbolos não mexem na pilha",
        "",
        "return new AutomatoPilha(q0, 'B', \"\");",
    ], sz=1050)
    terminal(s, x0, 5.55, w0, 1.3, [
        "> ap.procurarPalavra(\"((i))#\")      // ((x))",
        "true",
        "> ap.procurarPalavra(\"(λi.i#\")      // (λx.x",
        "false"], sz=1000)
    return s


# =====================================================================
# P6/P7 — AP parênteses passo a passo
# =====================================================================
def p6():
    s = S(); s.frame(LBL, "AP de parênteses passo a passo — ((x))")
    s.ibar(0.62, 1.51, 12.0, "procurarPalavra(\"((i))#\")   ·   topo da pilha a escuro")
    cols = [dict(title="início", stack=["B"], act=""),
            dict(chip="(", stack=["(", "B"], act="push ("),
            dict(chip="(", stack=["(", "(", "B"], act="push ("),
            dict(chip="i", stack=["(", "(", "B"], act="igual"),
            dict(chip=")", stack=["(", "B"], act="pop ("),
            dict(chip=")", stack=["B"], act="pop ("),
            dict(chip="#", stack=[], act="aceita", state="acc")]
    film(s, cols, y0=1.95, base_y=4.75)
    verdict(s, 5.75, True, "Todos os  (  foram fechados: a pilha voltou à base B.", "Executavel → mostrarAP(criarAPParenteses(), \"((x))\")")
    return s


def p7():
    s = S(); s.frame(LBL, "AP de parênteses passo a passo — (λx.x")
    s.ibar(0.62, 1.51, 12.0, "procurarPalavra(\"(λi.i#\")   ·   falta um  )")
    cols = [dict(title="início", stack=["B"], act=""),
            dict(chip="(", stack=["(", "B"], act="push ("),
            dict(chip="λ", stack=["(", "B"], act="igual"),
            dict(chip="i", stack=["(", "B"], act="igual"),
            dict(chip=".", stack=["(", "B"], act="igual"),
            dict(chip="i", stack=["(", "B"], act="igual"),
            dict(chip="#", stack=["(", "B"], act="BLOQUEIA", state="err")]
    film(s, cols, y0=1.95, base_y=4.75)
    verdict(s, 5.75, False, "Chegou ao fim (#) com  (  no topo: não há transição para (#, ().",
            "Só existe  # , B / ε  →  o AP só aceita se todos os  (  tiverem sido fechados.")
    return s


# =====================================================================
# P8 — AP da sintaxe: diagrama + regras + código
# =====================================================================
def p8():
    s = S(); s.frame(LBL, "Autómato 3 — AP que reconhece a linguagem")
    leg = [("E", "expressão"), ("L", "let"), ("A", "λ"), ("P", "aplicação"), ("C", "cauda"), ("T", "átomo"), ("$", "base")]
    lw = 12.0 / 7
    for k, (c, n) in enumerate(leg):
        x = 0.62 + k * lw
        s.box(x, 1.5, 0.42, 0.4, c, fill=INK, color=WHITE, line=None, sz=1300, f=MONO, b=True)
        s.t(x + 0.5, 1.5, 1.2, 0.4, [[R(n, sz=1100)]], anchor="ctr")

    s.ibar(0.62, 2.1, 6.3, "AS REGRAS  ·  topo  →  troca por  (consoante o que vem)")
    rules = [("E", "L", "l"), ("E", "A", "λ"), ("E", "P", "i ("), ("L", "l i = E n E", "l"), ("A", "λ i . E", "λ"),
             ("P", "T C", "i ("), ("C", "T C", "i ("), ("C", "ε", "n ) #"), ("T", "i", "i"), ("T", "( E )", "(")]
    for k, (a, b, w) in enumerate(rules):
        col, row = k % 2, k // 2
        x = 0.62 + col * 3.2
        y = 2.55 + row * 0.5
        s.box(x, y, 0.4, 0.4, a, fill=INK, color=WHITE, line=None, sz=1150, f=MONO, b=True, geom="rect")
        s.t(x + 0.45, y, 0.35, 0.4, [[R("→", sz=1150)]], anchor="ctr")
        s.box(x + 0.8, y, 1.35, 0.4, b, fill=WHITE, line=INK, sz=1100, f=MONO, b=True, geom="rect")
        s.t(x + 2.2, y, 0.95, 0.4, [[R("se vem " + w, sz=900, c=MUTED, f=MONO)]], anchor="ctr")
    s.icard(0.62, 5.15, 6.3, 1.7, fill=TINT)
    s.t(0.8, 5.2, 6.0, 1.6, [
        [R("Dois tipos de passo:", sz=1200, b=True)],
        [R("regra", sz=1150, b=True, f=MONO), R("  topo é uma letra grande → troca-a (só espreita)", sz=1150)],
        [R("lê", sz=1150, b=True, f=MONO), R("     topo igual ao símbolo → tira-o e avança", sz=1150)],
        [R("Aceita quando lê  #  com  $  no topo.", sz=1150, c=MUTED)],
    ], aft=300)

    x0, w0 = 7.2, 5.42
    s.ibar(x0, 2.1, w0, "Automatos.criarAPSintaxe()")
    s.icode(x0, 2.55, w0, 4.3, [
        "Estado q  = new Estado(\"q\", false);",
        "Estado qf = new Estado(\"qf\", true);",
        "",
        "regra(q, 'l', 'E', \"L\");",
        "regra(q, 'λ', 'E', \"A\");",
        "regra(q, 'l', 'L', \"li=EnE\");",
        "regra(q, 'λ', 'A', \"λi.E\");",
        "regra(q, '#', 'C', \"\");     // C -> ε",
        "// ... uma linha por regra",
        "",
        "// lê: topo igual ao símbolo",
        "q.transicoes.add(new TransicaoPilha(t, t, \"\", q, true));",
        "q.transicoes.add(new TransicaoPilha('#','$',\"\", qf, true));",
        "return new AutomatoPilha(q, '$', \"E\");",
    ], sz=1080)
    return s


# =====================================================================
# P9/P10/P11 — AP da sintaxe passo a passo
# =====================================================================
SYN = [  # (símbolo da frente, modo, acção, pilha depois [topo primeiro])
    ("λ", "espreita", "E → A", ["A", "$"]),
    ("λ", "espreita", "A → λi.E", ["λ", "i", ".", "E", "$"]),
    ("λ", "lê", "lê λ", ["i", ".", "E", "$"]),
    ("i", "lê", "lê i", [".", "E", "$"]),
    (".", "lê", "lê .", ["E", "$"]),
    ("i", "espreita", "E → P", ["P", "$"]),
    ("i", "espreita", "P → TC", ["T", "C", "$"]),
    ("i", "espreita", "T → i", ["i", "C", "$"]),
    ("i", "lê", "lê i", ["C", "$"]),
    ("i", "espreita", "C → TC", ["T", "C", "$"]),
    ("i", "espreita", "T → i", ["i", "C", "$"]),
    ("i", "lê", "lê i", ["C", "$"]),
    ("#", "espreita", "C → ε", ["$"]),
    ("#", "lê", "aceita", []),
]


def syn_cols(rng, start=None):
    cols = []
    if start: cols.append(start)
    for k in rng:
        ch, md, act, st = SYN[k]
        cols.append(dict(title=f"passo {k + 1}", chip=ch, chiplbl=md, act=act, stack=st,
                         state="acc" if act == "aceita" else "ok"))
    return cols


def p9():
    s = S(); s.frame(LBL, "AP da sintaxe passo a passo — λx.x y  (1/2)")
    s.ibar(0.62, 1.51, 12.0, "procurarPalavra(\"λi.ii#\")   ·   palavra:  λ i . i i #")
    film(s, syn_cols(range(0, 7), dict(title="início", stack=["E", "$"], act="")), y0=1.95, base_y=5.25, elem_h=0.36, fsz=1200)
    s.t(0.62, 5.95, 12.0, 0.8, [[R("espreita", sz=1150, b=True, f=MONO), R(" = aplica uma regra sem avançar      ", sz=1150),
                                 R("lê", sz=1150, b=True, f=MONO), R(" = o topo é igual ao símbolo: tira e avança", sz=1150)]], anchor="ctr")
    return s


def p10():
    s = S(); s.frame(LBL, "AP da sintaxe passo a passo — λx.x y  (2/2)")
    s.ibar(0.62, 1.51, 12.0, "continua com  i i #  por ler   ·   o corpo  x y  é uma aplicação")
    film(s, syn_cols(range(7, 14)), y0=1.95, base_y=4.85, elem_h=0.36, fsz=1200)
    verdict(s, 5.85, True, "14 passos: a pilha ficou vazia ao ler #.", "A expressão λx.x y está bem escrita.")
    return s


def p11():
    s = S(); s.frame(LBL, "AP da sintaxe — uma expressão errada: λx x")
    s.ibar(0.62, 1.51, 12.0, "procurarPalavra(\"λii#\")   ·   falta o ponto depois de  λx")
    cols = [dict(title="início", stack=["E", "$"], act=""),
            dict(title="passo 1", chip="λ", chiplbl="espreita", act="E → A", stack=["A", "$"]),
            dict(title="passo 2", chip="λ", chiplbl="espreita", act="A → λi.E", stack=["λ", "i", ".", "E", "$"]),
            dict(title="passo 3", chip="λ", chiplbl="lê", act="lê λ", stack=["i", ".", "E", "$"]),
            dict(title="passo 4", chip="i", chiplbl="lê", act="lê i", stack=[".", "E", "$"]),
            dict(title="passo 5", chip="i", chiplbl="vem", act="BLOQUEIA", stack=[".", "E", "$"], state="err")]
    film(s, cols, y0=1.95, base_y=5.25, elem_h=0.36, fsz=1200)
    verdict(s, 6.15, False, "O topo pede  .  mas vem  i  (o segundo x): não há transição.",
            "Executavel: Erro sintáctico [1:4]: 'x' inesperado")
    return s


# =====================================================================
# P12 — semântica: regras + código
# =====================================================================
def p12():
    s = S(); s.frame(LBL, "Semântica com uma pilha de nomes")
    s.ibar(0.62, 1.51, 5.9, "PARA CADA TOKEN, DA ESQUERDA PARA A DIREITA")
    rules = [("λ x", "push x", "x passa a existir"),
             ("let x =", "push 'let x'", "marcador: x ainda não existe"),
             ("in", "pop até 'let x', push x", "agora x existe"),
             ("(", "push (", "marcador"),
             (")", "pop até (", "o que abriu lá dentro acaba"),
             ("nome", "procurar na pilha", "não está? ERRO")]
    for k, (tok, act, note) in enumerate(rules):
        y = 2.0 + k * 0.7
        s.box(0.62, y, 1.25, 0.52, tok, fill=INK, color=WHITE, line=None, sz=1200, f=MONO, b=True)
        s.arrow(1.92, y + 0.26, 2.22, y + 0.26)
        s.box(2.27, y, 2.35, 0.52, act, fill=WHITE, line=INK, sz=1000, f=MONO, b=True,
              color=RED if "ERRO" in note else INK)
        s.t(4.7, y, 1.9, 0.52, [[R(note, sz=1000, c=RED if "ERRO" in note else MUTED)]], anchor="ctr")
    s.t(0.62, 6.25, 5.9, 0.5, [[R("Procura do topo para a base: o nome mais recente ganha.", sz=1100, i=True, c=MUTED)]])

    x0, w0 = 6.8, 5.82
    s.ibar(x0, 1.51, w0, "AnalisadorSemantico.verificar()")
    s.icode(x0, 1.95, w0, 4.9, [
        "if (t.tipo.equals(\"LAMBDA\")) {",
        "    pilha.push(x);",
        "} else if (t.tipo.equals(\"LET\")) {",
        "    pilha.push(\"let \" + x);",
        "} else if (t.tipo.equals(\"IN\")) {",
        "    x = popAte(pilha, \"let \").substring(4);",
        "    pilha.push(x);",
        "} else if (t.tipo.equals(\"LPAREN\")) {",
        "    pilha.push(\"(\");",
        "} else if (t.tipo.equals(\"RPAREN\")) {",
        "    popAte(pilha, \"(\");",
        "} else if (t.tipo.equals(\"ID\")) {",
        "    if (!procurar(pilha, t.lexema))",
        "        erros.add(\"variável não ligada\");",
        "}",
    ], sz=1050)
    return s


# =====================================================================
# P13/P14 — semântica passo a passo
# =====================================================================
def p13():
    s = S(); s.frame(LBL, "Pilha de nomes passo a passo — let id = λx.x in id y")
    s.ibar(0.62, 1.51, 12.0, "cinzento = marcador (o nome ainda não existe)   ·   escuro = topo")
    cols = [dict(title="início", stack=[], act=""),
            dict(chip="let id", chiplbl="token", stack=["let id"], act="push", marks={0}),
            dict(chip="λx", chiplbl="token", stack=["x", "let id"], act="push x", marks={1}),
            dict(chip="x", chiplbl="token", stack=["x", "let id"], act="x ✔", marks={1}, state="acc"),
            dict(chip="in", chiplbl="token", stack=["id"], act="pop + push id"),
            dict(chip="id", chiplbl="token", stack=["id"], act="id ✔", state="acc"),
            dict(chip="y", chiplbl="token", stack=["id"], act="y ✘", state="err", keeptop=True)]
    film(s, cols, y0=1.95, base_y=4.75, elem_w=1.15, fsz=1200)
    verdict(s, 5.75, False, "Erro semântico [1:21]: variável 'y' não ligada",
            "x só existia dentro do λ; no  in  sai da pilha e entra id.")
    return s


def p14():
    s = S(); s.frame(LBL, "Pilha de nomes passo a passo — (λx.x) y z")
    s.ibar(0.62, 1.51, 12.0, "o  )  fecha o escopo: tudo o que entrou depois do  (  sai")
    cols = [dict(title="início", stack=[], act=""),
            dict(chip="(", chiplbl="token", stack=["("], act="push (", marks={0}),
            dict(chip="λx", chiplbl="token", stack=["x", "("], act="push x", marks={1}),
            dict(chip="x", chiplbl="token", stack=["x", "("], act="x ✔", marks={1}, state="acc"),
            dict(chip=")", chiplbl="token", stack=[], act="pop até ("),
            dict(chip="y", chiplbl="token", stack=[], act="y ✘", state="err", keeptop=True),
            dict(chip="z", chiplbl="token", stack=[], act="z ✘", state="err", keeptop=True)]
    film(s, cols, y0=1.95, base_y=4.75, elem_w=1.15, fsz=1200)
    verdict(s, 5.75, False, "Dois erros, os dois acumulados:  [1:8] y   e   [1:10] z",
            "A sintaxe está certa (o AP aceita); o problema é só de nomes.")
    return s


# =====================================================================
# P15 — testes
# =====================================================================
def p15():
    s = S(); s.frame(LBL, "Testes — java AutomatoFinito.Testes")
    groups = [("AFD léxico + aula", ["00 aceite", "01 rejeitada", "let id = λx.x in id y", "letter → ID", "lambda1 x → ID ID",
                                     "\\x.x → λ", "palavra li=λi.inii#", "erro léxico em @"]),
              ("AP de parênteses", ["((x))", "(λx.(x))", "(λx.x  rejeita", "x)  rejeita"]),
              ("AP da sintaxe", ["λx.x", "λx.x y", "let id = λx.x in id y", "λf.λx.f (f x)", "(λx.x) y z",
                                 "λx x  rejeita", "(λx.x  rejeita", "let id = x y  rejeita", "f λx.x  rejeita"]),
              ("Pilha de nomes", ["λx.x", "λf.λx.f (f x)", "let id = λx.x in id id", "λx.λx.x  + aviso", "λx.y  [1:4]",
                                  "let f = f in f  [1:9]", "let id = λx.x in x  [1:18]", "(λx.x) y z  [1:8] [1:10]",
                                  "let id = λx.x in id y  [1:21]"])]
    gw = 2.1
    for g, (name, items) in enumerate(groups):
        x = 0.62 + g * (gw + 0.12)
        s.box(x, 1.5, gw, 0.42, name, fill=INK, color=WHITE, line=None, sz=1050, b=True, geom="rect")
        for k, it in enumerate(items):
            y = 2.0 + k * 0.37
            s.t(x, y, 0.3, 0.33, [[R("✔", sz=1100, b=True, c=GREEN)]], anchor="ctr")
            s.t(x + 0.28, y, gw - 0.28, 0.33, [[R(it, sz=900, f=MONO)]], anchor="ctr")
    x0, w0 = 9.62, 3.0
    s.icard(x0, 1.5, w0, 1.9, fill=TINT)
    s.t(x0 + 0.1, 1.55, w0 - 0.2, 1.8, [[R("31 / 31", sz=4400, b=True, algn="ctr")], [R("testes passaram", sz=1200, b=True, algn="ctr")]], anchor="ctr")
    s.icode(x0, 3.55, w0, 1.85, [
        "verificar(nome, obtido,",
        "          esperado) {",
        "  if (obtido == esperado)",
        "       -> OK",
        "  else -> FALHA",
        "}",
    ], sz=1000)
    terminal(s, x0, 5.55, w0, 1.3, [
        "> java AutomatoFinito.Testes",
        "  OK    AP () ((x))",
        "  ...",
        "Resultado: 31 passaram, 0 falharam"], sz=900)
    return s


# =====================================================================
# P16 — tudo junto
# =====================================================================
def p16():
    s = S(); s.frame(LBL, "Tudo junto — java AutomatoFinito.Executavel")
    steps = [("AFD", "texto → tokens"), ("AP", "sintaxe OK?"), ("Pilha de nomes", "variáveis OK?")]
    for k, (a, b) in enumerate(steps):
        x = 0.62 + k * 2.1
        s.box(x, 1.5, 1.8, 0.75, [[R(a, sz=1200, b=True, c=WHITE, algn="ctr")], [R(b, sz=950, c=WHITE, algn="ctr")]], fill=INK, line=None)
        if k < 2: s.arrow(x + 1.83, 1.875, x + 2.07, 1.875)
    s.icode(0.62, 2.45, 6.2, 4.4, [
        "static boolean compilar(String expressao) {",
        "  // 1) AFD",
        "  tokens = lexico.tokenizar(expressao);",
        "  if (!lexico.erros.isEmpty()) return false;",
        "",
        "  // 2) AP",
        "  ap = Automatos.criarAPSintaxe();",
        "  if (!ap.procurarPalavra(palavra(tokens)))",
        "      return false;          // erro sintáctico",
        "",
        "  // 3) pilha de nomes",
        "  return semantico.verificar(tokens);",
        "}",
    ], sz=1150)
    x0, w0 = 7.05, 5.57
    out = [
        "Expressão: λf.λx.f (f x)",
        "  Sintaxe: aceite pelo AP",
        "  λ   push f                  [f]",
        "  λ   push x                  [f, x]",
        "  f   procura f -> encontrada [f, x]",
        "  (   push (                  [f, x, (]",
        "  f   procura f -> encontrada [f, x, (]",
        "  x   procura x -> encontrada [f, x, (]",
        "  )   pop até (               [f, x]",
        "  => ACEITE",
        "",
        "Expressão: let id = λx.x in id y",
        "  Sintaxe: aceite pelo AP",
        "  let push marcador 'let id'  [let id]",
        "  λ   push x                  [let id, x]",
        "  x   procura x -> encontrada [let id, x]",
        "  in  pop até 'let', push id  [id]",
        "  id  procura id -> encontrada [id]",
        "  y   procura y -> ERRO       [id]",
        "  Erro semântico [1:21]: variável 'y' não ligada",
        "  => REJEITADA",
    ]
    terminal(s, x0, 1.5, w0, 5.35, out, sz=950)
    return s


# =====================================================================
# P17 — conclusão
# =====================================================================
def p17():
    s = S(); s.frame("00  /  SÍNTESE", "Conclusão")
    s.text(685800, 1450000, 10881360, 347472,
           [[("Três autómatos, uma pilha, as classes da aula:", dict(sz=2050, b=1, algn="ctr"))]])
    cards = [("01", "AFD", "Corta o texto em tokens. Estado + Transicao + maiorPrefixo()."),
             ("02", "AP de parênteses", "Mostra porque é preciso pilha: conta os ( abertos."),
             ("03", "AP da sintaxe", "Reconhece toda a linguagem com regras na pilha."),
             ("04", "Pilha de nomes", "Verifica se cada variável foi declarada antes de ser usada."),
             ("05", "Passo a passo", "O Executavel imprime cada transição e cada pilha."),
             ("06", "Testes", "31 testes automáticos, todos a passar.")]
    cw, ch, gap = 3500000, 1450000, 260000
    for k, (n, t, d) in enumerate(cards):
        x = 612648 + (k % 3) * (cw + gap)
        y = 2000000 + (k // 3) * (ch + 230000)
        s.card(x, y, cw, ch, fill=TINT if k == 5 else WHITE)
        s.text(x + 130000, y + 190000, 480000, 300000, [[(n, dict(sz=1800, c=MUTED))]])
        s.line(x + 660000, y + 170000, 0, ch - 340000)
        s.text(x + 780000, y + 160000, cw - 880000, 330000, [[(t, dict(sz=1700, b=1))]])
        s.text(x + 780000, y + 540000, cw - 880000, 800000, [[(d, dict(sz=1250))]])
    s.line(1371600, 5480000, 9445752, 0)
    s.text(713232, 5640000, 10835640, 283464, [[("texto  →  AFD  →  tokens  →  AP  →  pilha de nomes  →  expressão válida",
                                                  dict(sz=1450, b=1, algn="ctr"))]])
    s.text(713232, 6071616, 10789920, 219456, [[("Base académica: Tema de Projecto n.º 10; ISUTC — Compiladores, Aulas 7 e 8.",
                                                  dict(sz=1130, c=MUTED, algn="ctr"))]])
    return s


# =====================================================================
prs = Presentation(SRC)
old = list(prs.slides)
blank = old[15].slide_layout
bg = old[15]._element.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}bg')


def add(builder):
    sl = prs.slides.add_slide(blank)
    for shp in list(sl.shapes):
        shp._element.getparent().remove(shp._element)
    cSld = sl._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}cSld')
    cSld.insert(0, copy.deepcopy(bg))
    for el in builder().xml():
        sl.shapes._spTree.append(el)
    return sl


B = {f.__name__: add(f) for f in [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17]}


def set_text(shape, txt):
    runs = [r for p in shape.text_frame.paragraphs for r in p.runs]
    runs[0].text = txt
    for r in runs[1:]: r.text = ""


def shape_by_text(slide, start):
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.startswith(start): return sh
    raise KeyError(start)


set_text(shape_by_text(old[0], "Arquitectura"),
         "Arquitectura   /   Linguagens formais   /   Autómatos na prática (AFD + AP)   /   Análise semântica   /   Java")
set_text(shape_by_text(old[2], "Especificar tokens"), "Reconhecer tokens com um AFD e a sintaxe com autómatos de pilha.")
set_text(shape_by_text(old[2], "Definir o parser"), "Verificar as variáveis com uma pilha de nomes; testar tudo em Java.")
set_text(shape_by_text(old[2], "Lógica de exposição"),
         "Lógica: arquitectura  →  definição formal  →  AFD  →  AP  →  pilha de nomes  →  testes")

# ordem: teoria base intercalada com a prática
order = (old[0:8]                                   # 1-8: intro … AFD (teoria)
         + [B["p1"], B["p2"], B["p3"], B["p4"]]     # AFD na prática
         + old[8:12]                                # parser, AST, erros, AP (teoria)
         + [B["p5"], B["p6"], B["p7"], B["p8"], B["p9"], B["p10"], B["p11"]]   # AP na prática
         + old[12:16]                               # semântica (teoria)
         + [B["p12"], B["p13"], B["p14"]]           # semântica na prática
         + [old[16], B["p15"], B["p16"], B["p17"]]) # casos de teste, testes, tudo junto, conclusão
sldIdLst = prs.slides._sldIdLst
part2sid = {id(prs.part.related_part(sid.rId)): sid for sid in sldIdLst}
ids = [part2sid[id(sl.part)] for sl in order]
dropped = [sid for sid in list(sldIdLst) if sid not in ids]
for sid in list(sldIdLst): sldIdLst.remove(sid)
for sid in ids: sldIdLst.append(sid)
for sid in dropped: prs.part.drop_rel(sid.rId)

N = len(order)
for i, sl in enumerate(order, start=1):
    if i == 1: continue
    for sh in sl.shapes:
        if not sh.has_text_frame: continue
        t = sh.text_frame.text
        if sh.top == 201168 and re.match(r"^\d\d  /  ", t):
            set_text(sh, f"{i-1:02d}" + t[2:])
        elif sh.top == 6574536 and re.match(r"^\d\d  /  \d\d$", t):
            set_text(sh, f"{i:02d}  /  {N}")
prs.save(OUT)
print("slides:", N)
