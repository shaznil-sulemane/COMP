package AutomatoFinito;

import java.util.List;

/** Unidade lexical: tipo, lexema e posição (linha:coluna, a contar de 1). */
public record Token(TokenType tipo, String lexema, int linha, int coluna) {

	public String pos() { return linha + ":" + coluna; }

	@Override
	public String toString() {
		return switch (tipo) {
			case ID -> "ID(" + lexema + ")";
			default -> tipo.name();
		};
	}

	/** Converte a lista de tokens na palavra lida pelos autómatos de pilha. */
	public static String palavra(List<Token> tokens) {
		StringBuilder sb = new StringBuilder();
		for (Token t : tokens) sb.append(t.tipo().simbolo);
		return sb.toString();
	}

	public static String lista(List<Token> tokens) {
		StringBuilder sb = new StringBuilder();
		for (Token t : tokens) sb.append(t).append(' ');
		return sb.toString().trim();
	}
}
