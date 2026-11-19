package AutomatoFinito;

/**
 * Transição de autómato de pilha — estende a Transicao da aula.
 *
 *   δ(estado, simbolo, topo) = (proximoEstado, empilhar)
 *
 * Ao disparar: desempilha 'topo' e empilha a cadeia 'empilhar'
 * (o 1.º carácter fica no topo). Se 'consome' for falso, o símbolo de
 * entrada é apenas consultado (antevisão), não consumido.
 */
public class TransicaoPilha extends Transicao {
	char topo;
	String empilhar;
	boolean consome;

	public TransicaoPilha(char simbolo, char topo, String empilhar, Estado proxEstado, boolean consome) {
		super(simbolo, proxEstado);
		this.topo = topo;
		this.empilhar = empilhar;
		this.consome = consome;
	}

	/** Descrição curta para o traço de execução. */
	public String descricao() {
		String alfa = empilhar.isEmpty() ? "ε" : empilhar;
		if (simbolo == '#' && consome) return "aceitar (EOF)";              // fim com a base no topo
		if (!consome) return topo + " → " + alfa;                         // expansão
		if (empilhar.isEmpty() && simbolo == topo) return "match " + simbolo;
		if (empilhar.isEmpty()) return "pop " + topo;
		if (empilhar.length() > 1) return "push " + empilhar.charAt(0);
		return "sem alteração";
	}
}
