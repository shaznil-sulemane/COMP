package AutomatoFinito;

import java.util.ArrayList;

public class Estado {
	ArrayList<Transicao> transicoes = new ArrayList<Transicao>();
	boolean terminal;
	int identificador;
	static int contadorInstancia = 0;

	String nome; // ACRESCENTADO: nome do estado (no AFD léxico = token que reconhece)

	public Estado() {
		this.identificador = contadorInstancia;
		contadorInstancia++;
	}
	public Estado(boolean terminal) {
		this ();
		this.terminal = terminal;
	}

	// ACRESCENTADO: estado com nome
	public Estado(String nome, boolean terminal) {
		this(terminal);
		this.nome = nome;
	}

	public String toString() {
		if (nome != null) return nome;
		return "q" + identificador;
	}
}
