import sqlite3
from config import ORIGIN_DATA

def select_all():
    con =sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    result = cur.execute("SELECT id, date, concept, quantity from movements order by date;")

    filas = result.fetchall()
    columnas = result.description

    """
    buscar .zip de las funciones de python
    """
    #Con el metodo zip
    resultado=[]
    list_col_solo_con_titulos=[]
    for col in columnas:
        list_col_solo_con_titulos.append(col[0])
    for valor_fila in filas:
        dic_combinado = dict(zip(list_col_solo_con_titulos,valor_fila))
        resultado.append(dic_combinado)    
    '''
    metodo .zip Ramon
    lista=[]
    for fila in filas:
        registro={}
        for columna,valor in zip(columnas,fila):
            registro[columna[0]] = valor
        lista.append(registro)    
    '''    
    
    #Con el metodo de clase
    '''    
    resultado=[]
    for fila in filas:
        d={}
        for posicion,campo in enumerate(columnas):
            d[campo[0]] = fila[posicion]
        resultado.append(d)
    '''    
    con.close()    
    return resultado
    
def insert(registro):
    """
    INSERT INTO moviments(date,concept,quantity) values(?,?,?)
    params

    cur.execute("INSERT INTO moviments(date,concept,quantity) values(?,?,?), ['20022-04-08','cumple',-80]")

    importante 
    con.commit() antes de hacer el con.close()
    """

    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    cur.execute("INSERT INTO movements(date,concept,quantity) values(?,?,?);",registro)

    con.commit()
    con.close()

def select_by(id):
    print(id)
    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    result = cur.execute("SELECT id, date, concept, quantity FROM movements WHERE id=? " , (id,))
    filas = result.fetchall()
    con.close()
    return filas[0]

def delete_by(id):
    con =sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    result = cur.execute("DELETE FROM movements WHERE id=? " , (id,))
    con.commit()
    con.close()

def update_by(registro_mod):
    con =sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    result = cur.execute("UPDATE movements SET date=?,concept=?,quantity=? WHERE id=?; " , (registro_mod[1],registro_mod[2],registro_mod[3],registro_mod[0]))
    con.commit()
    con.close()

    



