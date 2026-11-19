package AutomatoFinito;

/**
 * Autómato finito determinístico (classe base da aula, mantida).
 *
 * procurarPalavra(): aceita/rejeita uma palavra inteira (versão original).
 * maiorPrefixo():    acrescento para o analisador léxico — percorre o mesmo
 *                    grafo de estados, mas pára no bloqueio e devolve o maior
 *                    prefixo aceite (política de maior correspondência).
 */
public class Automato {
	Estado estadoInicial;

	// acrescentos preenchidos por maiorPrefixo()
	Estado ultimoAceite;
	StringBuilder caminho = new StringBuilder();

	Automato(Estado estadoIni) {
		this.estadoInicial = estadoIni;
	}

	public Estado getEstadoInicial() {
		return estadoInicial;
	}

	public boolean procurarPalavra(String palavra) {
		Estado corrente = estadoInicial;
		int tamanho = palavra.length();
		char c;
		for (int i = 0; i < tamanho; i++) {
			c = palavra.charAt(i);
			boolean encontrado = false;
			for (int j = 0; j < corrente.transicoes.size(); j++) {
				if (c == corrente.transicoes.get(j).getSimbolo()) {
					corrente = corrente.transicoes.get(j).proximoEstado;
					encontrado = true;
					break;
				}
			}
			if(encontrado == false) {
				return false;
			}
		}
		return corrente.terminal;
	}

	/**
	 * Acrescento — maximal munch. Lê a partir de 'inicio' enquanto houver
	 * transição; memoriza o último estado terminal visitado.
	 * @return posição a seguir ao maior lexema aceite, ou -1 se nenhum.
	 */
	public int maiorPrefixo(String texto, int inicio) {
		Estado corrente = estadoInicial;
		ultimoAceite = null;
		caminho.setLength(0);
		caminho.append(corrente);
		int fim = -1;
		for (int i = inicio; i < texto.length(); i++) {
			char c = texto.charAt(i);
			Estado proximo = null;
			for (int j = 0; j < corrente.transicoes.size(); j++) {
				if (c == corrente.transicoes.get(j).getSimbolo()) {
					proximo = corrente.transicoes.get(j).proximoEstado;
					break;
				}
			}
			if (proximo == null) {
				break;                         // bloqueio: não há transição
			}
			corrente = proximo;
			caminho.append(" -").append(Character.isWhitespace(c) ? '␣' : c).append("→ ").append(corrente);
			if (corrente.terminal) {           // memoriza o último aceite
				ultimoAceite = corrente;
				fim = i + 1;
			}
		}
		return fim;
	}

	public Estado getUltimoAceite() { return ultimoAceite; }
	public String getCaminho()      { return caminho.toString(); }
}
