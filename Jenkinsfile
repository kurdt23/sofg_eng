pipeline {
// Запрет одновременного запуска разных сборок
properties([disableConcurrentBuilds()])

    // Использование Docker в качестве агента
    agent {
        docker {
            // Docker file attached below. Image pushed to dockerhub
            image 'efimovaleksey/mlops:stable'
            args '-u root:sudo '
        }
    }

//     environment {
//         JENKINS_HOME = "$JENKINS_HOME"
//         BUILD = "${JENKINS_HOME}/workspace/mlops_final"
//     }

    stages {
         stage('Start') {
            steps {
                script {
                    echo 'Начало работы скриптов.'
                }
            }
        }
        stage('Preparation') {
            steps {
                // Очистка рабочего пространства
                cleanWs()
                checkout scm
            }
        }

        stage('Checkout') {
            steps {
                script {
                    // Клонирование репозитория Git
                    git branch: 'main', url: 'https://github.com/kurdt23/sofg_eng'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                // Установка зависимостей
                script {
                    if (isUnix()) {
                        sh 'chmod +x install.sh && ./install.sh'
                        sh './venv/scripts/activate.bat'
                    } else {
                        bat 'install.bat'
                        bat '.\\venv\\scripts\\activate.bat'
                    }
                }
            }
        }

        stage('Install DVC and Sync Data') {
            steps {
                // Установка DVC и конфигурация удаленного хранилища
                sh 'pip install dvc-gdrive'

                // Копирование секретного файла для DVC
		        withCredentials([file(credentialsId: 'gdrive', variable: 'gdrive')]) {
		            sh "cp $gdrive $WORKSPACE/gdrive.json"
		        }

                // Модификация удаленного хранилища DVC с использованием секретного файла
                sh "dvc remote modify myremote --local gdrive_user_credentials_file $WORKSPACE/gdrive.json"

                sh 'dvc pull'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest tests/'
            }
        }


        stage('Build Docker image') {
            steps {
                 script {
                    // Для Линукс
                    if (isUnix()) {
                        sh 'docker build -t sof_eng .'
                    } else {
                        bat "docker build -t sof_eng -f Dockerfile ."
                    }
                 }
            }
        }

        stage('Push Docker Image') {
            steps {
                // Логин в DockerHub и пуш Docker образа
                withCredentials([string(credentialsId: 'dockerhub-credentials', variable: 'DOCKERHUB_PASSWORD')]) {
                    sh 'docker login -u kurdt23 -p $DOCKERHUB_PASSWORD'
                    sh 'docker push kurdt23/sof_eng'
                }
            }
        }

        stage('Finish') {
            steps {
                script {
                    echo 'Работа скриптов завершена успешно'
                }
            }
        }

        post {
            always {
                cleanWs()
            }
        }
    }
}