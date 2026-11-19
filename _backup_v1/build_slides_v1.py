import copy, re, sys
from xml.sax.saxutils import escape
from lxml import etree
from pptx import Presentation

SRC, OUT = sys.argv[1], sys.argv[2]
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


# =====================================================================
def slide_afd():
    s = S(); s.frame("00  /  IMPLEMENTAÇÃO JAVA", "AFD léxico em Java — tabela de transição δ")
    lw = 5650000
    s.bar(L, 1380744, lw, "FUNÇÃO DE TRANSIÇÃO  δ  ·  LexerAFD.DELTA")
    cols = [770000] + [542000] * 9
    X = "✗"
    end = s.table(L, 1792224, cols,
                  ["δ", "letra", "díg.", "_", "λ  \\", ".", "(", ")", "=", "esp."],
                  [["q0", "qID", X, "qID", "qλ", "qDOT", "qLP", "qRP", "qEQ", "qWS"],
                   ["qID", "qID", "qID", "qID", X, X, X, X, X, X],
                   ["qWS", X, X, X, X, X, X, X, X, "qWS"]],
                  rh=400000, sz=1000, hsz=1000, mono_cols=range(10), algn="ctr")
    s.text(L, end + 80000, lw, 420000,
           [[("qλ, qDOT, qLP, qRP, qEQ: aceitação sem saídas.   ✗ = qERR → bloqueio: emitir o último estado aceite.", dict(sz=1150, c=MUTED))]])
    cy = end + 600000
    s.card(L, cy, lw, 5420000 - cy)
    s.text(L + 180000, cy + 130000, lw - 300000, 5420000 - cy - 200000, [
        [("M = (Q, Σ, δ, q0, F)", dict(sz=1600, b=1))],
        [("Q = { q0, qID, qλ, qDOT, qLP, qRP, qEQ, qWS, qERR }", dict(sz=1150, f=MONO))],
        [("F = Q \\ { q0, qERR }", dict(sz=1150, f=MONO))],
        [("qRES:  lambda→LAMBDA · let→LET · in→IN · outro→ID", dict(sz=1150, f=MONO))],
    ], aft=500)

    rx = L + lw + 300000; rw = RIGHT_END - rx
    s.bar(rx, 1380744, rw, "SIMULAÇÃO COM MAXIMAL MUNCH  ·  tokenizar()")
    s.code(rx, 1792224, rw, 5420000 - 1792224, [
        "int estado = Q0, ultimoAceite = -1, fim = -1;",
        "for (int i = pos; i < fonte.length(); i++) {",
        "  int prox = DELTA[estado][classe(fonte.charAt(i))];",
        "  if (prox == QERR) break;        // bloqueio",
        "  estado = prox;",
        "  if (ACEITA[estado]) {           // memoriza",
        "    ultimoAceite = estado; fim = i + 1;",
        "  }",
        "}",
        "if (ultimoAceite == -1) erroLexico(c, linha, col);",
        "String lexema = fonte.substring(pos, fim);",
        "TokenType tipo = EMITE[ultimoAceite];",
        "if (ultimoAceite == QID)          // estado qRES",
        "  tipo = RESERVADAS.getOrDefault(lexema, ID);",
    ], sz=1100)

    s.rect(L, 5560000, RIGHT_END - L, 800000)
    s.text(L + 150000, 5600000, RIGHT_END - L - 300000, 720000, [
        [("let     ", dict(sz=1100, f=MONO, b=1)), ("q0 -l→ qID -e→ qID -t→ qID ⇒ qRES ⇒ LET", dict(sz=1100, f=MONO)),
         ("        letter ⇒ ID(letter)", dict(sz=1100, f=MONO))],
        [("lambda1 x ⇒ ID(lambda1) ID(x)", dict(sz=1100, f=MONO)),
         ("     lambda @. x ⇒ Erro léxico [1:8]: carácter '@' não reconhecido", dict(sz=1100, f=MONO))],
    ], anchor="ctr", aft=400)
    return s


def slide_parser():
    s = S(); s.frame("00  /  IMPLEMENTAÇÃO JAVA", "Parser descendente recursivo em Java")
    w = (RIGHT_END - L - 300000) // 2
    s.bar(L, 1380744, w, "parseExpr()  ·  LOOKAHEAD + MODO DE PÂNICO")
    s.code(L, 1792224, w, 3450000, [
        "Ast.Expr parseExpr() {",
        "  try {",
        "    return switch (espiar().tipo()) {",
        "      case LET        -> parseLet();",
        "      case LAMBDA     -> parseLambda();",
        "      case ID, LPAREN -> parseApplication();",
        "      default -> throw erro(\"esperado expressão\");",
        "    };",
        "  } catch (CompilerError e) {  // 01 detectar",
        "    erros.add(e);              // 02 relatar",
        "    sincronizar();             // 03 IN, ), EOF",
        "    return new Ast.Erro();     // 04 retomar",
        "  }",
        "}",
    ], sz=1150)
    rx = L + w + 300000
    s.bar(rx, 1380744, w, "parseLet()  ·  parseApplication()")
    s.code(rx, 1792224, w, 3450000, [
        "Ast.Expr parseLet() {",
        "  consumir(LET);",
        "  Token nome = consumir(ID);",
        "  consumir(EQUALS);",
        "  Ast.Expr valor = parseExpr();",
        "  consumir(IN);",
        "  Ast.Expr corpo = parseExpr();",
        "  return new Ast.Let(nome, valor, corpo);",
        "}",
        "Ast.Expr parseApplication() {",
        "  Ast.Expr e = parseAtom();",
        "  while (verifica(ID) || verifica(LPAREN))",
        "    e = new Ast.Apply(e, parseAtom()); // à esq.",
        "  return e;",
        "}",
    ], sz=1150)
    s.bar(L, 5380000, RIGHT_END - L, "SAÍDA REAL DO PARSER")
    s.text(L + 120000, 5740000, 6900000, 720000, [
        [("λx x          →  Erro sintáctico [1:4]: esperado '.'; recebido ID(x)", dict(sz=1050, f=MONO))],
        [("(λx.x         →  Erro sintáctico [1:6]: esperado ')'; recebido EOF", dict(sz=1050, f=MONO))],
        [("let id = x y  →  Erro sintáctico [1:13]: esperado 'in'; recebido EOF", dict(sz=1050, f=MONO))],
    ], aft=200)
    s.line(L + 7150000, 5800000, 0, 600000)
    s.text(L + 7300000, 5740000, RIGHT_END - L - 7350000, 720000, [
        [("f x y  →", dict(sz=1050, f=MONO, b=1))],
        [("Apply(Apply(Var(f), Var(x)), Var(y))", dict(sz=1050, f=MONO))],
    ], aft=200)
    return s


def slide_ap_paren():
    s = S(); s.frame("00  /  IMPLEMENTAÇÃO JAVA", "Autómato de pilha em Java — parênteses")
    lw = 4900000
    s.bar(L, 1380744, lw, "DEFINIÇÃO FORMAL")
    s.card(L, 1792224, lw, 3150000)
    s.text(L + 180000, 1900000, lw - 300000, 2950000, [
        [("P = (Q, Σ, Γ, δ, q0, B, F)", dict(sz=1800, b=1))],
        [("Γ = { (, B }   ·   B = símbolo de base", dict(sz=1200, c=MUTED))],
        [("δ(q0, (,   X) = (q0, ( X)   push", dict(sz=1250, f=MONO))],
        [("δ(q0, ),   () = (q0, ε)     pop", dict(sz=1250, f=MONO))],
        [("δ(q0, ),   B) = rejeitar", dict(sz=1250, f=MONO))],
        [("δ(q0, a,   X) = (q0, X)     a ∉ { (, ) }", dict(sz=1250, f=MONO))],
        [("δ(q0, EOF, B) = aceitar", dict(sz=1250, f=MONO))],
        [("Lê os tokens LPAREN / RPAREN emitidos pelo AFD.", dict(sz=1200, c=MUTED))],
    ], aft=600)
    rx = L + lw + 300000; rw = RIGHT_END - rx
    s.bar(rx, 1380744, rw, "AutomatoPilhaParenteses.reconhece()")
    s.code(rx, 1792224, rw, 3150000, [
        "Deque<Character> pilha = new ArrayDeque<>();",
        "pilha.push('B');                     // base",
        "for (Token t : tokens) {",
        "  switch (t.tipo()) {",
        "    case LPAREN -> pilha.push('(');",
        "    case RPAREN -> {",
        "      if (pilha.peek() == 'B') return false;",
        "      pilha.pop();",
        "    }",
        "    case EOF -> { return pilha.peek() == 'B'; }",
        "    default  -> { }                  // sem alteração",
        "  }",
        "}",
    ], sz=1150)
    tiles = [("((x))", "ACEITA", "pilha regressa a B"),
             ("(λx.x", "REJEITA", "1 '(' por fechar no EOF"),
             ("x)", "REJEITA", "')' sem '(' em 1:2")]
    tw = (RIGHT_END - L - 2 * 300000) // 3
    for k, (e, r, m) in enumerate(tiles):
        tx = L + k * (tw + 300000)
        s.card(tx, 5150000, tw, 1150000, fill=TINT if k == 0 else WHITE)
        s.text(tx + 180000, 5230000, tw - 300000, 1000000, [
            [(e, dict(sz=1600, f=MONO, b=1))],
            [(r, dict(sz=1300, b=1))],
            [(m, dict(sz=1150, c=MUTED))],
        ], aft=300)
    return s


def slide_ll1():
    s = S(); s.frame("00  /  IMPLEMENTAÇÃO JAVA", "Autómato de pilha LL(1) — sintaxe completa")
    cols = [900000, 1450000, 1500000, 1050000, 1200000, 700000]
    lw = sum(cols)
    s.bar(L, 1380744, lw, "TABELA DE ANÁLISE  M[A, a]")
    E = ("—", dict(c=LINE))
    end = s.table(L, 1792224, cols, ["A", "LET", "LAMBDA", "ID", "(", "IN ) EOF"], [
        [("Expr", dict(b=1)), "Let", "Abs", "App", "App", E],
        [("Let", dict(b=1)), "LET ID =\nExpr IN Expr", E, E, E, E],
        [("Abs", dict(b=1)), E, "LAMBDA ID .\nExpr", E, E, E],
        [("App", dict(b=1)), E, E, "Atom Cauda", "Atom Cauda", E],
        [("Cauda", dict(b=1)), E, E, "Atom Cauda", "Atom Cauda", "ε"],
        [("Atom", dict(b=1)), E, E, "ID", "( Expr )", E],
    ], rh=430000, sz=1000, hsz=1000, mono_cols=range(1, 6))
    s.card(L, end + 180000, lw, 6330000 - end - 180000)
    s.text(L + 180000, end + 260000, lw - 300000, 6330000 - end - 320000, [
        [("FIRST(Atom) = { ID, ( }   ·   FOLLOW(Cauda) = { IN, ), EOF }", dict(sz=1150, f=MONO))],
        [("Cauda → Atom Cauda | ε   substitui  { Atom }  da EBNF", dict(sz=1150, f=MONO))],
        [("Conjuntos disjuntos ⇒ uma produção por célula ⇒ AP determinístico. Célula vazia = erro sintáctico.", dict(sz=1300, c=MUTED))],
    ], aft=500)
    rx = L + lw + 300000; rw = RIGHT_END - rx
    s.bar(rx, 1380744, rw, "AutomatoPilhaLL1.reconhece()")
    s.code(rx, 1792224, rw, 6330000 - 1792224, [
        "pilha.push(FUNDO); pilha.push(Expr);",
        "while (true) {",
        "  Token a = tokens.get(i);",
        "  Simbolo X = pilha.peek();",
        "  if (X.ehFundo())",
        "    return a.tipo() == EOF; // aceitar",
        "  if (X.ehTerminal()) {",
        "    if (X.terminal() != a.tipo())",
        "      return falha(a);",
        "    pilha.pop(); i++;       // match",
        "  } else {",
        "    var rhs = M.get(X).get(a.tipo());",
        "    if (rhs == null) return falha(a);",
        "    pilha.pop();            // expand",
        "    for (int k = rhs.size()-1; k >= 0; k--)",
        "      pilha.push(rhs.get(k));",
        "  }",
        "}",
    ], sz=1100)
    return s


def slide_ll1_trace():
    s = S(); s.frame("00  /  IMPLEMENTAÇÃO JAVA", "Execução do AP LL(1) para  λx.x y")
    trace = """Expr $|LAMBDA ID DOT ID ID EOF|Expr → Abs
Abs $|LAMBDA ID DOT ID ID EOF|Abs → LAMBDA ID DOT Expr
LAMBDA ID DOT Expr $|LAMBDA ID DOT ID ID EOF|match LAMBDA
ID DOT Expr $|ID DOT ID ID EOF|match ID(x)
DOT Expr $|DOT ID ID EOF|match DOT
Expr $|ID ID EOF|Expr → App
App $|ID ID EOF|App → Atom Cauda
Atom Cauda $|ID ID EOF|Atom → ID
ID Cauda $|ID ID EOF|match ID(x)
Cauda $|ID EOF|Cauda → Atom Cauda
Atom Cauda $|ID EOF|Atom → ID
ID Cauda $|ID EOF|match ID(y)
Cauda $|EOF|Cauda → ε
$|EOF|aceitar""".split("\n")
    rows = []
    for k, t in enumerate(trace):
        p, e, a = t.split("|")
        if a == "aceitar": a = ("aceitar ✔", dict(b=1))
        rows.append([str(k + 1), p, e, a])
    cols = [420000, 2450000, 2500000, 2650000]
    lw = sum(cols)
    s.bar(L, 1380744, lw, "SAÍDA DE  java minilambda.Main  (topo da pilha à esquerda)")
    s.table(L, 1792224, cols, ["#", "PILHA", "ENTRADA", "ACÇÃO"], rows, rh=300000, hh=330000,
            sz=1000, hsz=1000, mono_cols=(0, 1, 2, 3))
    rx = L + lw + 300000; rw = RIGHT_END - rx
    s.bar(rx, 1380744, rw, "LEITURA")
    s.card(rx, 1792224, rw, 4530000)
    s.text(rx + 160000, 1900000, rw - 280000, 4350000, [
        [("expand", dict(sz=1400, b=1))],
        [("Não-terminal no topo: troca-o por M[A, a].", dict(sz=1200, c=MUTED))],
        [("match", dict(sz=1400, b=1))],
        [("Terminal igual ao lookahead: desempilha e consome.", dict(sz=1200, c=MUTED))],
        [("aceitar", dict(sz=1400, b=1))],
        [("Pilha = $ e entrada = EOF.", dict(sz=1200, c=MUTED))],
        [("14 passos · 1 lookahead", dict(sz=1400, b=1))],
        [("Mesma estrutura que o parser devolve como AST:", dict(sz=1200, c=MUTED))],
        [("Lambda(x, Apply(Var(x), Var(y)))", dict(sz=1000, f=MONO))],
    ], aft=500)
    return s


def slide_sem():
    s = S(); s.frame("00  /  IMPLEMENTAÇÃO JAVA", "Analisador semântico em Java")
    lw = 5900000
    s.bar(L, 1380744, lw, "AnalisadorSemantico.check()  ·  PERCURSO DA AST")
    s.code(L, 1792224, lw, 4540000, [
        "void check(Ast.Expr e) {",
        "  switch (e) {",
        "    case Var v -> {",
        "      if (tabela.lookup(v.nome()) == null)",
        "        erros.add(erro(v, \"variável não ligada\"));",
        "    }",
        "    case Lambda l -> {",
        "      tabela.enterScope();",
        "      tabela.declare(l.param(), PARAM, l.pos());",
        "      check(l.corpo());",
        "      tabela.exitScope();",
        "    }",
        "    case Apply a -> { check(a.funcao()); check(a.argumento()); }",
        "    case Let l -> {",
        "      check(l.valor());            // não recursivo",
        "      tabela.enterScope();",
        "      tabela.declare(l.nome(), LET, l.pos());",
        "      check(l.corpo());",
        "      tabela.exitScope();",
        "    }",
        "  }",
        "}",
    ], sz=1100)
    rx = L + lw + 300000; rw = RIGHT_END - rx
    s.bar(rx, 1380744, rw, "TabelaSimbolos  ·  PILHA DE ESCOPOS")
    s.code(rx, 1792224, rw, 1650000, [
        "Deque<Map<String,Simbolo>> escopos;",
        "Simbolo lookup(String nome) {",
        "  for (var escopo : escopos) // interno→externo",
        "    if (escopo.containsKey(nome))",
        "      return escopo.get(nome);",
        "  return null;               // ∅",
        "}",
    ], sz=1100)
    s.bar(rx, 3600000, rw, "DIAGNÓSTICOS REAIS")
    s.card(rx, 4012000, rw, 2320000)
    s.text(rx + 150000, 4100000, rw - 250000, 2200000, [
        [("λx.y", dict(sz=1100, f=MONO, b=1))],
        [("Erro semântico [1:4]: variável 'y' não ligada", dict(sz=1000, f=MONO))],
        [("λx.λx.x", dict(sz=1100, f=MONO, b=1))],
        [("Aviso [1:5]: 'x' oculta a declaração em 1:2", dict(sz=1000, f=MONO))],
        [("let f = f in f", dict(sz=1100, f=MONO, b=1))],
        [("Erro semântico [1:9]: variável 'f' não ligada", dict(sz=1000, f=MONO))],
        [("Erros acumulados; só avalia se FV(e) = ∅.", dict(sz=1150, c=MUTED))],
    ], aft=300)
    return s


def slide_validacao():
    s = S(); s.frame("00  /  IMPLEMENTAÇÃO JAVA", "Estrutura do código e validação")
    cols = [2900000, 3400000]
    lw = sum(cols)
    s.bar(L, 1380744, lw, "PACOTE  minilambda  (Java 21)")
    s.table(L, 1792224, cols, ["FICHEIRO", "PAPEL"], [
        ["LexerAFD.java", ("Autómato 1 · AFD léxico", dict(b=1))],
        ["AutomatoPilhaParenteses.java", ("Autómato 2 · AP de parênteses", dict(b=1))],
        ["AutomatoPilhaLL1.java", ("Autómato 3 · AP LL(1) da sintaxe", dict(b=1))],
        ["Parser.java · Ast.java", "Descendente recursivo e AST"],
        ["TabelaSimbolos.java", "Ambiente em pilha de escopos"],
        ["AnalisadorSemantico.java", "Escopo, FV(e), erros e avisos"],
        ["Token · TokenType · CompilerError", "Tokens e diagnósticos com posição"],
        ["Main.java · Testes.java", "Demonstração e testes automáticos"],
    ], rh=480000, sz=1100, hsz=1050, mono_cols=(0,))
    rx = L + lw + 300000; rw = RIGHT_END - rx
    s.card(rx, 1380744, rw, 2100000, fill=TINT)
    s.text(rx + 200000, 1480000, rw - 350000, 2200000, [
        [("37 / 37", dict(sz=4400, b=1))],
        [("testes automáticos aprovados", dict(sz=1400, b=1))],
        [("AFD · AP parênteses · AP LL(1) · AST · erros sintácticos · FV(e) · casos V1–V4 e I1–I4", dict(sz=1200, c=MUTED))],
    ], aft=500)
    s.bar(rx, 3700000, rw, "COMPILAR E EXECUTAR")
    s.code(rx, 4112000, rw, 2220000, [
        "cd codigo_java",
        "javac -encoding UTF-8 -d out \\",
        "      src/minilambda/*.java",
        "java -cp out minilambda.Testes",
        "java -cp out minilambda.Main",
        "java -cp out minilambda.Main \"\\x.x y\"",
    ], sz=1200)
    return s


def slide_conclusao():
    s = S(); s.frame("00  /  SÍNTESE TÉCNICA", "Conclusão estrutural")
    s.text(685800, 1450000, 10881360, 347472,
           [[("Seis decisões dão coerência formal ao interpretador:", dict(sz=2050, b=1, algn="ctr"))]])
    cards = [("01", "Arquitectura", "Estratégia interpretada, com separação entre reconhecimento e avaliação."),
             ("02", "Definição formal", "EBNF, aplicação associativa à esquerda e sintaxe livre de contexto."),
             ("03", "Análise léxica", "AFD por tabela, palavras reservadas em qRES e maximal munch."),
             ("04", "Análise sintáctica", "AP LL(1), parser recursivo, AST e recuperação em modo de pânico."),
             ("05", "Análise semântica", "Pilha de escopos, FV(e) = ∅ e erros acumulados com posição."),
             ("06", "Implementação Java", "Três autómatos e verificador semântico, validados por 37 testes.")]
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
    tree = sl.shapes._spTree
    for el in builder().xml():
        tree.append(el)
    return sl


new = {k: add(f) for k, f in [("afd", slide_afd), ("parser", slide_parser), ("ap", slide_ap_paren),
                              ("ll1", slide_ll1), ("trace", slide_ll1_trace), ("sem", slide_sem),
                              ("val", slide_validacao), ("concl", slide_conclusao)]}


def set_text(shape, txt):
    runs = [r for p in shape.text_frame.paragraphs for r in p.runs]
    runs[0].text = txt
    for r in runs[1:]: r.text = ""


def shape_by_text(slide, start):
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.startswith(start): return sh
    raise KeyError(start)


# ---- edits to existing slides ----
set_text(shape_by_text(old[0], "Arquitectura"),
         "Arquitectura   /   Linguagens formais   /   Análise lexicográfica   /   Análise sintáctica   /   Análise semântica   /   Java")
set_text(shape_by_text(old[2], "Especificar tokens"), "Especificar tokens e reconhecê-los por AFD; fundamentar o autómato de pilha.")
set_text(shape_by_text(old[2], "Definir o parser"), "Definir o parser, a AST e os erros; verificar escopo e ligações (semântica).")
set_text(shape_by_text(old[2], "Lógica de exposição"),
         "Lógica: arquitectura  →  definição formal  →  tokens  →  sintaxe e AST  →  semântica  →  Java")

# ---- final order ----
order = (old[0:8] + [new["afd"]] + old[8:11] + [new["parser"]] + [old[11], new["ap"], new["ll1"], new["trace"]]
         + old[12:16] + [new["sem"], old[16], new["val"], new["concl"]])
sldIdLst = prs.slides._sldIdLst
by_rid = {sid.rId: sid for sid in sldIdLst}
slide_rid = {}
for sid in sldIdLst:
    slide_rid[id(prs.part.related_part(sid.rId))] = sid.rId
ids = [by_rid[slide_rid[id(s.part)]] for s in order]
dropped = [sid for sid in list(sldIdLst) if sid not in ids]
for sid in list(sldIdLst): sldIdLst.remove(sid)
for sid in ids: sldIdLst.append(sid)
for sid in dropped: prs.part.drop_rel(sid.rId)

# ---- renumber section labels and page numbers ----
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
