pipeline {


agent any


environment {


IMAGE_NAME="localhost:8082/docker-hosted/python-mongo-app"


IMAGE_TAG="${BUILD_NUMBER}"


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



stage('Install Dependencies') {


steps {


sh """

python3 -m venv venv

. venv/bin/activate

pip install -r requirements.txt

"""


}


}



stage('Unit Test') {


steps {


sh """

. venv/bin/activate

pytest

"""


}


}



stage('SonarQube Analysis') {


steps {


withSonarQubeEnv('sonarqube') {


sh """

sonar-scanner \

-Dsonar.projectKey=python-mongo-app \

-Dsonar.sources=. \

-Dsonar.python.coverage.reportPaths=coverage.xml


"""


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

credentialsId:'nexus-creds',

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

usernamePassword(

credentialsId:'mongo-password',

usernameVariable:'MONGO_USER',

passwordVariable:'MONGO_PASS'

)

]){


sh """

docker rm -f python-app || true


docker rm -f mongo || true



docker run -d \

--name mongo \

--network devops \

-e MONGO_INITDB_ROOT_USERNAME=$MONGO_USER \

-e MONGO_INITDB_ROOT_PASSWORD=$MONGO_PASS \

mongo:7.0.9



sleep 20



docker run -d \

--name python-app \

--network devops \

-p 5000:5000 \

-e MONGO_DB_HOSTNAME=mongo \

-e MONGO_DB_USERNAME=$MONGO_USER \

-e MONGO_DB_PASSWORD=$MONGO_PASS \

${IMAGE_NAME}:${IMAGE_TAG}


"""


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