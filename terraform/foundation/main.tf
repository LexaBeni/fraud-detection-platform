resource "aws_ecr_repository" "streamlit" {
  name = "fraud-detection-streamlit"
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_ecr_repository" "fastapi" {
  name = "fastapi-fraud-detection"
  lifecycle {
    prevent_destroy = true
  }
}