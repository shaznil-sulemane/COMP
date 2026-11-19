package minilambda;

import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.List;

/**
 * Demonstração das fases até à análise semântica:
 *   código-fonte → [AFD] tokens → [AP] reconhecimento → [Parser] AST → [Semântica] AST verificada
 *
 * Uso:
 *   java -cp out minilambda.Main                       (demonstração completa)
 *   java -cp out minilambda.Main "let id = λx.x in id y"   (pipeline para uma expressão)
 */
public class Main {

    static PrintStream out = new PrintStream(System.out, true, StandardCharsets.UTF_8);

    public static void main(String[] args) {
        if (args.length > 0) {
            pipeline(String.join(" ", args), true);
            return;
        }
        demoAFD();
        demoPilhaParenteses();
        demoPilhaLL1();
        demoParser();
        demoSemantica();
    }

    /** Executa todas as fases para uma expressão; devolve true se for aceite. */
    static boolean pipeline(String fonte, boolean detalhe) {
        out.println("Entrada: " + fonte);
        LexerAFD lexer = new LexerAFD(fonte);
        List<Token> tokens = lexer.tokenizar();
        if (detalhe) out.println("  Tokens:   " + tokensStr(tokens));
        if (!lexer.erros().isEmpty()) { lexer.erros().forEach(e -> out.println("  " + e)); return false; }

        AutomatoPilhaLL1 ap = new AutomatoPilhaLL1();
        boolean aceiteAP = ap.reconhece(tokens);
        if (detalhe) out.println("  AP LL(1): " + (aceiteAP ? "aceita" : "rejeita"));

        Parser parser = new Parser(tokens);
        Ast.Expr ast = parser.parse();
        if (!parser.erros().isEmpty()) { parser.erros().forEach(e -> out.println("  " + e)); return false; }
        if (detalhe) out.println("  AST:      " + Ast.linear(ast));

        AnalisadorSemantico sem = new AnalisadorSemantico();
        boolean ok = sem.analisar(ast);
        if (detalhe) out.println("  Ligadas:  " + conj(sem.ligadas()) + "   FV = " + conj(AnalisadorSemantico.livres(ast)));
        sem.avisos().forEach(a -> out.println("  " + a));
        sem.erros().forEach(e -> out.println("  " + e));
        out.println("  Resultado: " + (ok ? "ACEITE (expressão fechada)" : "REJEITADA (" + sem.erros().size() + " erro(s))"));
        return ok;
    }

    // ---------------------------------------------------------------- AFD
    static void demoAFD() {
        titulo("AUTÓMATO 1 — AFD LÉXICO (maximal munch + qRES)");
        LexerAFD lx = new LexerAFD("let id = λx.x in id y", true);
        List<Token> ts = lx.tokenizar();
        out.println("Entrada: let id = λx.x in id y");
        lx.passos().forEach(p -> out.println("  " + p));
        out.println("Saída:   " + tokensStr(ts));
        out.println();
        for (String s : new String[]{ "letter", "lambda1 x", "lambda x. x", "\\x.x", "lambda @. x", "1x" }) {
            LexerAFD l = new LexerAFD(s);
            List<Token> t = l.tokenizar();
            out.printf("  %-14s → %s%n", s, tokensStr(t));
            l.erros().forEach(e -> out.println("                   " + e));
        }
    }

    // ---------------------------------------------------- AP parênteses
    static void demoPilhaParenteses() {
        titulo("AUTÓMATO 2 — AP DE EQUILÍBRIO DE PARÊNTESES");
        for (String s : new String[]{ "((x))", "(λx.x", "x)" }) {
            AutomatoPilhaParenteses ap = new AutomatoPilhaParenteses();
            boolean ok = ap.reconhece(new LexerAFD(s).tokenizar());
            out.println("Entrada: " + s);
            out.printf("  %-10s %-14s %s%n", "ENTRADA", "ACÇÃO", "PILHA");
            ap.passos().forEach(p -> out.printf("  %-10s %-14s %s%n", p.entrada(), p.accao(), p.pilha()));
            out.println("  → " + (ok ? "ACEITA" : "REJEITA: " + ap.motivo()));
            out.println();
        }
    }

    // ---------------------------------------------------------- AP LL(1)
    static void demoPilhaLL1() {
        titulo("AUTÓMATO 3 — AP PREDITIVO LL(1) (sintaxe completa)");
        for (String s : new String[]{ "let id = λx.x in id y", "λx x" }) {
            AutomatoPilhaLL1 ap = new AutomatoPilhaLL1();
            boolean ok = ap.reconhece(new LexerAFD(s).tokenizar());
            out.println("Entrada: " + s);
            out.printf("  %-34s %-46s %s%n", "PILHA (topo à esquerda)", "ENTRADA", "ACÇÃO");
            ap.passos().forEach(p -> out.printf("  %-34s %-46s %s%n", p.pilha(), p.entrada(), p.accao()));
            out.println("  → " + (ok ? "ACEITA" : "REJEITA: " + ap.erro()));
            out.println();
        }
    }

    // ------------------------------------------------------------- Parser
    static void demoParser() {
        titulo("PARSER DESCENDENTE RECURSIVO → AST");
        String s = "let id = λx.x in id y";
        Parser p = new Parser(new LexerAFD(s).tokenizar());
        Ast.Expr ast = p.parse();
        out.println("Entrada: " + s);
        out.println("  " + Ast.linear(ast));
        out.print(Ast.arvore(ast).indent(2));
        out.println("  f x y → " + Ast.linear(new Parser(new LexerAFD("f x y").tokenizar()).parse()));
        out.println();
        out.println("Erros sintácticos (modo de pânico):");
        for (String e : new String[]{ "λx x", "(λx.x", "let id = x y", "let = x in y" }) {
            Parser pe = new Parser(new LexerAFD(e).tokenizar());
            pe.parse();
            out.printf("  %-14s %s%n", e, pe.erros().get(0));
        }
    }

    // ---------------------------------------------------------- Semântica
    static void demoSemantica() {
        titulo("ANÁLISE SEMÂNTICA — ESCOPO E LIGAÇÕES");
        String s = "let id = λx.x in id y";
        AnalisadorSemantico sem = new AnalisadorSemantico();
        sem.analisar(new Parser(new LexerAFD(s).tokenizar()).parse());
        out.println("Percurso de: " + s);
        out.printf("  %-12s %-20s %s%n", "NÓ", "ACÇÃO", "AMBIENTE");
        sem.passos().forEach(p -> out.printf("  %-12s %-20s %s%n", p.no(), p.accao(), p.ambiente()));
        sem.erros().forEach(e -> out.println("  " + e));
        out.println();

        out.println("Casos de teste (slide 17):");
        String[][] casos = {
            { "V1", "λx.x" }, { "V2", "λf.λx.f (f x)" }, { "V3", "let id = λx.x in id id" },
            { "V4", "λx.λx.x" }, { "I1", "λx.y" }, { "I2", "let f = f in f" },
            { "I3", "let id = λx.x in x" }, { "I4", "(λx.x) y z" },
        };
        for (String[] c : casos) {
            out.print(c[0] + "  ");
            pipeline(c[1], false);
        }
    }

    // ---------------------------------------------------------- utilitários
    static String tokensStr(List<Token> ts) {
        StringBuilder sb = new StringBuilder();
        for (Token t : ts) sb.append(t).append(' ');
        return sb.toString().trim();
    }

    static String conj(java.util.Set<String> s) {
        return s.isEmpty() ? "∅" : "{ " + String.join(", ", s) + " }";
    }

    static void titulo(String t) {
        out.println();
        out.println("=".repeat(78));
        out.println(t);
        out.println("=".repeat(78));
    }
}
