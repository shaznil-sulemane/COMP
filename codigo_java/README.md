# Mini Linguagem Funcional — código Java (Tema 10, até à análise semântica)

Estrutura baseada nas classes da aula (`Estado`, `Transicao`, `Automato`, `Executavel`).
Os três autómatos da linguagem são construídos da mesma forma que o exemplo da aula:
criar estados → ligar transições → criar o autómato → `procurarPalavra(...)`.

Requer Java 21.

```
cd codigo_java
javac -encoding UTF-8 -d out src/AutomatoFinito/*.java
java -cp out AutomatoFinito.Testes             # 40 testes automáticos
java -cp out AutomatoFinito.Executavel         # exemplo da aula + todos os autómatos e fases
java -cp out AutomatoFinito.Executavel "\x.x y"
```

> No terminal do Windows use `\` em vez de `λ` nos argumentos (o AFD aceita os dois).

## Classes

| Classe | Origem | Papel |
|---|---|---|
| `Estado`, `Transicao`, `Automato` | aula (mantidas) | AFD genérico. Acrescentos: nome/token no `Estado`, `maiorPrefixo()` no `Automato` |
| `TransicaoPilha` | estende `Transicao` | δ(estado, símbolo, topo) = (destino, empilhar) |
| `AutomatoPilha` | mesma lógica do `Automato` | `procurarPalavra()` com pilha e traço de execução |
| `AutomatosLinguagem` | novo | Constrói o **AFD léxico**, o **AP de parênteses** e o **AP LL(1)** |
| `AnalisadorLexico` | novo | Aplica o AFD com maior correspondência + qRES (palavras reservadas) |
| `Token`, `TokenType` | novo | Cada token tem um símbolo: `let id = λx.x in id y` → `li=λi.inii#` |
| `Parser`, `Ast` | novo | Descendente recursivo, AST, modo de pânico |
| `TabelaSimbolos`, `AnalisadorSemantico` | novo | Pilha de escopos, FV(e), variáveis não ligadas |
| `Executavel`, `Testes` | aula / novo | Demonstração e testes |

A versão anterior do código e dos slides está guardada em `../_backup_v1/`.
