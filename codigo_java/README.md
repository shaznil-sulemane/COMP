# Mini Linguagem Funcional — código Java

Baseado nas classes da aula: `Estado`, `Transicao`, `Automato`, `Executavel`.
Tudo é feito com **autómatos e pilhas**:

```
texto ──AFD──▶ tokens ──AP──▶ sintaxe OK ──pilha de nomes──▶ variáveis OK
```

| Ficheiro | O que faz |
|---|---|
| `Estado.java`, `Transicao.java`, `Automato.java` | Classes da aula. `Transicao` está igual; `Estado` ganhou um `nome`; `Automato` ganhou `maiorPrefixo()` |
| `TransicaoPilha.java` | `Transicao` + topo da pilha + o que empilhar |
| `AutomatoPilha.java` | O mesmo ciclo de `procurarPalavra()`, agora com uma `Stack` |
| `Automatos.java` | Constrói os 3 autómatos: **AFD léxico**, **AP de parênteses**, **AP da sintaxe** |
| `Token.java`, `AnalisadorLexico.java` | Usa o AFD para cortar o texto em tokens |
| `AnalisadorSemantico.java` | Pilha de nomes: verifica se cada variável foi declarada |
| `Executavel.java` | Exemplo da aula + demonstração passo a passo de tudo |
| `Testes.java` | 31 testes |

## Executar

```
cd codigo_java
javac -encoding UTF-8 -d out src/AutomatoFinito/*.java
java -cp out AutomatoFinito.Executavel
java -cp out AutomatoFinito.Testes
java -cp out AutomatoFinito.Executavel "\x.x y"     (no Windows use \ em vez de λ)
```
