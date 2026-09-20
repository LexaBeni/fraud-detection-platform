variable "aws_region" {
  type = string
  default = "eu-central-1"
}

variable "fastapi_image"{
  type = string
  default = "773658094755.dkr.ecr.eu-central-1.amazonaws.com/fastapi-fraud-detection:e3c5d17b19c10f0e4ea6955b84be786c7fe5c51a"
}