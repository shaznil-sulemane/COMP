package minilambda;

/**
 * Unidade lexical: tipo, lexema e posição (linha:coluna, a contar de 1).
 */
public record Token(TokenType tipo, String lexema, int linha, int coluna) {

    public String pos() {
        return linha + ":" + coluna;
    }

    @Override
    public String toString() {
        return switch (tipo) {
            case ID -> "ID(" + lexema + ")";
            case EOF -> "EOF";
            default -> tipo.name();
        };
    }
}
