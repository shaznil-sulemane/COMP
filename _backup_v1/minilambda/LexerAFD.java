package minilambda;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * AUTÓMATO 1 — Analisador léxico implementado como AFD dirigido por tabela.
 *
 *   M = (Q, Σ, δ, q0, F)
 *   Q  = { q0, qID, qλ, qDOT, qLP, qRP, qEQ, qWS, qERR }
 *   F  = { qID, qλ, qDOT, qLP, qRP, qEQ, qWS }
 *
 * Política de maior correspondência (maximal munch): o AFD avança enquanto
 * houver transição válida, memorizando o último estado de aceitação; quando
 * bloqueia, emite o token do maior lexema aceite. Só então o estado de
 * classificação qRES decide se o lexema de qID é palavra reservada.
 *   "letter" -> ID(letter)   (nunca LET + ID(ter))
 */
public class LexerAFD {

    // ---------- Estados (Q) ----------
    static final int Q0 = 0, QID = 1, QLAMBDA = 2, QDOT = 3, QLP = 4,
                     QRP = 5, QEQ = 6, QWS = 7, QERR = 8;
    static final String[] NOME_ESTADO =
        { "q0", "qID", "qλ", "qDOT", "qLP", "qRP", "qEQ", "qWS", "qERR" };

    // ---------- Classes de caracteres (partição de Σ) ----------
    static final int C_LETRA = 0, C_DIGITO = 1, C_SUB = 2, C_LAMBDA = 3, C_PONTO = 4,
                     C_ABRE = 5, C_FECHA = 6, C_IGUAL = 7, C_ESPACO = 8, C_OUTRO = 9;

    /** Função de transição δ : Q × classe → Q  (linhas = estados, colunas = classes). */
    static final int[][] DELTA = {
        //            letra  dígito  _     λ \   .     (     )     =     espaço  outro
        /* q0   */ { QID,   QERR,   QID,  QLAMBDA, QDOT, QLP, QRP, QEQ, QWS,  QERR },
        /* qID  */ { QID,   QID,    QID,  QERR, QERR, QERR, QERR, QERR, QERR, QERR },
        /* qλ   */ { QERR,  QERR,   QERR, QERR, QERR, QERR, QERR, QERR, QERR, QERR },
        /* qDOT */ { QERR,  QERR,   QERR, QERR, QERR, QERR, QERR, QERR, QERR, QERR },
        /* qLP  */ { QERR,  QERR,   QERR, QERR, QERR, QERR, QERR, QERR, QERR, QERR },
        /* qRP  */ { QERR,  QERR,   QERR, QERR, QERR, QERR, QERR, QERR, QERR, QERR },
        /* qEQ  */ { QERR,  QERR,   QERR, QERR, QERR, QERR, QERR, QERR, QERR, QERR },
        /* qWS  */ { QERR,  QERR,   QERR, QERR, QERR, QERR, QERR, QERR, QWS,  QERR },
        /* qERR */ { QERR,  QERR,   QERR, QERR, QERR, QERR, QERR, QERR, QERR, QERR },
    };

    /** Estados de aceitação (F). qWS aceita mas o lexema é descartado. */
    static final boolean[] ACEITA = { false, true, true, true, true, true, true, true, false };

    /** Token emitido por cada estado de aceitação (qID passa por qRES). */
    static final TokenType[] EMITE =
        { null, TokenType.ID, TokenType.LAMBDA, TokenType.DOT, TokenType.LPAREN,
          TokenType.RPAREN, TokenType.EQUALS, null, null };

    /** qRES — classificação após o lexema: tabela de palavras reservadas. */
    static final Map<String, TokenType> RESERVADAS = Map.of(
        "lambda", TokenType.LAMBDA,
        "let",    TokenType.LET,
        "in",     TokenType.IN
    );

    private final String fonte;
    private final boolean traco;
    private final List<String> passos = new ArrayList<>();
    private final List<CompilerError> erros = new ArrayList<>();

    private int pos = 0, linha = 1, coluna = 1;

    public LexerAFD(String fonte) { this(fonte, false); }

    public LexerAFD(String fonte, boolean traco) {
        this.fonte = fonte;
        this.traco = traco;
    }

    /** Mapeia um carácter para a sua classe de Σ. */
    static int classe(char c) {
        if (c == 'λ' || c == '\\') return C_LAMBDA;
        if (c == '_') return C_SUB;
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) return C_LETRA;
        if (c >= '0' && c <= '9') return C_DIGITO;
        return switch (c) {
            case '.' -> C_PONTO;
            case '(' -> C_ABRE;
            case ')' -> C_FECHA;
            case '=' -> C_IGUAL;
            case ' ', '\t', '\r', '\n' -> C_ESPACO;
            default -> C_OUTRO;
        };
    }

    /** Percorre toda a entrada e devolve a lista de tokens (terminada em EOF). */
    public List<Token> tokenizar() {
        List<Token> tokens = new ArrayList<>();
        while (pos < fonte.length()) {
            int inicio = pos, linIni = linha, colIni = coluna;

            // --- simulação do AFD com maximal munch ---
            int estado = Q0, ultimoAceite = -1, fimAceite = -1;
            int i = pos;
            StringBuilder caminho = new StringBuilder(NOME_ESTADO[Q0]);
            while (i < fonte.length()) {
                int prox = DELTA[estado][classe(fonte.charAt(i))];
                if (prox == QERR) break;
                estado = prox;
                i++;
                caminho.append(" -").append(mostrar(fonte.charAt(i - 1))).append("-> ")
                       .append(NOME_ESTADO[estado]);
                if (ACEITA[estado]) { ultimoAceite = estado; fimAceite = i; }
            }

            if (ultimoAceite == -1) {           // nenhum prefixo aceite: erro léxico
                char c = fonte.charAt(pos);
                erros.add(new CompilerError(CompilerError.Fase.LEXICO, linIni, colIni,
                        "carácter '" + c + "' não reconhecido"));
                avancar(pos + 1);               // recuperação: descarta 1 carácter
                continue;
            }

            String lexema = fonte.substring(inicio, fimAceite);
            avancar(fimAceite);
            if (ultimoAceite == QWS) continue;  // espaços são ignorados

            TokenType tipo = EMITE[ultimoAceite];
            if (ultimoAceite == QID) {          // qRES: classificação
                tipo = RESERVADAS.getOrDefault(lexema, TokenType.ID);
            }
            Token t = new Token(tipo, lexema, linIni, colIni);
            tokens.add(t);
            if (traco) passos.add(String.format("%-28s => %s", caminho, t));
        }
        tokens.add(new Token(TokenType.EOF, "", linha, coluna));
        return tokens;
    }

    /** Actualiza pos, linha e coluna até à posição alvo. */
    private void avancar(int alvo) {
        while (pos < alvo) {
            if (fonte.charAt(pos) == '\n') { linha++; coluna = 1; } else { coluna++; }
            pos++;
        }
    }

    private static String mostrar(char c) {
        return Character.isWhitespace(c) ? "␣" : String.valueOf(c);
    }

    public List<CompilerError> erros() { return erros; }
    public List<String> passos()       { return passos; }
}
