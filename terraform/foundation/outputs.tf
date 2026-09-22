output "fastapi_ecr_repository_url" {
  value = aws_ecr_repository.fastapi.repository_url
}

output "streamlit_ecr_repository_url"{
    value = aws_ecr_repository.streamlit.repository_url
}