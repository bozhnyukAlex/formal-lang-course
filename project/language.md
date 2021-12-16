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
PROGRAM -> STMT ; PROGRAM | eps
STMT -> VAR = EXPR | Print(EXPR)
LOWERCASE -> [a-z]
UPPERCASE -> [A-Z]
DIGIT -> [0-9]
INT -> 0 | [1-9] DIGIT*
STRING -> (_ | . | LOWERCASE | UPPERCASE) (_ | . | LOWERCASE | UPPERCASE | DIGIT)*
BOOL -> True | False
PATH -> " (/ | _ | . | LOWERCASE | UPPERCASE | DIGIT)+ "
VAR -> STRING
VAL ->
    INT
    | " STRING "
    | BOOL
    | PATH
    | LIST<INT>
    | LIST<" STRING ">
    | LIST<BOOL>
SET ->
    SET<INT>
    | SET<" STRING ">
    | Range ( INT , INT )
    | Int . . . Int
EXPR -> VAR | VAL | GRAPH
GRAPH -> " STRING "
        | SetStart(SET, GRAPH)
        | SetFinal(SET, GRAPH)
        | AddStart(SET, GRAPH)
        | AddFinal(SET, GRAPH)
EXPR -> VERTEX | VERTICES
VERTEX -> INT
VERTICES -> SET<VERTEX>
            | Range ( INT , INT )
            | Int . . . Int
            | GetStart(GRAPH)
            | GetFinal(SET, GRAPH)
EXPR -> PAIR_OF_VERTICES
PAIR_OF_VERTICES -> SET<(INT, INT)>
PAIR_OF_VERTICES -> GetReachable(GRAPH)
VERTICES -> GetVertices(GRAPH)
EXPR -> EDGE | EDGES
EDGE -> (INT, " STRING ", INT) | (INT, INT, INT)
EDGES -> SET<EDGE> | GetEdges(GRAPH)
EXPR -> LABELS
LABELS -> SET<INT> | SET<" STRING ">
        | GetLabels(GRAPH)
EXPR -> Map(LAMBDA, EXPR)
EXPR -> Filter(LAMBDA, EXPR)
GRAPH -> LoadGraph(" PATH ")
         | Intersect(GRAPH, GRAPH)
         | Concat(GRAPH, GRAPH)
         | Union(GRAPH, GRAPH)
         | Star(GRAPH, GRAPH)
LAMBDA -> (LIST<VAR> -> [BOOL_EXPR | EXPR])
BOOL_EXPR ->
    BOOL_EXPR or BOOL_EXPR
    | BOOL_EXPR and BOOL_EXPR
    | not BOOL_EXPR
    | BOOL
    | HasLabel(EDGE, " STRING ")
    | IsStart(VERTEX)
    | IsFinal(VERTEX)
    | X in SET<X>
LIST<X> -> List(X [, X]*) | List()
SET<X> -> Set(X [, X]*) | Set()
```

### Пример программы
```
g = Load("geospecies")
h = SetStart(SetFinal(GetVertices(g), g)), 1...100)
l1 = Union("l1", "l2")
q1 = Star(Union("type", l1))
q2 = Concat("sub_class_of", l1)
res1 = Intersect(g, q1)
res2 = Intersect(g, q2)
Print(res1)
s = GetStart(g)
vertices = Filter((list(v) -> v in s), GetEdges(res1))
Print(vertices)
```
