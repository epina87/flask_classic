from flask import render_template, request, redirect,url_for
from registro_ig import app
from registro_ig.model import select_all,insert,select_by,delete_by,update_by
from datetime import date



@app.route("/")
def index():
    registro = select_all()
    return render_template("index.html",pageTitle="Todos",data=registro)

@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html", pageTitle="Alta", 
                               dataForm={})
    else:
        """
            1. Validar el formulario
                Fecha valida y <= hoy
            2. Concepto no sea vacío
            3. Cantidad no se cero     
        """
        errores = validaFormulario(request.form)

        if not errores:
            insert([request.form['date'],request.form['concept'],request.form['quantity']])

            return redirect(url_for("index"))
        else:
            return render_template("new.html", pageTitle="Alta", msgErrors=errores, dataForm=request.form)

def validaFormulario(camposFormulario):
    errores = []
    hoy = date.today().isoformat()
    if camposFormulario['date'] > hoy:
        errores.append("La fecha introducida es es futuro.")

    if camposFormulario['concept'] == "":
        errores.append("Introduce un concepto para la transacción.")

    #La primera condición es para que el número sea distinto de cero
    #la segunda condición es para que el campo no esté vacío
    if camposFormulario["quantity"] == "" or float(camposFormulario["quantity"]) == 0.0:
        errores.append("Introduce una cantidad positiva o negativa.")

    return errores

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def borrar(id):
    if request.method == "GET":
        """
        1. Consultar en movimientos.txt y recueperar el registro con id al de la petición
        2. Devolver el formulario html con los datos de mi registro, no modificables 
        3. Tendrá un boton que diga confirmar.
        """
        
        registro_definitivo = select_by(id)  
    
        if registro_definitivo:
            return render_template("delete.html", registro=registro_definitivo)
        else:
            return redirect(url_for("index")) 

    else:      
        """
            Borrar el registro
        """     
        
        delete_by(id)
        
        return redirect(url_for("index"))

@app.route("/update/<int:id>", methods=["GET", "POST"])
def modifica(id):
    if request.method == "GET":
        """
        1. Consultar en movimientos.txt y recueperar el registro con id al de la petición
        2. Devolver el formulario html con los datos de mi registro
        """
        registro_definitivo = select_by(id)
        if registro_definitivo:
            return render_template("update.html", pageTitle="Modificar", registro=registro_definitivo)
        else:
            return redirect(url_for("index")) 
       
    else:
        """
        1. validar registro de entrada
        2. Si el registro es correcto lo sustituyo en movimientos.txt. La mejor manera es copiar registro a registro e fichero nuevo y dar el cambiazo
        3. redirect 
        4. Si el registro es incorrecto la gestion de errores que conocemos
        """
        errores = validaFormulario(request.form)

        if not errores:
            
            update_by(fomr_to_list(id,request.form))
            return redirect(url_for("index"))

        else:                         
            return render_template("update.html", pageTitle="Modificar", msgErrors=errores, registro=fomr_to_list(id,request.form))

def fomr_to_list(id,form):   
    return [str(id),form['date'],form['concept'],form['quantity']]