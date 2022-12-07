safe_values = []
arbol= []
def cabecera(variable):
    file = open("spimprueba.s", "a")
    file.write(".data\n")
    valor_res = variable[::-1]
    for i in range(len(valor_res)): 
        file.write("var_"+ str(valor_res[i])+":    "".word      ""0:1" + "\n")
    file.write(".text\n")
    file.write("\nmain:\n")
    file.close()
def push():
    file = open("spimprueba.s", "a")
    file.write("\n\nsw  " + "$a0,  " + "0($sp)")
    file.write("\naddiu  " + "$sp,  " + "$sp,  " + "-4" + "\n")
def agregar_stack():
    file = open("spimprueba.s", "a")
    file.write("add  " + "$a0,  "   "$a0,  " + "$t1 \n")
    file.write("\naddiu  "  + "$sp  "+ "$sp  " + "4")
def cuerpo(variable, signo, valor):
    file = open("spimprueba.s", "a")
    valor_res = valor[::-1]
    arbol.append(valor_res)
    signo_res = signo[::-1]
    index = len(signo_res)
    index_signo = 0
    safe_values.append(variable)
    if len(signo_res) > 0:
            for j in range(len(valor_res)):
                if j == 0:
                    for  i in range(len(safe_values)):
                        if valor_res[j] == safe_values[i].lexeme: 
                            file.write("\n\nla   $t0," + "   var_"+safe_values[i].lexeme)
                            file.write("\nlw  " + "$a0," + "  0($t0)")
                            break
                    else:
                        file.write("\nli $a0,    "  + str(valor_res[j]) + "\n") 
                if  j >= 1:
                    for  i in range(len(safe_values)):
                        if valor_res[j] == safe_values[i].lexeme:
                            push()
                            file.write("\n\nla $t0, var_"+safe_values[i].lexeme)
                            file.write("\nlw  " + "$a0," + "  0($t0)")
                            break
                    else:
                        push()
                        file.write("\nli $a0,   "  + str(valor_res[j]) + "\n")
                        
                    if index_signo < index:
                        if signo_res[index_signo] == "+":
                            file.write("\nlw   " + "$t1,   "  + "4($sp) \n")
                            agregar_stack()
                            index_signo += 1

            file.write("\n\nla   " +"$t0,  " + "var_"+variable.lexeme)
            file.write("\nsw  " +"$a0,  "+ "0($t0)")
            file.close()
    else:  
        file.write("\nli $a0,    "  + str(valor_res[0]) + "\n") 
        file.write("\nla   $t0," + "   var_"+variable.lexeme)
        file.write("\nsw  " + "$a0," + "  0($t0)\n")
        file.close()
def bgt():
    file = open("spimprueba.s", "a")
    file.write("\nlw  " + "$t1,  " + " 4($sp)")
    file.write("\nadd  " + "$sp,  " + "$sp, 4")
    file.write("\nbgt  " + "$a0,  " + "$t1,  " + "label_true")
    
def blt():
    file = open("spimprueba.s", "a")
    file.write("\nlw  " + "$t1,  " + " 4($sp)")
    file.write("\nadd  " + "$sp,  " + "$sp, 4")
    file.write("\nblt  " + "$a0,  " + "$t1,  " + "label_true")
    
def condicionality(var, simbolo, asig, var2, var23):
    file = open("spimprueba.s", "a")
    print(var, simbolo, asig, var2, var23)
    for i in range(len(safe_values)):
        file.write("\n\nla $t0, var_"+safe_values[i].lexeme)
        file.write("\nlw  " + "$a0,  " + "0($t0)")
        file.write("\n\nsw  " + "$a0,  " + "0($sp)")
        file.write("\naddiu  " + "$sp,  " + "$sp,  " + "-4" + "\n")
    if len(var) > 0:
        if var2[1].isdigit():
            file.write("\nli $a0,    " + var[0] + "\n")
            if simbolo[0] == ">":
                bgt()  
            elif simbolo[0] == "<":  
                blt()
        else:
            file.write("\nli $a0,    " + var[0] + "\n")
            if simbolo[0] == ">":  
                blt()
            elif simbolo[0] == "<": 
                bgt()
    else:
        if var23[0].isdigit():
            file.write("\nli $a0,    " + var23[0] + "\n")
            if simbolo[0] == ">":  
                bgt()  
            elif simbolo[0] == "<": 
                blt()
        else:
            if simbolo[0] == ">": 
                blt()
            elif simbolo[0] == "<": 
                bgt()  
    file.close()
def comprobatysi(asig):
    file = open("spimprueba.s", "a")
    file.write("\nlabel_true:")
    for h in range(len(asig)):
        for f in range(len(safe_values)):
            if asig[h][1] == safe_values[f].lexeme:
                file.write("\nli $a0,    " + (asig[h][0]) + "\n")
                file.write("\nla   $t0," + "   var_"+safe_values[f].lexeme)
                file.write("\nsw  " + "$a0," + "  0($t0)\n")
    file.write("\n\nlabel_end:")
    file.close()
def othercondicionality(asig):
    file = open("spimprueba.s", "a")
    file.write("\n\nlabel_false:")
    for h in range(len(asig)):
        for f in range(len(safe_values)):
            if asig[h][1] == safe_values[f].lexeme:
                file.write("\nli $a0,    " + (asig[h][0]) + "\n")
                file.write("\nla   $t0," + "   var_"+safe_values[f].lexeme)
                file.write("\nsw  " + "$a0," + "  0($t0)\n")
    file.write("\nb  " + "label_end\n")
    file.close()
def funcion(valor, variable, nameFuction):
    file = open("spimprueba.s", "a")
    file.write("\nsw  " + "$fp  " + "0($sp)")
    file.write("\naddiu  " + "$sp  " + "$sp-4")
    for i in valor:
        file.write("\n\nli  " + "$a0,  " + i)
        file.write("\n\nsw  " + "$a0  " + "0($sp)")
        file.write("\naddiu  " + "$sp  " + "$sp-4")
    file.write("\n\njal  " + nameFuction[0])
    file.write("\n\nla  " + "$t0,  " + "var_"+variable)
    file.write("\nsw  " + "$a0,  " "0($t0)")
    file.write("\n\nli $v0, 1")
    file.write("\nsyscall")
    file.write("\n\nli $v0, 10")
    file.write("\nsyscall")
def funcioncuerpo(valor, signo, nombreFuncion):
    file = open("spimprueba.s", "a")
    file.write("\n\nmove  " + "$fp  " + "$sp  ")
    file.write("\n\n" + nombreFuncion + ":")
    push()
    file.write("\nlw  " + "$a0,  " + "8($sp)")
    push()
    file.write("\n\naddiu  " + "$sp,  " + "$sp,  4")
    file.write("\n\nlw  " + "$ra  " + "4($sp)\n")
    file.write("addiu  " + "$sp  " + "$sp  12\n")  
    file.write("lw  "  + "$fp  " + "0($sp)\n")
    file.write("jr  " + "$ra")
    file.close()
def finaly():
    file = open("spimprueba.s", "a")
    file.write("\n\nli $v0, 1")
    file.write("\nsyscall")
    file.write("\n\njr $ra ")
    file.close()