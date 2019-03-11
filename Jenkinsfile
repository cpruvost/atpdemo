pipeline {
	agent any 
	
	parameters {
        password(defaultValue: "WdPdcgUA1XNy23MoiR8uuOWu", description: 'What is the vault token ?', name: 'VAULT_TOKEN')
		string(defaultValue: "130.61.125.123", description: 'What is the vault server IP Address ?', name: 'VAULT_SERVER_IP')
		string(defaultValue: "demoatp", description: 'What is the vault secret name ?', name: 'VAULT_SECRET_NAME')  
    }
	
	environment {
		VAULT_TOKEN = "${params.VAULT_TOKEN}"
		VAULT_SERVER_IP = "${params.VAULT_SERVER_IP}"
		VAULT_SECRET_NAME = "${params.VAULT_SECRET_NAME}"
	}
	
    stages {
        stage('Stage Init Atp Variables') {
            steps {
				
				echo "VAULT_TOKEN=${VAULT_TOKEN}"
			
				script {
					env.TENANCY_OCID = sh returnStdout: true, script: '''curl --header "X-Vault-Token: ${VAULT_TOKEN}" --request GET http://${VAULT_SERVER_IP}:8200/v1/secret/${VAULT_SECRET_NAME} | jq .data.tenancy_ocid'''
				}
				
                echo "TENANCY_OCID=${TENANCY_OCID}"
            }
        }
    }
}
