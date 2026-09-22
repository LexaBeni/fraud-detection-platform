data "aws_vpc" "main" {
  id = "vpc-01682372737f51f9d"
}

data "aws_subnets" "main" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }
}

resource "aws_security_group" "alb" {
  name        = "fraud-api-alb-sg"
  description = "security group for fraud-detection alb"
  vpc_id      = data.aws_vpc.main.id
}

resource "aws_security_group" "fastapi" {
  name        = "fraud-api-ecs-sg"
  description = "security group for fraud-detection ecs"
  vpc_id      = data.aws_vpc.main.id
}

resource "aws_vpc_security_group_ingress_rule" "fastapi" {
  security_group_id            = aws_security_group.fastapi.id
  referenced_security_group_id = "sg-066f821d15bebc3e8"
  from_port                    = 8000
  to_port                      = 8000
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "fastapi" {
  security_group_id = aws_security_group.fastapi.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_security_group" "streamlit" {
  name        = "fraud-streamlit-ecs-sg"
  description = "Security group for fraud streamlit application"
  vpc_id      = data.aws_vpc.main.id
}

resource "aws_vpc_security_group_ingress_rule" "streamlit" {
  security_group_id            = aws_security_group.streamlit.id
  to_port                      = 8501
  from_port                    = 8501
  ip_protocol                  = "tcp"
  referenced_security_group_id = "sg-066f821d15bebc3e8"
}

resource "aws_vpc_security_group_egress_rule" "streamlit" {
  security_group_id = aws_security_group.streamlit.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

/* resource "aws_security_group" "rds" {
  name        = "fraud-api-rds-sg"
  description = "security group for fraud-detection RDS"
  vpc_id      = data.aws_vpc.main.id
}

resource "aws_vpc_security_group_ingress_rule" "rds" {
  security_group_id            = aws_security_group.rds.id
  to_port                      = 3306
  from_port                    = 3306
  ip_protocol                  = "tcp"
  referenced_security_group_id = "sg-08ba2c3695a8a909f"
}

resource "aws_vpc_security_group_egress_rule" "rds" {
  security_group_id = aws_security_group.rds.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
} */