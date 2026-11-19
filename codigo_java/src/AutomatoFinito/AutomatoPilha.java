package AutomatoFinito;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

/**
 * Autómato de pilha — mesma ideia do Automato da aula, com memória extra.
 * procurarPalavra() segue o mesmo esquema: para cada símbolo procura a
 * transição aplicável no estado corrente; se não existir, rejeita.
 * Diferença: a transição também tem de corresponder ao TOPO da pilha.
 */
public class AutomatoPilha {
	Estado estadoInicial;
	char base;                 // símbolo de base da pilha (B ou $)
	String pilhaInicial;       // símbolos empilhados no arranque (ex.: "E")

	/** Uma linha do traço: pilha (topo à esquerda), entrada restante, acção. */
	public record Passo(String pilha, String entrada, String accao) {}

	private final List<Passo> passos = new ArrayList<>();
	private String motivo = "";

	AutomatoPilha(Estado estadoIni, char base, String pilhaInicial) {
		this.estadoInicial = estadoIni;
		this.base = base;
		this.pilhaInicial = pilhaInicial;
	}

	public boolean procurarPalavra(String palavra) {
		Deque<Character> pilha = new ArrayDeque<>();
		pilha.push(base);
		empilhar(pilha, pilhaInicial);
		passos.clear();
		motivo = "";
		passos.add(new Passo(mostrar(pilha), palavra, "inicializar"));

		Estado corrente = estadoInicial;
		int i = 0;
		while (i < palavra.length()) {
			char c = palavra.charAt(i);
			if (pilha.isEmpty()) return rejeitar("pilha vazia antes do fim");
			char topo = pilha.peek();

			TransicaoPilha t = null;
			for (int j = 0; j < corrente.transicoes.size(); j++) {
				TransicaoPilha tp = (TransicaoPilha) corrente.transicoes.get(j);
				if (tp.getSimbolo() == c && tp.topo == topo) {
					t = tp;
					break;
				}
			}
			if (t == null) {
				passos.add(new Passo(mostrar(pilha), palavra.substring(i), "rejeitar"));
				return rejeitar("sem transição para (" + corrente + ", " + c + ", topo " + topo + ")");
			}
			String antes = mostrar(pilha);
			pilha.pop();
			empilhar(pilha, t.empilhar);
			passos.add(new Passo(antes, palavra.substring(i), t.descricao()));
			if (t.consome) i++;
			corrente = t.proximoEstado;
		}
		if (!corrente.terminal) return rejeitar("entrada terminou fora de estado de aceitação");
		return true;
	}

	private boolean rejeitar(String m) {
		motivo = m;
		return false;
	}

	/** Empilha de trás para a frente: o 1.º carácter da cadeia fica no topo. */
	private static void empilhar(Deque<Character> pilha, String s) {
		for (int k = s.length() - 1; k >= 0; k--) pilha.push(s.charAt(k));
	}

	private static String mostrar(Deque<Character> pilha) {
		StringBuilder sb = new StringBuilder();
		for (char c : pilha) sb.append(c).append(' ');
		return sb.toString().trim();
	}

	public List<Passo> getPassos() { return passos; }
	public String getMotivo()      { return motivo; }
}
