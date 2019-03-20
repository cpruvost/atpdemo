pipeline {
	agent any
	
	/*agent {
        docker { 
            image 'cpruvost/devops:latest'
            args '-u root:root'
        }
    }*/
	
	parameters {
        password(defaultValue: "WdPdcgUA1XNy23MoiR8uuOWu", description: 'What is the vault token ?', name: 'VAULT_TOKEN')
		string(defaultValue: "130.61.125.123", description: 'What is the vault server IP Address ?', name: 'VAULT_SERVER_IP')
		string(defaultValue: "demoatp", description: 'What is the vault secret name ?', name: 'VAULT_SECRET_NAME')  
		string(defaultValue: "atpdb", description: 'What is the database name ?', name: 'DATABASE_NAME')  
		string(defaultValue: "https://objectstorage.eu-frankfurt-1.oraclecloud.com/p/avJQClo6ZzbMBxkSBNfvXhkYdE8kSy2IEipcDViiBmI/n/oraseemeafrtech1/b/AtpDemo/o/terraform.tfstate", description: 'Where is stored the terraform state ?', name: 'TERRAFORM_STATE_URL')  
    }
	
	environment {
		VAULT_TOKEN = "${params.VAULT_TOKEN}"
		VAULT_SERVER_IP = "${params.VAULT_SERVER_IP}"
		VAULT_ADDR = "http://${params.VAULT_SERVER_IP}:8200"
		VAULT_SECRET_NAME = "${params.VAULT_SECRET_NAME}"
		TF_VAR_autonomous_database_db_name = "${params.DATABASE_NAME}"
		TF_CLI_ARGS = "-no-color"
		TF_VAR_terraform_state_url = "${params.TERRAFORM_STATE_URL}"
	}
	
    stages {
        stage('Init Atp Variables') {
            steps {
			
				script {
					sh 'whoami'
					sh 'pwd'
					//sh 'source ~/.bashrc' 
					sh 'terraform --version'
					sh '/home/tomcat/bin/oci --version'
					//sh '/root/bin/oci --version'
					sh '/usr/local/bin/vault --version'
					//sh 'vault --version'
					//sh '/opt/vault --version'
					sh 'curl --version'
					//sh 'echo "show version" > show_version.sql'
					//sh 'exit | /opt/sqlcl/bin/sql /nolog @./show_version.sql'
				
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
				echo "TF_VAR_terraform_state_url=${TF_VAR_terraform_state_url}"
				
				dir ('./tf/modules/atp') {
					script {
						sh '/usr/local/bin/vault kv get -field=api_private_key secret/demoatp | tr -d "\n" | base64 --decode > bmcs_api_key.pem'
						//sh 'vault kv get -field=api_private_key secret/demoatp | tr -d "\n" | base64 --decode > bmcs_api_key.pem'
						//sh '/opt/vault kv get -field=api_private_key secret/demoatp | tr -d "\n" | base64 --decode > bmcs_api_key.pem'
						env.TF_VAR_private_key_path = './bmcs_api_key.pem'
						sh 'ls'
						sh 'cat ./bmcs_api_key.pem'
					}
					
					echo "TF_VAR_private_key_path=${TF_VAR_private_key_path}"
				}
            }
        }
		
		stage('TF Plan Create Atp ') { 
            steps {
				dir ('./tf/modules/atp') {
					sh 'ls'
					//Bugg Remote backend
					//sh 'mv ./backend.tf ./backend.tf.donotuse'
					sh 'terraform init -input=false'
					//sh(script: "terraform init -input=false", returnStdout: true)
					//sh 'terraform init -input=false -backend-config="address=${TF_VAR_terraform_state_url}"'
					sh 'terraform plan -out myplan'
					//sh(script: "terraform plan", returnStdout: true)
				}
			}
		}
		
		stage('TF Apply Create Atp ') { 
            steps {
				dir ('./tf/modules/atp') {
					script {
						def deploy_validation = input(
							id: 'Deploy',
							message: 'Let\'s continue the deploy plan',
							type: "boolean")
							
						//Bugg terraform oci so replace by OciCli for the moment	
						//sh 'terraform apply -input=false -auto-approve "myplan"'
						
						sh 'rm -rf /home/tomcat/.oci/config'
						sh 'echo "[DEFAULT]" > /home/tomcat/.oci/config'
						sh 'echo "user=${TF_VAR_user_ocid}" >> /home/tomcat/.oci/config'
						sh 'echo "fingerprint=${TF_VAR_fingerprint}" >> /home/tomcat/.oci/config'
						sh 'echo "key_file=./bmcs_api_key.pem" >> /home/tomcat/.oci/config'
						sh 'echo "tenancy=${TF_VAR_tenancy_ocid}" >> /home/tomcat/.oci/config'
						sh 'echo "region=${TF_VAR_region}" >> /home/tomcat/.oci/config'
						sh 'cat /home/tomcat/.oci/config'
						
						sh '/home/tomcat/bin/oci db autonomous-database create --admin-password=AlphA_2014_! --compartment-id=${TF_VAR_compartment_ocid} --cpu-core-count=2 --data-storage-size-in-tbs=1 --db-name=AutoDbDevOps --display-name=Demo_InfraAsCode_ADW --license-model=BRING_YOUR_OWN_LICENSE --wait-for-state=AVAILABLE'
					}
				}
			}
		}
	}	
}
