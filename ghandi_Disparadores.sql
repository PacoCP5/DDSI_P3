CREATE OR REPLACE TRIGGER facturaYaPagada
   BEFORE
   UPDATE
   ON FACTURA
   FOR EACH ROW
DECLARE
   facturaPagada INTEGER;
   errFacturaYaPagada EXCEPTION;
BEGIN
   SELECT COUNT(*) INTO facturaPagada
   FROM FACTURA WHERE IDFACTURA = :new.IDFACTURA AND PAGADO='S';
   IF facturaPagada = 1 THEN
       RAISE errFacturaYaPagada;
   END IF;
EXCEPTION
   WHEN errFacturaYaPagada THEN
       DBMS_OUTPUT.PUT_LINE('[ERROR] Factura ya pagada.');
       raise_application_error(-10121, :new.IDFACTURA || ' ya estaba pagada.');  
END;
/

CREATE OR REPLACE TRIGGER pedidoYaPagado
   BEFORE
   UPDATE
   ON PEDIDO
   FOR EACH ROW
DECLARE
   pedidoPagado INTEGER;
   errPedidoYaPagado EXCEPTION;
BEGIN
   SELECT PAGADO INTO pedidoPagado
   FROM PEDIDO WHERE IDPEDIDO = :new.IDPEDIDO;
   IF pedidoPagado = 1 THEN
       RAISE errPedidoYaPagado;
   END IF;
EXCEPTION
   WHEN errPedidoYaPagado THEN
       DBMS_OUTPUT.PUT_LINE('[ERROR] Pedido ya pagada.');
       raise_application_error(-10142, :new.IDPEDIDO || ' ya estaba pagado.');  
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
	errorSalario EXCEPTION;
BEGIN
	IF :new.SUELDO < 1000 THEN
		RAISE errorSalario;
	END IF;
EXCEPTION
    WHEN errorSalario THEN
        DBMS_OUTPUT.PUT_LINE('[ERROR] El salario debe ser superior a 1000 euros');
        raise_application_error(-10213,:new.DNI || ' tiene un salario menor del mínimo establecido.');
END;
/

create or replace TRIGGER citaLibre
   BEFORE
   INSERT OR UPDATE
   ON CITA
   FOR EACH ROW
DECLARE
   existecliente INTEGER;
   errorCliente EXCEPTION;
   errorDisponibilidad EXCEPTION;
   errorValores EXCEPTION;

BEGIN

    IF UPDATING('DNI') or UPDATING('DISPONIBILIDAD') THEN
        IF (:NEW.DNI IS NULL AND :NEW.DISPONIBILIDAD='N' ) OR (NOT :NEW.DNI IS NULL AND :NEW.DISPONIBILIDAD='Y') THEN
            RAISE errorValores;
        END IF;
    END IF;

    IF UPDATING('DNI') THEN
        IF NOT :NEW.DNI IS NULL THEN 
           SELECT COUNT(*) INTO existeCliente
           FROM CLIENTE WHERE DNI = :new.dni;
           IF existeCliente = 0 THEN
               RAISE errorCliente;
           END IF;
        END IF;
    END IF;
    IF UPDATING('DISPONIBILIDAD') THEN
        IF :NEW.DISPONIBILIDAD != 'N' AND :NEW.DISPONIBILIDAD != 'Y' THEN 

            RAISE errorDisponibilidad;

        END IF;
    END IF;

EXCEPTION
   WHEN errorCliente THEN
       DBMS_OUTPUT.PUT_LINE('[ERROR] Cliente unavailable');
       raise_application_error(-20324, 'El cliente ' || :new.DNI || ' no está registrado');  
    WHEN errorDisponibilidad THEN
       DBMS_OUTPUT.PUT_LINE('[ERROR] Disponibilidad mal');
       raise_application_error(-20325, 'El valor ' || :new.DISPONIBILIDAD || ' no es correcto');  
    WHEN errorValores THEN
       DBMS_OUTPUT.PUT_LINE('[ERROR] Valores mal');
       raise_application_error(-20326, 'Los valores de cita y dni no son consistentes');  

END;
/

CREATE OR REPLACE TRIGGER animalYaEnjaulado
   BEFORE
   INSERT OR UPDATE
   ON JAULA
   FOR EACH ROW
DECLARE
   animalRepetido INTEGER;
   errAnimalRepetido EXCEPTION;
BEGIN
   SELECT COUNT(*) INTO animalRepetido
   FROM JAULA WHERE IDANIMAL = :new.IDANIMAL;
   IF animalRepetido > 0 THEN
       RAISE errAnimalRepetido;
   END IF;
EXCEPTION
   WHEN errAnimalRepetido THEN
       DBMS_OUTPUT.PUT_LINE('[ERROR] El animal ya está asignado a una jaula');
       raise_application_error(-10441, :new.IDANIMAL || ' ya tiene una jaula asignada');  
END;
/

CREATE OR REPLACE TRIGGER clienteAltaAnimal
   BEFORE
   INSERT OR UPDATE
   ON ANIMAL
   FOR EACH ROW
DECLARE
   existeCliente INTEGER;
   errExisteCliente EXCEPTION;
BEGIN
   SELECT COUNT(*) INTO existeCliente
   FROM CLIENTE WHERE DNI = :new.DNI;
   IF existeCliente != 1 THEN
       RAISE errExisteCliente;
   END IF;
EXCEPTION
   WHEN errExisteCliente THEN
       DBMS_OUTPUT.PUT_LINE('[ERROR] No existe un Cliente asociado a ese DNI.');
       raise_application_error(-10511, :new.DNI || ' no existe.');  
END;
/