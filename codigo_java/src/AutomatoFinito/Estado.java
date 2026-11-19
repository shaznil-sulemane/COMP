package AutomatoFinito;

import java.util.ArrayList;

/**
 * Estado de um autómato (classe base da aula, mantida).
 * Acrescentos para a mini-linguagem: nome legível e o token que o estado
 * emite quando é de aceitação (usado pelo AFD léxico).
 */
public class Estado {
	ArrayList<Transicao> transicoes = new ArrayList<Transicao>();
	boolean terminal;
	int identificador;
	static int contadorInstancia = 0;

	String nome;          // acrescento: ex. "q0", "qID"
	TokenType token;      // acrescento: token emitido (null = ignorar, ex. espaços)

	public Estado() {
		this.identificador = contadorInstancia;
		contadorInstancia++;
	}
	public Estado(boolean terminal) {
		this ();
		this.terminal = terminal;
	}

	/** Acrescento: estado com nome e token emitido. */
	public Estado(String nome, boolean terminal, TokenType token) {
		this(terminal);
		this.nome = nome;
		this.token = token;
	}

	/** Acrescento: atalho para várias transições com o mesmo destino. */
	public void adicionarTransicoes(String simbolos, Estado destino) {
		for (char c : simbolos.toCharArray()) {
			transicoes.add(new Transicao(c, destino));
		}
	}

	@Override
	public String toString() {
		return nome != null ? nome : "q" + identificador;
	}
}
