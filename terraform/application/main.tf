resource "aws_ecs_cluster" "main" {
  name = "fraud-detection-cluster"

  configuration {
    execute_command_configuration {
      logging = "DEFAULT"
    }
  }
}

resource "aws_ecs_task_definition" "streamlit" {
  family                   = "fraud-streamlit"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  runtime_platform {
    cpu_architecture        = "X86_64"
    operating_system_family = "LINUX"
  }
  execution_role_arn = "arn:aws:iam::773658094755:role/ecsTaskExecutionRole-fraud-api"
  task_role_arn      = "arn:aws:iam::773658094755:role/ecsTaskExecutionRole-fraud-api"
  container_definitions = jsonencode([
    { name      = "streamlit"
      image     = var.streamlit_image
      cpu       = 0
      essential = true
      portMappings = [{
        containerPort = 8501
        hostPort      = 8501
        "protocol"    = "tcp"
        "name"        = "main-8501-tcp"
        "appProtocol" = "http"
      }]
      secrets = [
        {
          name      = "API_URL",
          valueFrom = "arn:aws:ssm:eu-central-1:773658094755:parameter/fraud-api/API_URL"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = "/ecs/fraud-streamlit",
          awslogs-create-group  = "true",
          awslogs-region        = "eu-central-1",
          awslogs-stream-prefix = "ecs"
      } }
  }])
}

resource "aws_ecs_task_definition" "fastapi" {
  family                   = "fraud-api"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  runtime_platform {
    cpu_architecture        = "X86_64"
    operating_system_family = "LINUX"
  }
  execution_role_arn = "arn:aws:iam::773658094755:role/ecsTaskExecutionRole-fraud-api"
  task_role_arn      = "arn:aws:iam::773658094755:role/ecsTaskExecutionRole-fraud-api"
  container_definitions = jsonencode([
    { name      = "fraud-api"
      image     = var.fastapi_image
      cpu       = 0
      essential = true
      portMappings = [{
        containerPort = 8000
        hostPort      = 8000
        "protocol"    = "tcp"
        "name"        = "fraud-api-8000-tcp"
        "appProtocol" = "http"
      }]
      secrets = [
        {
          name      = "ACCESS_TOKEN_EXPIRES_MINUTES"
          valueFrom = "arn:aws:ssm:eu-central-1:773658094755:parameter/fraud-api/ACCESS_TOKEN_EXPIRES_MINUTES"
        },
        {
          name      = "ADMIN_EMAIL"
          valueFrom = "arn:aws:ssm:eu-central-1:773658094755:parameter/fraud-api/ADMIN_EMAIL"
        },
        {
          name      = "ADMIN_PASSWORD"
          valueFrom = "arn:aws:ssm:eu-central-1:773658094755:parameter/fraud-api/ADMIN_PASSWORD"
        },
        {
          name      = "DATABASE_SERVER_URL"
          valueFrom = "/fraud-api/DATABASE_SERVER_URL"
        },
        {
          name      = "DATABASE_URL"
          valueFrom = "arn:aws:ssm:eu-central-1:773658094755:parameter/fraud-api/DATABASE_URL"
        },
        {
          name      = "JWT_ALGORITHM"
          valueFrom = "arn:aws:ssm:eu-central-1:773658094755:parameter/fraud-api/JWT_ALGORITHM"
        },
        {
          name      = "JWT_SECRET_KEY"
          valueFrom = "arn:aws:ssm:eu-central-1:773658094755:parameter/fraud-api/JWT_SECRET_KEY"
        },
        {
          name      = "MODEL_PATH"
          valueFrom = "arn:aws:ssm:eu-central-1:773658094755:parameter/fraud-api/MODEL_PATH"
        },
        {
          name      = "REFRESH_TOKEN_EXPIRES_DAYS"
          valueFrom = "arn:aws:ssm:eu-central-1:773658094755:parameter/fraud-api/REFRESH_TOKEN_EXPIRES_DAYS"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = "/ecs/fraud-api",
          awslogs-create-group  = "true",
          awslogs-region        = "eu-central-1",
          awslogs-stream-prefix = "ecs"
      } }
  }])
}

resource "aws_alb_target_group" "fastapi" {
  name        = "fraud-api-tg"
  port        = 8000
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = data.aws_vpc.main.id
}

resource "aws_alb_target_group" "streamlit" {
  name        = "fraud-streamlit-tg"
  port        = 8501
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = data.aws_vpc.main.id
}

resource "aws_lb" "main" {
  name               = "fraud-detection-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = data.aws_subnets.main.ids
}

resource "aws_lb_listener" "fastapi" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.fastapi.arn
    forward {
      target_group {
        arn = aws_alb_target_group.fastapi.arn
      }
      stickiness {
        duration = 3600
        enabled  = false
      }
    }
  }
}

resource "aws_lb_listener" "streamlit" {
  load_balancer_arn = aws_lb.main.arn
  protocol          = "HTTP"
  port              = "8501"
  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.streamlit.arn
    forward {
      target_group {
        arn = aws_alb_target_group.streamlit.arn
      }
      stickiness {
        duration = 3600
        enabled  = false
      }
    }
  }
}


resource "aws_ecs_service" "fastapi" {
  name                    = "fraud-api-service-w30jxco7"
  cluster                 = aws_ecs_cluster.main.id
  task_definition         = aws_ecs_task_definition.fastapi.arn
  desired_count           = 1
  enable_ecs_managed_tags = true
  enable_execute_command  = true
  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
  lifecycle {
    ignore_changes = [
      task_definition
    ]
  }
  capacity_provider_strategy {
    capacity_provider = "FARGATE"
    weight            = 1
    base              = 0
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.fastapi.arn
    container_name   = "fraud-api"
    container_port   = 8000
  }

  network_configuration {
    subnets          = data.aws_subnets.main.ids
    security_groups  = [aws_security_group.fastapi.id]
    assign_public_ip = true
  }
}

resource "aws_ecs_service" "streamlit" {
  name                    = "fraud-streamlit-service-72do6j1b"
  cluster                 = aws_ecs_cluster.main.id
  task_definition         = aws_ecs_task_definition.streamlit.arn
  desired_count           = 1
  enable_ecs_managed_tags = true
  enable_execute_command  = true
  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
  lifecycle {
    ignore_changes = [
      task_definition
    ]
  }
  capacity_provider_strategy {
    capacity_provider = "FARGATE"
    weight            = 1
    base              = 0
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.streamlit.arn
    container_name   = "streamlit"
    container_port   = 8501
  }

  network_configuration {
    subnets          = data.aws_subnets.main.ids
    security_groups  = [aws_security_group.streamlit.id]
    assign_public_ip = true
  }
}