package AutomatoFinito;

import java.io.PrintStream;
import java.util.ArrayList;

public class Executavel {
	public static void main(String[] args) throws Exception {
		System.setOut(new PrintStream(System.out, true, "UTF-8")); // para ver o λ

		// ==============================================================
		// 0. EXEMPLO DA AULA (sem alterações)
		// ==============================================================
		titulo("0. Exemplo da aula");
		Estado q1 = new Estado();
		Estado q2 = new Estado(true);
		q1.transicoes.add(new Transicao('1', q1));
		q1.transicoes.add(new Transicao('0', q2));
		q2.transicoes.add(new Transicao('0', q2));
		q2.transicoes.add(new Transicao('1', q1));

		Automato automato = new Automato(q1);
		System.out.println(automato.procurarPalavra("00"));
		System.out.println(automato.procurarPalavra("01"));

		// uma expressão dada na linha de comandos: só corre o compilador
		if (args.length > 0) {
			compilar(String.join(" ", args));
			return;
		}

		// ==============================================================
		// 1. AFD LÉXICO, PASSO A PASSO
		// ==============================================================
		titulo("1. AFD léxico: 'let' e 'letter'");
		Automato afd = Automatos.criarAFDLexico();
		afd.mostrarPassos = true;
		System.out.println(" let:");
		afd.maiorPrefixo("let", 0);
		System.out.println("   lexema 'let' -> " + AnalisadorLexico.palavraReservada("let"));
		System.out.println(" letter:");
		afd.maiorPrefixo("letter", 0);
		System.out.println("   lexema 'letter' -> " + AnalisadorLexico.palavraReservada("letter"));

		// ==============================================================
		// 2. AP DE PARÊNTESES, PASSO A PASSO
		// ==============================================================
		titulo("2. AP de parênteses");
		mostrarAP(Automatos.criarAPParenteses(), "((x))");
		mostrarAP(Automatos.criarAPParenteses(), "(λx.x");

		// ==============================================================
		// 3. AP DA SINTAXE, PASSO A PASSO
		// ==============================================================
		titulo("3. AP da sintaxe");
		mostrarAP(Automatos.criarAPSintaxe(), "λx.x y");
		mostrarAP(Automatos.criarAPSintaxe(), "λx x");

		// ==============================================================
		// 4. COMPILADOR COMPLETO (AFD -> AP -> pilha de nomes)
		// ==============================================================
		titulo("4. Compilador completo");
		compilar("let id = λx.x in id y");
		compilar("(λx.x) y z");
		compilar("λf.λx.f (f x)");
	}

	// corre um AP sobre a palavra de tokens da expressão e mostra cada passo
	static void mostrarAP(AutomatoPilha ap, String expressao) {
		ArrayList<Token> tokens = new AnalisadorLexico().tokenizar(expressao);
		String palavra = AnalisadorLexico.palavra(tokens);
		System.out.println(" Expressão: " + expressao + "    palavra: " + palavra);
		System.out.println(String.format("   %-12s %-10s %s", "PILHA", "FALTA LER", "ACÇÃO"));
		ap.mostrarPassos = true;
		boolean ok = ap.procurarPalavra(palavra);
		System.out.println("   => " + (ok ? "ACEITA" : "REJEITA"));
		System.out.println();
	}

	// as três fases, uma a seguir à outra
	static boolean compilar(String expressao) {
		System.out.println(" Expressão: " + expressao);

		// 1) AFD: texto -> tokens
		AnalisadorLexico lexico = new AnalisadorLexico();
		ArrayList<Token> tokens = lexico.tokenizar(expressao);
		System.out.println("   Tokens:  " + tokens);
		if (!lexico.erros.isEmpty()) {
			System.out.println("   " + lexico.erros);
			return false;
		}

		// 2) AP: a sintaxe está certa?
		AutomatoPilha ap = Automatos.criarAPSintaxe();
		if (!ap.procurarPalavra(AnalisadorLexico.palavra(tokens))) {
			Token t = tokens.get(ap.posicaoErro);
			System.out.println("   Erro sintáctico [" + t.linha + ":" + t.coluna + "]: '" + t.lexema + "' inesperado");
			return false;
		}
		System.out.println("   Sintaxe: aceite pelo AP");

		// 3) pilha de nomes: todas as variáveis estão ligadas?
		AnalisadorSemantico semantico = new AnalisadorSemantico();
		semantico.mostrarPassos = true;
		boolean ok = semantico.verificar(tokens);
		for (int k = 0; k < semantico.avisos.size(); k++) System.out.println("   " + semantico.avisos.get(k));
		for (int k = 0; k < semantico.erros.size(); k++)  System.out.println("   " + semantico.erros.get(k));
		System.out.println("   => " + (ok ? "ACEITE" : "REJEITADA"));
		System.out.println();
		return ok;
	}

	static void titulo(String t) {
		System.out.println();
		System.out.println("===== " + t + " =====");
	}
}
