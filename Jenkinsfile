pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            label 'docker-pipeline'
        }
    }
    stages {
        stage('Test') {
            steps {
                sh 'python partmanager/manage.py test ./partmanager'
            }
        }
            
    }
}
