data "aws_vpc" "main" {
  id = "vpc-01682372737f51f9d"
}

data "aws_subnets" "main" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }
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