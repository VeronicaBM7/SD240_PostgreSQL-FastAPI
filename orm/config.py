#Permite configurar la conexion a la BD
from sqlalchemy import create_engine
#El session marker perimite creer sesiones para hacer consultas
#por cada consulta abre y cierra una sesion
from sqlalchemy.orm import sessionmaker
# declarative_base permite definir la clase base para mapear las tablas de la BD
from sqlalchemy.ext.declarative import declarative_base

#1.- Configurar la conexion BD
#Crear la URL de la BD--> servidor//usuario:password@url:puerto/nomnreBD
URL_BASE_DATOS = "postgresql://usuario-ejemplo:12345@localhost:5432/base-ejemplo"
#Conectarnos mediante el esquema app
engine = create_engine(URL_BASE_DATOS, 
                            connect_args={
                                "options": "-csearch_path=app"
                            })
#2. Obtener la clase que nos permite crear objetos tipo session
SessionClass = sessionmaker(engine) 
#Crear una funcion para obtener objetos de la clase SessionClass
def generador_sesion():
    sesion = SessionClass()
    try:
        #Equivalente a un return sesion pero de manera segura
        yield sesion 
    finally:
        sesion.close()

#3 obter la clase base para mapear
BaseClass = declarative_base()
