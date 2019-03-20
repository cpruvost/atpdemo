pipeline {
	//agent by default
	agent any
	
	//use a docker image instead of the jenkins host
	/*agent {
        docker { 
            image 'cpruvost/devops:latest'
            args '-u root:root'
        }
    }*/
	
	//Parameters of the pipeline. You can define more parameters in this pipeline in order to have less hard code variables.
	parameters {
        password(defaultValue: "WdPdcgUA1XNy23MoiR8uuOWu", description: 'What is the vault token ?', name: 'VAULT_TOKEN')
		string(defaultValue: "130.61.125.123", description: 'What is the vault server IP Address ?', name: 'VAULT_SERVER_IP')
		string(defaultValue: "demoatp", description: 'What is the vault secret name ?', name: 'VAULT_SECRET_NAME')  
		string(defaultValue: "atpdb", description: 'What is the database name ?', name: 'DATABASE_NAME') 
		password(defaultValue: "AlphA_2014_!", description: 'What is the database password ?', name: 'DATABASE_PASSWORD')  		
		string(defaultValue: "https://objectstorage.eu-frankfurt-1.oraclecloud.com/p/avJQClo6ZzbMBxkSBNfvXhkYdE8kSy2IEipcDViiBmI/n/oraseemeafrtech1/b/AtpDemo/o/terraform.tfstate", description: 'Where is stored the terraform state ?', name: 'TERRAFORM_STATE_URL')  
    }
	
	//Load the parameters as environment variables
	environment {
		VAULT_TOKEN = "${params.VAULT_TOKEN}"
		VAULT_SERVER_IP = "${params.VAULT_SERVER_IP}"
		VAULT_ADDR = "http://${params.VAULT_SERVER_IP}:8200"
		VAULT_SECRET_NAME = "${params.VAULT_SECRET_NAME}"
		TF_VAR_autonomous_database_db_name = "${params.DATABASE_NAME}"
		TF_VAR_database_password = "${params.DATABASE_PASSWORD}"
		TF_CLI_ARGS = "-no-color"
		TF_VAR_terraform_state_url = "${params.TERRAFORM_STATE_URL}"
		
		//Update env variables for sqlcl oci option. You can improve that.
		TNS_ADMIN = "./"
        LD_LIBRARY_PATH = "/opt/instantclient_18_5"
	}
	
    stages {
        stage('Init Atp Variables') {
            steps {
			
				script {
					sh 'whoami'
					sh 'pwd'
					
					//Check that our tools for pipeline are all there. Note that Jenkins uses sh and that we lost some alias of bash. You can improve that point.
					sh 'terraform --version'
					
					//paths with jenkins host.
					sh '/home/tomcat/bin/oci --version'
					sh '/usr/local/bin/vault --version'
					//sh 'echo "show version" > show_version.sql'
					sh 'exit | /opt/sqlcl/bin/sql /nolog @./sql/show_version.sql'
					
					//paths with docker image. 
					//sh '/root/bin/oci --version'
					//sh '/opt/vault --version'
					//sh 'echo "show version" > show_version.sql'
					//sh 'exit | /opt/sqlcl/bin/sql /nolog @./show_version.sql'
					
					sh 'curl --version'
					sh 'jq --version'
					sh 'docker --version'
				
					//Get all cloud information needed from Hachicorp Vault.
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
						//Get the API key File with vault client because curl breaks the end line of the key file
						
						//paths with jenkins host.
						sh '/usr/local/bin/vault kv get -field=api_private_key secret/demoatp | tr -d "\n" | base64 --decode > bmcs_api_key.pem'
						
						//paths with docker.
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
					
					//Terraform initialization in order to get oci plugin provider	
					sh 'terraform init -input=false -backend-config="address=${TF_VAR_terraform_state_url}"'
					
					//Terraform plan
					sh 'terraform plan -out myplan'
				}
			}
		}
		
		stage('TF Apply Create Atp ') { 
            steps {
				dir ('./tf/modules/atp') {
					script {
						//Ask Question in order to apply terraform plan or not
						def deploy_validation = input(
							id: 'Deploy',
							message: 'Let\'s continue the deploy plan',
							type: "boolean")
							
						//Bugg terraform oci when run by jenkins so we used OciCli for the moment. Later we will update this pipeline in order to use only terraform.	
						//sh 'terraform apply -input=false -auto-approve "myplan"'
						
						//OCI CLI Setup
						sh 'rm -rf /home/tomcat/.oci/config'
						sh 'echo "[DEFAULT]" > /home/tomcat/.oci/config'
						sh 'echo "user=${TF_VAR_user_ocid}" >> /home/tomcat/.oci/config'
						sh 'echo "fingerprint=${TF_VAR_fingerprint}" >> /home/tomcat/.oci/config'
						sh 'echo "key_file=./bmcs_api_key.pem" >> /home/tomcat/.oci/config'
						sh 'echo "tenancy=${TF_VAR_tenancy_ocid}" >> /home/tomcat/.oci/config'
						sh 'echo "region=${TF_VAR_region}" >> /home/tomcat/.oci/config'
						sh 'cat /home/tomcat/.oci/config'
						
						//OCI CLI permissions mandatory on some files.
						sh '/home/tomcat/bin/oci setup repair-file-permissions --file ./bmcs_api_key.pem'
						sh '/home/tomcat/bin/oci setup repair-file-permissions --file /home/tomcat/.oci/config'
						
						//Check if Db is already there
						sh '/home/tomcat/bin/oci db autonomous-database list --compartment-id=${TF_VAR_compartment_ocid} --display-name=Demo_InfraAsCode_ATW | jq ". | length" > result.test'	
						env.CHECK_DB = sh (script: 'cat ./result.test', returnStdout: true).trim()
						sh 'echo ${CHECK_DB}'
						
						script {
							if (env.CHECK_DB == "1") {
								echo "Db Already Exists"
								//sh '/home/tomcat/bin/oci db autonomous-database list --compartment-id=${TF_VAR_compartment_ocid} --display-name=Demo_InfraAsCode_ATW | jq .data[0].id | cut -d \'"\' -f 2 > result.test'	
								//env.DB_OCID = sh (script: 'cat ./result.test', returnStdout: true).trim()
								//Get atp wallet
								//sh '/home/tomcat/bin/oci db autonomous-database generate-wallet --autonomous-database-id=${DB_OCID} --password=${TF_VAR_database_password} --file=./myatpwallet.zip'
							}
							else {
								echo "Go Create Db"
								sh '/home/tomcat/bin/oci db autonomous-database create --admin-password=${TF_VAR_database_password} --compartment-id=${TF_VAR_compartment_ocid} --cpu-core-count=1 --data-storage-size-in-tbs=1 --db-name=${TF_VAR_autonomous_database_db_name} --display-name=Demo_InfraAsCode_ATW --license-model=BRING_YOUR_OWN_LICENSE --wait-for-state=AVAILABLE'
							}
							
							//Get atp wallet
							sh '/home/tomcat/bin/oci db autonomous-database list --compartment-id=${TF_VAR_compartment_ocid} --display-name=Demo_InfraAsCode_ATW | jq .data[0].id | cut -d \'"\' -f 2 > result.test'	
							env.DB_OCID = sh (script: 'cat ./result.test', returnStdout: true).trim()
							sh '/home/tomcat/bin/oci db autonomous-database generate-wallet --autonomous-database-id=${DB_OCID} --password=${TF_VAR_database_password} --file=./myatpwallet.zip'
						}
						
						sh 'ls'
					}
				}
			}
		}
		
		stage('Create Schema in Atp') {
            steps {
                dir ('./sql') {
                    sh 'pwd'
                    sh 'cp ../tf/modules/atp/myatpwallet.zip ./'
					sh 'unzip -o ./myatpwallet.zip'
					sh 'ls'
					//Prepare sqlcl oci option
					sh 'echo $TNS_ADMIN'
					sh 'rm -rf ./sqlnet.ora'
					sh 'mv ./sqlnet.ora.ref ./sqlnet.ora'
					sh 'cat ./tnsnames.ora'
                    sh 'cat ./sqlnet.ora'
					//Check Connection to Atp
					sh 'exit | /opt/sqlcl/bin/sql -oci admin/${TF_VAR_database_password}@atpdb_HIGH @./show_version.sql'
					//Create schema in Atp
					sh 'exit | /opt/sqlcl/bin/sql -oci admin/${TF_VAR_database_password}@atpdb_HIGH @./check_schema.sql'
					sh 'ls'
					sh 'cat ./result.test'
					sh (script: 'cat ./result.test', returnStdout: true).trim()
                }
            }
        }
		
	}	
}
