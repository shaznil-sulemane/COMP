package AutomatoFinito;

import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Set;

/**
 * Programa principal.
 *  0. Exemplo original da aula (AFD sobre {0,1}).
 *  1. AFD léxico da mini-linguagem.
 *  2. AP de equilíbrio de parênteses.
 *  3. AP LL(1) da sintaxe completa.
 *  4. Parser → AST.
 *  5. Análise semântica.
 *
 *   java -cp out AutomatoFinito.Executavel
 *   java -cp out AutomatoFinito.Executavel "\x.x y"
 */
public class Executavel {

	static PrintStream out = new PrintStream(System.out, true, StandardCharsets.UTF_8);

	public static void main(String[] args) {
		if (args.length > 0) {
			pipeline(String.join(" ", args), true);
			return;
		}
		exemploDaAula();
		demoAFD();
		demoParenteses();
		demoSintaxe();
		demoParser();
		demoSemantica();
	}

	// ---------------------------------------------------------- 0. aula
	static void exemploDaAula() {
		titulo("0. EXEMPLO DA AULA — AFD sobre {0, 1} (palavras terminadas em 0)");
		Estado q1 = new Estado();
		Estado q2 = new Estado(true);
		q1.transicoes.add(new Transicao('1', q1));
		q1.transicoes.add(new Transicao('0', q2));
		q2.transicoes.add(new Transicao('0', q2));
		q2.transicoes.add(new Transicao('1', q1));

		Automato automato = new Automato(q1);
		for (String p : new String[]{ "00", "10", "01", "1110" }) {
			out.printf("  procurarPalavra(\"%s\") = %s%n", p, automato.procurarPalavra(p));
		}
	}

	// ---------------------------------------------------------- 1. AFD
	static void demoAFD() {
		titulo("1. AFD LÉXICO (Estado + Transicao, maior correspondência + qRES)");
		String src = "let id = λx.x in id y";
		AnalisadorLexico lx = new AnalisadorLexico();
		List<Token> ts = lx.tokenizar(src);
		out.println("Entrada: " + src);
		lx.getCaminhos().forEach(c -> out.println("  " + c));
		out.println("Tokens:  " + Token.lista(ts));
		out.println("Palavra de tokens (entrada dos AP): " + Token.palavra(ts));
		out.println();
		for (String s : new String[]{ "letter", "lambda1 x", "\\x.x", "lambda @. x" }) {
			AnalisadorLexico l = new AnalisadorLexico();
			out.printf("  %-12s → %s%n", s, Token.lista(l.tokenizar(s)));
			l.getErros().forEach(e -> out.println("                 " + e));
		}
	}

	// ---------------------------------------------------------- 2. AP ()
	static void demoParenteses() {
		titulo("2. AP DE PARÊNTESES (TransicaoPilha + AutomatoPilha)");
		for (String s : new String[]{ "((x))", "(λx.x", "x)" }) {
			String palavra = Token.palavra(new AnalisadorLexico().tokenizar(s));
			AutomatoPilha ap = AutomatosLinguagem.criarAPParenteses();
			boolean ok = ap.procurarPalavra(palavra);
			out.println("Entrada: " + s + "   palavra: " + palavra);
			imprimirPassos(ap);
			out.println("  → " + (ok ? "ACEITA" : "REJEITA: " + ap.getMotivo()));
			out.println();
		}
	}

	// ---------------------------------------------------------- 3. AP LL(1)
	static void demoSintaxe() {
		titulo("3. AP LL(1) DA SINTAXE  (E=Expr L=Let A=Abs P=App C=Cauda T=Atom)");
		for (String s : new String[]{ "λx.x y", "λx x" }) {
			String palavra = Token.palavra(new AnalisadorLexico().tokenizar(s));
			AutomatoPilha ap = AutomatosLinguagem.criarAPSintaxe();
			boolean ok = ap.procurarPalavra(palavra);
			out.println("Entrada: " + s + "   palavra: " + palavra);
			imprimirPassos(ap);
			out.println("  → " + (ok ? "ACEITA" : "REJEITA: " + ap.getMotivo()));
			out.println();
		}
	}

	static void imprimirPassos(AutomatoPilha ap) {
		out.printf("  %-4s %-16s %-14s %s%n", "#", "PILHA", "ENTRADA", "ACÇÃO");
		int k = 0;
		for (AutomatoPilha.Passo p : ap.getPassos()) {
			out.printf("  %-4d %-16s %-14s %s%n", k++, p.pilha(), p.entrada(), p.accao());
		}
	}

	// ---------------------------------------------------------- 4. Parser
	static void demoParser() {
		titulo("4. PARSER DESCENDENTE RECURSIVO → AST");
		String s = "let id = λx.x in id y";
		Ast.Expr ast = new Parser(new AnalisadorLexico().tokenizar(s)).parse();
		out.println("Entrada: " + s);
		out.println("  " + Ast.linear(ast));
		out.print(Ast.arvore(ast).indent(2));
		out.println();
		out.println("Erros sintácticos (modo de pânico):");
		for (String e : new String[]{ "λx x", "(λx.x", "let id = x y" }) {
			Parser p = new Parser(new AnalisadorLexico().tokenizar(e));
			p.parse();
			out.printf("  %-14s %s%n", e, p.erros().get(0));
		}
	}

	// ---------------------------------------------------------- 5. Semântica
	static void demoSemantica() {
		titulo("5. ANÁLISE SEMÂNTICA — ESCOPO E LIGAÇÕES");
		String s = "let id = λx.x in id y";
		AnalisadorSemantico sem = new AnalisadorSemantico();
		sem.analisar(new Parser(new AnalisadorLexico().tokenizar(s)).parse());
		out.println("Percurso de: " + s);
		out.printf("  %-12s %-20s %s%n", "NÓ", "ACÇÃO", "AMBIENTE");
		sem.passos().forEach(p -> out.printf("  %-12s %-20s %s%n", p.no(), p.accao(), p.ambiente()));
		sem.erros().forEach(e -> out.println("  " + e));
		out.println();
		String[][] casos = {
			{ "V1", "λx.x" }, { "V2", "λf.λx.f (f x)" }, { "V3", "let id = λx.x in id id" },
			{ "V4", "λx.λx.x" }, { "I1", "λx.y" }, { "I2", "let f = f in f" },
			{ "I3", "let id = λx.x in x" }, { "I4", "(λx.x) y z" },
		};
		for (String[] c : casos) {
			out.print(c[0] + "  ");
			pipeline(c[1], false);
		}
	}

	// ---------------------------------------------------------- pipeline
	static boolean pipeline(String fonte, boolean detalhe) {
		out.println("Entrada: " + fonte);
		AnalisadorLexico lx = new AnalisadorLexico();
		List<Token> tokens = lx.tokenizar(fonte);
		if (detalhe) out.println("  Tokens:    " + Token.lista(tokens) + "   palavra: " + Token.palavra(tokens));
		if (!lx.getErros().isEmpty()) { lx.getErros().forEach(e -> out.println("  " + e)); return false; }

		if (detalhe) {
			out.println("  AP ():     " + (AutomatosLinguagem.criarAPParenteses().procurarPalavra(Token.palavra(tokens)) ? "aceita" : "rejeita"));
			out.println("  AP LL(1):  " + (AutomatosLinguagem.criarAPSintaxe().procurarPalavra(Token.palavra(tokens)) ? "aceita" : "rejeita"));
		}
		Parser parser = new Parser(tokens);
		Ast.Expr ast = parser.parse();
		if (!parser.erros().isEmpty()) { parser.erros().forEach(e -> out.println("  " + e)); return false; }
		if (detalhe) out.println("  AST:       " + Ast.linear(ast));

		AnalisadorSemantico sem = new AnalisadorSemantico();
		boolean ok = sem.analisar(ast);
		if (detalhe) out.println("  FV:        " + conj(AnalisadorSemantico.livres(ast)));
		sem.avisos().forEach(a -> out.println("  " + a));
		sem.erros().forEach(e -> out.println("  " + e));
		out.println("  Resultado: " + (ok ? "ACEITE (expressão fechada)" : "REJEITADA (" + sem.erros().size() + " erro(s))"));
		return ok;
	}

	static String conj(Set<String> s) {
		return s.isEmpty() ? "∅" : "{ " + String.join(", ", s) + " }";
	}

	static void titulo(String t) {
		out.println();
		out.println("=".repeat(72));
		out.println(t);
		out.println("=".repeat(72));
	}
}
