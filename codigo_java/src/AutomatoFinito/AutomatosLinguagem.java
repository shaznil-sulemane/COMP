package AutomatoFinito;

/**
 * Construção dos três autómatos da mini-linguagem, no mesmo estilo do
 * Executavel da aula: criar estados, ligar transições, criar o autómato.
 */
public class AutomatosLinguagem {

	static final String LETRAS  = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
	static final String DIGITOS = "0123456789";
	static final String ESPACOS = " \t\r\n";

	// =====================================================================
	// AUTÓMATO 1 — AFD LÉXICO
	// =====================================================================
	public static Automato criarAFDLexico() {
		Estado q0      = new Estado("q0",   false, null);
		Estado qID     = new Estado("qID",  true,  TokenType.ID);      // classificado depois em qRES
		Estado qLambda = new Estado("qλ",   true,  TokenType.LAMBDA);
		Estado qPonto  = new Estado("qDOT", true,  TokenType.DOT);
		Estado qAbre   = new Estado("qLP",  true,  TokenType.LPAREN);
		Estado qFecha  = new Estado("qRP",  true,  TokenType.RPAREN);
		Estado qIgual  = new Estado("qEQ",  true,  TokenType.EQUALS);
		Estado qEspaco = new Estado("qWS",  true,  null);              // aceita e descarta

		// q0: início de cada token
		q0.adicionarTransicoes(LETRAS + "_", qID);
		q0.transicoes.add(new Transicao('λ', qLambda));
		q0.transicoes.add(new Transicao('\\', qLambda));
		q0.transicoes.add(new Transicao('.', qPonto));
		q0.transicoes.add(new Transicao('(', qAbre));
		q0.transicoes.add(new Transicao(')', qFecha));
		q0.transicoes.add(new Transicao('=', qIgual));
		q0.adicionarTransicoes(ESPACOS, qEspaco);

		// laços: identificadores e espaços consecutivos
		qID.adicionarTransicoes(LETRAS + DIGITOS + "_", qID);
		qEspaco.adicionarTransicoes(ESPACOS, qEspaco);

		return new Automato(q0);
	}

	// =====================================================================
	// AUTÓMATO 2 — AP DE EQUILÍBRIO DE PARÊNTESES  (lê a palavra de tokens)
	// =====================================================================
	public static AutomatoPilha criarAPParenteses() {
		Estado q0 = new Estado("q0", false, null);
		Estado qf = new Estado("qf", true,  null);

		//                                   lê   topo  empilha  destino consome
		q0.transicoes.add(new TransicaoPilha('(', 'B', "(B", q0, true));   // push (
		q0.transicoes.add(new TransicaoPilha('(', '(', "((", q0, true));   // push (
		q0.transicoes.add(new TransicaoPilha(')', '(', "",   q0, true));   // pop  (
		for (char s : "λlni=.".toCharArray()) {                            // outros tokens
			q0.transicoes.add(new TransicaoPilha(s, 'B', "B", q0, true));
			q0.transicoes.add(new TransicaoPilha(s, '(', "(", q0, true));
		}
		q0.transicoes.add(new TransicaoPilha('#', 'B', "",   qf, true));   // EOF com base: aceita

		return new AutomatoPilha(q0, 'B', "");
	}

	// =====================================================================
	// AUTÓMATO 3 — AP LL(1) DA SINTAXE COMPLETA  (lê a palavra de tokens)
	//
	// Símbolos da pilha:  E=Expr  L=Let  A=Abs  P=App  C=Cauda  T=Atom  $=base
	// Terminais (tokens): l=LET n=IN i=ID λ=LAMBDA . ( ) =   #=EOF
	//
	//   E → L | A | P        L → l i = E n E        A → λ i . E
	//   P → T C              C → T C | ε            T → i | ( E )
	// =====================================================================
	public static AutomatoPilha criarAPSintaxe() {
		Estado q  = new Estado("q",  false, null);
		Estado qf = new Estado("qf", true,  null);

		// expansões: consultam o token (antevisão) sem o consumir
		expandir(q, 'l', 'E', "L");
		expandir(q, 'λ', 'E', "A");
		expandir(q, 'i', 'E', "P");
		expandir(q, '(', 'E', "P");
		expandir(q, 'l', 'L', "li=EnE");
		expandir(q, 'λ', 'A', "λi.E");
		expandir(q, 'i', 'P', "TC");
		expandir(q, '(', 'P', "TC");
		expandir(q, 'i', 'C', "TC");
		expandir(q, '(', 'C', "TC");
		expandir(q, 'n', 'C', "");      // C → ε  (FOLLOW = { in, ), EOF })
		expandir(q, ')', 'C', "");
		expandir(q, '#', 'C', "");
		expandir(q, 'i', 'T', "i");
		expandir(q, '(', 'T', "(E)");

		// match: terminal no topo igual ao token lido → desempilha e consome
		for (char t : "lni=λ.()".toCharArray()) {
			q.transicoes.add(new TransicaoPilha(t, t, "", q, true));
		}
		// aceitação: EOF com a base no topo
		q.transicoes.add(new TransicaoPilha('#', '$', "", qf, true));

		return new AutomatoPilha(q, '$', "E");
	}

	private static void expandir(Estado q, char token, char naoTerminal, String producao) {
		q.transicoes.add(new TransicaoPilha(token, naoTerminal, producao, q, false));
	}
}
