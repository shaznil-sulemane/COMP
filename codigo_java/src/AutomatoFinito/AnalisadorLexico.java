package AutomatoFinito;

import java.util.ArrayList;

// Corta o texto em tokens usando o AFD léxico.
public class AnalisadorLexico {
	Automato afd = Automatos.criarAFDLexico();
	ArrayList<String> erros = new ArrayList<String>();

	public ArrayList<Token> tokenizar(String texto) {
		ArrayList<Token> tokens = new ArrayList<Token>();
		int i = 0;
		int linha = 1, coluna = 1;

		while (i < texto.length()) {
			int fim = afd.maiorPrefixo(texto, i);   // maior pedaço que o AFD aceita

			if (fim == -1) {                         // nenhum: carácter inválido
				erros.add("Erro léxico [" + linha + ":" + coluna + "]: carácter '" + texto.charAt(i) + "' não reconhecido");
				fim = i + 1;                         // salta-o e continua
			} else {
				String lexema = texto.substring(i, fim);
				String tipo = afd.ultimoEstado.nome; // o estado final diz o tipo
				if (tipo.equals("ID")) {
					tipo = palavraReservada(lexema);  // lambda, let, in
				}
				if (!tipo.equals("ESPACO")) {         // espaços não viram token
					tokens.add(new Token(tipo, lexema, linha, coluna));
				}
			}

			// avançar a posição (linha:coluna)
			for (int k = i; k < fim; k++) {
				if (texto.charAt(k) == '\n') { linha++; coluna = 1; }
				else coluna++;
			}
			i = fim;
		}
		tokens.add(new Token("EOF", "", linha, coluna));
		return tokens;
	}

	// depois de ler um nome inteiro, ver se é palavra reservada
	static String palavraReservada(String lexema) {
		if (lexema.equals("lambda")) return "LAMBDA";
		if (lexema.equals("let"))    return "LET";
		if (lexema.equals("in"))     return "IN";
		return "ID";
	}

	// os tokens em forma de palavra para os autómatos de pilha
	static String palavra(ArrayList<Token> tokens) {
		String p = "";
		for (int k = 0; k < tokens.size(); k++) {
			p = p + tokens.get(k).simbolo;
		}
		return p;
	}
}
