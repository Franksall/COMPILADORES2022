import LL1
import Lexico
from collections import Counter
from asembly import cuerpo,cabecera,condicionality,finaly
from asembly import othercondicionality,comprobatysi,funcioncuerpo,funcion

prueba = open("code.txt")
tokens = Lexico.get_tokens(prueba)
tokens.append(['$', None, None])
root, node_list = LL1.principal(tokens)

class analizador:
    def __init__(self, lexema, tipo, categoria, funcion_padre, valor, line=None):
        self.lexema = lexema
        self.tipo = tipo
        self.categoria = categoria
        self.funcion_padre = funcion_padre
        self.line = line
        self.valor = valor
funcion5 = "def"
def identificado(root):
    stack = root.children
    arr = []
    valor = []
    signo = []
    while len(stack) > 0:
        if stack[0].symbol.symbol == "OPER":
            signo.append(stack[0].children[0].lexeme)
        if stack[0].symbol.symbol == 'TERM':
            arr.append(stack[0].children[0].symbol.symbol)
            valor.append(stack[0].children[0].lexeme)
        temp = stack[0].children
        stack.pop(0)
        for i in temp:
            stack.insert(0, i)
    ty = arr[0]

    flag = False
    for j in arr:
        if j != ty:
            flag = True
            break
    if flag:
        return "Error", valor, signo
    return ty, valor, signo
def arbol(root):
    stack = root.children
    valor_id = []
    while len(stack) > 0:
        if stack[0].symbol.symbol == 'DECLARATION':
            valor_id.append(stack[0].children[1].lexeme)
        temp = stack[0].children
        stack.pop(0)
        for i in temp:
            stack.insert(0, i)
    cabecera(valor_id)
def arbol_if(root):
    stack = root.children
    valor_id = []
    valor_oper = []
    arr = []
    while len(stack) > 0:
        if stack[0].symbol.symbol == 'TERM':
            valor_id.append(stack[0].children[0].lexeme)
        if stack[0].symbol.symbol == 'OPERCON':
            valor_oper.append(stack[0].children[0].lexeme)
        if stack[0].symbol.symbol == 'id':
            arr.append(stack[0].lexeme)
        temp = stack[0].children
        stack.pop(0)
        for i in temp:
            stack.insert(0, i)
    return valor_id, valor_oper, arr
def arbol_else(root):
    stack = root.children
    valor_id = []
    arr = []
    while len(stack) > 0:
        if stack[0].symbol.symbol == 'TERM':
            valor_id.append(stack[0].children[0].lexeme)
        if stack[0].symbol.symbol == 'id':
            arr.append(stack[0].lexeme)
        temp = stack[0].children
        stack.pop(0)
        for i in temp:
            stack.insert(0, i)
    return valor_id, arr
def buscarFunciones(root):
    stack = root.children
    nombre = []
    valor_id = []
    valor_oper = []
    valor_dec = []
    nombre.append(root.children[1].lexeme)
    while len(stack) > 0:
        if stack[0].symbol.symbol == 'TERM':
            valor_id.append(stack[0].children[0].lexeme)
        if stack[0].symbol.symbol == 'OPER':
            valor_oper.append(stack[0].children[0].lexeme)
        if stack[0].symbol.symbol == 'int':
            valor_dec.append(stack[0].lexeme)
        temp = stack[0].children
        stack.pop(0)
        for i in temp:
            stack.insert(0, i)
    return valor_dec, valor_id, valor_oper, nombre
#arbol(root)

safe_data = []
def agregar(lexema, tipo, categoria, funcion_padre, valor):
    node_symbol = analizador(lexema, tipo, categoria, funcion_padre, valor)
    safe_data.append(node_symbol)
def encontrar(lexema):
    valor = False
    for symbol in safe_data:
        if symbol.lexema == lexema:
            valor = True
    return valor

 

tuberia = []
def buscarVariables(root):
    global parametros_f, valor_f, signo_f, nombre_f
    if root.symbol.symbol == "FUNCTION":
        if encontrar(root.children[1].lexeme):
            print(" ERROR EN LINEA ->",
                root.children[1].line)
        else:
            print("FUNCION CREADA CORRECTAMENTE")
            tipo = "FUNCION"
            categoria = None
            padre = "LIBRE"
            agregar(root.children[1].lexeme, tipo, categoria, padre, None)
            parametros_f, valor_f, signo_f, nombre_f = buscarFunciones(root)
    if (root.symbol.symbol == 'DECLARATION'):
        variable = root.children[1]
        nodo_tipo = root.children[0]
        expresion, valor, signo = identificado(root)
        aux = root
        for i in (safe_data):
            for j in range(len(valor)):
                if i.lexema == valor[j]:
                    expresion = i.categoria
        while aux.symbol.symbol != 'FUNCTION':
            if aux.father == None:
                break
            aux = aux.father
        padre_asigando = "LIBRE"
        if aux.symbol.symbol == 'FUNCTION':
            padre_asigando = aux.children[1].lexeme
        else:
            if nodo_tipo.children[0].lexeme == "bool" and expresion == "BOOLEAN":
                tipo = "id"
                categoria = expresion
                padre = padre_asigando
                agregar(variable.lexeme, tipo, categoria, padre)
            elif nodo_tipo.children[0].lexeme == "int" and expresion == "num":
                tipo = "id"
                categoria = expresion
                padre = padre_asigando
                cuerpo(variable, signo, valor)
                agregar(variable.lexeme, tipo, categoria, padre, valor)
            else:
                valorG = valor_f[::-1]
                valorG = valorG[1:]
                signo_f = signo_f[::-1]
                valor_c = valor[1:]
                valor_n = valor[:1]
                valor_c = valor_c[::-1]
                if nombre_f[0] == valor[0]:
                    if len(parametros_f) == len(valor_c):
                        print("Correcto -> Funcion Ejecutada")
                        #print(valor_c, variable.lexeme, valor_n )
                        funcion(valor_c, variable.lexeme, valor_n )
                        funcioncuerpo(valorG, signo_f, nombre_f[0])
                    else:
                        print("Error -> En los valores ")
                else:
                    print("Error -> La funcion No fue llamada Correctamente")
    if root.symbol.symbol == 'ASSIGN' and root.father.symbol.symbol != 'DECLARATION' and root.father.symbol.symbol != 'FUNCTION':
        sub_valor = root.children[0]
        valor = identificado(root)
        flag = False
        for i in safe_data:
            if i.lexema == sub_valor.lexeme and i.categoria == valor[0]:
                flag = True
            elif i.lexema == sub_valor.lexeme and i.categoria != valor[0]:
                flag = True
    if root.symbol.symbol == 'IF' or root.symbol.symbol == 'ELSE':
        global tuberia
        if root.symbol.symbol == 'IF':
            aux = root
            arr_valor, arr_sim, arr_id = (arbol_if(root))
            arr_cuerpo = []
            copia2 = arr_valor[:2]
            for i in range(len(safe_data)):
                if safe_data[i].lexema == copia2[0]:
                    arr_cuerpo.append(copia2[i])
                    break
                else:
                    arr_cuerpo.append(copia2[i])
                    break
            copia = arr_valor[:2]
            arr_valor1 = arr_valor[:2]
            sub_arr = arr_valor[2:]
            sup_arr = []
            arr_id = arr_id[1:]
            sub = (list(zip(sub_arr, arr_id)))
            tuberia = sub[::-1]
            flag = 0
            con = 0
            copia3 = arr_valor[:2]

            for i in range(len(copia3)):
                if copia3[i] == arr_cuerpo[0]:
                    for t in safe_data:
                        if copia3[i] == t.lexema:
                            copia3[i] = t.valor[0]
                            print(copia3[i])

            for j in range(len(safe_data)):
                for i in arr_valor1:
                    if i == safe_data[j].lexema:
                        flag += 1
                        con += 1
                    elif i.isdigit():
                        flag += 1
                        con += 1
                        sup_arr.append(i)
                    else:
                        flag += 0
                        con += 1
            stack = aux
            valor_id = []
            arr = []
            if flag >= 1:
                condicionality(sup_arr, arr_sim, tuberia, copia, copia3)
            
        if root.symbol.symbol == 'ELSE':
            arr_valor, arr_id = (arbol_else(root))
            sub_arr = arr_valor[:]
            sup_arr = []
            arr_id = arr_id[:]
            sub = (list(zip(sub_arr, arr_id)))
            tuberia1 = sub[::-1]
            othercondicionality(tuberia1)
            comprobatysi(tuberia)

    if root.symbol.symbol == 'fin_llave' and root.father.symbol.symbol == 'FUNCTION':
        count = 0
        for i in safe_data:
            if i.funcion_padre == root.father.children[1].lexeme:
                count = count + 1
        while count > 0:
            for j in safe_data:
                if j.funcion_padre == root.father.children[1].lexeme:
                    safe_data.remove(j)
            count = count - 1

    for child in root.children:
        buscarVariables(child)

buscarVariables(root)
#finaly()

for symbol in safe_data:
    print(symbol.lexema, symbol.tipo, symbol.categoria,
        symbol.funcion_padre, symbol.valor)