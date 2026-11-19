# Mini Linguagem Funcional — código Java (Tema 10, até à análise semântica)

Requer Java 21 (usa records, sealed interfaces e pattern matching em `switch`).

```
cd codigo_java
javac -encoding UTF-8 -d out src/minilambda/*.java
java -cp out minilambda.Testes            # 37 testes automáticos
java -cp out minilambda.Main              # demonstração de todos os autómatos e fases
java -cp out minilambda.Main "\x.x y"     # pipeline completo para uma expressão
```

> No terminal do Windows, escreva `\` em vez de `λ` nos argumentos da linha de comandos
> (o AFD aceita os dois como LAMBDA). Se os acentos aparecerem trocados, execute `chcp 65001` primeiro.

| Ficheiro | Papel |
|---|---|
| `LexerAFD.java` | **Autómato 1**: AFD léxico dirigido por tabela (δ), com maximal munch e classificação qRES |
| `AutomatoPilhaParenteses.java` | **Autómato 2**: autómato de pilha que verifica o equilíbrio de parênteses |
| `AutomatoPilhaLL1.java` | **Autómato 3**: autómato de pilha preditivo LL(1) que reconhece toda a sintaxe |
| `Parser.java`, `Ast.java` | Parser descendente recursivo, AST e recuperação em modo de pânico |
| `TabelaSimbolos.java` | Ambiente organizado em pilha de escopos (`enterScope`, `declare`, `lookup`, `exitScope`) |
| `AnalisadorSemantico.java` | Variáveis livres/ligadas, FV(e), variáveis não ligadas, aviso de sombreamento |
| `Token`, `TokenType`, `CompilerError` | Tokens e diagnósticos com posição linha:coluna |
| `Main.java`, `Testes.java` | Demonstração e testes |
