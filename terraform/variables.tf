variable "aws-region" {
  description = "AWS region"
  default     = "us-west-1"
}

variable "http_listener_action_type" {
  type        = string
  description = "[forward|redirect] If redirect, HTTP traffic will always be redirected to HTTPS. If forward, HTTP traffic will work on its own."
  default     = "forward"
}