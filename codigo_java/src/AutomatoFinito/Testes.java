package AutomatoFinito;

import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

/** Testes automáticos sem dependências:  java -cp out AutomatoFinito.Testes */
public class Testes {

	static PrintStream out = new PrintStream(System.out, true, StandardCharsets.UTF_8);
	static int ok = 0, falhas = 0;

	public static void main(String[] args) {
		// ---------- exemplo da aula ----------
		Estado q1 = new Estado();
		Estado q2 = new Estado(true);
		q1.transicoes.add(new Transicao('1', q1));
		q1.transicoes.add(new Transicao('0', q2));
		q2.transicoes.add(new Transicao('0', q2));
		q2.transicoes.add(new Transicao('1', q1));
		Automato a = new Automato(q1);
		verifica("Aula 00", a.procurarPalavra("00") + "", "true");
		verifica("Aula 01", a.procurarPalavra("01") + "", "false");

		// ---------- AFD léxico ----------
		tokens("let id = λx.x in id y", "LET ID(id) EQUALS LAMBDA ID(x) DOT ID(x) IN ID(id) ID(y) EOF");
		tokens("letter", "ID(letter) EOF");
		tokens("lambda1 x", "ID(lambda1) ID(x) EOF");
		tokens("lambda x. x", "LAMBDA ID(x) DOT ID(x) EOF");
		tokens("\\x.x", "LAMBDA ID(x) DOT ID(x) EOF");
		tokens("nome_1 _a", "ID(nome_1) ID(_a) EOF");
		palavra("let id = λx.x in id y", "li=λi.inii#");
		erroLexico("lambda @. x", "[1:8]");

		// ---------- AP de parênteses ----------
		ap(AutomatosLinguagem::criarAPParenteses, "((x))", true);
		ap(AutomatosLinguagem::criarAPParenteses, "(λx.(x))", true);
		ap(AutomatosLinguagem::criarAPParenteses, "(λx.x", false);
		ap(AutomatosLinguagem::criarAPParenteses, "x)", false);

		// ---------- AP LL(1) ----------
		ap(AutomatosLinguagem::criarAPSintaxe, "let id = λx.x in id y", true);
		ap(AutomatosLinguagem::criarAPSintaxe, "λf.λx.f (f x)", true);
		ap(AutomatosLinguagem::criarAPSintaxe, "(λx.x) y z", true);
		ap(AutomatosLinguagem::criarAPSintaxe, "λx x", false);
		ap(AutomatosLinguagem::criarAPSintaxe, "(λx.x", false);
		ap(AutomatosLinguagem::criarAPSintaxe, "let id = x y", false);
		ap(AutomatosLinguagem::criarAPSintaxe, "f λx.x", false);

		// ---------- Parser / AST ----------
		ast("f x y", "Apply(Apply(Var(f), Var(x)), Var(y))");
		ast("let id = λx.x in id y", "Let(id, Lambda(x, Var(x)), Apply(Var(id), Var(y)))");
		ast("λx.x y", "Lambda(x, Apply(Var(x), Var(y)))");
		erroSintactico("λx x", "esperado '.'");
		erroSintactico("(λx.x", "esperado ')'");
		erroSintactico("let id = x y", "esperado 'in'");

		// ---------- FV ----------
		fv("λx.x", Set.of());
		fv("λx.x y", Set.of("y"));
		fv("λf.λx.f (f x)", Set.of());
		fv("let id = λx.x in id y", Set.of("y"));
		fv("λx.λx.x", Set.of());

		// ---------- Semântica (casos do slide) ----------
		semantica("λx.x", List.of(), 0);
		semantica("λf.λx.f (f x)", List.of(), 0);
		semantica("let id = λx.x in id id", List.of(), 0);
		semantica("λx.λx.x", List.of(), 1);
		semantica("λx.y", List.of("1:4"), 0);
		semantica("let f = f in f", List.of("1:9"), 0);
		semantica("let id = λx.x in x", List.of("1:18"), 0);
		semantica("(λx.x) y z", List.of("1:8", "1:10"), 0);

		out.println();
		out.println("Resultado: " + ok + " passaram, " + falhas + " falharam");
		if (falhas > 0) System.exit(1);
	}

	static List<Token> lex(String s) { return new AnalisadorLexico().tokenizar(s); }

	static void tokens(String src, String esp)  { verifica("AFD " + src, Token.lista(lex(src)), esp); }
	static void palavra(String src, String esp) { verifica("Palavra " + src, Token.palavra(lex(src)), esp); }

	static void erroLexico(String src, String pos) {
		AnalisadorLexico l = new AnalisadorLexico();
		l.tokenizar(src);
		boolean r = !l.getErros().isEmpty() && l.getErros().get(0).toString().contains(pos);
		verifica("AFD erro " + src, r + "", "true");
	}

	static void ap(java.util.function.Supplier<AutomatoPilha> f, String src, boolean esp) {
		verifica("AP " + src, f.get().procurarPalavra(Token.palavra(lex(src))) + "", esp + "");
	}

	static void ast(String src, String esp) { verifica("AST " + src, Ast.linear(new Parser(lex(src)).parse()), esp); }

	static void erroSintactico(String src, String trecho) {
		Parser p = new Parser(lex(src));
		p.parse();
		boolean r = !p.erros().isEmpty() && p.erros().get(0).getMessage().contains(trecho);
		verifica("SIN " + src, r + "", "true");
	}

	static void fv(String src, Set<String> esp) {
		Set<String> r = AnalisadorSemantico.livres(new Parser(lex(src)).parse());
		verifica("FV " + src, Set.copyOf(r).equals(esp) + "", "true");
	}

	static void semantica(String src, List<String> posErros, int avisos) {
		AnalisadorSemantico s = new AnalisadorSemantico();
		s.analisar(new Parser(lex(src)).parse());
		String r = s.erros().stream().map(e -> e.linha() + ":" + e.coluna()).collect(Collectors.joining(","))
				+ " avisos=" + s.avisos().size();
		verifica("SEM " + src, r, String.join(",", posErros) + " avisos=" + avisos);
	}

	static void verifica(String nome, String obtido, String esperado) {
		if (obtido.equals(esperado)) { ok++; out.println("  ✔ " + nome); }
		else { falhas++; out.println("  ✘ " + nome + "\n      esperado: " + esperado + "\n      obtido:   " + obtido); }
	}
}
