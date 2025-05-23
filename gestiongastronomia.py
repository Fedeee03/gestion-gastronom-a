import sqlite3
conectarbase=sqlite3.connect("BBDD_Gestion_De_Costos_Menú.db")
cursor=conectarbase.cursor()
#---------------------------------------------------------------Creacion de las tablas de la base de datos-------------------------------------------------------------
cursor.execute("CREATE TABLE IF NOT EXISTS MATERIAS_PRIMAS(Codigo INTEGER PRIMARY KEY AUTOINCREMENT,Nombre VARCHAR(20),Unidad_De_Medida VARCHAR(5),Costo_por_Medida INTEGER,Tipo VARCHAR(2))")
cursor.execute("CREATE TABLE IF NOT EXISTS MENU(Codigo INTEGER PRIMARY KEY AUTOINCREMENT,Nombre VARCHAR(20),Tipo VARCHAR(2),Cantidad_Producida NUMBER(3))")
cursor.execute("CREATE TABLE IF NOT EXISTS COSTEO(Codigo_Menu VARCHAR(3),Codigo_Materia_Prima VARCHAR(20),Cantidad INTEGER)")
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def menus(op):#Funcion universal para todos los menús
    global a,ban,e,v1,v2
    while True:
        d=len(op)
        print("╔═══════════════════════════════════════════════════════╗")
        print("Seleccione una de estas opciones:")
        for i in range (d):
            print(i,"-",op[i])
        print("╚═══════════════════════════════════════════════════════╝")
        try:
            a=int(input("Ingrese su elección: "))
            if a<0 or a>d-1:
                print("La eleccion debe de ser valida, ingrese el numero de la opcion a elegir")
                break
            break
        except ValueError:
            print("La elección debe ser un número")
while True:
    menus(["Salir","Materias Primas","Menu"])
    eleccion1=a
    if eleccion1==0:
        conectarbase.close()
        break
    if eleccion1==1:#MATERIAS PRIMAS
        while True:
            menus(["Atras","Cargar una nueva Materia Prima","Modificar una Materia Prima","Listado de Materias Primas","Consulta de Materias Primas","Dar de Baja una Materia Prima"])
            eleccion2=a
            if eleccion2==0:
                  break
            if eleccion2==1:#CARGA MATERIAS PRIMAS
                  while True:
                        n=input("Ingrese el nombre de la materia prima(S para salir): ")
                        n=n.lower()
                        if n=="s":
                            break
                        cursor.execute("SELECT * FROM MATERIAS_PRIMAS WHERE Nombre=?",(n,))
                        validar=cursor.fetchall()
                        if len(validar)>0:
                            print("Materia prima ya cargada")
                        else:
                            u=input("Ingrese la unidad de medida(kg,lt,unidad): ")
                            u=u.lower()
                            while u!='kg' and u!='lt' and u!='unidad':
                                u=input("Ingrese la unidad de medida(kg,lt,unidad): ")
                                u=u.lower()
                            t=input("Ingrese si es Materia Prima o Materia Elaborada(MP/ME): ")
                            t=t.upper()
                            while t!="MP" and t!="ME":
                                print("Formato MP o ME")
                                t=input("Ingrese si es Materia Prima o Materia Elaborada(MP/ME): ")
                                t=t.upper()
                            if t=="MP":
                                v=int(input("Ingrese el costo por unidad: "))
                                añadir=[(n),(u),(v),(t)]
                                print("{:<10}{}\n{:<10}{}\n{:<10}{}\n{:<10}{}".format("Nombre:", n, "Unidad:", u, "Costo:", v, "Tipo:", t))
                                conf=input("Desea cargar estos datos?(S/N): ")
                                conf=conf.lower()
                                while conf != 's' and conf != 'n':
                                    print("Debe ingresar S o N")
                                    conf=input("Desea cargar estos datos?(S/N): ")
                                    conf=conf.lower()
                                if conf=='s':
                                    cursor.execute("INSERT INTO MATERIAS_PRIMAS VALUES(null,?,?,?,?)",añadir)
                                    conectarbase.commit()
                                    print("Materia Prima Cargada")
                                else:
                                    print("Materia Prima No Cargada")
                            else:
                                #ACA AGREGAMOS LAS CANTIDADES DE INGREDIENTES QUE NECESITA LA MATERIA ELABORADA ADENTRO DE LA TABLA DE COSTEOS
                                añadir=[(n),(u),(t)]
                                lista1=[]
                                lista2=[]
                                lista3=[]
                                cursor.execute("SELECT * FROM MATERIAS_PRIMAS")
                                Validacion=cursor.fetchall()
                                if len(Validacion)<2:
                                    print("Debe tener como minimo 2 ingredientes cargados")
                                    break
                                print("Enliste que materias primas utiliza,\nsi ya cargo todas las materias primas ingrese 0: ")
                                while True:
                                    ingrediente=input("Nombre de la Materia Prima: ")
                                    if ingrediente!="0":
                                        ingrediente=ingrediente.lower()
                                        cursor.execute("SELECT * FROM MATERIAS_PRIMAS WHERE Nombre=?",(ingrediente,))
                                        validar=cursor.fetchall()
                                        if len(validar)==0:
                                            print("Materia prima no encontrada")
                                        else:
                                            cantidad=float(input("Cantidad de "+ingrediente.capitalize()+": "))
                                            while cantidad<=0:
                                                cantidad=float(input("Cantidad de "+ingrediente.capitalize()+": "))
                                            lista1.append(ingrediente)
                                            lista2.append(validar[0][0])
                                            lista3.append(cantidad)
                                    else:
                                        if len(lista1)<2:
                                            print("Toda receta debe contar con mas de una materia prima")
                                            break
                                        print("Confirmacion de materias primas:")
                                        for i in range(len(lista1)):
                                            print(lista1[i])
                                        ele=input("Ingrese S/N: ")
                                        ele=ele.upper()
                                        while ele!="S" and ele!="N":
                                            ele=input("Ingrese S/N: ")
                                            ele=ele.upper()
                                        if ele=="S":
                                            cant=float(input("Ingrese la cantidad de produccion final(en kilos): "))
                                            while cant<=0:
                                                cant=float(input("Ingrese la cantidad de produccion final(en kilos): "))
                                            cursor.execute("INSERT INTO MENU VALUES (null,?,?,?)",(n,"ME",cant))
                                            cursor.execute("SELECT Codigo FROM MENU WHERE Nombre=?",(n,))
                                            cod_menu=cursor.fetchall()
                                            cod_menu=cod_menu[0][0]
                                            print("Ingrese la cantidad de cada materia prima a usar")
                                            for i in range(len(lista1)):
                                                cursor.execute("INSERT INTO COSTEO VALUES (?,?,?)",(cod_menu,lista2[i],lista3[i]))
                                                conectarbase.commit()
                                            print("Receta Cargada")
                                            cursor.execute("INSERT INTO MATERIAS_PRIMAS VALUES(null,?,?,null,?)",añadir)
                                            conectarbase.commit()
                                            break
                                        if ele=="N":
                                            print("Receta No Cargada")
                                            break
            if eleccion2==2:#MODIFICACION DE MATERIAS PRIMAS
                while True:
                    n=input("Ingrese el nombre de la materia prima(S para salir): ")
                    n=n.lower()
                    if n=="s":
                        break
                    cursor.execute("SELECT * FROM MATERIAS_PRIMAS WHERE Nombre=?",(n,))
                    consulta=cursor.fetchall()
                    if len(consulta)==0:
                        print("Materia Prima no encontrada")
                    print("Elija que desea cambiar")
                    if consulta[0][4]=="ME":
                        menus(["Atras","Nombre: "+str(consulta[0][1]),"Unidad de Medida: "+str(consulta[0][2]),"Costo: ---"])
                    else:
                        menus(["Atras","Nombre: "+str(consulta[0][1]),"Unidad de Medida: "+str(consulta[0][2]),"Costo: "+str(consulta[0][3])])
                    cambio=str(a)
                    if cambio=="0":
                        break
                    if cambio=="1":
                        n2=input("Ingrese el nuevo nombre: ")
                        conf=input("{} --> {}\nConfirma el cambio (S o N)?: ".format(consulta[0][1], n2))
                        conf=conf.lower()
                        while conf!="s" and conf!="n":
                            conf=input("{} --> {}\nConfirma el cambio (S o N)?: ".format(consulta[0][1], n2))
                            conf=conf.lower()
                        if conf=="s":
                            cursor.execute("UPDATE MATERIAS_PRIMAS SET Nombre=? WHERE Nombre=?",(n2,n))
                            conectarbase.commit()
                            print("Nombre cambiado")
                        else:
                            print("No se cambio el nombre")
                    if cambio=="2":
                        u2=input("Ingrese la unidad de medida(kg,lt,unidad): ")
                        u2=u2.lower()
                        while u2!='kg' and u2!='lt' and u2!='unidad':
                            u2=input("Ingrese la unidad de medida(kg,lt,unidad): ")
                            u2=u2.lower()
                        conf=input("{} --> {}\nConfirma el cambio (S o N)?: ".format(consulta[0][2], u2))
                        conf=conf.lower()
                        while conf!="s" and conf!="n":
                            conf=input("{} --> {}\nConfirma el cambio (S o N)?: ".format(consulta[0][2], u2))
                            conf=conf.lower()
                        if conf=="s":
                            cursor.execute("UPDATE MATERIAS_PRIMAS SET Unidad_De_Medida=? WHERE Nombre=?",(u2,n))
                            conectarbase.commit()
                            print("Unidad de Medida cambiada")
                        else:
                            print("No se cambio la unidad de Medida")
                    if cambio=="3":
                        if consulta[0][4]=="ME":
                            print("No se puede cambiar el costo de una materia elaborada")
                        else:
                            v2=int(input("Ingrese el nuevo costo: "))
                            conf=input("{} --> {}\nConfirma el cambio (S o N)?: ".format(consulta[0][3], v2))
                            conf=conf.lower()
                            while conf!="s" and conf!="n":
                                conf=input("{} --> {}\nConfirma el cambio (S o N)?: ".format(consulta[0][3], v2))
                                conf=conf.lower()
                            if conf=="s":
                                cursor.execute("UPDATE MATERIAS_PRIMAS SET Costo_por_Medida=? WHERE Nombre=?",(v2,n))
                                conectarbase.commit()
                                print("Costo cambiado")
                            else:
                                print("No se cambio el costo")
            if eleccion2==3:#LISTADO DE MATERIAS PRIMAS
                cursor.execute("SELECT * FROM MATERIAS_PRIMAS")
                consulta=cursor.fetchall()
                ban=0
                ban2=0
                print("{:<8} {:<15} {:<10} {:<15} {:<8}".format("ID", "Nombre", "Unidad", "Precio", "Tipo"))
                print("-" * 55)
                for fila in consulta:
                    cantidad_producida=0
                    if str(fila[4])=="ME":
                        cursor.execute("SELECT Codigo FROM MENU WHERE Nombre=?",(fila[1],))
                        codigo_menu=cursor.fetchall()
                        codigo_menu=codigo_menu[0][0]
                        cursor.execute("SELECT * FROM COSTEO WHERE Codigo_Menu=?",(codigo_menu,))
                        listado=cursor.fetchall()
                        v_me=0
                        for b in range(len(listado)):
                            cursor.execute("SELECT Costo_por_Medida FROM MATERIAS_PRIMAS WHERE Codigo=?",(listado[b][1],))
                            costo_medida=cursor.fetchall()
                            costo=int(costo_medida[0][0])*(listado[b][2])
                            v_me+=costo
                        cursor.execute("SELECT Cantidad_Producida FROM MENU WHERE Codigo=?",(str(codigo_menu)),)
                        cantidad_producida=cursor.fetchall()
                    if cantidad_producida==0:
                        print("{:<8} {:<15} {:<10} {:<15} {:<8}".format(fila[0], fila[1], fila[2], fila[3] if fila[3] is not None else "N/A", fila[4]))
                    else:
                        print("{:<8} {:<15} {:<10} ${:<14.2f} {:<8}".format(fila[0], fila[1], fila[2], v_me, fila[4]))          
            if eleccion2==4:#CONSULTA DE MATERIAS PRIMAS
                while True:
                    n=input("Ingrese el nombre de la materia prima(S para salir): ")
                    n=n.lower()
                    if n=="s":
                        break
                    cursor.execute("SELECT * FROM MATERIAS_PRIMAS WHERE Nombre=?",(n,))
                    consulta=cursor.fetchall()
                    if len(consulta)==0:
                        print("Materia Prima no encontrada")
                    else:
                        consulta=consulta[0]
                        if consulta[4]=="MP":
                            print("{:<8} {:<20} {:<20} {:<20} {:<5}".format("Codigo", "Nombre", "Unidad de medida", "Costo por medida", "Tipo"))
                            print("-" * 75)
                            print("{:<8} {:<20} {:<20} {:<20} {:<5}".format(consulta[0],consulta[1],consulta[2],consulta[3],consulta[4]))
                        else:
                            print("{:<8} {:<20} {:<20} {:<20} {:<5}".format("Codigo", "Nombre", "Unidad de medida", "Costo de Produccion", "Tipo"))
                            print("-" * 75)
                            print("{:<8} {:<20} {:<20} {:<20} {:<5}".format(consulta[0],consulta[1],consulta[2],consulta[3] if consulta[3] is not None else "N/A",consulta[4]))
                       
            if eleccion2==5:#BORRAR MATERIA PRIMA
                while True:
                    n=input("Ingrese el nombre de la materia prima que quiera dar de baja(S para salir): ")
                    n=n.lower()
                    if n=="s":
                        break
                    cursor.execute("SELECT * FROM MATERIAS_PRIMAS WHERE Nombre=?",(n,))
                    consulta=cursor.fetchall()
                    if len(consulta)==0:
                        print("Materia Prima no encontrada")
                    else:
                        print("¿Está seguro que quiere dar de baja la materia prima?")
                        fila=consulta[0]
                        print("{:<8} {:<15} {:<10} {:<15} {:<5}".format("Codigo", "Nombre", "Unidad", "Costo", "Tipo"))
                        print("{:<8} {:<15} {:<10} {:<15} {:<5}".format(fila[0], fila[1], fila[2], fila[3] if fila[3] is not None else "N/A", fila[4]))
                        seguir=input("S o N: ")
                        seguir=seguir.lower()
                        while seguir!="s" and seguir!="n":
                            seguir=input("S o N: ")
                        if seguir=="s":
                            cursor.execute("SELECT * FROM COSTEO WHERE Codigo_Materia_Prima=?",(consulta[0][0],))
                            consulta2=cursor.fetchall()
                            if len(consulta2)==0:
                                cursor.execute("DELETE FROM MATERIAS_PRIMAS WHERE Nombre=?",(n,))
                                conectarbase.commit()
                                print("Materia Prima dada de baja")
                            else:
                                print("No se puede dar de baja la materia prima porque está siendo utilizada en una receta")
                        else:
                            print("Materia prima No dada de Baja")
    if eleccion1==2:#MENU
        while True:
            menus(["Atras","Ver Menu","Cargar Plato","Modificar Plato","Borrar Plato"])
            eleccion2=a
            if eleccion2==0:
                break
            if eleccion2==1:#CONSULTA MENU
                respuesta=input("Elija el tipo de consulta:\n0- Atras\n1- Menu Completo(Listado)\n2-Receta Especifica(Filtrado)")
                if respuesta=="0":
                    break
                while respuesta!="1" and respuesta!="2":
                    respuesta=input("Elija el tipo de consulta:\n1- Menu Completo(Listado)\n2-Receta Especifica(Filtrado)\nAqui: ")
                if respuesta=="1":
                    cursor.execute("SELECT * FROM MENU WHERE TIPO=?",("RE",))
                    consulta=cursor.fetchall()
                    for i in range (len(consulta)):
                        cursor.execute("SELECT * FROM COSTEO WHERE Codigo_Menu=?",(consulta[i][0],))
                        materias_primas=cursor.fetchall()
                        if len(materias_primas)!=0:
                            a=0
                            cantidad_me=0
                            for z in range (len(materias_primas)):
                                cursor.execute("SELECT * FROM MATERIAS_PRIMAS WHERE Codigo=?",(materias_primas[z][1],))
                                tipo=cursor.fetchall()
                                if tipo[0][4]=="MP":
                                    cursor.execute("SELECT Costo_por_Medida FROM MATERIAS_PRIMAS WHERE Codigo=?",(materias_primas[z][1],))
                                    costo_medida=cursor.fetchall()
                                    costo=int(costo_medida[0][0])*(materias_primas[z][2])
                                    a+=costo
                                else:
                                    cursor.execute("SELECT Codigo FROM MENU WHERE Nombre=?",(tipo[0][1],))
                                    codigo_menu=cursor.fetchall()
                                    cursor.execute("SELECT * FROM COSTEO WHERE Codigo_Menu=?",(codigo_menu[0][0],))
                                    listado=cursor.fetchall()
                                    v_me=0
                                    for b in range(len(listado)):
                                        cursor.execute("SELECT Costo_por_Medida FROM MATERIAS_PRIMAS WHERE Codigo=?",(listado[b][1],))
                                        costo_medida=cursor.fetchall()
                                        costo=int(costo_medida[0][0])*(listado[b][2])
                                        v_me+=costo
                                    cursor.execute("SELECT Cantidad FROM COSTEO WHERE Codigo_Menu=? AND Codigo_Materia_Prima=?",(materias_primas[0][0],materias_primas[0][1]))
                                    cantidad_me=cursor.fetchall()
                                    cursor.execute("SELECT Cantidad_Producida FROM MENU WHERE Codigo=?",(str(codigo_menu[0][0])),)
                                    cantidad_producida=cursor.fetchall()
                            if cantidad_me==0:
                                print("{:<8} {:<15} {:<10} {:<15} {:<10}".format("Codigo", "Nombre", "Tipo", "Cant. Producida", "Precio"))
                                print("{:<8} {:<15} {:<10} {:<15} ${:<10.2f}".format(consulta[i][0], consulta[i][1], consulta[i][2], consulta[i][3] if consulta[i][3] is not None else "N/A", a))
                            else:
                                cursor.execute("SELECT * FROM COSTEO WHERE Codigo_Menu=?",(str(codigo_menu[0][0]),))
                                v_me_ca=cantidad_me[0][0]*v_me/float(cantidad_producida[0][0])
                                a+=v_me_ca
                                print("{:<8} {:<15} {:<10} {:<5} {:<10}".format("Codigo", "Nombre", "Unidad", "Tipo", "Precio"))
                                print("{:<8} {:<15} {:<10} {:<5} ${:<10.2f}".format(consulta[i][0], consulta[i][1], consulta[i][2], consulta[i][3] if consulta[i][3] is not None else "N/A", a))
                else:
                    n=input("Ingrese el nombre de la receta: ")
                    n=n.lower()
                    cursor.execute("SELECT * FROM MENU WHERE NOMBRE=? AND TIPO=?",(n,"RE"))
                    consulta=cursor.fetchall()
                    if len(consulta)==0:
                        print("No se encontraron recetas con ese nombre")
                    else:
                        nombres=[]
                        costos=[]
                        cantidades=[]
                        for i in range (len(consulta)):
                            cursor.execute("SELECT * FROM COSTEO WHERE Codigo_Menu=?",(consulta[i][0],))
                            materias_primas=cursor.fetchall()
                            if len(materias_primas)==0:
                                pass
                            else:
                                a=0
                                cantidad_me=0
                                for z in range (len(materias_primas)):
                                    cursor.execute("SELECT * FROM MATERIAS_PRIMAS WHERE Codigo=?",(materias_primas[z][1],))
                                    tipo=cursor.fetchall()
                                    if tipo[0][4]=="MP":
                                        cursor.execute("SELECT Costo_por_Medida FROM MATERIAS_PRIMAS WHERE Codigo=?",(materias_primas[z][1],))
                                        costo_medida=cursor.fetchall()
                                        costo=int(costo_medida[0][0])*(materias_primas[z][2])
                                        a+=costo
                                        cursor.execute("SELECT Nombre FROM MATERIAS_PRIMAS WHERE Codigo=?",(materias_primas[z][1],))
                                        nombre=cursor.fetchall()
                                        nombres.append(nombre[0][0])
                                        costos.append(costo)
                                        cantidades.append(materias_primas[z][2])
                                    else:
                                        cursor.execute("SELECT Codigo FROM MENU WHERE Nombre=?",(tipo[0][1],))
                                        codigo_menu=cursor.fetchall()
                                        cursor.execute("SELECT * FROM COSTEO WHERE Codigo_Menu=?",(codigo_menu[0][0],))
                                        listado=cursor.fetchall()
                                        v_me=0
                                        for b in range(len(listado)):
                                            cursor.execute("SELECT Costo_por_Medida FROM MATERIAS_PRIMAS WHERE Codigo=?",(listado[b][1],))
                                            costo_medida=cursor.fetchall()
                                            costo=int(costo_medida[0][0])*(listado[b][2])
                                            v_me+=costo
                                        cursor.execute("SELECT Cantidad FROM COSTEO WHERE Codigo_Menu=? AND Codigo_Materia_Prima=?",(materias_primas[0][0],materias_primas[0][1]))
                                        cantidad_me=cursor.fetchall()
                                        cursor.execute("SELECT Cantidad_Producida FROM MENU WHERE Codigo=?",(str(codigo_menu[0][0])),)
                                        cantidad_producida=cursor.fetchall()
                                        cursor.execute("SELECT Nombre FROM MATERIAS_PRIMAS WHERE Codigo=?",(materias_primas[z][1],))
                                        nombre=cursor.fetchall()
                                        nombres.append(nombre[0][0])
                                        v_me_ca=cantidad_me[0][0]*v_me/float(cantidad_producida[0][0])
                                        costos.append(v_me_ca)
                                        cantidades.append(cantidad_producida[0][0])
                                if cantidad_me==0:
                                    print("{:<8} {:<15} {:<10} {:<5} {:<10}".format("Codigo", "Nombre", "Unidad", "Tipo", "Precio"))
                                    print("{:<8} {:<15} {:<10} {:<5} ${:<10.2f}".format(consulta[i][0], consulta[i][1], consulta[i][2], consulta[i][3] if consulta[i][3] is not None else "N/A", a))
                                    print("\nLa Receta consiste en:")
                                    print("{:<20} {:>10} {:>12}".format("Ingrediente", "Cantidad", "Costo"))
                                    for i in range(len(nombres)):
                                        print("{:<25} {:<10} ${:<10.2f}".format(str(nombres[i][0]), cantidades[i], costos[i]))                                    
                                else:
                                    v_me_ca=cantidad_me[0][0]*v_me/float(cantidad_producida[0][0])
                                    a+=v_me_ca
                                    print("{:<8} {:<15} {:<10} {:<5} {:<10}".format("Codigo", "Nombre", "Unidad", "Tipo", "Precio"))
                                    print("{:<8} {:<15} {:<10} {:<5} ${:<10.2f}".format(consulta[i][0], consulta[i][1], consulta[i][2], consulta[i][3] if consulta[i][3] is not None else "N/A", a))
                                    print("\nLa Receta consiste en:")
                                    print("{:<20} {:>10} {:>12}".format("Ingrediente", "Cantidad", "Costo"))
                                    for i in range(len(nombres)):
                                        print("{:<25} {:<10} ${:<10.2f}".format(str(nombres[i]), cantidades[i], costos[i]))                                    
            if eleccion2==2:#CARGA MENU
                while True:
                    cursor.execute("SELECT * FROM MATERIAS_PRIMAS")
                    Validacion=cursor.fetchall()
                    if len(Validacion)<2:
                        print("Debe tener como minimo 2 ingredientes cargados")
                        break
                    n=input("Ingrese el nombre del plato que quiera agregar(S para salir): ")
                    n=n.lower()
                    if n=="s":
                        break
                    cursor.execute("SELECT * FROM MENU WHERE Nombre=?",(n,))
                    consulta=cursor.fetchall()
                    if len(consulta)!=0:
                        print("Esta Receta ya fue Cargada")
                    else:
                        lista1=[]
                        lista2=[]
                        lista3=[]
                        print("Enliste que materias primas utiliza,\nsi ya cargo todas las materias primas ingrese 0: ")
                        while True:
                            ingrediente=input("Materia Prima: ")
                            if ingrediente!="0":
                                ingrediente=ingrediente.lower()
                                cursor.execute("SELECT * FROM MATERIAS_PRIMAS WHERE Nombre=?",(ingrediente,))
                                validar=cursor.fetchall()
                                if len(validar)==0:
                                    print("Materia prima no encontrada")
                                else:
                                    cantidad=float(input("Cantidad de "+ingrediente+": "))
                                    while cantidad<=0:
                                        cantidad=float(input(ingrediente+": "))
                                    lista1.append(ingrediente)
                                    lista2.append(validar[0][0])
                                    lista3.append(cantidad)
                            else:
                                if len(lista1)<2:
                                    print("Toda receta debe contar con mas de un ingrediente")
                                    break
                                print("Confirmacion de materias primas:")
                                print("{:<20} {:<10} {:<10}".format("Nombre","Codigo","Cantidad"))
                                for i in range (len(lista1)):
                                    print("{:<20} {:<10} {:<10}".format(lista1[i], lista2[i], lista3[i]))
                                ele=input("Ingrese S/N: ")
                                ele=ele.upper()
                                while ele!="S" and ele!="N":
                                    ele=input("Ingrese S/N: ")
                                    ele=ele.upper()
                                if ele=="S":
                                    cursor.execute("INSERT INTO MENU VALUES (NULL,?,?,NULL)",(n,"RE"))
                                    conectarbase.commit()
                                    cursor.execute("SELECT Codigo FROM MENU WHERE NOMBRE=?",(n,))
                                    cod_menu=cursor.fetchall()
                                    cod_menu=cod_menu[0][0]
                                    for i in range (len(lista1)):
                                        cursor.execute("INSERT INTO COSTEO VALUES (?,?,?)",(cod_menu,lista2[i],lista3[i]))
                                        conectarbase.commit()
                                    print("Receta Cargada")
                                    break
                                if ele=="N":
                                    print("Receta No Cargada")
                                    break
            if eleccion2==3:#MODIFICAR RECETA
                while True:
                    n=input("Ingrese el nombre del plato que quiera modificar(S para salir): ")
                    n=n.lower()
                    if n=="s":
                        break
                    cursor.execute("SELECT Codigo FROM MENU WHERE Nombre=?",(n,))
                    consulta=cursor.fetchall()
                    if len(consulta)==0:
                        print("Plato no encontrado")
                    else:
                        codigo_menu=consulta[0][0]
                        cursor.execute("SELECT * FROM COSTEO WHERE Codigo_Menu=?",(consulta[0][0],))
                        consulta_i=cursor.fetchall()
                        print(" La Receta Consiste En: ")
                        for i in range(len(consulta_i)):
                            cursor.execute("SELECT * FROM MATERIAS_PRIMAS WHERE Codigo=?",(consulta_i[i][1],))
                            consultamp=cursor.fetchall()
                            print("{:<3}- {:<20} | Cantidad: {}".format(i + 1, consultamp[0][1], consulta_i[i][2]))
                        menus(["Salir","Modificar Cantidad","Agregar Ingrediente","Quitar Ingrediente"])
                        eleccion=a
                        codigo_menu=consulta[0][0]
                        if eleccion==0:
                            break
                        if eleccion==1:
                            n=input("Ingrese el nombre del ingrediente: ")
                            n=n.lower()
                            cursor.execute("SELECT Codigo FROM MATERIAS_PRIMAS WHERE Nombre=?",(n,))
                            consulta=cursor.fetchall()
                            cursor.execute("SELECT Cantidad FROM COSTEO WHERE Codigo_Menu=? AND Codigo_Materia_Prima=?",(codigo_menu,consulta[0][0]))
                            consulta1=cursor.fetchall()
                            print("La cantidad actual es: ",consulta1[0][0])
                            c=float(input("Ingrese la nueva cantidad: "))
                            conf=input("Confirme el cambio(S o N): ")
                            conf=conf.lower()
                            while conf!="s" and conf!="n":
                                conf=input("Confirme el cambio(S o N): ")
                                conf=conf.lower()
                            if conf=="s":
                                cursor.execute("UPDATE COSTEO SET Cantidad=? WHERE Codigo_Menu=? AND Codigo_Materia_Prima=?",(c,codigo_menu,consulta[0][0]))
                                conectarbase.commit()
                                print("Cantidad modificada")
                            else:
                                print("Cantidad no modificada")
                        if eleccion==2:
                            n=input("Ingrese el nombre del ingrediente: ")
                            n=n.lower()
                            cursor.execute("SELECT Codigo FROM MATERIAS_PRIMAS WHERE Nombre=?",(n,))
                            consulta1=cursor.fetchall()
                            if len(consulta1)==0:
                                print("El ingrediente no existe")
                            else:
                                cursor.execute("SELECT * FROM COSTEO WHERE Codigo_Materia_Prima=? AND Codigo_Menu=?",(consulta1[0][0],codigo_menu))
                                datos=cursor.fetchall()
                                print(datos)
                                if len(datos)>0:
                                    print("El ingrediente ya esta cargado para la receta")
                                else:
                                    c=int(input("Ingrese la cantidad: "))
                                    cursor.execute("INSERT INTO COSTEO VALUES (?,?,?)",(consulta[0][0],consulta1[0][0],c))
                                    conectarbase.commit()
                                    print("El ingrediente se cargo con exito")
                        if eleccion==3:
                            n=input("Ingrese el nombre del ingrediente: ")
                            n=n.lower()
                            cursor.execute("SELECT Codigo FROM MATERIAS_PRIMAS WHERE Nombre=?",(n,))
                            consulta1=cursor.fetchall()
                            if len(consulta1)==0:
                                print("El ingrediente no existe")
                            else:
                                cursor.execute("SELECT * FROM COSTEO WHERE Codigo_Menu=? AND Codigo_Materia_Prima=?",(consulta[0][0],consulta1[0][0]))
                                datos=cursor.fetchall()
                                if len(datos)>0:
                                    print("¿Está seguro que quiere dar de baja el ingrediente?")
                                    print(n)
                                    seguir=input("S o N: ")
                                    seguir=seguir.lower()
                                    while seguir!="s" and seguir!="n":
                                        seguir=input("S o N: ")
                                    if seguir=="s":
                                        cursor.execute("DELETE FROM COSTEO WHERE Codigo_Materia_Prima=?",(consulta1[0][0],))
                                        conectarbase.commit()
                                        print("Ingrediente eliminado con exito")
                                    else:
                                        print("No se ha borrado el ingrediente")
                                else:
                                    print("El ingrediente no esta en la receta")
            if eleccion2==4:#BORRAR RECETA
                while True:
                    n=input("Ingrese el nombre del plato que quiera borrar(S para salir): ")
                    n=n.lower()
                    if n=="s":
                        break
                    cursor.execute("SELECT * FROM MENU WHERE Nombre=?",(n,))
                    consulta=cursor.fetchall()
                    if len(consulta)==0:
                        print("Plato no encontrado")
                    else:
                        print("¿Está seguro que quiere dar de baja el plato?")
                        print("Codigo: {:<5} Nombre: {:<15}".format(consulta[0][0], consulta[0][1]))
                        seguir=input("S o N: ")
                        seguir=seguir.lower()
                        while seguir!="s" and seguir!="n":
                            seguir=input("S o N: ")
                        if seguir=="s":
                            cursor.execute("DELETE FROM COSTEO WHERE Codigo_Menu=?",(consulta[0][0],))
                            cursor.execute("DELETE FROM MENU WHERE Codigo=?",(consulta[0][0],))
                            conectarbase.commit()
                            print("Receta Borrada")
                        else:
                            print("No se ha borrado la receta")