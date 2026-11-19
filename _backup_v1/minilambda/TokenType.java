package minilambda;

/**
 * Categorias lexicais da mini-linguagem funcional (Tema 10).
 * Cada constante corresponde a um terminal da gramática.
 */
public enum TokenType {
    LAMBDA,   // lambda | λ | \
    LET,      // let
    IN,       // in
    ID,       // [A-Za-z_][A-Za-z0-9_]*
    DOT,      // .
    LPAREN,   // (
    RPAREN,   // )
    EQUALS,   // =
    EOF       // fim da entrada
}
