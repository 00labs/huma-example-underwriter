
locals {
  subnets = [
    "subnet-0bafae6a5d8fac9ae",
    "subnet-0cd4f1d473dbf9d73"
  ]
  vpc_id          = "vpc-09faae5ce4c0611fd"
  route53_zone_id = "Z05722142Q0E6Y0RCXN9Y"
  huma_dev_sg_id  = "sg-0d0ebf457bfd17201"
}

data "aws_vpc" "vpc" {
  id = local.vpc_id
}

resource "aws_lb" "application_load_balancer" {
  name               = "${local.service_name}-${local.env}"
  load_balancer_type = "application"
  subnets            = local.subnets

  # enable_deletion_protection = true

  security_groups = [aws_security_group.load_balancer_security_group.id]


  lifecycle {
    # don't rename an existing lb because that requires destroying and recreating the load balander
    # which points to a different url
    ignore_changes = [name]
  }
}

resource "aws_lb_target_group" "target_group" {
  name        = "${local.service_name}-${local.env}"
  port        = local.container_port
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = data.aws_vpc.vpc.id

  # default is 300 seconds which makes deploy slow
  deregistration_delay = 60

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 60
    matcher             = "200"
    path                = "/health"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }


  depends_on = [aws_lb.application_load_balancer]

  lifecycle {
    # for ecs deployment, port for target doesn't matter:
    # https://stackoverflow.com/questions/42715647/whats-the-target-group-port-for-when-using-application-load-balancer-ec2-con
    ignore_changes = [name, port]
  }
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_lb.application_load_balancer.arn
  port              = "80"
  protocol          = "HTTP"
  default_action {
    # "forward" or "redirect"
    type = var.http_listener_action_type

    # only used if type = "forward"
    target_group_arn = aws_lb_target_group.target_group.arn

    # only used if type = "redirect"
    redirect {
      host        = "#{host}"
      path        = "/#{path}"
      port        = "443"
      protocol    = "HTTPS"
      query       = "#{query}"
      status_code = "HTTP_301"
    }
  }
}


resource "aws_lb_listener" "api_listener" {
  load_balancer_arn = aws_lb.application_load_balancer.arn
  port              = "8000"
  protocol          = "HTTP"
  default_action {
    # "forward" or "redirect"
    type = var.http_listener_action_type

    # only used if type = "forward"
    target_group_arn = aws_lb_target_group.target_group.arn

    # only used if type = "redirect"
    redirect {
      host        = "#{host}"
      path        = "/#{path}"
      port        = "443"
      protocol    = "HTTPS"
      query       = "#{query}"
      status_code = "HTTP_301"
    }
  }
}

# resource "aws_lb_listener" "listener_https" {
#   load_balancer_arn = aws_lb.application_load_balancer.arn
#   port              = "443"
#   protocol          = "HTTPS"
#   certificate_arn   = var.ssl_certificate_arn
#   default_action {
#     type             = "forward"
#     target_group_arn = aws_lb_target_group.target_group.arn
#   }
# }

resource "aws_security_group" "load_balancer_security_group" {
  name = "${local.service_name}-${local.env}-lb"

  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"

    # allow all IP addresses
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"

    # allow all IP addresses
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    from_port = 8000
    to_port   = 8000
    protocol  = "tcp"

    # allow all IP addresses
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port = 0    # Allowing any incoming port
    to_port   = 0    # Allowing any outgoing port
    protocol  = "-1" # Allowing any outgoing protocol

    # allow all IP addresses
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  lifecycle {
    # don't rename an existing lb because that requires destroying and recreating the load balander
    # which points to a different url
    ignore_changes = [name]
  }
}

# This is the security group for the application deployment, specifically, it only allows access from
# load balancer security group since ECS deployment itself should not be public-facing.
resource "aws_security_group" "service_security_group" {
  name = "${local.service_name}-${local.env}-service"
  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"

    # allow all IP addresses
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]

    # Only allowing traffic in from the load balancer security group
    security_groups = [aws_security_group.load_balancer_security_group.id]
  }

  egress {
    from_port = 0    # Allowing any incoming port
    to_port   = 0    # Allowing any outgoing port
    protocol  = "-1" # Allowing any outgoing protocol

    # allow all IP addresses
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }


  lifecycle {
    # don't rename an existing lb because that requires destroying and recreating the load balander
    # which points to a different url
    ignore_changes = [name]
  }
}



resource "aws_route53_record" "internal_dns_record" {
  zone_id = local.route53_zone_id # This is the internal.huma.finance hosted zone on route53
  name    = "${local.service_name}.${local.env}.internal.huma.finance"
  type    = "A"

  alias {
    name                   = aws_lb.application_load_balancer.dns_name
    zone_id                = aws_lb.application_load_balancer.zone_id
    evaluate_target_health = true
  }
}
