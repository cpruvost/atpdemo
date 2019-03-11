String tenancy_ocid = 'Test'

pipeline {
	environment { 
        VAULT_TOKEN = 'WdPdcgUA1XNy23MoiR8uuOWu'
    }
	
    agent any 
    stages {
        stage('Stage Init Atp Variables') {
            steps {
				
				tenancy_ocid = sh (
					script : 'curl --header "X-Vault-Token: ${VAULT_TOKEN}" --request GET http://130.61.125.123:8200/v1/secret/demoatp | jq .data.tenancy_ocid',
					returnStdout: true
				).trim()
                echo "${tenancy_ocid}"
            }
        }
    }
}
