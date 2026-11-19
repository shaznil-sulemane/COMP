package AutomatoFinito;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.StringJoiner;

/**
 * Tabela de símbolos como ambiente: pilha de escopos (alínea E).
 * Cada λ e cada let abre um escopo novo; o lookup percorre do escopo mais
 * interno para o mais externo, resolvendo o sombreamento para a declaração
 * mais próxima (escopo léxico/estático).
 */
public class TabelaSimbolos {

    public enum Tipo { PARAM, LET }

    /** Símbolo: nome, tipo (PARAM ou LET) e posição linha:coluna. */
    public record Simbolo(String nome, Tipo tipo, int linha, int coluna) {}

    private final Deque<Map<String, Simbolo>> escopos = new ArrayDeque<>();

    public void enterScope() { escopos.push(new LinkedHashMap<>()); }

    public void exitScope()  { escopos.pop(); }

    public void declare(String nome, Tipo tipo, int linha, int coluna) {
        escopos.peek().put(nome, new Simbolo(nome, tipo, linha, coluna));
    }

    /** Procura do escopo mais interno para o mais externo; null = ∅. */
    public Simbolo lookup(String nome) {
        for (Map<String, Simbolo> escopo : escopos) {     // ArrayDeque itera do topo
            Simbolo s = escopo.get(nome);
            if (s != null) return s;
        }
        return null;
    }

    /** Ambiente visível, do mais externo para o mais interno: { x, id }. */
    @Override
    public String toString() {
        StringJoiner j = new StringJoiner(", ", "{ ", " }");
        j.setEmptyValue("{ }");
        Iterator<Map<String, Simbolo>> it = escopos.descendingIterator();
        while (it.hasNext()) for (String n : it.next().keySet()) j.add(n);
        return j.toString();
    }
}
