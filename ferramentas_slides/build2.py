import copy, math, re, sys
sys.path.insert(0, ".")
from helpers import *
from pptx import Presentation

SRC, OUT = sys.argv[1], sys.argv[2]
LBL = "00  /  IMPLEMENTAÇÃO JAVA"
M = dict(f=MONO)


# =====================================================================
# N1 — Base da aula
# =====================================================================
def n1():
    s = S(); s.frame(LBL, "Ponto de partida: as classes da aula")
    s.ibar(0.62, 1.51, 5.6, "EXEMPLO DA AULA  ·  palavras terminadas em 0")
    s.icard(0.62, 1.95, 5.6, 1.75)
    s.t(0.7, 2.62, 0.6, 0.3, [[R("início", sz=1000, c=MUTED)]])
    s.arrow(0.78, 2.95, 1.23, 2.95)
    s.state(1.65, 2.95, 0.8, "q1")
    s.state(4.45, 2.95, 0.8, "q2", terminal=True)
    s.arrow(2.02, 2.78, 4.07, 2.78)
    s.t(2.85, 2.38, 0.4, 0.35, [[R("0", sz=1400, b=1, f=MONO, algn="ctr")]])
    s.arrow(4.07, 3.12, 2.02, 3.12)
    s.t(2.85, 3.15, 0.4, 0.35, [[R("1", sz=1400, b=1, f=MONO, algn="ctr")]])
    s.t(1.25, 2.03, 0.8, 0.3, [[R("↻ 1", sz=1300, b=1, f=MONO, algn="ctr")]])
    s.t(4.05, 2.03, 0.8, 0.3, [[R("↻ 0", sz=1300, b=1, f=MONO, algn="ctr")]])
    s.icode(0.62, 3.85, 5.6, 2.1, [
        "Estado q1 = new Estado();",
        "Estado q2 = new Estado(true);      // terminal",
        "q1.transicoes.add(new Transicao('1', q1));",
        "q1.transicoes.add(new Transicao('0', q2));",
        "q2.transicoes.add(new Transicao('0', q2));",
        "q2.transicoes.add(new Transicao('1', q1));",
        "Automato automato = new Automato(q1);",
    ], sz=1200)
    s.box(0.62, 6.15, 2.7, 0.5, [[R('procurarPalavra("00")  ', sz=1050, f=MONO, c=WHITE), R("true", sz=1100, b=1, f=MONO, c=WHITE)]], fill=INK, line=None)
    s.box(3.52, 6.15, 2.7, 0.5, [[R('procurarPalavra("01")  ', sz=1050, f=MONO), R("false", sz=1100, b=1, f=MONO)]], fill=WHITE)

    x0 = 6.55
    s.ibar(x0, 1.51, 6.07, "A MESMA ESTRUTURA, ESTENDIDA PARA A MINI-LINGUAGEM")
    cw, ch = 1.85, 1.35
    cols = [6.6, 8.69, 10.78]

    def cls(x, y, name, fields, aula=True):
        s.icard(x, y, cw, ch, fill=WHITE if aula else TINT)
        s.t(x + 0.08, y + 0.08, cw - 0.16, 0.32, [[R(name, sz=1000 if len(name) > 14 else 1250, b=1)]])
        s.line(I(x + 0.12), I(y + 0.45), I(cw - 0.24), 0)
        s.t(x + 0.08, y + 0.5, cw - 0.16, ch - 0.55, [[R(f_, sz=950, f=MONO, c=INK if not f_.startswith("+") else MUTED)] for f_ in fields], aft=200)

    y1, y2 = 2.0, 4.3
    cls(cols[0], y1, "Automato", ["estadoInicial", "procurarPalavra()", "+ maiorPrefixo()"])
    cls(cols[1], y1, "Estado", ["transicoes", "terminal", "+ nome, token"])
    cls(cols[2], y1, "Transicao", ["simbolo", "proximoEstado"])
    s.arrow(cols[0] + cw, y1 + 0.67, cols[1], y1 + 0.67)
    s.arrow(cols[1] + cw, y1 + 0.67, cols[2], y1 + 0.67)
    cls(cols[0], y2, "AutomatoPilha", ["base, pilha", "procurarPalavra()", "getPassos()"], aula=False)
    cls(cols[1], y2, "AutomatosLinguagem", ["criarAFDLexico()", "criarAPParenteses()", "criarAPSintaxe()"], aula=False)
    cls(cols[2], y2, "TransicaoPilha", ["+ topo", "+ empilhar", "+ consome"], aula=False)
    s.arrow(cols[2] + cw / 2, y2, cols[2] + cw / 2, y1 + ch, dash=True)
    s.t(cols[2] + cw / 2 + 0.05, y1 + ch + 0.2, 1.0, 0.3, [[R("estende", sz=1000, i=True, c=MUTED)]])
    s.arrow(cols[0] + cw / 2, y2, cols[1] + 0.3, y1 + ch, dash=True)
    s.t(cols[0] + cw / 2 - 0.05, y1 + ch + 0.2, 0.8, 0.3, [[R("usa", sz=1000, i=True, c=MUTED, algn="r")]])
    # legenda
    s.box(6.6, 5.95, 0.3, 0.3, "", fill=WHITE, line=INK)
    s.t(6.98, 5.93, 2.2, 0.35, [[R("classe da aula (mantida)", sz=1100)]], anchor="ctr")
    s.box(9.2, 5.95, 0.3, 0.3, "", fill=TINT, line=INK)
    s.t(9.58, 5.93, 3.0, 0.35, [[R("acrescento do projecto", sz=1100)]], anchor="ctr")
    s.t(6.6, 6.38, 6.0, 0.35, [[R("+ campo/método acrescentado a uma classe da aula", sz=1050, c=MUTED, f=MONO)]])
    return s


# =====================================================================
# N2 — AFD léxico (diagrama)
# =====================================================================
def n2():
    s = S(); s.frame(LBL, "AFD léxico construído com Estado e Transicao")
    s.ibar(0.62, 1.51, 6.35, "DIAGRAMA DE ESTADOS  ·  criarAFDLexico()")
    q0x, q0y, d0 = 1.35, 4.05, 0.78
    s.t(0.6, 3.55, 0.7, 0.3, [[R("início", sz=1000, c=MUTED)]])
    s.arrow(0.62, 4.05, q0x - d0 / 2, 4.05)
    s.state(q0x, q0y, d0, "q0", sz=1300)
    tx, td = 4.05, 0.56
    targets = [("qID", "letra  _", "ID ⇒ qRES", "↻ letra · dígito · _"),
               ("qλ", "λ  \\", "LAMBDA", ""),
               ("qDOT", ".", "DOT", ""),
               ("qLP", "(", "LPAREN", ""),
               ("qRP", ")", "RPAREN", ""),
               ("qEQ", "=", "EQUALS", ""),
               ("qWS", "espaço", "ignorado", "↻ espaço")]
    for k, (nm, lab, tok, loop) in enumerate(targets):
        ty = 2.2 + k * 0.62
        dx, dy = tx - q0x, ty - q0y
        dist = math.hypot(dx, dy)
        ux, uy = dx / dist, dy / dist
        x1, y1 = q0x + ux * d0 / 2, q0y + uy * d0 / 2
        x2, y2 = tx - ux * td / 2, ty - uy * td / 2
        s.arrow(x1, y1, x2, y2, wd=12700)
        ly = y2 - 0.3 if k <= 3 else y2 + 0.04
        s.t(x2 - 1.1, ly, 0.95, 0.26, [[R(lab, sz=950, f=MONO, b=True, algn="r")]], anchor="ctr", ins=0)
        s.state(tx, ty, td, nm, terminal=True, sz=1000)
        paras = [[R(tok, sz=1150, b=True)]]
        if loop: paras.append([R(loop, sz=950, c=MUTED, f=MONO)])
        s.t(tx + 0.38, ty - 0.3, 2.55, 0.6, paras, anchor="ctr")

    x0, w0 = 7.15, 5.47
    s.ibar(x0, 1.51, w0, "CONSTRUÇÃO  ·  mesmo estilo do Executavel")
    s.icode(x0, 1.95, w0, 3.05, [
        "Estado q0  = new Estado(\"q0\",  false, null);",
        "Estado qID = new Estado(\"qID\", true,  ID);",
        "Estado qλ  = new Estado(\"qλ\",  true,  LAMBDA);",
        "Estado qWS = new Estado(\"qWS\", true,  null);",
        "// ... qDOT, qLP, qRP, qEQ",
        "q0.adicionarTransicoes(LETRAS + \"_\", qID);",
        "q0.transicoes.add(new Transicao('λ', qλ));",
        "q0.transicoes.add(new Transicao('.', qDOT));",
        "qID.adicionarTransicoes(LETRAS+DIGITOS+\"_\", qID);",
        "qWS.adicionarTransicoes(ESPACOS, qWS);",
        "return new Automato(q0);",
    ], sz=1100)
    s.ibar(x0, 5.15, w0, "qRES  ·  CLASSIFICAÇÃO DO LEXEMA DE qID")
    pairs = [("lambda", "LAMBDA"), ("let", "LET"), ("in", "IN"), ("outro", "ID")]
    pw = (w0 - 0.3) / 4
    for k, (a, b) in enumerate(pairs):
        x = x0 + k * (pw + 0.1)
        s.box(x, 5.6, pw, 0.42, a, fill=WHITE, sz=1100, f=MONO)
        s.t(x, 6.04, pw, 0.25, [[R("↓", sz=1000, c=MUTED, algn="ctr")]])
        s.box(x, 6.3, pw, 0.42, b, fill=INK, color=WHITE, line=None, sz=1050, b=True)
    return s


# =====================================================================
# N3 — Maior correspondência e palavra de tokens
# =====================================================================
def n3():
    s = S(); s.frame(LBL, "Do texto aos tokens, dos tokens à palavra dos AP")
    s.ibar(0.62, 1.51, 12.0, "1 · O AFD LÊ SEMPRE O MAIOR LEXEMA  (Automato.maiorPrefixo)")
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

    s.ibar(0.62, 3.3, 12.0, "2 · CADA TOKEN VIRA UM SÍMBOLO  →  PALAVRA LIDA PELOS AUTÓMATOS DE PILHA")
    word = [("l", "LET"), ("i", "ID"), ("=", "EQUALS"), ("λ", "LAMBDA"), ("i", "ID"), (".", "DOT"),
            ("i", "ID"), ("n", "IN"), ("i", "ID"), ("i", "ID"), ("#", "EOF")]
    cw, cg = 0.66, 0.12
    cx0 = 0.62 + (12.0 - len(word) * (cw + cg)) / 2
    for k, (c, t) in enumerate(word):
        x = cx0 + k * (cw + cg)
        s.box(x, 3.85, cw, 0.62, c, fill=WHITE, line=INK, sz=2000, f=MONO, b=True)
        s.t(x - 0.1, 4.5, cw + 0.2, 0.25, [[R(t, sz=800, c=MUTED, algn="ctr")]])

    s.icard(0.62, 5.0, 5.85, 1.85)
    s.t(0.8, 5.08, 5.5, 0.35, [[R("Exemplo crítico:  letter", sz=1300, b=True)]])
    for k, c in enumerate("letter"):
        s.box(0.8 + k * 0.42, 5.5, 0.38, 0.4, c, fill=TINT, sz=1200, f=MONO, b=True)
    s.t(3.4, 5.5, 3.0, 0.4, [[R("q0 → qID → … → qID", sz=1050, f=MONO)]], anchor="ctr")
    s.t(0.8, 6.0, 5.5, 0.75, [[R("ID(letter)", sz=1200, b=True, f=MONO), R("  —  nunca  LET + ID(ter): o AFD só pára quando bloqueia.", sz=1150, c=MUTED)]])
    s.icard(6.77, 5.0, 5.85, 1.85, fill=TINT)
    s.t(6.95, 5.08, 5.5, 1.7, [
        [R("Porquê uma palavra de símbolos?", sz=1300, b=True)],
        [R("Os autómatos de pilha usam procurarPalavra(\"li=λi.inii#\"), tal como o AFD da aula usa procurarPalavra(\"00\").", sz=1150)],
        [R("LET→l · IN→n · ID→i · LAMBDA→λ · EOF→#", sz=1050, f=MONO, c=MUTED)],
    ], aft=500)
    return s


# =====================================================================
# N4 — Parser
# =====================================================================
def n4():
    s = S(); s.frame(LBL, "Parser em Java — cada regra é um método")
    s.ibar(0.62, 1.51, 5.95, "REGRA DA GRAMÁTICA  →  MÉTODO")
    rules = [("Expr ::= Let | Lambda | App", "parseExpr()"),
             ("LetExpr ::= let ID = Expr in Expr", "parseLet()"),
             ("LambdaExpr ::= λ ID . Expr", "parseLambda()"),
             ("Application ::= Atom { Atom }", "parseApplication()"),
             ("Atom ::= ID | ( Expr )", "parseAtom()")]
    for k, (r, m) in enumerate(rules):
        y = 2.0 + k * 0.6
        s.box(0.62, y, 3.45, 0.46, r, fill=TINT, sz=1000, f=MONO, algn="l")
        s.arrow(4.12, y + 0.23, 4.45, y + 0.23)
        s.box(4.5, y, 2.07, 0.46, m, fill=INK, color=WHITE, line=None, sz=1050, f=MONO, b=True)
    s.t(0.62, 5.0, 5.95, 0.4, [[R("A pilha de chamadas Java faz o papel da pilha do autómato.", sz=1200, c=MUTED, i=True)]])

    x0 = 6.85
    s.ibar(x0, 1.51, 5.77, "CHAMADAS PARA  let id = λx.x in id y")
    tree = [(0, "parseExpr → parseLet", "Let(id)"),
            (1, "valor: parseLambda", "Lambda(x)"),
            (2, "corpo: parseApplication → parseAtom", "Var(x)"),
            (1, "corpo: parseApplication", "Apply"),
            (2, "parseAtom", "Var(id)"),
            (2, "parseAtom", "Var(y)")]
    for k, (dpt, call, node) in enumerate(tree):
        y = 2.0 + k * 0.52
        x = x0 + 0.05 + dpt * 0.45
        if dpt:
            p = max(j for j in range(k) if tree[j][0] == dpt - 1)
            px = x0 + 0.05 + (dpt - 1) * 0.45 + 0.2
            py = 2.0 + p * 0.52 + 0.44
            s.line(I(px), I(py), 0, I(y + 0.22 - py), MUTED, 12700)
            s.line(I(px), I(y + 0.22), I(x - px), 0, MUTED, 12700)
        w = 3.75 - dpt * 0.45
        s.box(x, y, w, 0.44, call, fill=WHITE, sz=950, f=MONO, algn="l")
        s.box(x0 + 4.05, y, 1.65, 0.44, node, fill=TINT, sz=1000, f=MONO, b=True)
    s.t(x0 + 4.05, 5.15, 1.65, 0.3, [[R("nó da AST", sz=950, c=MUTED, algn="ctr")]])

    s.ibar(0.62, 5.5, 12.0, "ERRO SINTÁCTICO  ·  MODO DE PÂNICO NO catch de parseExpr()")
    steps = ["01 detectar", "02 relatar", "03 sincronizar", "04 retomar"]
    for k, st in enumerate(steps):
        x = 0.62 + k * 1.85
        s.box(x, 6.0, 1.55, 0.5, st, fill=WHITE if k else INK, color=INK if k else WHITE, line=INK if k else None, sz=1050, b=True)
        if k < 3: s.arrow(x + 1.58, 6.25, x + 1.82, 6.25)
    s.t(8.15, 5.92, 4.5, 0.7, [[R("λx x", sz=1100, b=True, f=MONO)],
                               [R("[1:4] esperado '.'; recebido ID(x)", sz=1000, f=MONO, c=RED)]])
    return s


# =====================================================================
# N5 — AP parênteses: pilha passo a passo
# =====================================================================
def n5():
    s = S(); s.frame(LBL, "Autómato de pilha — a pilha a evoluir")
    s.ibar(0.62, 1.51, 12.0, "criarAPParenteses().procurarPalavra(\"((i))#\")   ·   entrada  ((x))")
    steps = [("", ["B"], "início"), ("(", ["(", "B"], "push ("), ("(", ["(", "(", "B"], "push ("),
             ("i", ["(", "(", "B"], "mantém"), (")", ["(", "B"], "pop ("), (")", ["B"], "pop ("),
             ("#", [], "aceitar ✔")]
    cw = 12.0 / 7
    for k, (rd, st, act) in enumerate(steps):
        cx = 0.62 + k * cw + cw / 2
        s.t(cx - 0.6, 1.95, 1.2, 0.25, [[R(f"passo {k}", sz=900, c=MUTED, algn="ctr")]])
        if rd:
            s.box(cx - 0.3, 2.22, 0.6, 0.45, rd, fill=WHITE, line=INK, sz=1400, f=MONO, b=True)
            s.t(cx - 0.6, 2.67, 1.2, 0.22, [[R("lê", sz=850, c=MUTED, algn="ctr")]])
        base = 4.3
        for j, sym in enumerate(reversed(st)):
            top = j == len(st) - 1
            s.box(cx - 0.45, base - (j + 1) * 0.42, 0.9, 0.4, sym, fill=INK if top else TINT,
                  color=WHITE if top else INK, line=None if top else LINE, sz=1300, f=MONO, b=True, geom="rect")
        if not st:
            s.t(cx - 0.6, base - 0.42, 1.2, 0.4, [[R("vazia · qf", sz=1000, c=MUTED, algn="ctr")]], anchor="ctr")
        s.line(I(cx - 0.55), I(base + 0.02), I(1.1), 0, INK, 15875)
        s.t(cx - 0.8, base + 0.08, 1.6, 0.32, [[R(act, sz=1100, b=True, algn="ctr", c=GREEN if "✔" in act else INK)]])
        if k < 6:
            s.arrow(cx + 0.62, 3.6, cx + cw - 0.62, 3.6, color=LINE, wd=12700)
    s.t(0.62, 4.72, 12.0, 0.3, [[R("topo da pilha a escuro  ·  B = símbolo de base  ·  # = fim da entrada (EOF)", sz=1000, c=MUTED, algn="ctr")]])

    s.icode(0.62, 5.1, 7.0, 1.75, [
        "//                   lê   topo  empilha destino",
        "new TransicaoPilha('(', 'B', \"(B\",  q0, true)  // push",
        "new TransicaoPilha('(', '(', \"((\",  q0, true)  // push",
        "new TransicaoPilha(')', '(', \"\",    q0, true)  // pop",
        "new TransicaoPilha('#', 'B', \"\",    qf, true)  // aceitar",
    ], sz=1000)
    for k, (e, m) in enumerate([("(λx.x", "chega a # com '(' no topo"), ("x)", "lê ')' com B no topo")]):
        y = 5.1 + k * 0.9
        s.icard(7.85, y, 4.77, 0.8)
        s.t(8.0, y + 0.05, 1.3, 0.7, [[R(e, sz=1400, b=True, f=MONO)]], anchor="ctr")
        s.t(9.3, y + 0.05, 3.25, 0.7, [[R("REJEITA", sz=1150, b=True, c=RED)], [R(m + " → sem transição", sz=1000, c=MUTED)]], anchor="ctr")
    return s


# =====================================================================
# N6 — AP LL(1): gramática vira transições
# =====================================================================
def n6():
    s = S(); s.frame(LBL, "AP LL(1) — a gramática vira transições")
    leg = [("E", "Expr"), ("L", "Let"), ("A", "Abs"), ("P", "App"), ("C", "Cauda"), ("T", "Atom"), ("$", "base")]
    lw = 12.0 / 7
    for k, (c, n) in enumerate(leg):
        x = 0.62 + k * lw
        s.box(x, 1.5, 0.45, 0.42, c, fill=INK, color=WHITE, line=None, sz=1400, f=MONO, b=True)
        s.t(x + 0.52, 1.5, 1.1, 0.42, [[R(n, sz=1150)]], anchor="ctr")
    cols = [1.85, 1.65, 0.85, 1.9]
    tx = 0.62
    s.ibar(tx, 2.12, sum(cols), "PRODUÇÃO  →  TRANSIÇÃO DE EXPANSÃO (não consome)")
    rows = [["E → L", "l", "E", "L"], ["E → A", "λ", "E", "A"], ["E → P", "i  (", "E", "P"],
            ["L → l i = E n E", "l", "L", "li=EnE"], ["A → λ i . E", "λ", "A", "λi.E"],
            ["P → T C", "i  (", "P", "TC"], ["C → T C", "i  (", "C", "TC"], ["C → ε", "n  )  #", "C", "ε"],
            ["T → i", "i", "T", "i"], ["T → ( E )", "(", "T", "(E)"]]
    end = s.table(I(tx), I(2.55), [I(c) for c in cols], ["PRODUÇÃO", "LÊ (antevisão)", "TOPO", "EMPILHA"], rows,
                  rh=I(0.315), hh=I(0.34), sz=1000, hsz=950, mono_cols=(0, 1, 2, 3))
    s.t(tx, end / EMU + 0.07, sum(cols), 0.5, [
        [R("match:", sz=1050, b=True), R(" topo = token → desempilha e consome     ", sz=1050),
         R("aceitar:", sz=1050, b=True), R(" lê # com $ no topo", sz=1050)]])

    x0 = 7.3; w0 = 12.62 - x0
    s.ibar(x0, 2.12, w0, "AutomatosLinguagem.criarAPSintaxe()")
    s.icode(x0, 2.55, w0, 3.0, [
        "Estado q  = new Estado(\"q\",  false, null);",
        "Estado qf = new Estado(\"qf\", true,  null);",
        "expandir(q, 'l', 'E', \"L\");",
        "expandir(q, 'l', 'L', \"li=EnE\");",
        "expandir(q, 'λ', 'A', \"λi.E\");",
        "expandir(q, 'n', 'C', \"\");      // C → ε",
        "// ... restantes linhas da tabela",
        "for (char t : \"lni=λ.()\".toCharArray())",
        "  q.transicoes.add(new TransicaoPilha(t,t,\"\",q,true));",
        "q.transicoes.add(new TransicaoPilha('#','$',\"\",qf,true));",
        "return new AutomatoPilha(q, '$', \"E\");",
    ], sz=1080)
    s.icard(x0, 5.72, w0, 1.13, fill=WHITE)
    s.t(x0 + 0.15, 5.78, w0 - 0.3, 1.0, [
        [R("FIRST(T) = { i, ( }   ·   FOLLOW(C) = { n, ), # }", sz=1050, f=MONO)],
        [R("Disjuntos ⇒ no máximo uma transição por (token, topo): o AP é determinístico.", sz=1100, c=MUTED)],
    ], aft=400)
    return s


# =====================================================================
# N7 — AP LL(1) em execução (chips)
# =====================================================================
def n7():
    s = S(); s.frame(LBL, "AP LL(1) em execução — λx.x y")
    s.ibar(0.62, 1.51, 8.55, "procurarPalavra(\"λi.ii#\")   ·   saída real do Executavel")
    data = [("E$", "λi.ii#", "E → A"), ("A$", "λi.ii#", "A → λi.E"), ("λi.E$", "λi.ii#", "match λ"),
            ("i.E$", "i.ii#", "match i"), (".E$", ".ii#", "match ."), ("E$", "ii#", "E → P"),
            ("P$", "ii#", "P → TC"), ("TC$", "ii#", "T → i"), ("iC$", "ii#", "match i"),
            ("C$", "i#", "C → TC"), ("TC$", "i#", "T → i"), ("iC$", "i#", "match i"),
            ("C$", "#", "C → ε"), ("$", "#", "aceitar ✔")]
    cols = [0.45, 2.6, 2.6, 2.9]
    y = 1.95; hh, rh = 0.34, 0.33
    s.box(0.62, y, sum(cols), hh, "", fill=INK, line=None, geom="rect")
    cx = 0.62
    for c, h in zip(cols, ["#", "PILHA (topo à esquerda)", "ENTRADA", "ACÇÃO"]):
        s.t(cx + 0.06, y, c, hh, [[R(h, sz=1000, b=True, c=WHITE)]], anchor="ctr")
        cx += c
    y += hh
    chip = 0.27
    for k, (st, inp, act) in enumerate(data):
        s.box(0.62, y, sum(cols), rh, "", fill=TINT if k % 2 == 0 else WHITE, geom="rect")
        s.t(0.68, y, 0.4, rh, [[R(str(k + 1), sz=1000, c=MUTED)]], anchor="ctr")
        x = 0.62 + cols[0] + 0.06
        for j, c in enumerate(st):
            if j == 0:
                s.box(x, y + 0.035, chip, rh - 0.07, c, fill=INK, color=WHITE, line=None, sz=1050, f=MONO, b=True, geom="rect")
            else:
                s.t(x, y, chip, rh, [[R(c, sz=1050, f=MONO, algn="ctr")]], anchor="ctr", ins=0)
            x += chip + 0.04
        x = 0.62 + cols[0] + cols[1] + 0.06
        for j, c in enumerate(inp):
            if j == 0:
                s.box(x, y + 0.035, chip, rh - 0.07, c, fill=WHITE, line=INK, sz=1050, f=MONO, b=True, geom="rect")
            else:
                s.t(x, y, chip, rh, [[R(c, sz=1050, f=MONO, c=MUTED, algn="ctr")]], anchor="ctr", ins=0)
            x += chip + 0.04
        ac = dict(sz=1050, f=MONO, b=act.startswith("aceitar") or "→" in act)
        if act.startswith("aceitar"): ac["c"] = GREEN
        s.t(0.62 + sum(cols[:3]) + 0.06, y, cols[3], rh, [[R(act, **ac)]], anchor="ctr")
        y += rh

    x0 = 9.42; w0 = 12.62 - x0
    s.ibar(x0, 1.51, w0, "COMO LER")
    s.icard(x0, 1.95, w0, 4.95)
    s.box(x0 + 0.2, 2.15, 0.3, 0.3, "E", fill=INK, color=WHITE, line=None, sz=1000, f=MONO, b=True, geom="rect")
    s.t(x0 + 0.6, 2.1, w0 - 0.7, 0.4, [[R("topo da pilha", sz=1150)]], anchor="ctr")
    s.box(x0 + 0.2, 2.6, 0.3, 0.3, "λ", fill=WHITE, line=INK, sz=1000, f=MONO, b=True, geom="rect")
    s.t(x0 + 0.6, 2.55, w0 - 0.7, 0.4, [[R("token lido (antevisão)", sz=1150)]], anchor="ctr")
    s.t(x0 + 0.2, 3.1, w0 - 0.35, 3.7, [
        [R("X → α", sz=1250, b=True, f=MONO)], [R("troca o não-terminal pela produção", sz=1100, c=MUTED)],
        [R("match", sz=1250, b=True, f=MONO)], [R("topo igual ao token: retira e avança", sz=1100, c=MUTED)],
        [R("ACEITA em 14 passos", sz=1250, b=True, c=GREEN)],
        [R("Mesma forma da AST:", sz=1100, c=MUTED)],
        [R("Lambda(x, Apply(x, y))", sz=1000, f=MONO)],
    ], aft=400)
    return s


# =====================================================================
# N8 — Semântica: ligações
# =====================================================================
def n8():
    s = S(); s.frame(LBL, "Análise semântica em Java — quem liga cada nome")
    s.ibar(0.62, 1.51, 7.1, "LIGAÇÕES EM   let id = λx.x in id y")
    toks = ["let", "id", "=", "λ", "x", ".", "x", "in", "id", "y"]
    decl = {1, 4}
    bw, gp = 0.6, 0.08
    x0 = 0.62 + (7.1 - len(toks) * (bw + gp)) / 2
    ty = 3.35
    cx = lambda k: x0 + k * (bw + gp) + bw / 2
    for k, t in enumerate(toks):
        x = x0 + k * (bw + gp)
        if k in decl:
            s.box(x, ty, bw, 0.52, t, fill=INK, color=WHITE, line=None, sz=1300, f=MONO, b=True, geom="rect")
        elif k == 9:
            s.box(x, ty, bw, 0.52, t, fill=WHITE, color=RED, line=RED, sz=1300, f=MONO, b=True, geom="rect")
        elif k in (6, 8):
            s.box(x, ty, bw, 0.52, t, fill=WHITE, line=INK, sz=1300, f=MONO, b=True, geom="rect")
        else:
            s.box(x, ty, bw, 0.52, t, fill=TINT, color=MUTED, sz=1200, f=MONO, geom="rect")
    # setas de ligação (uso → declaração)
    for use, dcl, h, lab in [(6, 4, 2.95, "lookup x ✔"), (8, 1, 2.45, "lookup id ✔")]:
        s.line(I(cx(use)), I(h), 0, I(ty - h), INK, 15875)
        s.line(I(cx(dcl)), I(h), I(cx(use) - cx(dcl)), 0, INK, 15875)
        s.arrow(cx(dcl), h, cx(dcl), ty - 0.02)
        s.t((cx(use) + cx(dcl)) / 2 - 0.8, h - 0.32, 1.6, 0.3, [[R(lab, sz=1000, b=True, algn="ctr", c=GREEN)]])
    s.line(I(cx(9)), I(2.42), 0, I(ty - 2.42), RED, 15875)
    s.t(5.6, 2.02, 2.1, 0.34, [[R("y ✘ sem declaração", sz=1000, b=True, c=RED, algn="r")]])
    # escopos (abaixo)
    for a, b, lab in [(5, 6, "escopo de x"), (8, 9, "escopo de id")]:
        xa = x0 + a * (bw + gp); xb = x0 + b * (bw + gp) + bw
        s.line(I(xa), I(ty + 0.65), I(xb - xa), 0, MUTED, 19050)
        s.t(xa - 0.3, ty + 0.7, xb - xa + 0.6, 0.3, [[R(lab, sz=950, c=MUTED, algn="ctr")]])
    s.t(0.62, 4.45, 7.1, 0.3, [[R("AMBIENTE (TabelaSimbolos) DURANTE O PERCURSO", sz=1000, b=True, c=MUTED)]])
    env = [("{ }", "valor do let"), ("{ x }", "enter λx"), ("{ }", "exit λx"), ("{ id }", "enter let"), ("y ✘", "lookup y")]
    for k, (e, c) in enumerate(env):
        x = 0.62 + k * 1.45
        err = "✘" in e
        s.box(x, 4.8, 1.1, 0.45, e, fill=WHITE if err else TINT, color=RED if err else INK, line=RED if err else LINE, sz=1150, f=MONO, b=True)
        s.t(x - 0.1, 5.27, 1.3, 0.28, [[R(c, sz=900, c=MUTED, algn="ctr")]])
        if k < 4: s.arrow(x + 1.13, 5.02, x + 1.42, 5.02, color=MUTED, wd=12700)
    s.icard(0.62, 5.8, 7.1, 0.95, fill=WHITE)
    s.t(0.8, 5.8, 6.8, 1.0, [
        [R("Erro semântico [1:21]: variável 'y' não ligada", sz=1100, f=MONO, b=True, c=RED)],
        [R("Os erros são acumulados; só se avalia uma expressão fechada (FV(e) = ∅).", sz=1100, c=MUTED)],
    ], aft=400)

    x1 = 7.95; w1 = 12.62 - x1
    s.ibar(x1, 1.51, w1, "AnalisadorSemantico.check()")
    s.icode(x1, 1.95, w1, 4.9, [
        "switch (e) {",
        "  case Var v ->",
        "    if (tabela.lookup(v.nome()) == null)",
        "      erro(v, \"não ligada\");",
        "  case Lambda l -> {",
        "    tabela.enterScope();",
        "    tabela.declare(l.param(), PARAM);",
        "    check(l.corpo());",
        "    tabela.exitScope();",
        "  }",
        "  case Apply a -> {",
        "    check(a.funcao()); check(a.argumento());",
        "  }",
        "  case Let l -> {",
        "    check(l.valor());      // não recursivo",
        "    tabela.enterScope();",
        "    tabela.declare(l.nome(), LET);",
        "    check(l.corpo());",
        "    tabela.exitScope();",
        "  }",
        "}",
    ], sz=1000)
    return s


# =====================================================================
# N9 — Estrutura e validação
# =====================================================================
def n9():
    s = S(); s.frame(LBL, "Organização do código e validação")
    s.ibar(0.62, 1.51, 12.0, "PIPELINE  ·  QUE CLASSE TRATA CADA FASE")
    boxes = [("Código-fonte", "let id = λx.x …"), ("AnalisadorLexico", "AFD · maior lexema"),
             ("Tokens", "li=λi.inii#"), ("AutomatoPilha", "parênteses · LL(1)"),
             ("Parser", "AST"), ("AnalisadorSemantico", "escopos · FV(e)")]
    bw, gp = 1.78, 0.264
    for k, (a, b) in enumerate(boxes):
        x = 0.62 + k * (bw + gp)
        dark = k in (1, 3, 5)
        s.box(x, 2.0, bw, 0.95, [[R(a, sz=1100, b=True, c=WHITE if dark else INK, algn="ctr")],
                                 [R(b, sz=900, f=MONO, c=WHITE if dark else MUTED, algn="ctr")]],
              fill=INK if dark else TINT, line=None if dark else LINE)
        if k < 5: s.arrow(x + bw + 0.03, 2.475, x + bw + gp - 0.03, 2.475)
    s.t(0.62, 3.0, 12.0, 0.3, [[R("caixas escuras = os três reconhecedores e o verificador semântico", sz=1000, c=MUTED, algn="ctr")]])

    s.icard(0.62, 3.5, 7.3, 2.15)
    s.t(0.8, 3.58, 7.0, 0.35, [[R("CLASSES DA AULA  ·  mantidas", sz=1050, b=True, c=MUTED)]])
    for k, n in enumerate(["Estado", "Transicao", "Automato", "Executavel"]):
        s.box(0.8 + k * 1.75, 3.98, 1.6, 0.42, n, fill=WHITE, line=INK, sz=1050, f=MONO, b=True)
    s.t(0.8, 4.5, 7.0, 0.32, [[R("ACRESCENTOS", sz=1050, b=True, c=MUTED)]])
    adds = ["TransicaoPilha", "AutomatoPilha", "AutomatosLinguagem", "AnalisadorLexico", "Parser · Ast", "AnalisadorSemantico"]
    for k, n in enumerate(adds):
        s.box(0.8 + (k % 3) * 2.33, 4.85 + (k // 3) * 0.42, 2.23, 0.34, n, fill=TINT, sz=950, f=MONO)

    s.icard(0.62, 5.8, 7.3, 1.05, fill=WHITE)
    s.t(0.8, 5.83, 7.0, 0.32, [[R("O MESMO RITUAL DA AULA PARA OS TRÊS AUTÓMATOS", sz=1050, b=True, c=MUTED)]])
    rit = ["new Estado(…)", "transicoes.add(…)", "new Automato(q0)", "procurarPalavra(…)"]
    for k, r in enumerate(rit):
        x = 0.8 + k * 1.77
        s.box(x, 6.2, 1.55, 0.48, r, fill=TINT, sz=900, f=MONO, b=True)
        if k < 3: s.arrow(x + 1.57, 6.44, x + 1.75, 6.44)

    x0 = 8.2; w0 = 12.62 - x0
    s.icard(x0, 3.5, w0, 1.6, fill=TINT)
    s.t(x0 + 0.2, 3.55, w0 - 0.3, 1.5, [[R("40 / 40", sz=4000, b=True)],
                                         [R("testes automáticos aprovados", sz=1250, b=True)]], aft=200)
    s.icode(x0, 5.25, w0, 1.6, [
        "cd codigo_java",
        "javac -encoding UTF-8 -d out \\",
        "      src/AutomatoFinito/*.java",
        "java -cp out AutomatoFinito.Testes",
        "java -cp out AutomatoFinito.Executavel",
    ], sz=1000)
    return s


# =====================================================================
# N10 — Conclusão
# =====================================================================
def n10():
    s = S(); s.frame("00  /  SÍNTESE TÉCNICA", "Conclusão estrutural")
    s.text(685800, 1450000, 10881360, 347472,
           [[("Seis decisões dão coerência formal ao interpretador:", dict(sz=2050, b=1, algn="ctr"))]])
    cards = [("01", "Arquitectura", "Estratégia interpretada, com separação entre reconhecimento e avaliação."),
             ("02", "Definição formal", "EBNF, aplicação associativa à esquerda e sintaxe livre de contexto."),
             ("03", "Análise léxica", "AFD com Estado/Transicao, maior lexema e palavras reservadas em qRES."),
             ("04", "Análise sintáctica", "AP LL(1), parser recursivo, AST e recuperação em modo de pânico."),
             ("05", "Análise semântica", "Pilha de escopos, FV(e) = ∅ e erros acumulados com posição."),
             ("06", "Implementação Java", "Classes da aula estendidas para AFD e AP; 40 testes aprovados.")]
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
    s.text(713232, 5640000, 10835640, 283464, [[("Código-fonte  →  tokens (AFD)  →  AST (AP / parser)  →  AST verificada (escopo)  →  avaliação",
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


new = {f.__name__: add(f) for f in [n1, n2, n3, n4, n5, n6, n7, n8, n9, n10]}


def set_text(shape, txt):
    runs = [r for p in shape.text_frame.paragraphs for r in p.runs]
    runs[0].text = txt
    for r in runs[1:]: r.text = ""


def shape_by_text(slide, start):
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.startswith(start): return sh
    raise KeyError(start)


set_text(shape_by_text(old[0], "Arquitectura"),
         "Arquitectura   /   Linguagens formais   /   Análise lexicográfica   /   Análise sintáctica   /   Análise semântica   /   Java")
set_text(shape_by_text(old[2], "Especificar tokens"), "Especificar tokens e reconhecê-los por AFD; fundamentar o autómato de pilha.")
set_text(shape_by_text(old[2], "Definir o parser"), "Definir o parser, a AST e os erros; verificar escopo e ligações (semântica).")
set_text(shape_by_text(old[2], "Lógica de exposição"),
         "Lógica: arquitectura  →  definição formal  →  tokens  →  sintaxe e AST  →  semântica  →  Java")

order = (old[0:8] + [new["n1"], new["n2"], new["n3"]] + old[8:11] + [new["n4"], old[11], new["n5"], new["n6"], new["n7"]]
         + old[12:16] + [new["n8"], old[16], new["n9"], new["n10"]])
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
