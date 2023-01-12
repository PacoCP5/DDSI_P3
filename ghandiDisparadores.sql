CREATE OR REPLACE TRIGGER facturaYaPagada
   BEFORE
   UPDATE
   ON FACTURA
   FOR EACH ROW
DECLARE
   PRAGMA AUTONOMOUS_TRANSACTION;
   facturaPagada INTEGER;
BEGIN
   SELECT COUNT(*) INTO facturaPagada FROM FACTURA 
   WHERE IDFACTURA = :new.IDFACTURA AND PAGADO='S';
   
   IF facturaPagada = 1 THEN
      raise_application_error(-10121, 'ERROR: Esta Factura ya estaba pagada');  
   END IF;
END;
/

CREATE OR REPLACE TRIGGER pedidoYaPagado
   BEFORE
   UPDATE
   ON PEDIDO
   FOR EACH ROW
DECLARE
   PRAGMA AUTONOMOUS_TRANSACTION;
   pedidoPagado INTEGER;
BEGIN
   SELECT COUNT(*) INTO pedidoPagado FROM PEDIDO 
   WHERE IDPEDIDO = :new.IDPEDIDO AND PAGADO='S';
   
   IF pedidoPagado = 1 THEN
      raise_application_error(-10121, 'ERROR: Este Pedido ya estaba pagada');  
   END IF;
END;
/

CREATE OR REPLACE TRIGGER contratoMayorEdad
    BEFORE 
    INSERT OR UPDATE 
    ON CONTRATO 
    FOR EACH ROW
DECLARE
	errorEdad EXCEPTION;
BEGIN
	IF DATEDIFF(year, :new.Fecha_Nacim, GETDATE()) < 18 THEN
		RAISE errorEdad;
	END IF;
EXCEPTION
    WHEN errorEdad THEN
        DBMS_OUTPUT.PUT_LINE('[ERROR] El nuevo empleado debe ser mayor de edad');
        raise_application_error(-10212, :new.DNI || ' es menor de edad');
END;
/

CREATE OR REPLACE TRIGGER contratoSalarioLegal
    BEFORE 
    INSERT OR UPDATE 
    ON CONTRATO 
    FOR EACH ROW
DECLARE
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
	IF :new.SUELDO < 1000 THEN
        raise_application_error(-10213, 'ERROR: El Salario debe ser mayor que el SMI');
	END IF;
END;
/

CREATE OR REPLACE TRIGGER citaLibre
   BEFORE
   UPDATE
   ON CITA
   FOR EACH ROW
DECLARE
   existecliente INTEGER;
BEGIN

    IF UPDATING('DNI') or UPDATING('DISPONIBILIDAD') THEN
        IF (:NEW.DNI IS NULL AND :NEW.DISPONIBILIDAD='N' ) OR (NOT :NEW.DNI IS NULL AND :NEW.DISPONIBILIDAD='Y') THEN
           raise_application_error(-20326, 'ERROR: Los valores de Cita y DNI no son consistentes');  
        END IF;
    END IF;

    IF UPDATING('DNI') THEN
        IF NOT :NEW.DNI IS NULL THEN 
           SELECT COUNT(*) INTO existeCliente
        FROM CLIENTE WHERE DNI = :new.dni;
           IF existeCliente = 0 THEN
              raise_application_error(-20324, 'ERROR: Ese Cliente no está registrado');  
           END IF;
        END IF;
    END IF;
    
    IF UPDATING('DISPONIBILIDAD') THEN
        IF :NEW.DISPONIBILIDAD != 'N' AND :NEW.DISPONIBILIDAD != 'Y' THEN 
           raise_application_error(-20325, 'ERROR: El valor de Disponibilidad no es correcto');  
        END IF;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER citaMismoDia
   BEFORE
   UPDATE
   ON CITA
   FOR EACH ROW
DECLARE
   PRAGMA AUTONOMOUS_TRANSACTION;
   clienteYaTeniaCita INTEGER;
BEGIN

    IF UPDATING('DNI') OR UPDATING('DISPONIBILIDAD') OR UPDATING('FECHAHORA') OR INSERTING THEN
        SELECT COUNT(*) INTO clienteYaTeniaCita FROM CITA 
        WHERE (TO_CHAR(FECHAHORA,'DD/MM/YY') LIKE TO_CHAR(:NEW.FECHAHORA,'DD/MM/YY') AND DNI = :NEW.DNI);
        
        IF clienteYaTeniaCita > 0 THEN
            raise_application_error(-20340, 'ERROR: Un Cliente solo puede tener 1 cita por dia');
        END IF;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER animalYaEnjaulado
   BEFORE
   INSERT OR UPDATE
   ON JAULA
   FOR EACH ROW
DECLARE
   PRAGMA AUTONOMOUS_TRANSACTION;
   animalRepetido INTEGER;
BEGIN
   SELECT COUNT(*) INTO animalRepetido
   FROM JAULA WHERE IDANIMAL = :new.IDANIMAL;
   
   IF animalRepetido > 0 THEN
      raise_application_error(-10441, 'ERROR: El Animal ya tiene una Jaula asignada');  
   END IF;
END;
/

CREATE OR REPLACE TRIGGER cantidadPedido
   BEFORE
   INSERT OR UPDATE
   ON PEDIDO
   FOR EACH ROW
DECLARE
   PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
   IF INSERTING OR UPDATING('cantidad') THEN
       IF :NEW.CANTIDAD <= 0 THEN
          raise_application_error(-10410, 'ERROR: La Cantidad de un Pedido debe ser positiva');         
       END IF;
   END IF;
END;
/

CREATE OR REPLACE TRIGGER cantidadProductoAlmacen
   BEFORE
   INSERT OR UPDATE
   ON PRODUCTO
   FOR EACH ROW
DECLARE
   PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
   IF INSERTING OR UPDATING('cantidad') THEN
       IF :NEW.CANTIDAD < 0 THEN
          raise_application_error(-10430, 'ERROR: La Cantidad de un Producto en el Almacén debe ser positiva o 0');         
       END IF;
   END IF;
END;
/

CREATE OR REPLACE TRIGGER clienteAltaAnimal
   BEFORE
   INSERT OR UPDATE
   ON ANIMAL
   FOR EACH ROW
DECLARE
   PRAGMA AUTONOMOUS_TRANSACTION;
   existeCliente INTEGER;
BEGIN
   SELECT COUNT(*) INTO existeCliente
   FROM CLIENTE WHERE DNI = :new.DNI;
   
   IF existeCliente != 1 THEN
      raise_application_error(-10511, 'ERROR: Ese Cliente no existe');  
   END IF;
END;
/
