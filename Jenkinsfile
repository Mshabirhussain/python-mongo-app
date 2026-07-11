pipeline {


agent any

 

environment {


IMAGE_NAME="localhost:8082/docker-hosted/python-mongo-app"


IMAGE_TAG="${BUILD_NUMBER}"

SONAR_HOME = tool 'SonarScanner'


}


options {


timeout(
time:30,
unit:'MINUTES'
)


buildDiscarder(
logRotator(
numToKeepStr:'10'
)
)


}


stages {



stage('Checkout') {


steps {

checkout scm

}

}

stage('Unit Test') {
    steps {
        sh '''
        docker run --rm \
        --volumes-from $(hostname) \
        python:3.12 \
        sh -c "
            cd /var/jenkins_home/workspace/python-mongodb-pipeline &&
            pip install -r requirements.txt &&
            pytest
        "
        '''
    }
}

stage('Debug Sonar Mount') {
    steps {
        sh '''
        echo "Jenkins workspace:"
        pwd
        ls -la

        echo "Inside scanner container:"
        docker run --rm \
        -v $WORKSPACE:/usr/src \
        -w /usr/src \
        sonarsource/sonar-scanner-cli \
        sh -c "pwd && ls -la"
        '''
    }
}


stage('SonarQube Analysis') {

    steps {

        withCredentials([
            string(
                credentialsId: 'sonar-token',
                variable: 'SONAR_TOKEN'
            )
        ]) {

            sh '''
            docker run --rm \
            --network devops \
            --volumes-from jenkins \
            -w /var/jenkins_home/workspace/python-mongodb-pipeline \
            sonarsource/sonar-scanner-cli \
            -Dsonar.projectKey=python-mongo-app \
            -Dsonar.sources=app \
            -Dsonar.host.url=http://sonarqube:9000 \
            -Dsonar.token=$SONAR_TOKEN
            '''

        }

    }
}


stage('Docker Build') {


steps {


sh """

docker build \
-t ${IMAGE_NAME}:${IMAGE_TAG} .


"""


}


}



stage('Push Nexus') {


steps {


withCredentials([

usernamePassword(

credentialsId:'nexus-docker-creds',

usernameVariable:'USER',

passwordVariable:'PASS'

)

]){


sh """

echo $PASS | docker login localhost:8082 \
-u $USER \
--password-stdin


docker push ${IMAGE_NAME}:${IMAGE_TAG}


"""


}


}


}



stage('Deploy') {


steps {


withCredentials([
                    string(credentialsId: 'mongo-password', variable: 'MONGO_PASS')
                ]){


sh '''
docker rm -f python-app || true
docker rm -f mongo || true

docker run -d \
  --name mongo \
  --network devops \
  -e MONGO_INITDB_ROOT_USERNAME=devdb \
  -e MONGO_INITDB_ROOT_PASSWORD=$MONGO_PASS \
  mongo:7.0.9

sleep 20

docker run -d \
  --name python-app \
  --network devops \
  -p 5000:5000 \
  -e MONGO_DB_HOSTNAME=mongo \
  -e MONGO_DB_USERNAME=devdb \
  -e MONGO_DB_PASSWORD=$MONGO_PASS \
  ${IMAGE_NAME}:${IMAGE_TAG}
'''

}


}


}


}



post {


success {


echo "Python deployment successful"

}


failure {


echo "Pipeline failed"

}


}


}
