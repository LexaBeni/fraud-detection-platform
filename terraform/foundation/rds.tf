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

resource "aws_db_instance" "main" {
  allocated_storage = 20
  engine = "mysql"
  engine_version = "8.4.9"
  instance_class = "db.t3.micro"
  username = "admin"
  password = var.db_password
  db_name = "fraud_detection"
  skip_final_snapshot  = true
  storage_encrypted = true
  max_allocated_storage = 1000
  monitoring_interval = 60
  enabled_cloudwatch_logs_exports = ["audit", "error", "general"]
  copy_tags_to_snapshot = true
}