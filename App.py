from nicegui import ui,app,native
from GLC_Definitivo import *

app.native.window_args['resizable'] = True
app.native.start_args['debug'] = False
app.native.settings['ALLOW_DOWNLOADS'] = True

valores=[]

malla1=ui.grid(columns=3)
with malla1:

    def funcB1():
        status=("Valores aceptados") if (n1.value>n2.value) else ("La semilla debe ser menor al modulo")
        if n1.value>n2.value:
            valores.append(n2.value)
            valores.append(n1.value)
            n1.disable()
            n2.disable()
            b1.disable()
            b1.set_visibility(False)
            b2=ui.button("Siguiente",on_click= lambda:(malla2.set_visibility(True)))
            # b2.set_visibility(False)
        ui.notify(status,position="top")

    n1=ui.number("Modulo (m):",value=0,on_change=())
    n2=ui.number("Semilla (x0):",value=0,on_change=())
    b1=ui.button("Validar",on_click=lambda: (funcB1()))

ui.separator()

malla2=ui.grid(columns=1)
malla2.set_visibility(False)
with malla2:

    def opciones(m):
        try:
            Va=selectMult(m)
            Vc=selectConst(m)
            l1.set_text(f"posibles valores de a: \n{Va}")
            l2.set_text(f"posibles valores de c: \n{Vc}")
            b3.set_text("opciones para a y c")

        except: 
            pass
        # return (Va,Vc)

    b3=ui.button("Mostrar opciones para a y c", on_click=lambda:(opciones(valores[-1])))
    l1=ui.label()
    l2=ui.label()

ui.separator()

malla3=ui.grid(columns=3)
malla3.bind_visibility_from(malla2)
with malla3:

    def selectMultYConst():
        try:
            error=""
            if f", {round(n3.value)}," not in l1.text:
                error=(f"Valor de a seleccionado es invalido [{n3.value}]")
            elif f", {round(n4.value)}," not in l2.text:
                error=(f"Valor de c seleccionado es invalido [{n4.value}]")
            else:
                if len(valores)<4:
                    valores.insert(0,n3.value)
                    valores.insert(2,n4.value)
                n3.disable()
                n4.disable()
                b3.disable()    
                malla4.set_visibility(True)        
        except:
            pass
        finally:
            status=("Valores aceptados") if (not error) else error
            ui.notify(status)

    n3=ui.number("Multiplicador (a):",value=0,on_change=())
    n4=ui.number("Constante aditiva (c):",value=0,on_change=())
    b4=ui.button("Validar",on_click=lambda: (selectMultYConst()))

ui.separator()

malla4=ui.grid(columns=1)
malla4.set_visibility(False)
with malla4:
    

    def resultado(v):
        lista=list(map(lambda x: int(x), v))
        GLC=glc(lista[0],lista[1],lista[2],lista[3])
        with open('tabla.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(GLC)
        ui.download("tabla.csv")

    ui.label("Resultados generados con exito")
    ui.button("Descargar 'tabla.csv'", on_click=lambda: (resultado(valores)))


ui.run(port=native.find_open_port(), reload=False, native=True, window_size=(800,500),fullscreen=False)
# ui.run(port=5050)
