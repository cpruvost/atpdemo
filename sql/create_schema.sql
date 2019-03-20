set serveroutput on;

DECLARE
    cnt NUMBER;
BEGIN
    SELECT Count(*)
    INTO   cnt
    FROM   all_users
    WHERE  USERNAME = 'MEDREC';

    IF cnt = 1 THEN
	
        dbms_output.put_line('User MEDREC Already Exists');   
    
    ELSE
		EXECUTE IMMEDIATE 'CREATE USER medrec IDENTIFIED BY ATPwelcome1234';
		EXECUTE IMMEDIATE 'GRANT DWROLE to medrec';
		
		dbms_output.put_line('User MEDREC Created');   
    END IF;
END;
/


