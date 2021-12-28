grammar GraphQueryLanguage;

prog : (EOL? WS? stmt SEMI EOL?)+ EOF;

stmt : PRINT expr
     | VAR WS? ASSIGN WS? expr
     ;

expr : LP expr RP
     | anfunc
     | mapping
     | filtering
     | var
     | val
     | NOT expr
     | expr IN expr
     | expr AND expr
     | expr DOT expr
     | expr OR expr
     | expr KLEENE
     ;

graph : load_graph
      | cfg
      | string
      | set_start
      | set_final
      | add_start
      | add_final
      | LP graph RP
      ;

load_graph : LOAD GRAPH (path | string);
set_start : SET START OF (graph | var) TO (vertices | var) ;
set_final : SET FINAL OF (graph | var) TO (vertices | var) ;
add_start : ADD START OF (graph | var) TO (vertices | var) ;
add_final : ADD FINAL OF (graph | var) TO (vertices | var) ;

vertices : vertex
       | vertices_range
       | vertices_set
       | get_reachable
       | get_final
       | get_start
       | get_vertices
       | LP vertices RP
       ;


vertex : INT ;

edges : edge
      | edges_set
      | get_edges ;

edge : LP vertex COMMA label COMMA vertex RP
     | LP vertex COMMA vertex RP ;

labels : label
       | labels_set
       | get_labels ;

label : string ;

anfunc : LAMBDA variables COLON expr
       | LP anfunc RP ;

mapping : MAP anfunc expr;
filtering : FILTER anfunc expr;

get_edges : GET EDGES FROM (graph | var) ;
get_labels : GET LABELS FROM (graph | var) ;
get_reachable : GET REACHABLE VERTICES FROM (graph | var) ;
get_final : GET FINAL VERTICES FROM (graph | var) ;
get_start : GET START VERTICES FROM (graph | var) ;
get_vertices : GET VERTICES FROM (graph | var) ;
vertices_range : LCB INT DOT DOT INT RCB ;

cfg : CFG ;
string : STRING ;
path : PATH ;

vertices_set : LCB (INT COMMA)* (INT)? RCB
             | vertices_range ;

labels_set : LCB (STRING COMMA)* (STRING)? RCB ;

edges_set : LCB (edge COMMA)* (edge)? RCB ;
var : VAR ;

var_edge : LP var COMMA var RP
         | LP var COMMA var COMMA var RP
         | LP LP var COMMA var RP COMMA var COMMA LP var COMMA var RP RP
         ;

variables : (var COMMA)* var?
     | var_edge
     ;

val : boolean
    | graph
    | edges
    | labels
    | vertices
    | boolean
    ;


boolean : BOOL;


LAMBDA : WS? 'LAMBDA' WS?;
LOAD : WS? 'LOAD' WS? ;
SET : WS? 'SET' WS? ;
ADD : WS? 'ADD' WS? ;
OF : WS? 'OF' WS? ;
TO : WS? 'TO' WS? ;
GRAPH : WS? 'GRAPH' WS?;
VERTICES : WS? 'VERTICES' WS? ;
LABELS : WS? 'LABELS' WS? ;
GET : WS? 'GET' WS? ;
EDGES : WS? 'EDGES' WS? ;
REACHABLE : WS? 'REACHABLE' WS? ;
START : WS? 'START' WS? ;
FINAL : WS? 'FINAL' WS? ;
FROM : WS? 'FROM' WS? ;
FILTER : WS? 'FILTER' WS? ;
MAP : WS? 'MAP' WS? ;
PRINT : WS? 'PRINT' WS?;
BOOL : TRUE | FALSE;
TRUE : 'TRUE' ;
FALSE : 'FALSE' ;


ASSIGN : WS? '=' WS? ;
AND : WS? '&' WS?;
OR : WS? '|' WS? ;
NOT : WS? 'not' WS? ;
IN : WS? 'in' WS?;
KLEENE : WS? '*' WS?;
DOT : WS? '.' WS? ;
COMMA : WS? ',' WS?;
SEMI : ';' WS?;
LCB : '{' WS?;
RCB : WS? '}' WS?;
LP : '(' WS?;
RP : WS? ')' ;
QUOT : '"' ;
TRIPLE_QUOT : '"""' ;
COLON : ':' ;
ARROW : '->' ;



VAR : ('_' | CHAR) ID_CHAR* ;

INT : NONZERO_DIGIT DIGIT* | '0' ;
CFG : TRIPLE_QUOT (CHAR | DIGIT | ' ' | '\n' | ARROW)* TRIPLE_QUOT ;
STRING : QUOT (CHAR | DIGIT | '_' | ' ')* QUOT ;
PATH : QUOT (CHAR | DIGIT | '_' | ' ' | '/' | DOT)* QUOT ;
ID_CHAR : (CHAR | DIGIT | '_');
CHAR : [a-z] | [A-Z];
NONZERO_DIGIT : [1-9];
DIGIT : [0-9];
WS : [ \t\r]+ -> skip;
EOL : [\n]+;
