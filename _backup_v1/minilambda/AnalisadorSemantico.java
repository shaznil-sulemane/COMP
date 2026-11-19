package minilambda;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

/**
 * Analisador semântico (alínea E): escopo e ligações.
 *
 *   check(e, Γ):
 *     Var(x):        se lookup(Γ, x) = ∅ → erro(x, pos)
 *     Lambda(x, b):  check(b, Γ + { x : PARAM })
 *     Apply(f, a):   check(f, Γ);  check(a, Γ)
 *     Let(x, v, b):  check(v, Γ)              // não recursivo
 *                    check(b, Γ + { x : LET })
 *
 * Política: acumular todos os erros; o programa só é aceite se for fechado
 * (FV(e) = ∅). Sombreamento gera apenas um aviso.
 */
public class AnalisadorSemantico {

    public record Passo(String no, String accao, String ambiente) {}

    private final TabelaSimbolos tabela = new TabelaSimbolos();
    private final List<CompilerError> erros = new ArrayList<>();
    private final List<String> avisos = new ArrayList<>();
    private final List<Passo> passos = new ArrayList<>();
    private final Set<String> ligadas = new LinkedHashSet<>();

    /** Analisa a AST e devolve true se for semanticamente válida. */
    public boolean analisar(Ast.Expr raiz) {
        tabela.enterScope();          // escopo global (vazio)
        check(raiz);
        tabela.exitScope();
        return erros.isEmpty();
    }

    private void check(Ast.Expr e) {
        switch (e) {
            case Ast.Var v -> {
                boolean ok = tabela.lookup(v.nome()) != null;
                passos.add(new Passo("Var(" + v.nome() + ")",
                        ok ? "lookup ✔" : "lookup ✘ → erro", tabela.toString()));
                if (!ok) erros.add(new CompilerError(CompilerError.Fase.SEMANTICO,
                        v.linha(), v.coluna(), "variável '" + v.nome() + "' não ligada"));
            }
            case Ast.Lambda l -> {
                avisarSombreamento(l.param(), l.linha(), l.coluna());
                tabela.enterScope();
                tabela.declare(l.param(), TabelaSimbolos.Tipo.PARAM, l.linha(), l.coluna());
                ligadas.add(l.param());
                passos.add(new Passo("Lambda(" + l.param() + ")",
                        "enter + declare " + l.param(), tabela.toString()));
                check(l.corpo());
                tabela.exitScope();
                passos.add(new Passo("Lambda(" + l.param() + ")", "exit", tabela.toString()));
            }
            case Ast.Apply a -> {
                check(a.funcao());
                check(a.argumento());
            }
            case Ast.Let l -> {
                passos.add(new Passo("Let(" + l.nome() + ")", "visitar o valor", tabela.toString()));
                check(l.valor());                         // x NÃO é visível no valor
                avisarSombreamento(l.nome(), l.linha(), l.coluna());
                tabela.enterScope();
                tabela.declare(l.nome(), TabelaSimbolos.Tipo.LET, l.linha(), l.coluna());
                ligadas.add(l.nome());
                passos.add(new Passo("Let(" + l.nome() + ")",
                        "enter + declare " + l.nome(), tabela.toString()));
                check(l.corpo());
                tabela.exitScope();
                passos.add(new Passo("Let(" + l.nome() + ")", "exit", tabela.toString()));
            }
            case Ast.Erro x -> { /* já reportado na fase sintáctica */ }
        }
    }

    private void avisarSombreamento(String nome, int linha, int coluna) {
        TabelaSimbolos.Simbolo anterior = tabela.lookup(nome);
        if (anterior != null) {
            avisos.add("Aviso [" + linha + ":" + coluna + "]: '" + nome + "' oculta a declaração em "
                    + anterior.linha() + ":" + anterior.coluna() + " (sombreamento)");
        }
    }

    /**
     * Conjunto de variáveis livres FV(e):
     *   FV(x) = {x}                     FV(λx.e) = FV(e) \ {x}
     *   FV(e1 e2) = FV(e1) ∪ FV(e2)     FV(let x = e1 in e2) = FV(e1) ∪ (FV(e2) \ {x})
     */
    public static Set<String> livres(Ast.Expr e) {
        Set<String> r = new LinkedHashSet<>();
        switch (e) {
            case Ast.Var v -> r.add(v.nome());
            case Ast.Lambda l -> { r.addAll(livres(l.corpo())); r.remove(l.param()); }
            case Ast.Apply a -> { r.addAll(livres(a.funcao())); r.addAll(livres(a.argumento())); }
            case Ast.Let l -> {
                Set<String> corpo = livres(l.corpo());
                corpo.remove(l.nome());
                r.addAll(livres(l.valor()));
                r.addAll(corpo);
            }
            case Ast.Erro x -> { }
        }
        return r;
    }

    public List<CompilerError> erros() { return erros; }
    public List<String> avisos()       { return avisos; }
    public List<Passo> passos()        { return passos; }
    public Set<String> ligadas()       { return ligadas; }
}
