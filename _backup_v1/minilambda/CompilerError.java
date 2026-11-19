package minilambda;

/**
 * Diagnóstico produzido por qualquer fase (léxica, sintáctica ou semântica).
 */
public class CompilerError extends RuntimeException {

    public enum Fase { LEXICO, SINTACTICO, SEMANTICO }

    private final Fase fase;
    private final int linha;
    private final int coluna;

    public CompilerError(Fase fase, int linha, int coluna, String mensagem) {
        super(mensagem);
        this.fase = fase;
        this.linha = linha;
        this.coluna = coluna;
    }

    public Fase fase()   { return fase; }
    public int linha()   { return linha; }
    public int coluna()  { return coluna; }

    @Override
    public String toString() {
        String nome = switch (fase) {
            case LEXICO -> "Erro léxico";
            case SINTACTICO -> "Erro sintáctico";
            case SEMANTICO -> "Erro semântico";
        };
        return nome + " [" + linha + ":" + coluna + "]: " + getMessage();
    }
}
