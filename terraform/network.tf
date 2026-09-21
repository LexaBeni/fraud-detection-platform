data "aws_vpc" "main" {
  id = "vpc-01682372737f51f9d"
}

data "aws_subnets" "main" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }
}
