resource "aws_security_group" "rds" {
  name        = "fraud-api-rds-sg"
  description = "security group for fraud-detection RDS"
  vpc_id      = data.aws_vpc.main.id
}

resource "aws_vpc_security_group_ingress_rule" "rds" {
  security_group_id            = aws_security_group.rds.id
  to_port                      = 3306
  from_port                    = 3306
  ip_protocol                  = "tcp"
  referenced_security_group_id = aws_security_group.fastapi.id
}

resource "aws_vpc_security_group_egress_rule" "rds" {
  security_group_id = aws_security_group.rds.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}