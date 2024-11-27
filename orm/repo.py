#
import orm.modelos as modelos
#Sesion
from sqlalchemy.orm import Session
from sqlalchemy import and_

#Esta funcion es llamada por api.py
#para atender GET 'usuarios/{id}'
#SELECT * FROM app.usuarios WHERE 
def usuario_por_id(sesion:Session, id_usuario:int):
    print("select * from app.usuarios where id = ", id_usuario)
    return sesion.query(modelos.Usuario).filter(modelos.Usuario.id==id_usuario).first()

def compra_por_id(sesion:Session, id_compra: int):
    print("select * from app.compras where id = ", id_compra)
    return sesion.query(modelos.Compra).filter(modelos.Compra.id == id_compra).first()

def foto_por_id(sesion: Session, id_foto: int):
    print("select * from app.fotos where id_compra = ", id_foto)
    return sesion.query(modelos.Foto).filter(modelos.Foto.id == id_foto).filter()

def lista_usuarios(sesion:Session):
    print("select * from app.usuarios")
    return sesion.query(modelos.Usuario).all()

def lista_compras(sesion:Session):
    print("select * from app.compras")
    return sesion.query(modelos.Compra).all()

def lista_fotos(sesion:Session):
    print("select * from app.fotos")
    return sesion.query(modelos.Foto).all()

#GET '/compras?id_usuario={id_usr}&precio={p}'
#select * from app.compras where id_usuario=id_usr and precio>=p 
def compras_por_id_precio(sesion:Session, id_usr:int, p:float):
    print(f"select * from app.compras where id_usuario = {id_usr} and precio = {p}")
    return sesion.query(modelos.Compra).filter(and_(modelos.Compra.id_usuario == id_usr, modelos.Compra.precio >= p)).all()

def usuarios_por_edad(sesion:Session, edad_min:int, edad_max:int):
    print(f"select * from app.usuarios where edad >= {edad_min} and edad <= {edad_max}")
    return sesion.query(modelos.Usuario).filter(and_(modelos.Usuario.edad >= edad_min, modelos.Usuario.edad <= edad_max)).all()
          

