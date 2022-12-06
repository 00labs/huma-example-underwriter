locals {
  region       = "us-west-1"
  env          = "prod"
  service_name = "underwriter-eth-txns"
  cluster_name = "huma-underwriter"
  repo_name    = "huma-underwriter-eth-txns"
}

locals {
  ecr_repository_name = local.repo_name
  ecr_image_tag       = "latest"

  main_container_name = "${local.service_name}-container"
  container_port      = 8000
}


data "aws_ecr_repository" "repo" {
  name = local.ecr_repository_name
}

data "aws_ecr_image" "image" {
  repository_name = local.ecr_repository_name
  image_tag       = local.ecr_image_tag
}

data "aws_iam_role" "execution_role" {
  name = "ecsTaskExecutionRole"
}

resource "aws_ecs_cluster" "app" {
  name = local.cluster_name
}


resource "aws_cloudwatch_log_group" "log" {
  name = "/ecs/${local.env}/${local.service_name}"
}

resource "aws_ecs_task_definition" "huma" {
  family                   = local.service_name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = data.aws_iam_role.execution_role.arn

  container_definitions = jsonencode([
    {
      name      = local.main_container_name
      image     = "${data.aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.image.id}"
      essential = true
      portMappings = [
        {
          containerPort = local.container_port
          hostPort      = local.container_port
          protocol      = "tcp"
        }
      ]

      "environment" : [
        {
          "name" : "ENV",
          "value" : "production"
        },
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.log.name
          "awslogs-region"        = local.region
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])

  cpu    = 256
  memory = 512
}

resource "aws_ecs_service" "huma" {
  name                    = "huma-underwriter-eth-txns"
  cluster                 = aws_ecs_cluster.app.id
  task_definition         = aws_ecs_task_definition.huma.arn
  launch_type             = "FARGATE"
  propagate_tags          = "SERVICE"
  enable_ecs_managed_tags = true

  desired_count = 1
  load_balancer {
    target_group_arn = aws_lb_target_group.target_group.arn
    container_name   = local.main_container_name
    container_port   = local.container_port
  }

  network_configuration {
    subnets          = local.subnets
    security_groups  = [aws_security_group.load_balancer_security_group.id]
    assign_public_ip = true
  }
}
