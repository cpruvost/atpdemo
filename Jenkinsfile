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
			
				script {
					env.DATA =  sh returnStdout: true, script: 'curl --header "X-Vault-Token: ${VAULT_TOKEN}" --request GET http://${VAULT_SERVER_IP}:8200/v1/secret/${VAULT_SECRET_NAME} | jq .data'
					env.TENANCY_OCID = sh returnStdout: true, script: 'echo ${DATA}  | jq .tenancy_ocid | cut -d \'"\' -f 2'
					//env.USER_OCID = sh returnStdout: true, script: 'echo ${DATA}  | jq .user_ocid | cut -d \'"\' -f 2'
					//env.FINGERPRINT = sh returnStdout: true, script: 'echo ${DATA}  | jq .fingerprint | cut -d \'"\' -f 2'
					//env.API_PRIVATE_KEY = sh returnStdout: true, script: 'echo ${DATA}  | jq .api_private_key | cut -d \'"\' -f 2'
					//env.COMPARMENT_OCID = sh returnStdout: true, script: 'echo ${DATA}  | jq .compartment_ocid | cut -d \'"\' -f 2'
					//env.PUBLIC_KEY = sh returnStdout: true, script: 'echo ${DATA}  | jq .public_key | cut -d \'"\' -f 2'
					//env.PRIVATE_KEY = sh returnStdout: true, script: 'echo ${DATA}  | jq .private_key | cut -d \'"\' -f 2'
				}
				
                echo "TENANCY_OCID=${TENANCY_OCID}"
				//echo "USER_OCID=${USER_OCID}"
				//echo "FINGERPRINT=${FINGERPRINT}"
				//echo "API_PRIVATE_KEY=${API_PRIVATE_KEY}"
				//echo "COMPARTMENT_OCID=${COMPARTMENT_OCID}"
				//echo "PUBLIC_KEY=${PUBLIC_KEY}"
				//echo "PRIVATE_KEY=${PRIVATE_KEY}"
            }
        }
    }
}
