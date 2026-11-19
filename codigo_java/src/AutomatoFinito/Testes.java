package AutomatoFinito;

import java.io.PrintStream;
import java.util.ArrayList;

// Testes simples: cada linha compara o resultado obtido com o esperado.
public class Testes {
	static int passou = 0, falhou = 0;

	public static void main(String[] args) throws Exception {
		System.setOut(new PrintStream(System.out, true, "UTF-8"));

		System.out.println("--- Exemplo da aula ---");
		Estado q1 = new Estado();
		Estado q2 = new Estado(true);
		q1.transicoes.add(new Transicao('1', q1));
		q1.transicoes.add(new Transicao('0', q2));
		q2.transicoes.add(new Transicao('0', q2));
		q2.transicoes.add(new Transicao('1', q1));
		Automato automato = new Automato(q1);
		verificar("00 aceite", automato.procurarPalavra("00"), true);
		verificar("01 rejeitada", automato.procurarPalavra("01"), false);

		System.out.println("--- AFD léxico ---");
		tokens("let id = λx.x in id y", "[LET, ID(id), EQUALS, LAMBDA, ID(x), DOT, ID(x), IN, ID(id), ID(y), EOF]");
		tokens("letter", "[ID(letter), EOF]");
		tokens("lambda1 x", "[ID(lambda1), ID(x), EOF]");
		tokens("\\x.x", "[LAMBDA, ID(x), DOT, ID(x), EOF]");
		palavra("let id = λx.x in id y", "li=λi.inii#");
		erroLexico("lambda @. x");

		System.out.println("--- AP de parênteses ---");
		parenteses("((x))", true);
		parenteses("(λx.(x))", true);
		parenteses("(λx.x", false);
		parenteses("x)", false);

		System.out.println("--- AP da sintaxe ---");
		sintaxe("λx.x", true);
		sintaxe("λx.x y", true);
		sintaxe("let id = λx.x in id y", true);
		sintaxe("λf.λx.f (f x)", true);
		sintaxe("(λx.x) y z", true);
		sintaxe("λx x", false);
		sintaxe("(λx.x", false);
		sintaxe("let id = x y", false);
		sintaxe("f λx.x", false);

		System.out.println("--- Pilha de nomes (semântica) ---");
		semantica("λx.x", "");
		semantica("λf.λx.f (f x)", "");
		semantica("let id = λx.x in id id", "");
		semantica("λx.λx.x", "");
		semantica("λx.y", "1:4");
		semantica("let f = f in f", "1:9");
		semantica("let id = λx.x in x", "1:18");
		semantica("(λx.x) y z", "1:8 1:10");
		semantica("let id = λx.x in id y", "1:21");
		AnalisadorSemantico s = new AnalisadorSemantico();
		s.verificar(new AnalisadorLexico().tokenizar("λx.λx.x"));
		verificar("λx.λx.x dá aviso de sombreamento", s.avisos.size() == 1, true);

		System.out.println();
		System.out.println("Resultado: " + passou + " passaram, " + falhou + " falharam");
	}

	static void tokens(String texto, String esperado) {
		String obtido = new AnalisadorLexico().tokenizar(texto).toString();
		verificar("tokens de " + texto, obtido.equals(esperado), true);
	}

	static void palavra(String texto, String esperado) {
		String obtido = AnalisadorLexico.palavra(new AnalisadorLexico().tokenizar(texto));
		verificar("palavra de " + texto + " = " + obtido, obtido.equals(esperado), true);
	}

	static void erroLexico(String texto) {
		AnalisadorLexico lexico = new AnalisadorLexico();
		lexico.tokenizar(texto);
		verificar("erro léxico em " + texto, lexico.erros.size() == 1, true);
	}

	static void parenteses(String texto, boolean esperado) {
		String p = AnalisadorLexico.palavra(new AnalisadorLexico().tokenizar(texto));
		verificar("AP () " + texto, Automatos.criarAPParenteses().procurarPalavra(p), esperado);
	}

	static void sintaxe(String texto, boolean esperado) {
		String p = AnalisadorLexico.palavra(new AnalisadorLexico().tokenizar(texto));
		verificar("AP sintaxe " + texto, Automatos.criarAPSintaxe().procurarPalavra(p), esperado);
	}

	// posicoes: posições dos erros esperados, separadas por espaço ("" = sem erros)
	static void semantica(String texto, String posicoes) {
		ArrayList<Token> tokens = new AnalisadorLexico().tokenizar(texto);
		AnalisadorSemantico s = new AnalisadorSemantico();
		s.verificar(tokens);
		String obtido = "";
		for (int k = 0; k < s.erros.size(); k++) {
			String e = s.erros.get(k);
			obtido = obtido + (k > 0 ? " " : "") + e.substring(e.indexOf('[') + 1, e.indexOf(']'));
		}
		verificar("semântica " + texto + " -> erros em [" + obtido + "]", obtido.equals(posicoes), true);
	}

	static void verificar(String nome, boolean obtido, boolean esperado) {
		if (obtido == esperado) {
			passou++;
			System.out.println("  OK    " + nome);
		} else {
			falhou++;
			System.out.println("  FALHA " + nome);
		}
	}
}
