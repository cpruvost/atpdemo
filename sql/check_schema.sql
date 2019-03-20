set echo off head off feed off pagesize 0 trimspool on linesize 1000 colsep
spool result.test
SELECT Count(*) FROM all_users WHERE  USERNAME = 'MEDREC';
spool off;