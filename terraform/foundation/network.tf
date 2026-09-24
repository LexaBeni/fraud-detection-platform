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

resource "aws_vpc_security_group_ingress_rule" "alb_fastapi" {
  security_group_id = aws_security_group.alb.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = 80
  to_port           = 80
}

resource "aws_vpc_security_group_ingress_rule" "alb_streamlit" {
  security_group_id = aws_security_group.alb.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = 8501
  to_port           = 8501
}
resource "aws_vpc_security_group_egress_rule" "alb" {
  security_group_id = aws_security_group.alb.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_security_group" "fastapi" {
  name        = "fraud-api-ecs-sg"
  description = "security group for fraud-detection ecs"
  vpc_id      = data.aws_vpc.main.id
}

resource "aws_vpc_security_group_ingress_rule" "fastapi" {
  security_group_id            = aws_security_group.fastapi.id
  referenced_security_group_id = aws_security_group.alb.id
  from_port                    = 8000
  to_port                      = 8000
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "fastapi" {
  security_group_id = aws_security_group.fastapi.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}