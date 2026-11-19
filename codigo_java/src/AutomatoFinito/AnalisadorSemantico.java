package AutomatoFinito;

import java.util.ArrayList;
import java.util.Stack;

// Análise semântica com uma PILHA DE NOMES (o ambiente).
// Percorre os tokens da esquerda para a direita:
//
//   λ x        -> push x                 (x visível até o corpo acabar)
//   let x =    -> push "let x"            (marcador: x ainda NÃO visível)
//   in         -> pop até "let x", push x (o valor acabou; x fica visível)
//   (          -> push "("                (marcador)
//   )          -> pop até "("             (tudo o que abriu lá dentro acaba)
//   nome       -> procurar na pilha, do topo para baixo; se não está: ERRO
//
// Só corre depois de o AP da sintaxe aceitar a expressão.
public class AnalisadorSemantico {
	ArrayList<String> erros = new ArrayList<String>();
	ArrayList<String> avisos = new ArrayList<String>();
	boolean mostrarPassos = false;

	public boolean verificar(ArrayList<Token> tokens) {
		Stack<String> pilha = new Stack<String>();

		for (int k = 0; k < tokens.size(); k++) {
			Token t = tokens.get(k);
			String accao = "";

			if (t.tipo.equals("LAMBDA")) {
				String x = tokens.get(k + 1).lexema;
				if (procurar(pilha, x)) avisos.add("Aviso: '" + x + "' oculta outro '" + x + "' (sombreamento)");
				pilha.push(x);
				accao = "push " + x;
				k++;                                   // o parâmetro já foi tratado
			} else if (t.tipo.equals("LET")) {
				String x = tokens.get(k + 1).lexema;
				pilha.push("let " + x);
				accao = "push marcador 'let " + x + "'";
				k++;
			} else if (t.tipo.equals("IN")) {
				String x = popAte(pilha, "let ").substring(4);
				if (procurar(pilha, x)) avisos.add("Aviso: '" + x + "' oculta outro '" + x + "' (sombreamento)");
				pilha.push(x);
				accao = "pop até 'let', push " + x;
			} else if (t.tipo.equals("LPAREN")) {
				pilha.push("(");
				accao = "push (";
			} else if (t.tipo.equals("RPAREN")) {
				popAte(pilha, "(");
				accao = "pop até (";
			} else if (t.tipo.equals("ID")) {
				if (procurar(pilha, t.lexema)) {
					accao = "procura " + t.lexema + " -> encontrada";
				} else {
					accao = "procura " + t.lexema + " -> ERRO";
					erros.add("Erro semântico [" + t.linha + ":" + t.coluna + "]: variável '" + t.lexema + "' não ligada");
				}
			}
			if (mostrarPassos && !accao.isEmpty()) {
				System.out.println(String.format("   %-8s %-32s %s", t.lexema, accao, pilha));
			}
		}
		return erros.isEmpty();
	}

	// procura um nome do topo para a base (ignora marcadores)
	static boolean procurar(Stack<String> pilha, String nome) {
		for (int k = pilha.size() - 1; k >= 0; k--) {
			if (pilha.get(k).equals(nome)) return true;
		}
		return false;
	}

	// desempilha até encontrar um marcador que começa por 'prefixo'; devolve-o
	static String popAte(Stack<String> pilha, String prefixo) {
		while (!pilha.isEmpty()) {
			String s = pilha.pop();
			if (s.startsWith(prefixo)) return s;
		}
		return "";
	}
}
