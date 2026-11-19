package AutomatoFinito;

public class Automato {
	Estado estadoInicial;

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
			// c = 0
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

	// ------------------------------------------------------------------
	// ACRESCENTADO para o analisador léxico.
	// Igual a procurarPalavra, mas em vez de ler a palavra toda:
	//   - começa na posição 'inicio' do texto;
	//   - pára quando não há transição (bloqueia);
	//   - devolve onde acaba o MAIOR pedaço aceite (maior correspondência).
	// ------------------------------------------------------------------
	Estado ultimoEstado;           // estado terminal onde o maior pedaço acabou
	boolean mostrarPassos = false; // true = imprime cada transição

	public int maiorPrefixo(String texto, int inicio) {
		Estado corrente = estadoInicial;
		int fim = -1;
		ultimoEstado = null;
		for (int i = inicio; i < texto.length(); i++) {
			char c = texto.charAt(i);
			boolean encontrado = false;
			for (int j = 0; j < corrente.transicoes.size(); j++) {
				if (c == corrente.transicoes.get(j).getSimbolo()) {
					if (mostrarPassos) {
						System.out.println("   " + corrente + " --" + c + "--> " + corrente.transicoes.get(j).proximoEstado);
					}
					corrente = corrente.transicoes.get(j).proximoEstado;
					encontrado = true;
					break;
				}
			}
			if (encontrado == false) {
				break; // bloqueou: o pedaço acaba aqui
			}
			if (corrente.terminal) {
				fim = i + 1;
				ultimoEstado = corrente;
			}
		}
		return fim;
	}
}
