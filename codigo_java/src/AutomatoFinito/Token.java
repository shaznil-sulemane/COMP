package AutomatoFinito;

// Um token: tipo (LET, ID, ...), texto original e posição.
// Cada tipo tem um SÍMBOLO de uma letra, para os autómatos de pilha:
//   let id = λx.x in id y   ->   li=λi.inii#
public class Token {
	String tipo;
	String lexema;
	int linha;
	int coluna;
	char simbolo;

	public Token(String tipo, String lexema, int linha, int coluna) {
		this.tipo = tipo;
		this.lexema = lexema;
		this.linha = linha;
		this.coluna = coluna;
		this.simbolo = simboloDe(tipo);
	}

	static char simboloDe(String tipo) {
		if (tipo.equals("LET"))    return 'l';
		if (tipo.equals("IN"))     return 'n';
		if (tipo.equals("ID"))     return 'i';
		if (tipo.equals("LAMBDA")) return 'λ';
		if (tipo.equals("DOT"))    return '.';
		if (tipo.equals("LPAREN")) return '(';
		if (tipo.equals("RPAREN")) return ')';
		if (tipo.equals("EQUALS")) return '=';
		return '#'; // EOF
	}

	public String toString() {
		if (tipo.equals("ID")) return "ID(" + lexema + ")";
		return tipo;
	}
}
