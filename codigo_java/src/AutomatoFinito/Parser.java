package AutomatoFinito;

import java.util.ArrayList;
import java.util.EnumSet;
import java.util.List;
import java.util.Set;

/**
 * Analisador sintáctico descendente recursivo (alínea D).
 * Implementação equivalente ao AP LL(1): a pilha do autómato passa a ser a
 * pilha de chamadas dos métodos parseX(). Constrói a AST.
 *
 *   Expr        ::= LetExpr | LambdaExpr | Application
 *   LetExpr     ::= LET ID EQUALS Expr IN Expr
 *   LambdaExpr  ::= LAMBDA ID DOT Expr
 *   Application ::= Atom { Atom }            (associa à esquerda)
 *   Atom        ::= ID | LPAREN Expr RPAREN
 *
 * Recuperação de erros em modo de pânico: detectar → relatar → sincronizar
 * (IN, RPAREN, EOF) → retomar.
 */
public class Parser {

    private static final Set<TokenType> SINCRONIZACAO =
            EnumSet.of(TokenType.IN, TokenType.RPAREN, TokenType.EOF);

    private final List<Token> tokens;
    private final List<CompilerError> erros = new ArrayList<>();
    private int atual = 0;

    public Parser(List<Token> tokens) { this.tokens = tokens; }

    /** Ponto de entrada: Programa ::= Expr EOF */
    public Ast.Expr parse() {
        Ast.Expr e = parseExpr();
        if (!verifica(TokenType.EOF)) {
            relatar(espiar(), "token inesperado " + espiar() + "; esperado fim da entrada");
        }
        return e;
    }

    // Expr ::= LetExpr | LambdaExpr | Application   (decisão por 1 token de antevisão)
    private Ast.Expr parseExpr() {
        try {
            return switch (espiar().tipo()) {
                case LET -> parseLet();
                case LAMBDA -> parseLambda();
                case ID, LPAREN -> parseApplication();
                default -> throw erro(espiar(), "esperado expressão; recebido " + espiar());
            };
        } catch (CompilerError e) {
            erros.add(e);           // relatar
            sincronizar();          // sincronizar
            return new Ast.Erro();  // retomar com nó de erro
        }
    }

    // LetExpr ::= LET ID EQUALS Expr IN Expr
    private Ast.Expr parseLet() {
        consumir(TokenType.LET, "'let'");
        Token nome = consumir(TokenType.ID, "identificador");
        consumir(TokenType.EQUALS, "'='");
        Ast.Expr valor = parseExpr();
        consumir(TokenType.IN, "'in'");
        Ast.Expr corpo = parseExpr();
        return new Ast.Let(nome.lexema(), nome.linha(), nome.coluna(), valor, corpo);
    }

    // LambdaExpr ::= LAMBDA ID DOT Expr
    private Ast.Expr parseLambda() {
        consumir(TokenType.LAMBDA, "'λ'");
        Token param = consumir(TokenType.ID, "identificador");
        consumir(TokenType.DOT, "'.'");
        Ast.Expr corpo = parseExpr();
        return new Ast.Lambda(param.lexema(), param.linha(), param.coluna(), corpo);
    }

    // Application ::= Atom { Atom }  →  f x y = Apply(Apply(f, x), y)
    private Ast.Expr parseApplication() {
        Ast.Expr e = parseAtom();
        while (verifica(TokenType.ID) || verifica(TokenType.LPAREN)) {
            e = new Ast.Apply(e, parseAtom());
        }
        return e;
    }

    // Atom ::= ID | LPAREN Expr RPAREN
    private Ast.Expr parseAtom() {
        Token t = espiar();
        if (t.tipo() == TokenType.ID) {
            avancar();
            return new Ast.Var(t.lexema(), t.linha(), t.coluna());
        }
        if (t.tipo() == TokenType.LPAREN) {
            avancar();
            Ast.Expr e = parseExpr();
            consumir(TokenType.RPAREN, "')'");
            return e;
        }
        throw erro(t, "esperado identificador ou '('; recebido " + t);
    }

    // ---------------- utilitários ----------------

    private Token consumir(TokenType tipo, String descricao) {
        if (verifica(tipo)) return avancar();
        throw erro(espiar(), "esperado " + descricao + "; recebido " + espiar());
    }

    /** Modo de pânico: descarta tokens até um token de sincronização. */
    private void sincronizar() {
        while (!SINCRONIZACAO.contains(espiar().tipo())) avancar();
    }

    private void relatar(Token t, String msg) { erros.add(erro(t, msg)); }

    private CompilerError erro(Token t, String msg) {
        return new CompilerError(CompilerError.Fase.SINTACTICO, t.linha(), t.coluna(), msg);
    }

    private boolean verifica(TokenType tipo) { return espiar().tipo() == tipo; }
    private Token espiar() { return tokens.get(atual); }
    private Token avancar() {
        Token t = tokens.get(atual);
        if (t.tipo() != TokenType.EOF) atual++;
        return t;
    }

    public List<CompilerError> erros() { return erros; }
}
