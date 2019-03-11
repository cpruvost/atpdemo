String tenancy_ocid = 'Test'

pipeline {
	environment { 
        VAULT_TOKEN = 'WdPdcgUA1XNy23MoiR8uuOWu'
    }
	
    agent any 
    stages {
        stage('Stage Init Atp Variables') {
            steps {
				try {
					// Fails with non-zero exit if dir1 does not exist
					def dir1 = sh(script:'ls -la', returnStdout:true).trim()
				} catch (Exception ex) {
					println("Unable to read dir1: ${ex}")
				}
			
				//tenancy_ocid = sh 'curl --header "X-Vault-Token: ${VAULT_TOKEN}" --request GET http://130.61.125.123:8200/v1/secret/demoatp | jq .data.tenancy_ocid'
                echo "${tenancy_ocid}"
            }
        }
    }
}
