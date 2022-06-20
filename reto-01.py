"""
crear una aplicacion con tkinter que descargue los tipos de cambios de la sbs y los muestre en un treeview
crear un boton exportar que cree un archivo csv de la data que se descargo
enviar el repositorio de la tarea
"""

from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from tkinter import *
from tkinter import ttk

url = requests.get("https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx")
app = Tk()
app.title('Tipo de Cambio SBS')
app.geometry('610x300')

def grabarMonedas(monedas):
  strMonedas = ""
  for l in monedas:
    for clave,valor in l.items():
      strMonedas += valor
      if clave != 'venta':
        strMonedas += ';'
      else:
        strMonedas += '\n'
  return strMonedas

def scrapping_tipoCambio():
  if(url.status_code == 200):
    messagebox.showinfo("Info","¡Página encontrada!")
    html = BeautifulSoup(url.text,'html.parser')
    tabla = html.find_all('table',{'id':'ctl00_cphContent_rgTipoCambio_ctl00'})
    
    tree = ttk.Treeview(app)
    tree['columns'] = ('moneda','compra','venta')
    
    listaMonedas = []
    tree.column('#0',width=0,stretch=NO)
    tree.column('moneda')
    tree.column('compra')
    tree.column('venta')
    tree.heading('#0',text='id')
    tree.heading('moneda',text='Moneda')
    tree.heading('compra',text='Compra')
    tree.heading('venta',text='Venta')
    tree.grid(row=0,column=0,sticky='nsew')

    for i in range(7):
      fila = html.find('tr',{'id':'ctl00_cphContent_rgTipoCambio_ctl00__'+str(i)}) 
      moneda = fila.find('td',{'class':'APLI_fila3'})
      compra = fila.find('td',{'class':'APLI_fila2'})
      venta = fila.find('td',{'class':'APLI_fila2'}).findNext('td')
      dicMoneda = {
        'moneda': moneda.get_text(),
        'compra': compra.get_text(),
        'venta': venta.get_text()
      }
      tree.insert('',END,values=(moneda.get_text(),compra.get_text(),venta.get_text()))
      listaMonedas.append(dicMoneda)
      
    strMonedas = grabarMonedas(listaMonedas)
    fw = open('monedas.csv','w')
    fw.write(strMonedas)
    fw.close()
  else:
    print("error " + str(url.status_code))

if __name__ == "__main__" :
  scrapping_tipoCambio()
  app.mainloop()