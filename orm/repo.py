#
import orm.modelos as moledos
#Sesion
from sqlalchemy.orm import Session
#Esta funcion es llamada por api.py
#para atender GET 'usuarios/{id}'
#SELECT * FROM app.usuarios WHERE 
def usuario_por_id(sesion:Session, id_usuario:int):
    print("select * from app.usuarios where id = ", id_usuario)
    return sesion.query(moledos.Usuario).filter(moledos.Usuario.id==id_usuario).first()

def compra_por_id(sesion:Session, id_compra: int):
    print("select * from app.compras where id = ", id_compra)
    return sesion.query(moledos.Compra).filter(moledos.Compra.id == id_compra).first()

def foto_por_id(sesion: Session, id_foto: int):
    print("select * from app.fotos where id_compra = ", id_foto)
    return sesion.query(moledos.Foto).filter(moledos.Foto.id == id_foto).filter()

    
