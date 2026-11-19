package AutomatoFinito;

/**
 * Categorias lexicais. Cada token tem um SÍMBOLO de um carácter, usado para
 * formar a "palavra de tokens" lida pelos autómatos de pilha:
 *   let id = λx.x in id y   →   li=λi.inii#
 */
public enum TokenType {
	LAMBDA('λ'), LET('l'), IN('n'), ID('i'), DOT('.'),
	LPAREN('('), RPAREN(')'), EQUALS('='), EOF('#');

	public final char simbolo;

	TokenType(char simbolo) { this.simbolo = simbolo; }
}
