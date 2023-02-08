from flask import Flask, render_template, request
from proceso import proceso

app = Flask(__name__)

lista_procesos = []
lp = []
i = 0
colors = iter(['blue', 'yellow', 'green', 'gray', 'orange', 'white', 'red', 'lightblue', 'lightgreen', 'pink',
               'purple', 'cyan'] * 2)


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route('/resetear')
def resetear():
    global lista_procesos
    global lp
    global i
    global colors
    lista_procesos = []
    lp = []
    i = 0
    return render_template("index.html")


@app.route("/hilo", methods=['POST'])
def hilo():
    context = {
        'proceso': request.form['nombre'],
        't_entrada': request.form['t_entrada'],
        'prioridad': request.form['prioridad'],
        't_execute': request.form['t_execute']
    }
    lp.append(context)
    global i
    lista_procesos.append(
        proceso(request.form['nombre'], int(request.form['t_execute']), int(request.form['t_entrada']), next(colors)))
    i = i + 1
    return render_template('index.html', **{'list_procesos': lp})


@app.route("/procesos", methods=['POST'])
def procesos():
    global lista_procesos
    global lp
    serie_proceso = []

    quantum = int(request.form['quantum'])

    # método para ordenar los procesos por tiempo de llegada
    def ordena_insersion(lista):
        for i in range(1, len(lista)):
            j = i
            while j > 0 and lista[j].llegada < lista[j - 1].llegada:
                lista[j], lista[j - 1] = lista[j - 1], lista[j]
                j = j - 1
        return lista

    lista_procesos = ordena_insersion(lista_procesos)  # lista queda ordenada por tiempo de llegada
    print("[+] Se ordeno lista de procesos por tiempo de llegada")
    procesosEspejo = len(lista_procesos)  # es la variable que controla los procesos que hacen falta por terminar
    tiempo = 0
    procesosCola = []
    procesoEjecucion = None  # proceso en ejecución
    nproceso = 0  # variable utilizada para pasar al siguiente
    print("[+] Se establecieron variables para el funcionamiento")
    print("----- Inicio del Algoritmo -----")
    sw = True  # Variable de control
    while procesosEspejo > 0:
        print("---------------- Tiempo [" + str(tiempo) + "]  ---------------")
        if len(lista_procesos) > nproceso and tiempo >= lista_procesos[nproceso].llegada:
            print("[+]El proceso " + str(lista_procesos[nproceso].id) + " se ingreso a la cola de listos")
            procesosCola.append(lista_procesos[nproceso])
            nproceso = nproceso + 1

        else:
            if nproceso > 0 or len(procesosCola) > 0:
                if procesoEjecucion is None:
                    procesoEjecucion = procesosCola.pop(0)
                    sw = True
                    print("[+] Se saca el proceso " + str(procesoEjecucion.id) + " de la cola y se ejecuta.")
                else:
                    if sw:
                        if procesoEjecucion.rafagatmp >= quantum:
                            procesoEjecucion.rafagatmp = procesoEjecucion.rafagatmp - quantum
                            print("[+] Se resta " + str(quantum) + " a la ráfaga del proceso " + str(
                                procesoEjecucion.id))
                            tiempo = tiempo + quantum
                            print("[+] Se aumenta " + str(quantum) + " al tiempo")
                            for i in range(quantum):
                                serie_proceso.append({'id': procesoEjecucion.id, 'color': procesoEjecucion.color})
                        else:
                            tiempo = tiempo + procesoEjecucion.rafagatmp
                            print("[+] Se aumenta " + str(procesoEjecucion.rafagatmp) + " al tiempo")
                            print("[+] Se resta " + str(
                                procesoEjecucion.rafagatmp) + " a la ráfaga del proceso " + str(
                                procesoEjecucion.id))
                            procesoEjecucion.rafagatmp = 0
                            for i in range(procesoEjecucion.rafagatmp):
                                serie_proceso.append({'id': procesoEjecucion.id, 'color': procesoEjecucion.color})

                        if procesoEjecucion.rafagatmp < 1:
                            print("---------------- Tiempo [" + str(tiempo) + "]  ---------------")
                            print("[+] El Proceso " + str(procesoEjecucion.id) + " finalizo.")
                            procesoEjecucion.finalizacion = tiempo
                            procesoEjecucion.retorno = procesoEjecucion.finalizacion - procesoEjecucion.llegada
                            procesoEjecucion.espera = procesoEjecucion.retorno - procesoEjecucion.rafaga
                            procesosEspejo = procesosEspejo - 1
                            procesoEjecucion = None

                        else:
                            sw = False
                    else:
                        procesosCola.append(procesoEjecucion)
                        print("[+] Se agrega el proceso " + str(
                            procesoEjecucion.id) + " que estaba en ejecución a la cola de listos")
                        procesoEjecucion = None
            else:
                tiempo = tiempo + 1
    print("----- Algoritmo Finalizado -----")
    print("!!!!! Resultados !!!!!")
    total_retorno = 0
    total_espera = 0
    for proceso in lista_procesos:
        print("Proceso " + str(proceso.id) + " Finalizo: " + str(proceso.finalizacion) + " Espera: " + str(
            proceso.espera) + " Retorno: " + str(proceso.retorno))
        total_retorno = total_retorno + proceso.retorno
        total_espera = total_espera + proceso.espera
    ex = True

    context = {
        't_retorno': total_retorno,
        't_espera': total_espera,
        'ejecutado': ex,
        'c_procesos': len(lista_procesos),
        'lpc': lista_procesos,
        'sp': serie_proceso
    }
    return render_template("index.html", **context)


if __name__ == '__main__':
    app.run(debug=True)
