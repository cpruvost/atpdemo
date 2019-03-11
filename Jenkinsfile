pipeline {
	environment { 
        VAULT_TOKEN = 'WdPdcgUA1XNy23MoiR8uuOWu'
    }
	
    agent any 
    stages {
        stage('Stage Init Atp Variables') {
            steps {
				env.TENANCY_OCID = sh returnStdout: true, script: '''curl --header "X-Vault-Token: ${VAULT_TOKEN}" --request GET http://130.61.125.123:8200/v1/secret/demoatp | jq .data.tenancy_ocid'''
				
                echo "${TENANCY_OCID}"
            }
        }
    }
}
