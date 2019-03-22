# Copyright (c) 2018 Oracle and/or its affiliates. All rights reserved.
#
# WLST Offline for deploying medrec Datasource
#
# author: Christophe Pruvost
# since: March,2019
#
#startEdit()

# Read Domain in Offline Mode
# ===========================
readDomain('/u01/oracle/user_projects/domains/domain1')

# Create Datasource
# ==================
cd('/')
create(dsname, 'JDBCSystemResource')

cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
cmo.setName(dsname)

cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
create('myJdbcDataSourceParams','JDBCDataSourceParams')
cd('JDBCDataSourceParams/NO_NAME_0')
set('JNDIName', java.lang.String(dsjndiname))
set('GlobalTransactionsProtocol', java.lang.String('None'))

cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
create('myJdbcDriverParams','JDBCDriverParams')
cd('JDBCDriverParams/NO_NAME_0')
set('DriverName', dsdriver)
set('URL', dsurl)
set('PasswordEncrypted', dspassword)
set('UseXADataSourceInterface', 'false')

print 'create JDBCDriverParams Properties'
create('myProperties','Properties')
cd('Properties/NO_NAME_0')
create('oracle.net.tns_admin','Property')
cd('Property/oracle.net.tns_admin')
set('Value', dstnsadmin)

cd('../../')
create('oracle.net.ssl_version','Property')
cd('Property/oracle.net.ssl_version')
set('Value', dssslversion)

cd('../../')
create('javax.net.ssl.trustStore','Property')
cd('Property/javax.net.ssl.trustStore')
set('Value', dstrustore)

cd('../../')
create('oracle.net.ssl_server_dn_match','Property')
cd('Property/oracle.net.ssl_server_dn_match')
set('Value', dsdnmatch)

cd('../../')
create('user','Property')
cd('Property/user')
set('Value', dsusername)

cd('../../')
create('javax.net.ssl.keyStoreType','Property')
cd('Property/javax.net.ssl.keyStoreType')
set('Value', dskeystoretype)

cd('../../')
create('javax.net.ssl.trustStoreType','Property')
cd('Property/javax.net.ssl.trustStoreType')
set('Value', dstruststoretype)

cd('../../')
create('javax.net.ssl.keyStore','Property')
cd('Property/javax.net.ssl.keyStore')
set('Value', dskeystore)

cd('../../')
create('javax.net.ssl.keyStorePassword','Property')
cd('Property/javax.net.ssl.keyStorePassword')
set('Value', dskeystorepassword)

cd('../../')
create('javax.net.ssl.trustStorePassword','Property')
cd('Property/javax.net.ssl.trustStorePassword')
set('Value', dstruestorepassword)

cd('../../')
create('oracle.jdbc.fanEnabled','Property')
cd('Property/oracle.jdbc.fanEnabled')
set('Value', dsfanenabled)

print 'create JDBCConnectionPoolParams'
cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
create('myJdbcConnectionPoolParams','JDBCConnectionPoolParams')
cd('JDBCConnectionPoolParams/NO_NAME_0')
set('TestTableName',dstestquery)

# Assign
# ======
assign('JDBCSystemResource', dsname, 'Target', dsserver)

# Update Domain, Close It, Exit
# ==========================
updateDomain()
closeDomain()
exit()

#activate()

#startEdit()
