data "aws_vpc" "main" {
  id = "vpc-01682372737f51f9d"
}

data "aws_subnets" "main" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }
}

data "aws_security_group" "fastapi" {
  id = "sg-08ba2c3695a8a909f"
}

data "aws_security_group" "alb" {
  id = "sg-08e444fef6fe92788"
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
  referenced_security_group_id = data.aws_security_group.alb.id
}

resource "aws_vpc_security_group_egress_rule" "streamlit" {
  security_group_id = aws_security_group.streamlit.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}