DROP TABLE FACTURA;
DROP TABLE CITA;
DROP TABLE JAULA;
DROP TABLE ANIMAL;
DROP TABLE CLIENTE;
DROP TABLE CONTRATO;
DROP TABLE ENTREVISTA;
DROP TABLE PEDIDO;
DROP TABLE PRODUCTO;

CREATE TABLE CLIENTE(
	DNI VARCHAR2(9) NOT NULL,
	NOMBRE VARCHAR2(20),
	APELLIDOS VARCHAR2(40),
	TELEFONO NUMBER,
	DIRECCION VARCHAR2(60),
	CUENTABANCARIA VARCHAR2(20),
	CONSTRAINT CLIENTE_PK PRIMARY KEY (DNI)
);

CREATE TABLE FACTURA(
	IDFACTURA VARCHAR2(9) NOT NULL,
	DNI VARCHAR2(9),
	CANTIDAD FLOAT(126),	
	PAGADO CHAR(1) DEFAULT 'N',
	CONSTRAINT FACTURA_PK PRIMARY KEY (IDFACTURA),
	CONSTRAINT FACTURA_FK FOREIGN KEY (DNI) REFERENCES CLIENTE (DNI)
);

CREATE TABLE CITA(
	FECHAHORA TIMESTAMP NOT NULL,
	DISPONIBILIDAD CHAR(1) DEFAULT 'N',
	DNI VARCHAR2(9),
	CONSTRAINT CITA_PK PRIMARY KEY (FECHAHORA),
	CONSTRAINT CITA_FK FOREIGN KEY (DNI) REFERENCES CLIENTE(DNI) ON DELETE SET NULL ENABLE
);

CREATE TABLE ANIMAL(
	IDANIMAL VARCHAR2(9) NOT NULL,
	DNI VARCHAR2(9),
	TIPO VARCHAR2(20),
	ESPECIE VARCHAR2(40),
	CONSTRAINT ANIMAL_PK PRIMARY KEY (IDANIMAL),
	CONSTRAINT ANIMAL_FK FOREIGN KEY (DNI) REFERENCES CLIENTE(DNI) ON DELETE CASCADE ENABLE
);

CREATE TABLE JAULA(
	IDJAULA VARCHAR2(9) NOT NULL,
	IDANIMAL VARCHAR2(9),	
	TAMJAULA VARCHAR2(9),
	CONSTRAINT JAULA_PK PRIMARY KEY (IDJAULA),
	CONSTRAINT JAULA_FK FOREIGN KEY (IDANIMAL)
	REFERENCES ANIMAL(IDANIMAL) ON DELETE SET NULL ENABLE
);

CREATE TABLE CONTRATO(
	DNI VARCHAR2(9 BYTE) NOT NULL,
	NOMBRE VARCHAR2(20 BYTE),
	APELLIDOS VARCHAR2(40 BYTE),
	FECHA_NACIM DATE,
	TELEFONO VARCHAR2(20 BYTE),
	SUELDO FLOAT(126),
	CUENTABANCARIA VARCHAR2(24),
	DURACION VARCHAR2(20 BYTE),
	CONSTRAINT CONTRATO_PK PRIMARY KEY (DNI)
);

CREATE TABLE ENTREVISTA(
	DNI VARCHAR2(9 BYTE) NOT NULL,
	NOMBRE VARCHAR2(20 BYTE),
	APELLIDOS VARCHAR2(40 BYTE),
	FECHA DATE,
	HORA VARCHAR2(10 BYTE),
	CONSTRAINT ENTREVISTA_PK PRIMARY KEY (DNI)
);

CREATE TABLE PRODUCTO(
	IDPRODUCTO VARCHAR2(9) NOT NULL,
	NOMBRE VARCHAR2(30),
	CANTIDAD FLOAT,
	CONSTRAINT PRODUCTO_PK PRIMARY KEY (IDPRODUCTO)
);

CREATE TABLE PEDIDO(
	IDPEDIDO VARCHAR2(9) NOT NULL,
	CANTIDAD FLOAT,
    FECHA DATE,
	PAGADO CHAR(1) DEFAULT 'N',
	IDPRODUCTO VARCHAR2(9),
	CONSTRAINT PEDIDO_PK PRIMARY KEY (IDPEDIDO),
	CONSTRAINT PEDIDO_FK FOREIGN KEY (IDPRODUCTO) REFERENCES PRODUCTO(IDPRODUCTO)
);

INSERT INTO CLIENTE
VALUES ('12121212R','PEPE','LOPEZ LOPEZ','666666661','C/ FALSA 123','ES25 1234 1234 1234');
INSERT INTO CLIENTE
VALUES ('12121213J','PEPA','RUIZ RUIZ','666666662','C/ FALSA 125','ES25 1234 1234 1235');
INSERT INTO CLIENTE
VALUES ('12121214F','LUIS','PEREZ MARTINEZ','666666663','C/ FALSA 126','ES25 1234 1234 6533');
INSERT INTO CLIENTE
VALUES ('12121210S','ENRIQUE','GOMEZ FERNANDEZ','666666664','C/ FALSA 131','ES25 1234 1234 1145');
INSERT INTO CLIENTE
VALUES ('12121215G','ANTONIO','CASTRO JAEN','666666665','C/ FALSA 121','ES25 1234 1234 1146');
INSERT INTO CLIENTE
VALUES ('12121216W','MARTIN','GAMEZ SEDEÑO','666666666','C/ FALSA 143','ES25 1234 1234 1632');
INSERT INTO CLIENTE
VALUES ('12121217P','JAVIER','HERREROS GASOL','666666667','C/ FALSA 12','ES25 1234 1234 1643');
INSERT INTO CLIENTE
VALUES ('12121218M','DANIEL','ABRINES NADAL','666666668','C/ FALSA 31','ES25 1234 1234 1542');
INSERT INTO CLIENTE
VALUES ('12121219L','FRANCISCO','BARTOMEU PARRA','666666669','C/ FALSA 13','ES25 1234 1234 1124');
INSERT INTO CLIENTE
VALUES ('12121223R','MARIA','ALONSO MARTINEZ','666666660','C/ FALSA 19','ES25 1234 1234 1241');

INSERT INTO FACTURA
VALUES ('1','12121212R',40.0,'S');
INSERT INTO FACTURA
VALUES ('2','12121213J',200.0,'S');
INSERT INTO FACTURA
VALUES ('3','12121214F',40.0,'S');
INSERT INTO FACTURA
VALUES ('4','12121215G',20.0,'S');
INSERT INTO FACTURA
VALUES ('5','12121216W',110.0,'S');
INSERT INTO FACTURA
VALUES ('6','12121217P',150.0,'N');
INSERT INTO FACTURA
VALUES ('7','12121218M',150.0,'N');
INSERT INTO FACTURA
VALUES ('8','12121219L',100.0,'N');
INSERT INTO FACTURA
VALUES ('9','12121223R',50.0,'N');
INSERT INTO FACTURA
VALUES ('10','12121210S',50.0,'N');

INSERT INTO CITA
VALUES(TO_DATE( '30-06-2022 14:30', 'DD-MM-YYYY HH24:MI' ),'S','12121214F');
INSERT INTO CITA
VALUES(TO_DATE( '30-06-2022 15:30', 'DD-MM-YYYY HH24:MI' ),'S','12121212R');
INSERT INTO CITA
VALUES(TO_DATE( '30-06-2022 14:00', 'DD-MM-YYYY HH24:MI' ),'S','12121213J');
INSERT INTO CITA
VALUES(TO_DATE( '30-06-2022 16:00', 'DD-MM-YYYY HH24:MI' ),'S','12121215G');
INSERT INTO CITA
VALUES(TO_DATE( '30-06-2022 08:00', 'DD-MM-YYYY HH24:MI' ),'S','12121216W');
INSERT INTO CITA
VALUES(TO_DATE( '30-06-2022 09:00', 'DD-MM-YYYY HH24:MI' ),'N','12121217P');
INSERT INTO CITA
VALUES(TO_DATE( '30-06-2022 10:00', 'DD-MM-YYYY HH24:MI' ),'S','12121218M');
INSERT INTO CITA
VALUES(TO_DATE( '30-06-2022 11:00', 'DD-MM-YYYY HH24:MI' ),'S','12121219L');
INSERT INTO CITA
VALUES(TO_DATE( '30-06-2022 12:00', 'DD-MM-YYYY HH24:MI' ),'S','12121223R');
INSERT INTO CITA
VALUES(TO_DATE( '30-06-2022 13:00', 'DD-MM-YYYY HH24:MI' ),'N','12121210S');

INSERT INTO ANIMAL
VALUES('1','12121212R','PERRO','HUSKY');
INSERT INTO ANIMAL
VALUES('2','12121213J','GATO','SIAMES');
INSERT INTO ANIMAL
VALUES('3','12121214F','SERPIENTE','VIBORA');
INSERT INTO ANIMAL
VALUES('4','12121215G','SERPIENTE','BOA');
INSERT INTO ANIMAL
VALUES('5','12121216W','PERRO','DOBERMAN');
INSERT INTO ANIMAL
VALUES('6','12121217P','CONEJO','REX');
INSERT INTO ANIMAL
VALUES('7','12121218M','RATON','AGUAS');
INSERT INTO ANIMAL
VALUES('8','12121219L','GATO','AGUAS');
INSERT INTO ANIMAL
VALUES('9','12121223R','TORTUGA','MOTEADA');
INSERT INTO ANIMAL
VALUES('10','12121210S','TIGRE','BENGALA');

INSERT INTO JAULA
VALUES('1','1','L');
INSERT INTO JAULA
VALUES('2','2','S');
INSERT INTO JAULA
VALUES('3','3','XXL');
INSERT INTO JAULA
VALUES('4','4','XL');
INSERT INTO JAULA
VALUES('5','5','S');
INSERT INTO JAULA
VALUES('6','6','M');
INSERT INTO JAULA
VALUES('7','7','M');
INSERT INTO JAULA
VALUES('8','8','M');
INSERT INTO JAULA
VALUES('9','9','XXL');
INSERT INTO JAULA
VALUES('10','10','XL');

INSERT INTO CONTRATO
VALUES( '26262626R','JUAN','PEREZ LOPEZ', TO_DATE( '30-06-1995', 'DD-MM-YYYY' ),'673234132','1650,50','ES23 6542 1246 6342','6 MESES');
INSERT INTO CONTRATO
VALUES( '26262627J','LOLA','LOLITA', TO_DATE( '29-04-1990', 'DD-MM-YYYY' ),'673232342','1650,50','ES23 1232 1246 6352','1 AÑO');
INSERT INTO CONTRATO
VALUES( '26262628F','DANIEL','MARTINEZ', TO_DATE( '09-05-1992', 'DD-MM-YYYY' ),'673232425','1750,50','ES23 6523 1256 6364','INDEFINIDO');
INSERT INTO CONTRATO
VALUES( '26262674L','FRANCISCO','PEREZ', TO_DATE( '09-06-1992', 'DD-MM-YYYY' ),'673232426','1750,50','ES23 6523 1256 8273','INDEFINIDO');
INSERT INTO CONTRATO
VALUES( '26262612L','GREGORIO','MARANON', TO_DATE( '10-07-1992', 'DD-MM-YYYY' ),'673232427','1850,50','ES23 6523 1256 6432','INDEFINIDO');
INSERT INTO CONTRATO
VALUES( '26262623T','ANTONIO','CASTRO', TO_DATE( '11-08-1992', 'DD-MM-YYYY' ),'673232428','1950,50','ES23 6523 1256 6632','INDEFINIDO');
INSERT INTO CONTRATO
VALUES( '26262629F','JUAN','LEIVA', TO_DATE( '12-09-1992', 'DD-MM-YYYY' ),'673232429','1700,50','ES23 6523 1256 6422','INDEFINIDO');
INSERT INTO CONTRATO
VALUES( '26262651W','ADARA','MARA', TO_DATE( '13-05-1992', 'DD-MM-YYYY' ),'673232430','1350,50','ES23 6523 1256 2154','INDEFINIDO');
INSERT INTO CONTRATO
VALUES( '26262611D','LEIRE','SANZ', TO_DATE( '14-10-1992', 'DD-MM-YYYY' ),'673232431','1200,50','ES23 6523 1256 7542','INDEFINIDO');
INSERT INTO CONTRATO
VALUES( '26262693F','IRATI','OTADUI', TO_DATE( '15-11-1992', 'DD-MM-YYYY' ),'673232432','1000,50','ES23 6523 1256 6532','INDEFINIDO');

INSERT INTO ENTREVISTA
VALUES('72727272R','FAUSTO','LOPEZ JIMENEZ',TO_DATE( '09-12-2022', 'DD-MM-YYYY' ),'12:00');
INSERT INTO ENTREVISTA
VALUES('72727273J','LAURA','MARTINEZ PEREZ',TO_DATE( '09-12-2022', 'DD-MM-YYYY' ),'12:30');
INSERT INTO ENTREVISTA
VALUES('72727274F','JUAN','RUSILLO CASTILLO',TO_DATE( '09-12-2022', 'DD-MM-YYYY' ),'13:00');
INSERT INTO ENTREVISTA
VALUES('72727275F','FERNANDO','MARIN RUIZ',TO_DATE( '09-12-2022', 'DD-MM-YYYY' ),'13:30');
INSERT INTO ENTREVISTA
VALUES('72727276F','UNAI','OTADUI SANZ',TO_DATE( '09-12-2022', 'DD-MM-YYYY' ),'14:00');
INSERT INTO ENTREVISTA
VALUES('72727277F','IKER','EGAÑA OIANGUREN',TO_DATE( '09-12-2022', 'DD-MM-YYYY' ),'14:30');
INSERT INTO ENTREVISTA
VALUES('72727278F','IRATI','UGALDE GARCIA',TO_DATE( '09-12-2022', 'DD-MM-YYYY' ),'15:00');
INSERT INTO ENTREVISTA
VALUES('72727279F','LEIRE','DE LUIS SAGARDOTEGUI',TO_DATE( '09-12-2022', 'DD-MM-YYYY' ),'15:30');
INSERT INTO ENTREVISTA
VALUES('72727270F','AINHOA','IPARRAGUIRRE CASTILLO',TO_DATE( '09-12-2022', 'DD-MM-YYYY' ),'16:00');
INSERT INTO ENTREVISTA
VALUES('72727271F','ALFONSO','PEREZ IRRAZABALAGA',TO_DATE( '09-12-2022', 'DD-MM-YYYY' ),'16:30');

INSERT INTO PRODUCTO
VALUES( '1','GALLETAS PERRO','200,00');
INSERT INTO PRODUCTO
VALUES( '2','GALLETAS GATO','300,00');
INSERT INTO PRODUCTO
VALUES( '3','GALLETAS BALLENA','100,00');
INSERT INTO PRODUCTO
VALUES( '4','PARACETAMOL DOMESTICOS','20,00');
INSERT INTO PRODUCTO
VALUES( '5','PARACETAMOL GRANJA','30,00');
INSERT INTO PRODUCTO
VALUES( '6','COLIRIO','140,00');
INSERT INTO PRODUCTO
VALUES( '7','VACUNA PERRO','25,00');
INSERT INTO PRODUCTO
VALUES( '8','VACUNA GATO','20,00');
INSERT INTO PRODUCTO
VALUES( '9','AGUA OXIGENADA','300,00');
INSERT INTO PRODUCTO
VALUES( '10','GASAS','100,00');

INSERT INTO PEDIDO
VALUES('1','20,00',TO_DATE('28-02-2022', 'DD-MM-YYYY'),'N','1');
INSERT INTO PEDIDO
VALUES('2','30,00',TO_DATE('30-03-2022', 'DD-MM-YYYY'),'N','2');
INSERT INTO PEDIDO
VALUES('3','10,00',TO_DATE('30-04-2022', 'DD-MM-YYYY'),'N','3');
INSERT INTO PEDIDO
VALUES('4','2,50',TO_DATE('30-05-2022', 'DD-MM-YYYY'),'N','4');
INSERT INTO PEDIDO
VALUES('5','0,50',TO_DATE('30-06-2022', 'DD-MM-YYYY'),'N','5');
INSERT INTO PEDIDO
VALUES('6','1,00',TO_DATE('30-07-2022', 'DD-MM-YYYY'),'N','6');
INSERT INTO PEDIDO
VALUES('7','100,00',TO_DATE('30-08-2022', 'DD-MM-YYYY'),'S','7');
INSERT INTO PEDIDO
VALUES('8','200,00',TO_DATE('30-09-2022', 'DD-MM-YYYY'),'S','8');
INSERT INTO PEDIDO
VALUES('9','150,00',TO_DATE('30-10-2022', 'DD-MM-YYYY'),'S','9');
INSERT INTO PEDIDO
VALUES('10','40,00',TO_DATE('30-11-2022', 'DD-MM-YYYY'),'S','10');