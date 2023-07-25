# This file contains the infrastructure to support the user_retrieval lambda

# -----------------------------------------------
# Module Resources
resource "aws_lambda_function" "the_user_retrieval_lambda_function" {
  function_name    = local.user_retrieval_lambda_name
  handler          = "${local.user_retrieval_lambda_name}.lambda_handler"
  role             = aws_iam_role.the_user_retrieval_lambda_role.arn
  runtime          = var.python-runtime
  timeout          = 60
  filename         = data.archive_file.the_user_retrieval_lambda_zip.output_path
  source_code_hash = data.archive_file.the_user_retrieval_lambda_zip.output_base64sha256
  publish          = true

  environment {
    variables = {
      USER_TABLE_NAME = aws_dynamodb_table.the_user_table.name
    }
  }

  depends_on = [aws_cloudwatch_log_group.the_user_retrieval_lambda_cloudwatch_group]
}

# Configures the cloudwatch group for this lambda
# This resource needs to have the same name as the lambda function
resource "aws_cloudwatch_log_group" "the_user_retrieval_lambda_cloudwatch_group" {
  name              = local.user_retrieval_lambda_name
  retention_in_days = 90
}

resource "aws_iam_role" "the_user_retrieval_lambda_role" {
  name               = "${local.user_retrieval_lambda_name}_lambda_role"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.the_user_retrieval_lambda_assume_role_policy_document.json
}

# This policy defines the basic CloudWatch log permissions that every lambda needs to execute
resource "aws_iam_policy" "the_user_retrieval_lambda-execution_policy" {
  name   = "${local.user_retrieval_lambda_name}_lambda_execution_policy"
  policy = data.aws_iam_policy_document.the_user_retrieval_lambda_execution_policy_document.json
}

# Gives the lambda basic permission required for CloudWatch logging
resource "aws_iam_role_policy_attachment" "the_user_retrieval_lambda_execution_role_policy_attachment" {
  policy_arn = aws_iam_policy.the_user_retrieval_lambda-execution_policy.arn
  role       = aws_iam_role.the_user_retrieval_lambda_role.name
}

# -----------------------------------------------
# Module Data

# Data used to allow lambda to emit to cloudwatch logs
data "aws_iam_policy_document" "the_user_retrieval_lambda_execution_policy_document" {
  statement {
    effect = "Allow"

    actions = [
      "logs:*",
      "dynamodb:*"
    ]

    resources = [
      "arn:aws:logs:*",
      "arn:aws:dynamodb:*"
    ]
  }
}

data "aws_iam_policy_document" "the_user_retrieval_lambda_assume_role_policy_document" {
  version = "2012-10-17"

  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "archive_file" "the_user_retrieval_lambda_zip" {
  output_path = local.user_retrieval_lambda_function_output_path
  type        = "zip"

  source {
    content  = file(local.user_retrieval_lambda_function_source_path)
    filename = "${local.user_retrieval_lambda_name}.py"
  }
}

# -----------------------------------------------
# Module Locals
locals {
  user_retrieval_lambda_name                 = "user_retrieval"
  user_retrieval_lambda_function_source_path = "${path.module}/lambda/${local.user_retrieval_lambda_name}.py"
  user_retrieval_lambda_function_output_path = "${path.module}/lambda/${local.user_retrieval_lambda_name}.zip"
}