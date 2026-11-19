# Tema 10 — Mini Linguagem Funcional (Cálculo Lambda Reduzido)

Projecto de Compiladores · ISUTC · LECC31 · 2026
Autores: Ayrton Nhaguaga · Shaznil Sulemane · Jóse Dinis · Sousa Marufo

Desenvolvido até à **análise semântica**, mostrado na prática com autómatos em Java
(baseado nas classes da aula `Estado`, `Transicao`, `Automato`):

```
texto ──AFD──▶ tokens ──AP──▶ sintaxe OK ──pilha de nomes──▶ variáveis OK
```

## Conteúdo

| Caminho | O quê |
|---|---|
| `Mini_Linguagem_Funcional_ISUTC_Automatos_na_Pratica_2026_v3.pptx` | **Slides finais**: teoria (a–e) + autómatos na prática, passo a passo |
| `Mini_Linguagem_Funcional_ISUTC_Ate_Semantica_Java_2026_v2.pptx` | Slides v2 |
| `Mini_Linguagem_Funcional_ISUTC_Ate_Semantica_Java_2026.pptx` | Slides v1 |
| `ferramentas_slides/` | Scripts Python que geram os slides (v2 e v3) |
| `Mini_Linguagem_Funcional_ISUTC_Alineas_A_E_2026 (1).pptx` | Slides de base originais |
| `Relatorio_Tema10_Mini_Linguagem_Funcional_ISUTC.docx` | Relatório (alíneas a–c) |
| `codigo_java/` | Código Java dos autómatos, parser e analisador semântico — ver `codigo_java/README.md` |
| `_backup_v1/` | Versão anterior do código e dos slides |

## Executar o código

```
cd codigo_java
javac -encoding UTF-8 -d out src/AutomatoFinito/*.java
java -cp out AutomatoFinito.Testes
java -cp out AutomatoFinito.Executavel
```
