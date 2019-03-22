# Copyright (c) 2018 Oracle and/or its affiliates. All rights reserved.
#
# WLST Offline for deploying medrec Datasource
#
# author: Christophe Pruvost
# since: March,2019
#
#startEdit()

print('wlsserver  : [%s]' % wlsserver);

# Read Domain in Offline Mode
# ===========================
readDomain('/u01/oracle/user_projects/domains/domain1')

# Create a JMS Server
# ===================
cd('/')
myjmsserver=create(jmsserver, 'JMSServer')
print('Create JMSServer : [%s]' % jmsserver)

cd('/JMSServers/' + jmsserver)

cd('/')
assign('JMSServer', jmsserver, 'Target', wlsserver)

# Create a JMS System resource
# ============================
cd('/')
myjmsresource=create(jmsresource, 'JMSSystemResource')
cd('JMSSystemResource/' + jmsresource + '/JmsResource/NO_NAME_0')

# Create a JMS Queue and its subdeployment
# ========================================
myq = create(jmsqueue,'Queue')
myq.setJNDIName(jmsjndiqueue)
myq.setSubDeploymentName(jmssubdeployment)

cd('/JMSSystemResource/' + jmsresource)
create(jmssubdeployment, 'SubDeployment')

cd('/')
assign('JMSSystemResource.SubDeployment', jmsresource + '.' + jmssubdeployment, 'Target', jmsserver)

# Create a JMS Connection Factory
# ===============================
cd('/')
cd('JMSSystemResource/' + jmsresource + '/JmsResource/NO_NAME_0')

mycf = create(jmsconnfactory,'ConnectionFactory')
mycf.setJNDIName(jmsjndiconnfactory)
mycf.setDefaultTargetingEnabled(true)

# Update Domain, Close It, Exit
# ==========================
updateDomain()
closeDomain()
exit()
