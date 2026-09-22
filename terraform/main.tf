terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1" # Feel free to change to your preferred AWS region
}

# 1. Amazon ECR Repository for Container Images
resource "aws_ecr_repository" "app_repo" {
  name                 = "opsrelay-app"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# 2. CloudWatch Log Group for Application Telemetry
resource "aws_cloudwatch_log_group" "app_logs" {
  name              = "/aws/opsrelay/app-logs"
  retention_in_days = 7
}

# 3. CloudWatch Metric Alarm for HTTP 500 Spikes
resource "aws_cloudwatch_metric_alarm" "error_alarm" {
  alarm_name          = "opsrelay-high-error-rate"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "500Errors"
  namespace           = "OpsRelay/Application"
  period              = 60
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Triggers when application 500 errors exceed 5 in a 1-minute window."
}

# Output ECR Repository URL upon successful deployment
output "ecr_repository_url" {
  value       = aws_ecr_repository.app_repo.repository_url
  description = "The public/private URI for the opsrelay-app ECR repository."
}