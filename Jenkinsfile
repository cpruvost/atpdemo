pipeline {
	agent any 
	
	parameters {
        password(defaultValue: "WdPdcgUA1XNy23MoiR8uuOWu", description: 'What is the vault token ?', name: 'VAULT_TOKEN')
		string(defaultValue: "130.61.125.123", description: 'What is the vault server IP Address ?', name: 'VAULT_SERVER_IP')
		string(defaultValue: "demoatp", description: 'What is the vault secret name ?', name: 'VAULT_SECRET_NAME')  
		string(defaultValue: "atpdb", description: 'What is the database name ?', name: 'DATABASE_NAME')  
    }
	
	environment {
		VAULT_TOKEN = "${params.VAULT_TOKEN}"
		VAULT_SERVER_IP = "${params.VAULT_SERVER_IP}"
		VAULT_ADDR = "http://${params.VAULT_SERVER_IP}:8200"
		VAULT_SECRET_NAME = "${params.VAULT_SECRET_NAME}"
		TF_VAR_autonomous_database_db_name = "${params.DATABASE_NAME}"
		TF_CLI_ARGS = "-no-color"
	}
	
    stages {
        stage('Stage Init Atp Variables') {
            steps {
			
				script {
					sh 'whoami'
					sh 'source ~/.bashrc' 
					sh 'terraform --version'
					sh '/home/tomcat/bin/oci --version'
					sh '/usr/local/bin/vault --version'
					sh 'curl --version'
				
					env.DATA =  sh returnStdout: true, script: 'curl --header "X-Vault-Token: ${VAULT_TOKEN}" --request GET http://${VAULT_SERVER_IP}:8200/v1/secret/${VAULT_SECRET_NAME} | jq .data'
					env.TF_VAR_tenancy_ocid = sh returnStdout: true, script: 'echo ${DATA}  | jq .tenancy_ocid | cut -d \'"\' -f 2'
					env.TF_VAR_user_ocid = sh returnStdout: true, script: 'echo ${DATA}  | jq .user_ocid | cut -d \'"\' -f 2'
					env.TF_VAR_fingerprint = sh returnStdout: true, script: 'echo ${DATA}  | jq .fingerprint | cut -d \'"\' -f 2'
					env.api_private_key = sh returnStdout: true, script: 'echo ${DATA}  | jq .api_private_key | cut -d \'"\' -f 2'
					env.TF_VAR_compartment_ocid = sh returnStdout: true, script: 'echo ${DATA}  | jq .compartment_ocid | cut -d \'"\' -f 2'
					env.TF_VAR_ssh_public_key = sh returnStdout: true, script: 'echo ${DATA}  | jq .ssh_public_key | cut -d \'"\' -f 2'
					env.TF_VAR_ssh_private_key = sh returnStdout: true, script: 'echo ${DATA}  | jq .ssh_private_key | cut -d \'"\' -f 2'
					env.TF_VAR_region = sh returnStdout: true, script: 'echo ${DATA}  | jq .region | cut -d \'"\' -f 2'
				}
				
                echo "TF_VAR_tenancy_ocid=${TF_VAR_tenancy_ocid}"
				echo "TF_VAR_user_ocid=${TF_VAR_user_ocid}"
				echo "TF_VAR_fingerprint=${TF_VAR_fingerprint}"
				echo "api_private_key=${api_private_key}"
				echo "TF_VAR_compartment_ocid=${TF_VAR_compartment_ocid}"
				echo "TF_VAR_ssh_public_key=${TF_VAR_ssh_public_key}"
				echo "TF_VAR_ssh_private_key=${TF_VAR_ssh_private_key}"
				echo "TF_VAR_region=${TF_VAR_region}"
				
				dir ('./tf/modules/atp') {
					script {
						sh '/usr/local/bin/vault kv get -field=api_private_key secret/demoatp | tr -d "\n" | base64 --decode > bmcs_api_key.pem'
						env.TF_VAR_private_key_path = './bmcs_api_key.pem'
						sh 'ls'
						sh 'cat ./bmcs_api_key.pem'
					}
					
					echo "TF_VAR_private_key_path=${TF_VAR_private_key_path}"
				}
            }
        }
		
		stage('Stage TF Create Atp ') { 
            steps {
				dir ('./tf/modules/atp') {
					sh 'ls'
					sh 'terraform init'
					sh 'terraform plan -out myplan'
				}
				
				script {
					def userInput = input(id: 'confirm', message: 'Apply Terraform?', parameters: [ [$class: 'BooleanParameterDefinition', defaultValue: false, description: 'Apply terraform', name: 'confirm'] ])
				}
        }
    }
}
