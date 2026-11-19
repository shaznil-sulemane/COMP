package minilambda;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

/**
 * AUTÓMATO 2 — Autómato de pilha (AP) para o equilíbrio de parênteses.
 *
 *   P = (Q, Σ, Γ, δ, q0, B, F)
 *   Q = { q0, qAceita, qRejeita }    Γ = { (, B }    B = símbolo de base
 *
 *   δ(q0, LPAREN, X) = (q0, ( X)      push (
 *   δ(q0, RPAREN, () = (q0, ε)        pop  (
 *   δ(q0, RPAREN, B) = qRejeita       ")" sem "(" correspondente
 *   δ(q0, outro,  X) = (q0, X)        sem alteração
 *   δ(q0, EOF,    B) = qAceita        aceita se regressar à base
 *
 * Mostra porque um AFD não basta: o número de "(" abertos não tem limite fixo.
 * Opera sobre a sequência de tokens produzida pelo AFD léxico.
 */
public class AutomatoPilhaParenteses {

    public static final char BASE = 'B';

    /** Uma linha da tabela de execução: entrada, acção e conteúdo da pilha. */
    public record Passo(String entrada, String accao, String pilha) {}

    private final List<Passo> passos = new ArrayList<>();
    private String motivo = "";

    public boolean reconhece(List<Token> tokens) {
        Deque<Character> pilha = new ArrayDeque<>();
        pilha.push(BASE);
        passos.clear();
        passos.add(new Passo("início", "inicializar", mostrar(pilha)));

        for (Token t : tokens) {
            switch (t.tipo()) {
                case LPAREN -> {
                    pilha.push('(');
                    passos.add(new Passo("(", "push (", mostrar(pilha)));
                }
                case RPAREN -> {
                    if (pilha.peek() == BASE) {
                        passos.add(new Passo(")", "rejeitar", mostrar(pilha)));
                        motivo = "')' sem '(' correspondente em " + t.pos();
                        return false;
                    }
                    pilha.pop();
                    passos.add(new Passo(")", "pop (", mostrar(pilha)));
                }
                case EOF -> {
                    boolean ok = pilha.peek() == BASE;
                    passos.add(new Passo("EOF", ok ? "aceitar" : "rejeitar", mostrar(pilha)));
                    if (!ok) motivo = (pilha.size() - 1) + " '(' por fechar";
                    return ok;
                }
                default -> passos.add(new Passo(t.toString(), "sem alteração", mostrar(pilha)));
            }
        }
        return false;
    }

    private static String mostrar(Deque<Character> pilha) {
        StringBuilder sb = new StringBuilder();
        for (char c : pilha) sb.append(c).append(' ');   // topo à esquerda
        return sb.toString().trim();
    }

    public List<Passo> passos() { return passos; }
    public String motivo()      { return motivo; }
}
