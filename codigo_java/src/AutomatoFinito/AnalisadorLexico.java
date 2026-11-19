package AutomatoFinito;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Analisador léxico: usa o AFD construído com Estado/Transicao e aplica-o
 * repetidamente com maior correspondência (Automato.maiorPrefixo).
 * Depois de qID, o passo qRES classifica palavras reservadas.
 */
public class AnalisadorLexico {

	/** qRES — tabela de palavras reservadas. */
	static final Map<String, TokenType> RESERVADAS = Map.of(
		"lambda", TokenType.LAMBDA,
		"let",    TokenType.LET,
		"in",     TokenType.IN
	);

	private final Automato afd = AutomatosLinguagem.criarAFDLexico();
	private final List<CompilerError> erros = new ArrayList<>();
	private final List<String> caminhos = new ArrayList<>();

	public List<Token> tokenizar(String fonte) {
		List<Token> tokens = new ArrayList<>();
		int pos = 0, linha = 1, coluna = 1;

		while (pos < fonte.length()) {
			int fim = afd.maiorPrefixo(fonte, pos);

			if (fim == -1) {                            // nenhum prefixo aceite
				erros.add(new CompilerError(CompilerError.Fase.LEXICO, linha, coluna,
						"carácter '" + fonte.charAt(pos) + "' não reconhecido"));
				fim = pos + 1;                          // recuperação: salta 1 carácter
			} else {
				String lexema = fonte.substring(pos, fim);
				Estado aceite = afd.getUltimoAceite();
				TokenType tipo = aceite.token;
				if (tipo == TokenType.ID) {             // qRES: classificação
					tipo = RESERVADAS.getOrDefault(lexema, TokenType.ID);
				}
				if (tipo != null) {                     // null = espaço: ignorar
					Token t = new Token(tipo, lexema, linha, coluna);
					tokens.add(t);
					caminhos.add(String.format("%-30s ⇒ %s", afd.getCaminho(), t));
				}
			}
			for (int k = pos; k < fim; k++) {           // actualizar linha:coluna
				if (fonte.charAt(k) == '\n') { linha++; coluna = 1; } else { coluna++; }
			}
			pos = fim;
		}
		tokens.add(new Token(TokenType.EOF, "", linha, coluna));
		return tokens;
	}

	public List<CompilerError> getErros() { return erros; }
	public List<String> getCaminhos()     { return caminhos; }
}
