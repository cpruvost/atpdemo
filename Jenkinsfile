pipeline {
	agent any 
	
	parameters {
        string(defaultValue: "WdPdcgUA1XNy23MoiR8uuOWu", description: 'What is the vault token ?', name: 'VAULT_TOKEN')
		string(defaultValue: "130.61.125.123", description: 'What is the vault server IP Address ?', name: 'VAULT_SERVER_IP')
		string(defaultValue: "demoatp", description: 'What is the vault secret name ?', name: 'VAULT_SECRET_NAME')  
    }
	
	environment {
		VAULT_TOKEN ="${params.VAULT_TOKEN}"
	}
	
    stages {
        stage('Stage Init Atp Variables') {
            steps {
				
				echo "VAULT_TOKEN=${params.VAULT_TOKEN}"
			
				script {
					env.TENANCY_OCID = sh returnStdout: true, script: '''curl --header "X-Vault-Token: ${params.VAULT_TOKEN}" --request GET http://130.61.125.123:8200/v1/secret/demoatp | jq .data.tenancy_ocid | sed "s/\"//g"'''
				}
				
                echo "TENANCY_OCID=${TENANCY_OCID}"
            }
        }
    }
}
