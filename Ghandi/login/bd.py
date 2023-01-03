import cx_Oracle
import oracledb


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


#Python3
class ConnectionBD( metaclass=Singleton):
    def establecer_conexion(self,username, passwd):
        self.bd = oracledb.connect( user=username, 
                              password=passwd,
                              dsn="oracle0.ugr.es:1521/practbd.oracle0.ugr.es",
                              encoding="UTF-8")

    def cerrar_conexion(self):
        self.bd.close()
    
    def get_conexion(self):
        return self.bd