from fastapi import FastAPI, UploadFile, File, Form, Depends
from typing import Optional
from pydantic import BaseModel
import shutil
import os
import uuid
import orm.repo as repo #funciones para hacer consultas
from sqlalchemy.orm import Session
from orm.config import generador_sesion 

# creación del servidor
app = FastAPI()

#definición de la base del usuario
class UsuarioBase(BaseModel):
    nombre:Optional[str]=None
    edad:int
    domicilio:str    
    
usuarios = [{
    "id": 0,
    "nombre": "Homero Simpson",
    "edad": 40,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 1,
    "nombre": "Marge Simpson",
    "edad": 38,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 2,
    "nombre": "Lisa Simpson",
    "edad": 8,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 3,
    "nombre": "Bart Simpson",
    "edad": 10,
    "domicilio": "Av. Simpre Viva"
}]


# decorator
@app.get("/")
def hola_mundo():
    print("invocando a ruta /")
    respuesta = {
        "mensaje": "hola mundo!"
    }

    return respuesta


@app.get("/usuarios/{id}/compras/{id_compra}")
def compras_usuario_por_id(id: int, id_compra: int):
    print("buscando compra con id:", id_compra, " del usuario con id:", id)
    # simulamos la consulta
    compra = {
        "id_compra": 787,
        "producto": "TV",
        "precio": 14000
    }
    return compra

#Consultas a la BD Real   
@app.get("/usuarios/{id}")
def usuario_por_id(id: int, sesion:Session=Depends(generador_sesion)):
    print("Api consultando usuario por id:", id)
    return repo.usuario_por_id(sesion, id)

#GET 'usuarios?edad=edad_min&edad=edad_min
#select * from app.usuarios where edad >= {edad_min} and edad <= {edad_max} 
@app.get("/usuarios")
def usuarios_por_edad(edad_min: int, edad_max: int, sesion:Session=Depends(generador_sesion)):
    print(f"Api consultando usuarios por rango de edad de {edad_min} y {edad_max}")
    return repo.usuarios_por_edad(sesion, edad_min, edad_max)

@app.get("/compras/{id}")
def compra_por_id(id: int, sesion:Session=Depends(generador_sesion)):
    print("Api consultando compra por id:", id)
    return repo.compra_por_id(sesion, id)

#GET '/compras?id_usuario={id_usr}&precio={p}'
@app.get("/compras")
def compras_por_id_precio(id_usuario:int, precio:float, sesion:Session=Depends(generador_sesion)):
    print(f"/compras?id_usuario={id_usuario}&precio={precio}'")
    return repo.compras_por_id_precio(sesion, id_usuario, precio)



@app.get("/fotos/{id}")
def foto_por_id(id: int, sesion:Session=Depends(generador_sesion)):
    print("Api consultando foto por id:", id)
    return repo.foto_por_id(sesion, id)


@app.get("/usuarios")
def lista_usuarios(sesion:Session=Depends(generador_sesion)): 
    print("Api consultando usuarios")
    return repo.lista_usuarios(sesion)

@app.get("/compras")
def lista_compras(sesion:Session=Depends(generador_sesion)): 
    print("Api consultando compras")
    return repo.lista_compras(sesion)

@app.get("/fotos")
def lista_fotos(sesion:Session=Depends(generador_sesion)):
    print("Api consultando fotos")
    return repo.lista_fotos(sesion)







############Simulacion de consulta
@app.post("/usuarios")
def guardar_usuario(usuario:UsuarioBase, parametro1:str):
    print("usuario a guardar:", usuario, ", parametro1:", parametro1)
    #simulamos guardado en la base.
    
    usr_nuevo = {}
    usr_nuevo["id"] = len(usuarios)
    usr_nuevo["nombre"] = usuario.nombre
    usr_nuevo["edad"] = usuario.edad
    usr_nuevo["domicilio"] = usuario.domicilio

    usuarios.append(usuario)

    return usr_nuevo

@app.put("/usuario/{id}")
def actualizar_usuario(id:int, usuario:UsuarioBase):
    #simulamos consulta
    usr_act = usuarios[id]
    #simulamos la actualización
    usr_act["nombre"] = usuario.nombre
    usr_act["edad"] = usuario.edad
    usr_act["domicilio"] = usuario.domicilio    

    return usr_act
    
@app.delete("/usuario/{id}")
def borrar_usuario(id:int):
    #simulamos una consulta
    if id>=0 and id< len(usuarios):
        usuario = usuarios[id]
    else:
        usuario = None
    
    if usuario is not None:
        usuarios.remove(usuario)
    
    return {"status_borrado", "ok"}

@app.post("/fotos")
async def guardar_foto(titulo:str=Form(None), descripcion:str=Form(...), foto:UploadFile=File(...)):
    print("titulo:", titulo)
    print("descripcion:", descripcion)

    home_usuario=os.path.expanduser("~")
    nombre_archivo=uuid.uuid4().hex  #generamos nombre único en formato hexadecimal
    extension = os.path.splitext(foto.filename)[1]
    ruta_imagen=f'{home_usuario}/fotos-ejemplo/{nombre_archivo}{extension}'
    print("guardando imagen en ruta:", ruta_imagen)

    with open(ruta_imagen,"wb") as imagen:
        contenido = await foto.read() #read funciona de manera asyncrona
        imagen.write(contenido)

    return {"titulo":titulo, "descripcion":descripcion, "foto":foto.filename}
