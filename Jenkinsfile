pipeline {
	def tenancy_ocid = 'Test'

    agent any 
    stages {
        stage('Stage Init Atp Variables') {
            steps {
                echo $tenancy_ocid
            }
        }
    }
}
