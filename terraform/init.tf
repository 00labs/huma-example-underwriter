terraform {
  required_version = "~> 1.3"

  backend "s3" {
    bucket = "huma-terraform-state"
    key    = "underwriter-eth-txns.tfstate"
    region = "us-west-1"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.25.0"
    }
  }
}

provider "aws" {
  region = var.aws-region
}
