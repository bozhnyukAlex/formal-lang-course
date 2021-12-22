grammar GraphQueryLanguage;

program: stmt SEMI program | EPS;

stmt: var ;

var: expr | PRINT LP expr RP ;
var: STRING ;


val: INT
    | QUOT STRING QUOT
    | BOOL
    | PATH
    | LIST<INT>
    | LIST<QUOT STRING QUOT>
    | LIST<BOOL> ;

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


BOOL : TRUE | FALSE;
TRUE : 'True' ;
FALSE : 'False' ;
LOWERCASE : [a-z] ;
UPPERCASE : [A-Z] ;
STRING : ('_' | '.' LOWERCASE | UPPERCASE) ('_' | '.' | LOWERCASE | UPPERCASE | DIGIT)* ;
DIGIT : [0-9];
INT :  [1-9] DIGIT* | '0' ;
WS : [ \t\r]+ -> skip;
EOL : [\n]+;
EPS : '' ;
