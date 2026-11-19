package AutomatoFinito;

// Os autómatos da mini-linguagem, construídos como no Executavel da aula:
//   1) criar estados   2) ligar transições   3) criar o autómato
public class Automatos {

	static String LETRAS  = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_";
	static String DIGITOS = "0123456789";
	static String ESPACOS = " \t\r\n";

	// liga 'de' a 'para' com uma transição para cada carácter de 'simbolos'
	static void ligar(Estado de, String simbolos, Estado para) {
		for (int k = 0; k < simbolos.length(); k++) {
			de.transicoes.add(new Transicao(simbolos.charAt(k), para));
		}
	}

	// =================================================================
	// 1. AFD LÉXICO — reconhece um token de cada vez
	// =================================================================
	public static Automato criarAFDLexico() {
		Estado q0      = new Estado("q0", false);
		Estado qID     = new Estado("ID", true);      // nomes, e lambda/let/in
		Estado qLambda = new Estado("LAMBDA", true);  // λ ou \
		Estado qPonto  = new Estado("DOT", true);
		Estado qAbre   = new Estado("LPAREN", true);
		Estado qFecha  = new Estado("RPAREN", true);
		Estado qIgual  = new Estado("EQUALS", true);
		Estado qEspaco = new Estado("ESPACO", true);  // aceite mas ignorado

		ligar(q0, LETRAS, qID);
		ligar(qID, LETRAS + DIGITOS, qID);            // laço: continua o nome
		q0.transicoes.add(new Transicao('λ', qLambda));
		q0.transicoes.add(new Transicao('\\', qLambda));
		q0.transicoes.add(new Transicao('.', qPonto));
		q0.transicoes.add(new Transicao('(', qAbre));
		q0.transicoes.add(new Transicao(')', qFecha));
		q0.transicoes.add(new Transicao('=', qIgual));
		ligar(q0, ESPACOS, qEspaco);
		ligar(qEspaco, ESPACOS, qEspaco);             // laço: vários espaços

		return new Automato(q0);
	}

	// =================================================================
	// 2. AP DE PARÊNTESES — cada '(' tem o seu ')'
	//    Pilha: B = base.  Lê a palavra de tokens, ex.: "((i))#"
	// =================================================================
	public static AutomatoPilha criarAPParenteses() {
		Estado q0 = new Estado("q0", false);
		Estado qf = new Estado("qf", true);

		//                                   lê   topo  põe   vai  avança
		q0.transicoes.add(new TransicaoPilha('(', 'B', "(B", q0, true)); // push (
		q0.transicoes.add(new TransicaoPilha('(', '(', "((", q0, true)); // push (
		q0.transicoes.add(new TransicaoPilha(')', '(', "",   q0, true)); // pop (
		q0.transicoes.add(new TransicaoPilha('#', 'B', "",   qf, true)); // fim: aceita

		// os outros símbolos não mexem na pilha
		String outros = "lni=λ.";
		for (int k = 0; k < outros.length(); k++) {
			char s = outros.charAt(k);
			q0.transicoes.add(new TransicaoPilha(s, 'B', "B", q0, true));
			q0.transicoes.add(new TransicaoPilha(s, '(', "(", q0, true));
		}
		return new AutomatoPilha(q0, 'B', "");
	}

	// =================================================================
	// 3. AP DA SINTAXE — reconhece a linguagem completa (gramática LL(1))
	//
	//   E = expressão    L = let       A = abstracção λ
	//   P = aplicação    C = cauda     T = átomo        $ = base
	//
	//   E -> L | A | P          L -> l i = E n E      A -> λ i . E
	//   P -> T C                C -> T C | ε          T -> i | ( E )
	// =================================================================
	public static AutomatoPilha criarAPSintaxe() {
		Estado q  = new Estado("q", false);
		Estado qf = new Estado("qf", true);

		// "troca o topo pela regra" — só espreita o símbolo (não avança)
		regra(q, 'l', 'E', "L");
		regra(q, 'λ', 'E', "A");
		regra(q, 'i', 'E', "P");
		regra(q, '(', 'E', "P");
		regra(q, 'l', 'L', "li=EnE");
		regra(q, 'λ', 'A', "λi.E");
		regra(q, 'i', 'P', "TC");
		regra(q, '(', 'P', "TC");
		regra(q, 'i', 'C', "TC");
		regra(q, '(', 'C', "TC");
		regra(q, 'n', 'C', "");      // C -> ε  quando vem in
		regra(q, ')', 'C', "");      // C -> ε  quando vem )
		regra(q, '#', 'C', "");      // C -> ε  no fim
		regra(q, 'i', 'T', "i");
		regra(q, '(', 'T', "(E)");

		// "lê": o topo é igual ao símbolo -> desempilha e avança
		String terminais = "lni=λ.()";
		for (int k = 0; k < terminais.length(); k++) {
			char t = terminais.charAt(k);
			q.transicoes.add(new TransicaoPilha(t, t, "", q, true));
		}
		// fim da palavra com a base no topo: aceita
		q.transicoes.add(new TransicaoPilha('#', '$', "", qf, true));

		return new AutomatoPilha(q, '$', "E");
	}

	static void regra(Estado q, char espreita, char topo, String poe) {
		q.transicoes.add(new TransicaoPilha(espreita, topo, poe, q, false));
	}
}
