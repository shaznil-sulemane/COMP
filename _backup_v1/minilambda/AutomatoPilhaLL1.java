package minilambda;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;

/**
 * AUTÓMATO 3 — Autómato de pilha preditivo LL(1) que reconhece TODA a sintaxe
 * da mini-linguagem (linguagem livre de contexto, Tipo 2).
 *
 * Gramática (EBNF do slide 9) sem a repetição { }:
 *   Expr  → Let | Abs | App
 *   Let   → LET ID EQUALS Expr IN Expr
 *   Abs   → LAMBDA ID DOT Expr
 *   App   → Atom Cauda
 *   Cauda → Atom Cauda | ε
 *   Atom  → ID | LPAREN Expr RPAREN
 *
 * Conjuntos FIRST/FOLLOW:
 *   FIRST(Atom) = { ID, ( }      FOLLOW(Cauda) = FOLLOW(Expr) = { IN, ), EOF }
 * Como são disjuntos, a tabela M[A, a] tem no máximo uma produção por célula:
 * o AP é determinístico.
 *
 * Funcionamento: pilha inicial = [Expr, $].
 *   topo terminal   = lookahead  -> desempilha e consome (match)
 *   topo não-term.  A            -> substitui por M[A, lookahead] (expand)
 *   topo $ e EOF                 -> aceita
 */
public class AutomatoPilhaLL1 {

    /** Não-terminais (símbolos da pilha além dos terminais e de $). */
    public enum NT { Expr, Let, Abs, App, Cauda, Atom }

    /** Símbolo da pilha: terminal, não-terminal ou o fundo $. */
    public record Simbolo(TokenType terminal, NT naoTerminal) {
        static Simbolo t(TokenType t) { return new Simbolo(t, null); }
        static Simbolo n(NT n)        { return new Simbolo(null, n); }
        static final Simbolo FUNDO = new Simbolo(null, null);
        boolean ehTerminal() { return terminal != null; }
        boolean ehFundo()    { return terminal == null && naoTerminal == null; }
        @Override public String toString() {
            return ehFundo() ? "$" : ehTerminal() ? terminal.name() : naoTerminal.name();
        }
    }

    public record Passo(String pilha, String entrada, String accao) {}

    /** Tabela de análise M[A, a] → lado direito da produção (lista vazia = ε). */
    private static final Map<NT, Map<TokenType, List<Simbolo>>> M = new EnumMap<>(NT.class);

    static {
        for (NT n : NT.values()) M.put(n, new EnumMap<>(TokenType.class));
        Simbolo LET = Simbolo.t(TokenType.LET), IN = Simbolo.t(TokenType.IN),
            ID = Simbolo.t(TokenType.ID), EQ = Simbolo.t(TokenType.EQUALS),
            LAM = Simbolo.t(TokenType.LAMBDA), DOT = Simbolo.t(TokenType.DOT),
            LP = Simbolo.t(TokenType.LPAREN), RP = Simbolo.t(TokenType.RPAREN);
        Simbolo E = Simbolo.n(NT.Expr), L = Simbolo.n(NT.Let), A = Simbolo.n(NT.Abs),
            P = Simbolo.n(NT.App), C = Simbolo.n(NT.Cauda), T = Simbolo.n(NT.Atom);

        M.get(NT.Expr).put(TokenType.LET,    List.of(L));
        M.get(NT.Expr).put(TokenType.LAMBDA, List.of(A));
        M.get(NT.Expr).put(TokenType.ID,     List.of(P));
        M.get(NT.Expr).put(TokenType.LPAREN, List.of(P));

        M.get(NT.Let).put(TokenType.LET,     List.of(LET, ID, EQ, E, IN, E));
        M.get(NT.Abs).put(TokenType.LAMBDA,  List.of(LAM, ID, DOT, E));

        M.get(NT.App).put(TokenType.ID,      List.of(T, C));
        M.get(NT.App).put(TokenType.LPAREN,  List.of(T, C));

        M.get(NT.Cauda).put(TokenType.ID,     List.of(T, C));
        M.get(NT.Cauda).put(TokenType.LPAREN, List.of(T, C));
        M.get(NT.Cauda).put(TokenType.IN,     List.of());   // ε
        M.get(NT.Cauda).put(TokenType.RPAREN, List.of());   // ε
        M.get(NT.Cauda).put(TokenType.EOF,    List.of());   // ε

        M.get(NT.Atom).put(TokenType.ID,     List.of(ID));
        M.get(NT.Atom).put(TokenType.LPAREN, List.of(LP, E, RP));
    }

    private final List<Passo> passos = new ArrayList<>();
    private CompilerError erro;

    public boolean reconhece(List<Token> tokens) {
        Deque<Simbolo> pilha = new ArrayDeque<>();
        pilha.push(Simbolo.FUNDO);
        pilha.push(Simbolo.n(NT.Expr));
        passos.clear();
        erro = null;
        int i = 0;

        while (true) {
            Token a = tokens.get(i);
            Simbolo topo = pilha.peek();
            String antes = mostrar(pilha), resto = resto(tokens, i);

            if (topo.ehFundo()) {
                if (a.tipo() == TokenType.EOF) {
                    passos.add(new Passo(antes, resto, "aceitar"));
                    return true;
                }
                return falha(antes, resto, a, "esperado fim da entrada");
            }
            if (topo.ehTerminal()) {
                if (topo.terminal() != a.tipo())
                    return falha(antes, resto, a, "esperado " + topo.terminal());
                pilha.pop();
                i++;
                passos.add(new Passo(antes, resto, "match " + a));
                continue;
            }
            List<Simbolo> prod = M.get(topo.naoTerminal()).get(a.tipo());
            if (prod == null)
                return falha(antes, resto, a, "nenhuma produção para M[" + topo + ", " + a.tipo() + "]");
            pilha.pop();
            for (int k = prod.size() - 1; k >= 0; k--) pilha.push(prod.get(k));
            passos.add(new Passo(antes, resto, topo + " → " + (prod.isEmpty() ? "ε" : junta(prod))));
        }
    }

    private boolean falha(String pilha, String resto, Token a, String msg) {
        passos.add(new Passo(pilha, resto, "rejeitar"));
        erro = new CompilerError(CompilerError.Fase.SINTACTICO, a.linha(), a.coluna(),
                msg + "; recebido " + a);
        return false;
    }

    private static String junta(List<Simbolo> s) {
        StringBuilder sb = new StringBuilder();
        for (Simbolo x : s) sb.append(x).append(' ');
        return sb.toString().trim();
    }

    private static String mostrar(Deque<Simbolo> pilha) {
        StringBuilder sb = new StringBuilder();
        for (Simbolo s : pilha) sb.append(s).append(' ');   // topo à esquerda
        return sb.toString().trim();
    }

    private static String resto(List<Token> tokens, int i) {
        StringBuilder sb = new StringBuilder();
        for (int k = i; k < tokens.size(); k++) sb.append(tokens.get(k).tipo()).append(' ');
        return sb.toString().trim();
    }

    public List<Passo> passos() { return passos; }
    public CompilerError erro() { return erro; }
}
