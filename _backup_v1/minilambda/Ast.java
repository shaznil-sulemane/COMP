package minilambda;

/**
 * Árvore Sintáctica Abstracta: retém apenas Var, Lambda, Apply e Let.
 * Cada nó guarda a posição (linha:coluna) do nome que introduz/usa,
 * necessária para os diagnósticos semânticos.
 */
public final class Ast {

    private Ast() {}

    public sealed interface Expr permits Var, Lambda, Apply, Let, Erro {}

    /** Ocorrência de variável:  x */
    public record Var(String nome, int linha, int coluna) implements Expr {}

    /** Abstracção:  λparam.corpo */
    public record Lambda(String param, int linha, int coluna, Expr corpo) implements Expr {}

    /** Aplicação por justaposição:  funcao argumento  (associa à esquerda) */
    public record Apply(Expr funcao, Expr argumento) implements Expr {}

    /** Ligação local não recursiva:  let nome = valor in corpo */
    public record Let(String nome, int linha, int coluna, Expr valor, Expr corpo) implements Expr {}

    /** Nó de erro criado pela recuperação em modo de pânico. */
    public record Erro() implements Expr {}

    /** Forma linear: Let(id, Lambda(x, Var(x)), Apply(Var(id), Var(y))). */
    public static String linear(Expr e) {
        return switch (e) {
            case Var v -> "Var(" + v.nome() + ")";
            case Lambda l -> "Lambda(" + l.param() + ", " + linear(l.corpo()) + ")";
            case Apply a -> "Apply(" + linear(a.funcao()) + ", " + linear(a.argumento()) + ")";
            case Let l -> "Let(" + l.nome() + ", " + linear(l.valor()) + ", " + linear(l.corpo()) + ")";
            case Erro x -> "Erro";
        };
    }

    /** Desenho em árvore (indentação), como no slide 10. */
    public static String arvore(Expr e) {
        StringBuilder sb = new StringBuilder();
        arvore(e, "", true, sb, true);
        return sb.toString();
    }

    private static void arvore(Expr e, String pref, boolean ultimo, StringBuilder sb, boolean raiz) {
        String rotulo = switch (e) {
            case Var v -> "Var(" + v.nome() + ")";
            case Lambda l -> "Lambda(" + l.param() + ")";
            case Apply a -> "Apply";
            case Let l -> "Let(" + l.nome() + ")";
            case Erro x -> "Erro";
        };
        sb.append(pref).append(raiz ? "" : (ultimo ? "└── " : "├── ")).append(rotulo).append('\n');
        String novo = raiz ? "" : pref + (ultimo ? "    " : "│   ");
        Expr[] filhos = switch (e) {
            case Lambda l -> new Expr[]{ l.corpo() };
            case Apply a -> new Expr[]{ a.funcao(), a.argumento() };
            case Let l -> new Expr[]{ l.valor(), l.corpo() };
            default -> new Expr[0];
        };
        for (int i = 0; i < filhos.length; i++)
            arvore(filhos[i], novo, i == filhos.length - 1, sb, false);
    }
}
