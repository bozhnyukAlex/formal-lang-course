# Описание языка запросов

## Описание абстрактного синтаксиса языка

```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Bool of bool
  | Path of path
  | List of string
  | List of int
  | List of bool

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | Smb of expr                  // единичный переход

lambda =
    Lambda of List<var> * expr
```

## Правила вывода типов

Константы типизируются очевидным образом.

Тип переменной определяется типом выражения, с которым она связана.
```
[b(v)] => t
_________________
[Var (v)](b) => t
```

Загрузить можно только автомат.
```
_________________________
[Load (p)](b) => FA<int>
```

Установка финальных состояний, а так же добавление стартовых и финальных типизируется аналогично типизации установки стартовых, которая приведена ниже.
```
[s](b) => Set<t> ;  [e](b) => FA<t>
___________________________________
[Set_start (s, e)](b) => FA<t>


[s](b) => Set<t> ;  [e](b) => RSM<t>
____________________________________
[Set_start (s, e)](b) => RSM<t>

```

Получение финальных типизируется аналогично получению стартовых, правила для которого приведены ниже.
```
[e](b) => FA<t>
____________________________
[Get_start (e)](b) => Set<t>


[e](b) => RSM<t>
____________________________
[Get_start (e)](b) => RSM<t>

```

```
[e](b) => FA<t>
__________________________________
[Get_reachable (e)](b) => Set<t*t>


[e](b) => RSM<t>
__________________________________
[Get_reachable (e)](b) => Set<t*t>

```

```
[e](b) => FA<t>
_______________________________
[Get_vertices (e)](b) => Set<t>


[e](b) => RSM<t>
_______________________________
[Get_vertices (e)](b) => Set<t>


[e](b) => FA<t>
______________________________________
[Get_edges (e)](b) => Set<t*string*t>


[e](b) => RSM<t>
______________________________________
[Get_edges (e)](b) => Set<t*string*t>

[e](b) => FA<t>
__________________________________
[Get_labels (e)](b) => Set<string>


[e](b) => RSM<t>
__________________________________
[Get_labels (e)](b) => Set<string>

```

Правила для ```map``` и ```filter``` традиционные.
```
[f](b) => t1 -> t2 ; [q](b) => Set<t1>
_______________________________________
[Map (f,q)](b) => Set<t2>


[f](b) => t1 -> bool ; [q](b) => Set<t1>
________________________________________
[Filter (f,q)](b) => Set<t1>
```

Пересечение для двух КС не определено.
```
[e1](b) => FA<t1> ;  [e2](b) => FA<t2>
______________________________________
[Intersect (e1, e2)](b) => FA<t1*t2>


[e1](b) => FA<t1> ;  [e2](b) => RSM<t2>
_______________________________________
[Intersect (e1, e2)](b) => RSM<t1*t2>


[e1](b) => RSM<t1> ;  [e2](b) => FA<t2>
_______________________________________
[Intersect (e1, e2)](b) => RSM<t1*t2>

```

Остальные операции над автоматами типизируются согласно формальных свойств классов языков.
```
[e1](b) => FA<t> ;  [e2](b) => FA<t>
_____________________________________
[Concat (e1, e2)](b) => FA<t>


[e1](b) => FA<t> ;  [e2](b) => RSM<t>
______________________________________
[Concat (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => FA<t>
______________________________________
[Concat (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => RSM<t>
______________________________________
[Concat (e1, e2)](b) => RSM<t>

```

```
[e1](b) => FA<t> ;  [e2](b) => FA<t>
______________________________________
[Union (e1, e2)](b) => FA<t>


[e1](b) => FA<t> ;  [e2](b) => RSM<t>
_______________________________________
[Union (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => FA<t>
_______________________________________
[Union (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => RSM<t>
_______________________________________
[Union (e1, e2)](b) => RSM<t>

```

```
[e](b) => FA<t>
______________________
[Star (e)](b) => FA<t>


[e](b) => RSM<t>
______________________
[Star (e](b) => RSM<t>

```

```
[e](b) => string
________________________
[Smb (e)](b) => FA<int>

```


## Динамическая семантика языка запросов

Связывание переопределяет имя.

```
[e](b1) => x,b2
_____________________________________
[Bind (v, e)](b1) => (), (b1(v) <= x)

```

Загрузить можно только автомат и у него все вершины будут стартовыми и финальными.

```
[p](b1) => s,b2 ; read_fa_from_file s => fa
_____________________________________
[Load (p)](b1) => (fa | fa.start = fa.vertices, fa.final = fa.vertices), b1

```

### Описание конкретного синтаксиса языка
```
program -> (stmt SEMI EOL?)+

stmt -> PRINT expr
      | var ASSIGN expr

expr -> LP expr RP
      | anfunc
      | mapping
      | filtering
      | var
      | val
      | NOT expr
      | expr KLEENE
      | expr IN expr
      | expr AND expr
      | expr DOT expr
      | expr OR expr


graph -> load_graph
       | cfg
       | string
       | set_start
       | set_final
       | add_start
       | add_final
       | LP graph RP

load_graph -> LOAD GRAPH path
set_start -> SET START OF (graph | var) TO (vertices | var)
set_final -> SET FINAL OF (graph | var) TO (vertices | var)
add_start -> ADD START OF (graph | var) TO (vertices | var)
add_final -> ADD FINAL OF (graph | var) TO (vertices | var)

vertices -> vertex
          | vertices_range
          | vertices_set
          | get_reachable
          | get_final
          | get_start
          | get_vertices
          | LP vertices RP

vertex -> INT

edges -> edge
       | edges_set
       | get_edges

edge -> LP vertex COMMA label COMMA vertex RP
      | LP vertex COMMA vertex RP

labels -> label
        | labels_set
        | get_labels

label -> string

anfunc -> LAMBDA variables COLON expr
        | LP anfunc RP

mapping -> MAP anfunc expr
filtering -> FILTER anfunc expr

get_edges -> GET EDGES FROM (graph | var)
get_labels -> GET LABELS FROM (graph | var)
get_reachable -> GET REACHABLE VERTICES FROM (graph | var)
get_final -> GET FINAL VERTICES FROM (graph | var)
get_start -> GET START VERTICES FROM (graph | var)
get_vertices -> GET VERTICES FROM (graph | var)
vertices_range -> LCB INT DOT DOT INT RCB

cfg -> CFG
string -> STRING
path -> STRING

vertices_set -> LCB (INT COMMA)* (INT)? RCB
              | vertices_range

labels_set -> LCB (STRING COMMA)* (STRING)? RCB

edges_set -> LCB (edge COMMA)* (edge)? RCB
var -> VAR

var_edge -> LP var COMMA var RP
          | LP var COMMA var COMMA var RP
          | LP LP var COMMA var RP COMMA var COMMA LP var COMMA var RP RP

variables -> (var COMMA)* var? | var_edge

val -> boolean
     | graph
     | edges
     | labels
     | vertices


boolean -> boolean
boolean -> TRUE | FALSE
TRUE -> 'true'
FALSE -> 'false'

LAMBDA -> 'LAMBDA'
LOAD -> 'LOAD'
SET -> 'SET'
ADD -> 'ADD'
OF -> 'OF'
TO -> 'TO'
GRAPH -> 'GRAPH'
VERTICES -> 'VERTICES'
LABELS -> 'LABELS'
GET -> 'GET'
EDGES -> 'EDGES'
REACHABLE -> 'REACHABLE'
START -> 'START'
FINAL -> 'FINAL'
FROM -> 'FROM'
FILTER -> 'FILTER'
MAP -> 'MAP'
PRINT -> 'PRINT'
BOOL -> TRUE | FALSE
TRUE -> 'TRUE'
FALSE -> 'FALSE'

VAR -> ('_' | CHAR) ID_CHAR*

ASSIGN -> '='
AND -> '&'
OR -> '|'
NOT -> 'NOT'
IN -> 'IN'
KLEENE -> '*'
DOT -> '.'
COMMA -> ','
SEMI -> ';'
LCB -> '{'
RCB -> '}'
LB -> '['
RB -> ']'
LP -> '('
RP -> ')'
QUOT -> '"'
TRIPLE_QUOT -> '"""'
COLON -> ':'
ARROW -> '->'

INT -> NONZERO_DIGIT DIGIT* | '0'
CFG -> TRIPLE_QUOT (CHAR | DIGIT | ' ' | '\n' | ARROW)* TRIPLE_QUOT
STRING -> QUOT (CHAR | DIGIT | '_' | ' ')* QUOT
ID_CHAR -> (CHAR | DIGIT | '_')
CHAR -> [a-z] | [A-Z]
NONZERO_DIGIT -> [1-9]
DIGIT -> [0-9]
WS -> [ \t\r]+
EOL -> [\n]+

```

### Пример программы
Данный скрипт загружает граф "geospecies", задает стартовые и финальные вершины, создает запрос, выполняет пересечение
и печатает результат.
```
G = LOAD GRAPH "geospecies";
H = SET START OF (SET FINAL OF G TO (GET VERTICES FROM G)) TO {1...100};
L1 = "L1" | "L2"
Q = ("type" | l1)*;
RES = G & Q;
PRINT RES;
```

# Спецификация интерпретатора GQL (языка запросов к графам)
## Типизация
Типизация строгая динамическая с использованием проверки типов runtime.

## Типы данных языка GQL
### Bool
Булевый тип данных. Поддерживает основные логические операции И, ИЛИ, НЕ над объектами Bool.
Результатом логической операции является GQLBool.
### Set
Множество с элементами одного типа. Допустимы пересечение, объединение двух множеств. Реализована проверка на вхождение во множество IN.
### FiniteAutomata
Класс конечных автоматов. Служит для представления графов или регулярных выражений. Реализована поддержка операций, допустимых с точки зрения теории формальных языков: пересечение, объединение двух FiniteAutomata. Пересечение, объединение с GqlCFG.
### GqlCFG
Класс для КС-грамматик. Допустимы операции, аналогичные FiniteAutomata. Пересечение двух КС-грамматик не разрешено.


#### Особенности
FiniteAutomata, GqlCFG являются наследниками одного типа BaseAutomata.
Введённая строка интерпретируется как регулярное выражение и переводится в тип FiniteAutomata.
Введённая строка в тройных кавычках интерпретируется как КС-грамматика и переводится в тип GqlCFG.

## Используемые алгоритмы
Используются алгоритмы и функции, реализованные в предыдущих заданиях. В частности, для вычисления достижимых вершин используется класс булевых матриц BooleanMatrices.

## Пример работы интерпретатора
`regex.gql`
```
Regex_First = "l1" . "l2"*;
Regex_Second = "l1" | "l2"* | "l4";
Intersection = Regex_First & Regex_Second;
PRINT Intersection;
Regex_Third = Regex_First | Regex_Second;
PRINT Intersection & Regex_Third;
```
Пример запуска интерпретатора (из корня проекта):
`python -m project.graph_query_language.interpreter ./tests/graph_query_language/interpreter/scripts/labels_filter.gql`
