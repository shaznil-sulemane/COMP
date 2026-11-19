package AutomatoFinito;

/**
 * Transição de um autómato finito (classe base da aula, mantida).
 * δ(estado, simbolo) = proximoEstado
 */
public class Transicao {
	char simbolo;
	Estado proximoEstado;

	public Transicao(char simbolo, Estado proxEstado){
		this.simbolo = simbolo;
		this.proximoEstado = proxEstado;
	}

	public char getSimbolo() {
		return simbolo;
	}

	public Estado getProximoEstado() {
		return proximoEstado;
	}
}
