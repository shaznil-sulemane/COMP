package AutomatoFinito;

// Transição de autómato de pilha = Transicao da aula + 3 campos.
//
//   lê 'simbolo', com 'topo' no topo da pilha
//   -> tira o topo, põe 'empilhar' no seu lugar, vai para 'proximoEstado'
//
public class TransicaoPilha extends Transicao {
	char topo;        // o que tem de estar no topo da pilha
	String empilhar;  // o que entra no lugar do topo ("" = só desempilhar)
	boolean consome;  // true = avança para o próximo símbolo; false = só espreita

	public TransicaoPilha(char simbolo, char topo, String empilhar, Estado proxEstado, boolean consome) {
		super(simbolo, proxEstado);
		this.topo = topo;
		this.empilhar = empilhar;
		this.consome = consome;
	}
}
