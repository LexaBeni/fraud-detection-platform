resource "aws_ecr_repository" "streamlit" {
  name = "fraud-detection-streamlit"
}

resource "aws_ecr_repository" "fastapi" {
  name = "fastapi-fraud-detection"
}

resource "aws_ecs_cluster" "main" {
  name = "fraud-detection-cluster"

   configuration {
          execute_command_configuration {
            logging    = "DEFAULT"
          }
   }
}

