
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'BOOL COLON COMMA COMMENT DOT ELSE EQUAL EX FALSE FLOAT FOR FUNC GLOBAL ID IF INT LEFTBRACKET LEFTHAT LEFTKEY LEFTPAR LIST LOGIC OBJECT PRINT RELOP RETURN RIGHTBRACKET RIGHTHAT RIGHTKEY RIGHTPAR RUN SEMICOLON START STRING TBOOL TERMS TFLOAT TINT TLIST TOBJECT TRUE TSTRING VAR VOID WHILE \n    capi : global recfunc \n         | recfunc\n    \n    global : GLOBAL COLON LEFTKEY vars RIGHTKEY SEMICOLON\n     \n    vars : VAR recvars \n     \n    recvars : recids COLON type EQUAL expression SEMICOLON vars \n            | recids COLON type EQUAL expression SEMICOLON\n            | recids COLON type SEMICOLON vars\n            | recids COLON type SEMICOLON\n     \n    recids : ID \n           | ID COMMA recids \n    \n    block : COLON LEFTKEY recstatement RIGHTKEY SEMICOLON\n          | COLON LEFTKEY RIGHTKEY SEMICOLON\n     \n    recstatement : statement recstatement  \n                 | statement  \n    \n    statement : assign SEMICOLON\n              | condition\n              | vars\n              | loop\n              | write SEMICOLON\n              | return SEMICOLON\n              | functioncall SEMICOLON\n              | nestedassign SEMICOLON\n    \n    assign : ID EQUAL expression\n     condition : IF LEFTPAR expression RIGHTPAR block \n                  | IF LEFTPAR expression RIGHTPAR block ELSE block \n     \n    loop : for\n        | while\n    \n    for : FOR LEFTPAR assign SEMICOLON expression SEMICOLON expression SEMICOLON RIGHTPAR block\n    \n    while : WHILE LEFTPAR expression RIGHTPAR block\n    \n    function : type FUNC ID LEFTPAR recparams RIGHTPAR block\n             | type FUNC ID LEFTPAR RIGHTPAR block\n             | VOID FUNC ID LEFTPAR recparams RIGHTPAR block\n             | VOID FUNC ID LEFTPAR RIGHTPAR block\n    \n    recparams : ID COLON type\n              | ID COLON type COMMA recparams\n    \n    recfunc : function recfunc\n            | function\n     \n    write : PRINT LEFTPAR recwrite RIGHTPAR \n     \n    recwrite : expression COMMA recwrite \n               | STRING COMMA recwrite \n               | expression \n               | STRING\n    \n     return : RETURN expression\n    \n    functioncall : ID LEFTPAR recfuncexp RIGHTPAR \n                 | ID LEFTPAR RIGHTPAR \n    \n    recfuncexp : expression COMMA recfuncexp\n               | expression \n    \n    expression : exp RELOP exp\n               | exp LOGIC exp\n               | exp\n     \n    exp : term recexp\n        | term \n         \n    recexp : EX exp \n     \n    term : factor recterm \n            | factor \n     \n    recterm : TERMS term\n     factor : LEFTPAR expression RIGHTPAR \n               | EX cte\n               | cte\n    \n    type : primitivetype\n        | LIST LEFTHAT primitivetype RIGHTHAT\n    \n    primitivetype : TINT\n                  | TFLOAT\n                  | TSTRING\n                  | TBOOL\n                  | TOBJECT\n    \n    listaccess : ID LEFTBRACKET expression RIGHTBRACKET SEMICOLON\n    \n    nestedvalue : ID DOT ID\n    \n    nestedassign : nestedvalue EQUAL expression\n    \n    cte : STRING \n        | ID\n        | INT\n        | FLOAT\n        | BOOL\n        | nestedvalue\n        | functioncall\n        | listaccess\n    '
    
_lr_action_items = {'GLOBAL':([0,],[4,]),'VOID':([0,2,5,39,44,47,51,53,95,121,],[7,7,7,-3,-31,-33,-30,-32,-12,-11,]),'LIST':([0,2,5,39,40,42,44,47,51,53,95,121,],[9,9,9,-3,9,9,-31,-33,-30,-32,-12,-11,]),'TINT':([0,2,5,20,39,40,42,44,47,51,53,95,121,],[10,10,10,10,-3,10,10,-31,-33,-30,-32,-12,-11,]),'TFLOAT':([0,2,5,20,39,40,42,44,47,51,53,95,121,],[11,11,11,11,-3,11,11,-31,-33,-30,-32,-12,-11,]),'TSTRING':([0,2,5,20,39,40,42,44,47,51,53,95,121,],[12,12,12,12,-3,12,12,-31,-33,-30,-32,-12,-11,]),'TBOOL':([0,2,5,20,39,40,42,44,47,51,53,95,121,],[13,13,13,13,-3,13,13,-31,-33,-30,-32,-12,-11,]),'TOBJECT':([0,2,5,20,39,40,42,44,47,51,53,95,121,],[14,14,14,14,-3,14,14,-31,-33,-30,-32,-12,-11,]),'$end':([1,3,5,15,17,44,47,51,53,95,121,],[0,-2,-37,-1,-36,-31,-33,-30,-32,-12,-11,]),'COLON':([4,32,33,34,36,38,43,46,49,144,149,158,163,],[16,40,-9,42,45,45,45,45,-10,45,45,45,45,]),'FUNC':([6,7,8,10,11,12,13,14,29,],[18,19,-60,-62,-63,-64,-65,-66,-61,]),'EQUAL':([8,10,11,12,13,14,29,48,68,74,126,133,],[-60,-62,-63,-64,-65,-66,-61,54,102,108,-68,102,]),'SEMICOLON':([8,10,11,12,13,14,29,30,48,58,60,64,65,66,67,77,78,79,80,83,84,85,86,87,88,89,90,91,94,107,114,116,119,122,124,126,131,132,136,137,138,139,140,142,145,150,155,157,161,],[-60,-62,-63,-64,-65,-66,-61,39,55,95,97,98,99,100,101,111,-50,-52,-55,-59,-70,-71,-72,-73,-74,-75,-76,-77,121,-43,-51,-54,-58,-23,-45,-68,-69,148,-48,-49,-53,-56,-57,-44,-38,157,159,-67,162,]),'COMMA':([8,10,11,12,13,14,29,33,50,78,79,80,83,84,85,86,87,88,89,90,91,114,116,119,124,125,126,129,130,136,137,138,139,140,142,157,],[-60,-62,-63,-64,-65,-66,-61,41,56,-50,-52,-55,-59,-70,-71,-72,-73,-74,-75,-76,-77,-51,-54,-58,-45,143,-68,146,147,-48,-49,-53,-56,-57,-44,-67,]),'RIGHTPAR':([8,10,11,12,13,14,27,28,29,35,37,50,78,79,80,83,84,85,86,87,88,89,90,91,93,103,114,116,118,119,123,124,125,126,127,128,129,130,134,136,137,138,139,140,142,151,153,154,157,162,],[-60,-62,-63,-64,-65,-66,36,38,-61,43,46,-34,-50,-52,-55,-59,-70,-71,-72,-73,-74,-75,-76,-77,-35,124,-51,-54,140,-58,142,-45,-47,-68,144,145,-41,-42,149,-48,-49,-53,-56,-57,-44,-46,-39,-40,-67,163,]),'LEFTHAT':([9,],[20,]),'RIGHTHAT':([10,11,12,13,14,24,],[-62,-63,-64,-65,-66,29,]),'LEFTKEY':([16,45,],[21,52,]),'ID':([18,19,26,27,28,31,41,52,54,55,56,59,61,62,63,70,71,73,81,82,92,95,97,98,99,100,101,102,103,104,105,106,108,109,110,111,112,113,115,117,120,121,135,143,146,147,148,152,156,159,160,164,],[22,23,33,34,34,-4,33,68,85,-8,34,68,-16,-17,-18,-26,-27,85,85,85,-7,-12,-15,-19,-20,-21,-22,85,85,126,85,85,85,133,85,-6,85,85,85,85,85,-11,-5,85,85,85,85,-24,-29,85,-25,-28,]),'VAR':([21,31,52,55,59,61,62,63,70,71,92,95,97,98,99,100,101,111,121,135,152,156,160,164,],[26,-4,26,26,26,-16,-17,-18,-26,-27,-7,-12,-15,-19,-20,-21,-22,26,-11,-5,-24,-29,-25,-28,]),'LEFTPAR':([22,23,54,68,69,72,73,75,76,81,85,102,103,105,106,108,110,112,113,115,117,120,143,146,147,148,159,],[27,28,81,103,105,106,81,109,110,81,103,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,]),'RIGHTKEY':([25,31,52,55,57,59,61,62,63,70,71,92,95,96,97,98,99,100,101,111,121,135,152,156,160,164,],[30,-4,58,-8,94,-14,-16,-17,-18,-26,-27,-7,-12,-13,-15,-19,-20,-21,-22,-6,-11,-5,-24,-29,-25,-28,]),'IF':([31,52,55,59,61,62,63,70,71,92,95,97,98,99,100,101,111,121,135,152,156,160,164,],[-4,69,-8,69,-16,-17,-18,-26,-27,-7,-12,-15,-19,-20,-21,-22,-6,-11,-5,-24,-29,-25,-28,]),'PRINT':([31,52,55,59,61,62,63,70,71,92,95,97,98,99,100,101,111,121,135,152,156,160,164,],[-4,72,-8,72,-16,-17,-18,-26,-27,-7,-12,-15,-19,-20,-21,-22,-6,-11,-5,-24,-29,-25,-28,]),'RETURN':([31,52,55,59,61,62,63,70,71,92,95,97,98,99,100,101,111,121,135,152,156,160,164,],[-4,73,-8,73,-16,-17,-18,-26,-27,-7,-12,-15,-19,-20,-21,-22,-6,-11,-5,-24,-29,-25,-28,]),'FOR':([31,52,55,59,61,62,63,70,71,92,95,97,98,99,100,101,111,121,135,152,156,160,164,],[-4,75,-8,75,-16,-17,-18,-26,-27,-7,-12,-15,-19,-20,-21,-22,-6,-11,-5,-24,-29,-25,-28,]),'WHILE':([31,52,55,59,61,62,63,70,71,92,95,97,98,99,100,101,111,121,135,152,156,160,164,],[-4,76,-8,76,-16,-17,-18,-26,-27,-7,-12,-15,-19,-20,-21,-22,-6,-11,-5,-24,-29,-25,-28,]),'EX':([54,73,79,80,81,83,84,85,86,87,88,89,90,91,102,103,105,106,108,110,112,113,115,116,117,119,120,124,126,130,139,140,142,143,146,147,148,157,159,],[82,82,115,-55,82,-59,-70,-71,-72,-73,-74,-75,-76,-77,82,82,82,82,82,82,82,82,82,-54,82,-58,82,-45,-68,-70,-56,-57,-44,82,82,82,82,-67,82,]),'STRING':([54,73,81,82,102,103,105,106,108,110,112,113,115,117,120,143,146,147,148,159,],[84,84,84,84,84,84,84,130,84,84,84,84,84,84,84,84,130,130,84,84,]),'INT':([54,73,81,82,102,103,105,106,108,110,112,113,115,117,120,143,146,147,148,159,],[86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,]),'FLOAT':([54,73,81,82,102,103,105,106,108,110,112,113,115,117,120,143,146,147,148,159,],[87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,]),'BOOL':([54,73,81,82,102,103,105,106,108,110,112,113,115,117,120,143,146,147,148,159,],[88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,]),'DOT':([68,85,],[104,104,]),'RELOP':([78,79,80,83,84,85,86,87,88,89,90,91,114,116,119,124,126,130,138,139,140,142,157,],[112,-52,-55,-59,-70,-71,-72,-73,-74,-75,-76,-77,-51,-54,-58,-45,-68,-70,-53,-56,-57,-44,-67,]),'LOGIC':([78,79,80,83,84,85,86,87,88,89,90,91,114,116,119,124,126,130,138,139,140,142,157,],[113,-52,-55,-59,-70,-71,-72,-73,-74,-75,-76,-77,-51,-54,-58,-45,-68,-70,-53,-56,-57,-44,-67,]),'RIGHTBRACKET':([78,79,80,83,84,85,86,87,88,89,90,91,114,116,119,124,126,136,137,138,139,140,141,142,157,],[-50,-52,-55,-59,-70,-71,-72,-73,-74,-75,-76,-77,-51,-54,-58,-45,-68,-48,-49,-53,-56,-57,150,-44,-67,]),'TERMS':([80,83,84,85,86,87,88,89,90,91,119,124,126,130,140,142,157,],[117,-59,-70,-71,-72,-73,-74,-75,-76,-77,-58,-45,-68,-70,-57,-44,-67,]),'LEFTBRACKET':([85,],[120,]),'ELSE':([95,121,152,],[-12,-11,158,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'capi':([0,],[1,]),'global':([0,],[2,]),'recfunc':([0,2,5,],[3,15,17,]),'function':([0,2,5,],[5,5,5,]),'type':([0,2,5,40,42,],[6,6,6,48,50,]),'primitivetype':([0,2,5,20,40,42,],[8,8,8,24,8,8,]),'vars':([21,52,55,59,111,],[25,62,92,62,135,]),'recvars':([26,],[31,]),'recids':([26,41,],[32,49,]),'recparams':([27,28,56,],[35,37,93,]),'block':([36,38,43,46,144,149,158,163,],[44,47,51,53,152,156,160,164,]),'recstatement':([52,59,],[57,96,]),'statement':([52,59,],[59,59,]),'assign':([52,59,109,],[60,60,132,]),'condition':([52,59,],[61,61,]),'loop':([52,59,],[63,63,]),'write':([52,59,],[64,64,]),'return':([52,59,],[65,65,]),'functioncall':([52,54,59,73,81,82,102,103,105,106,108,110,112,113,115,117,120,143,146,147,148,159,],[66,90,66,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,]),'nestedassign':([52,59,],[67,67,]),'for':([52,59,],[70,70,]),'while':([52,59,],[71,71,]),'nestedvalue':([52,54,59,73,81,82,102,103,105,106,108,110,112,113,115,117,120,143,146,147,148,159,],[74,89,74,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,]),'expression':([54,73,81,102,103,105,106,108,110,120,143,146,147,148,159,],[77,107,118,122,125,127,129,131,134,141,125,129,129,155,161,]),'exp':([54,73,81,102,103,105,106,108,110,112,113,115,120,143,146,147,148,159,],[78,78,78,78,78,78,78,78,78,136,137,138,78,78,78,78,78,78,]),'term':([54,73,81,102,103,105,106,108,110,112,113,115,117,120,143,146,147,148,159,],[79,79,79,79,79,79,79,79,79,79,79,79,139,79,79,79,79,79,79,]),'factor':([54,73,81,102,103,105,106,108,110,112,113,115,117,120,143,146,147,148,159,],[80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,]),'cte':([54,73,81,82,102,103,105,106,108,110,112,113,115,117,120,143,146,147,148,159,],[83,83,83,119,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,]),'listaccess':([54,73,81,82,102,103,105,106,108,110,112,113,115,117,120,143,146,147,148,159,],[91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,]),'recexp':([79,],[114,]),'recterm':([80,],[116,]),'recfuncexp':([103,143,],[123,151,]),'recwrite':([106,146,147,],[128,153,154,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> capi","S'",1,None,None,None),
  ('capi -> global recfunc','capi',2,'p_capi','capi.py',117),
  ('capi -> recfunc','capi',1,'p_capi','capi.py',118),
  ('global -> GLOBAL COLON LEFTKEY vars RIGHTKEY SEMICOLON','global',6,'p_global','capi.py',123),
  ('vars -> VAR recvars','vars',2,'p_vars','capi.py',128),
  ('recvars -> recids COLON type EQUAL expression SEMICOLON vars','recvars',7,'p_recvars','capi.py',133),
  ('recvars -> recids COLON type EQUAL expression SEMICOLON','recvars',6,'p_recvars','capi.py',134),
  ('recvars -> recids COLON type SEMICOLON vars','recvars',5,'p_recvars','capi.py',135),
  ('recvars -> recids COLON type SEMICOLON','recvars',4,'p_recvars','capi.py',136),
  ('recids -> ID','recids',1,'p_recids','capi.py',141),
  ('recids -> ID COMMA recids','recids',3,'p_recids','capi.py',142),
  ('block -> COLON LEFTKEY recstatement RIGHTKEY SEMICOLON','block',5,'p_block','capi.py',147),
  ('block -> COLON LEFTKEY RIGHTKEY SEMICOLON','block',4,'p_block','capi.py',148),
  ('recstatement -> statement recstatement','recstatement',2,'p_recstatement','capi.py',153),
  ('recstatement -> statement','recstatement',1,'p_recstatement','capi.py',154),
  ('statement -> assign SEMICOLON','statement',2,'p_statement','capi.py',159),
  ('statement -> condition','statement',1,'p_statement','capi.py',160),
  ('statement -> vars','statement',1,'p_statement','capi.py',161),
  ('statement -> loop','statement',1,'p_statement','capi.py',162),
  ('statement -> write SEMICOLON','statement',2,'p_statement','capi.py',163),
  ('statement -> return SEMICOLON','statement',2,'p_statement','capi.py',164),
  ('statement -> functioncall SEMICOLON','statement',2,'p_statement','capi.py',165),
  ('statement -> nestedassign SEMICOLON','statement',2,'p_statement','capi.py',166),
  ('assign -> ID EQUAL expression','assign',3,'p_assign','capi.py',171),
  ('condition -> IF LEFTPAR expression RIGHTPAR block','condition',5,'p_condition','capi.py',175),
  ('condition -> IF LEFTPAR expression RIGHTPAR block ELSE block','condition',7,'p_condition','capi.py',176),
  ('loop -> for','loop',1,'p_loop','capi.py',181),
  ('loop -> while','loop',1,'p_loop','capi.py',182),
  ('for -> FOR LEFTPAR assign SEMICOLON expression SEMICOLON expression SEMICOLON RIGHTPAR block','for',10,'p_for','capi.py',186),
  ('while -> WHILE LEFTPAR expression RIGHTPAR block','while',5,'p_while','capi.py',190),
  ('function -> type FUNC ID LEFTPAR recparams RIGHTPAR block','function',7,'p_function','capi.py',195),
  ('function -> type FUNC ID LEFTPAR RIGHTPAR block','function',6,'p_function','capi.py',196),
  ('function -> VOID FUNC ID LEFTPAR recparams RIGHTPAR block','function',7,'p_function','capi.py',197),
  ('function -> VOID FUNC ID LEFTPAR RIGHTPAR block','function',6,'p_function','capi.py',198),
  ('recparams -> ID COLON type','recparams',3,'p_recparams','capi.py',203),
  ('recparams -> ID COLON type COMMA recparams','recparams',5,'p_recparams','capi.py',204),
  ('recfunc -> function recfunc','recfunc',2,'p_recfunc','capi.py',208),
  ('recfunc -> function','recfunc',1,'p_recfunc','capi.py',209),
  ('write -> PRINT LEFTPAR recwrite RIGHTPAR','write',4,'p_write','capi.py',214),
  ('recwrite -> expression COMMA recwrite','recwrite',3,'p_recwrite','capi.py',219),
  ('recwrite -> STRING COMMA recwrite','recwrite',3,'p_recwrite','capi.py',220),
  ('recwrite -> expression','recwrite',1,'p_recwrite','capi.py',221),
  ('recwrite -> STRING','recwrite',1,'p_recwrite','capi.py',222),
  ('return -> RETURN expression','return',2,'p_return','capi.py',227),
  ('functioncall -> ID LEFTPAR recfuncexp RIGHTPAR','functioncall',4,'p_functioncall','capi.py',232),
  ('functioncall -> ID LEFTPAR RIGHTPAR','functioncall',3,'p_functioncall','capi.py',233),
  ('recfuncexp -> expression COMMA recfuncexp','recfuncexp',3,'p_recfuncexp','capi.py',238),
  ('recfuncexp -> expression','recfuncexp',1,'p_recfuncexp','capi.py',239),
  ('expression -> exp RELOP exp','expression',3,'p_expression','capi.py',244),
  ('expression -> exp LOGIC exp','expression',3,'p_expression','capi.py',245),
  ('expression -> exp','expression',1,'p_expression','capi.py',246),
  ('exp -> term recexp','exp',2,'p_exp','capi.py',251),
  ('exp -> term','exp',1,'p_exp','capi.py',252),
  ('recexp -> EX exp','recexp',2,'p_recexp','capi.py',257),
  ('term -> factor recterm','term',2,'p_term','capi.py',262),
  ('term -> factor','term',1,'p_term','capi.py',263),
  ('recterm -> TERMS term','recterm',2,'p_recterm','capi.py',268),
  ('factor -> LEFTPAR expression RIGHTPAR','factor',3,'p_factor','capi.py',272),
  ('factor -> EX cte','factor',2,'p_factor','capi.py',273),
  ('factor -> cte','factor',1,'p_factor','capi.py',274),
  ('type -> primitivetype','type',1,'p_type','capi.py',279),
  ('type -> LIST LEFTHAT primitivetype RIGHTHAT','type',4,'p_type','capi.py',280),
  ('primitivetype -> TINT','primitivetype',1,'p_primitivetype','capi.py',285),
  ('primitivetype -> TFLOAT','primitivetype',1,'p_primitivetype','capi.py',286),
  ('primitivetype -> TSTRING','primitivetype',1,'p_primitivetype','capi.py',287),
  ('primitivetype -> TBOOL','primitivetype',1,'p_primitivetype','capi.py',288),
  ('primitivetype -> TOBJECT','primitivetype',1,'p_primitivetype','capi.py',289),
  ('listaccess -> ID LEFTBRACKET expression RIGHTBRACKET SEMICOLON','listaccess',5,'p_listaccess','capi.py',294),
  ('nestedvalue -> ID DOT ID','nestedvalue',3,'p_nestedvalue','capi.py',299),
  ('nestedassign -> nestedvalue EQUAL expression','nestedassign',3,'p_nestedassign','capi.py',304),
  ('cte -> STRING','cte',1,'p_cte','capi.py',309),
  ('cte -> ID','cte',1,'p_cte','capi.py',310),
  ('cte -> INT','cte',1,'p_cte','capi.py',311),
  ('cte -> FLOAT','cte',1,'p_cte','capi.py',312),
  ('cte -> BOOL','cte',1,'p_cte','capi.py',313),
  ('cte -> nestedvalue','cte',1,'p_cte','capi.py',314),
  ('cte -> functioncall','cte',1,'p_cte','capi.py',315),
  ('cte -> listaccess','cte',1,'p_cte','capi.py',316),
]
