package AutomatoFinito;

import java.util.Stack;

// Autómato de pilha: o mesmo ciclo do Automato da aula, mas cada
// transição também olha para o TOPO da pilha.
public class AutomatoPilha {
	Estado estadoInicial;
	char base;                     // fundo da pilha
	String inicioPilha;            // o que se empilha no arranque
	boolean mostrarPassos = false; // true = imprime a pilha em cada passo
	int posicaoErro = -1;          // onde bloqueou (-1 = não bloqueou)

	AutomatoPilha(Estado estadoIni, char base, String inicioPilha) {
		this.estadoInicial = estadoIni;
		this.base = base;
		this.inicioPilha = inicioPilha;
	}

	public boolean procurarPalavra(String palavra) {
		Stack<Character> pilha = new Stack<Character>();
		pilha.push(base);
		empilhar(pilha, inicioPilha);

		Estado corrente = estadoInicial;
		posicaoErro = -1;
		int i = 0;
		while (i < palavra.length()) {
			char c = palavra.charAt(i);

			// procurar a transição para (estado, símbolo, topo)
			TransicaoPilha t = null;
			if (!pilha.isEmpty()) {
				for (int j = 0; j < corrente.transicoes.size(); j++) {
					TransicaoPilha tp = (TransicaoPilha) corrente.transicoes.get(j);
					if (tp.getSimbolo() == c && tp.topo == pilha.peek()) {
						t = tp;
						break;
					}
				}
			}
			if (t == null) {
				if (mostrarPassos) mostrar(pilha, palavra.substring(i), "BLOQUEIA");
				posicaoErro = i;
				return false;
			}
			if (mostrarPassos) mostrar(pilha, palavra.substring(i), descrever(t));

			pilha.pop();                 // tira o topo
			empilhar(pilha, t.empilhar); // põe o que a transição manda
			if (t.consome) {
				i++;                     // avança na palavra
			}
			corrente = t.proximoEstado;
		}
		return corrente.terminal;
	}

	// empilha de trás para a frente: o 1.º carácter fica no topo
	static void empilhar(Stack<Character> pilha, String s) {
		for (int k = s.length() - 1; k >= 0; k--) {
			pilha.push(s.charAt(k));
		}
	}

	// texto curto para o que a transição faz
	static String descrever(TransicaoPilha t) {
		if (t.consome == false) {                          // troca o topo (não lê)
			if (t.empilhar.isEmpty()) return t.topo + " -> ε";
			return t.topo + " -> " + t.empilhar;
		}
		if (t.simbolo == '#') return "aceita";
		if (t.empilhar.length() == 2) return "push " + t.empilhar.charAt(0);
		if (t.empilhar.isEmpty() && t.simbolo == t.topo) return "lê " + t.simbolo;
		if (t.empilhar.isEmpty()) return "pop " + t.topo;
		return "lê " + t.simbolo + " (pilha igual)";
	}

	// imprime: pilha (topo à esquerda) | resto da palavra | acção
	static void mostrar(Stack<Character> pilha, String resto, String accao) {
		String p = "";
		for (int k = pilha.size() - 1; k >= 0; k--) {
			p = p + pilha.get(k) + " ";
		}
		System.out.println(String.format("   %-12s %-10s %s", p, resto, accao));
	}
}
