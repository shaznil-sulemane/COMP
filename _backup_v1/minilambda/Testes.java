package minilambda;

import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Testes automáticos (sem dependências externas) para todos os autómatos e fases.
 *   java -cp out minilambda.Testes
 */
public class Testes {

    static PrintStream out = new PrintStream(System.out, true, StandardCharsets.UTF_8);
    static int ok = 0, falhas = 0;

    public static void main(String[] args) {
        // ---------- AFD léxico ----------
        tokens("let id = λx.x in id y", "LET ID(id) EQUALS LAMBDA ID(x) DOT ID(x) IN ID(id) ID(y) EOF");
        tokens("letter", "ID(letter) EOF");
        tokens("lambda1 x", "ID(lambda1) ID(x) EOF");
        tokens("lambda x. x", "LAMBDA ID(x) DOT ID(x) EOF");
        tokens("\\x.x", "LAMBDA ID(x) DOT ID(x) EOF");
        tokens("nome_1 _a", "ID(nome_1) ID(_a) EOF");
        erroLexico("lambda @. x", "[1:8]");

        // ---------- AP de parênteses ----------
        parenteses("((x))", true);
        parenteses("(λx.(x))", true);
        parenteses("(λx.x", false);
        parenteses("x)", false);

        // ---------- AP LL(1) ----------
        ll1("let id = λx.x in id y", true);
        ll1("λf.λx.f (f x)", true);
        ll1("(λx.x) y z", true);
        ll1("λx x", false);
        ll1("(λx.x", false);
        ll1("let id = x y", false);
        ll1("f λx.x", false);

        // ---------- Parser / AST ----------
        ast("f x y", "Apply(Apply(Var(f), Var(x)), Var(y))");
        ast("let id = λx.x in id y", "Let(id, Lambda(x, Var(x)), Apply(Var(id), Var(y)))");
        ast("λx.x y", "Lambda(x, Apply(Var(x), Var(y)))");
        erroSintactico("λx x", "esperado '.'");
        erroSintactico("(λx.x", "esperado ')'");
        erroSintactico("let id = x y", "esperado 'in'");

        // ---------- Variáveis livres (slide 14) ----------
        fv("λx.x", Set.of());
        fv("λx.x y", Set.of("y"));
        fv("λf.λx.f (f x)", Set.of());
        fv("let id = λx.x in id y", Set.of("y"));
        fv("λx.λx.x", Set.of());

        // ---------- Semântica (slide 17) ----------
        semantica("λx.x", List.of(), 0);
        semantica("λf.λx.f (f x)", List.of(), 0);
        semantica("let id = λx.x in id id", List.of(), 0);
        semantica("λx.λx.x", List.of(), 1);
        semantica("λx.y", List.of("1:4"), 0);
        semantica("let f = f in f", List.of("1:9"), 0);
        semantica("let id = λx.x in x", List.of("1:18"), 0);
        semantica("(λx.x) y z", List.of("1:8", "1:10"), 0);

        out.println();
        out.println("Resultado: " + ok + " passaram, " + falhas + " falharam");
        if (falhas > 0) System.exit(1);
    }

    static void tokens(String src, String esperado) {
        verifica("AFD " + src, Main.tokensStr(new LexerAFD(src).tokenizar()), esperado);
    }

    static void erroLexico(String src, String pos) {
        LexerAFD l = new LexerAFD(src);
        l.tokenizar();
        boolean r = !l.erros().isEmpty() && l.erros().get(0).toString().contains(pos);
        verifica("AFD erro " + src, String.valueOf(r), "true");
    }

    static void parenteses(String src, boolean esperado) {
        verifica("AP() " + src, new AutomatoPilhaParenteses().reconhece(new LexerAFD(src).tokenizar()) + "", esperado + "");
    }

    static void ll1(String src, boolean esperado) {
        verifica("LL1 " + src, new AutomatoPilhaLL1().reconhece(new LexerAFD(src).tokenizar()) + "", esperado + "");
    }

    static void ast(String src, String esperado) {
        verifica("AST " + src, Ast.linear(new Parser(new LexerAFD(src).tokenizar()).parse()), esperado);
    }

    static void erroSintactico(String src, String trecho) {
        Parser p = new Parser(new LexerAFD(src).tokenizar());
        p.parse();
        boolean r = !p.erros().isEmpty() && p.erros().get(0).getMessage().contains(trecho);
        verifica("SIN " + src, String.valueOf(r), "true");
    }

    static void fv(String src, Set<String> esperado) {
        Set<String> r = AnalisadorSemantico.livres(new Parser(new LexerAFD(src).tokenizar()).parse());
        verifica("FV " + src, Set.copyOf(r).equals(esperado) + "", "true");
    }

    static void semantica(String src, List<String> posErros, int avisos) {
        AnalisadorSemantico s = new AnalisadorSemantico();
        s.analisar(new Parser(new LexerAFD(src).tokenizar()).parse());
        String r = s.erros().stream().map(e -> e.linha() + ":" + e.coluna()).collect(Collectors.joining(","))
                + " avisos=" + s.avisos().size();
        verifica("SEM " + src, r, String.join(",", posErros) + " avisos=" + avisos);
    }

    static void verifica(String nome, String obtido, String esperado) {
        if (obtido.equals(esperado)) { ok++; out.println("  ✔ " + nome); }
        else { falhas++; out.println("  ✘ " + nome + "\n      esperado: " + esperado + "\n      obtido:   " + obtido); }
    }
}
