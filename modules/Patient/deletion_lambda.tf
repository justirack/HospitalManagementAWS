# This file contains the infrastructure to support the patient_deletion lambda

# -----------------------------------------------
# Module Resources
resource "aws_lambda_function" "the_patient_deletion_lambda_function" {
  function_name    = local.patient_deletion_lambda_name
  handler          = "${local.patient_deletion_lambda_name}.lambda_handler"
  role             = aws_iam_role.the_patient_deletion_lambda_role.arn
  runtime          = var.python-runtime
  timeout          = 60
  filename         = data.archive_file.the_patient_deletion_lambda_zip.output_path
  source_code_hash = data.archive_file.the_patient_deletion_lambda_zip.output_base64sha256
  publish          = true

  environment {
    variables = {
      PATIENT_TABLE_NAME = aws_dynamodb_table.the_patient_table.name
    }
  }

  depends_on = [aws_cloudwatch_log_group.the_patient_deletion_lambda_cloudwatch_group]
}

# Configures the cloudwatch group for this lambda
# This resource needs to have the same name as the lambda function
resource "aws_cloudwatch_log_group" "the_patient_deletion_lambda_cloudwatch_group" {
  name              = local.patient_deletion_lambda_name
  retention_in_days = 90
}

resource "aws_iam_role" "the_patient_deletion_lambda_role" {
  name               = "${local.patient_deletion_lambda_name}_lambda_role"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.the_patient_deletion_lambda_assume_role_policy_document.json
}

# This policy defines the basic CloudWatch log permissions that every lambda needs to execute
resource "aws_iam_policy" "the_patient_deletion_lambda-execution_policy" {
  name   = "${local.patient_deletion_lambda_name}_lambda_execution_policy"
  policy = data.aws_iam_policy_document.the_patient_deletion_lambda_execution_policy_document.json
}

# Gives the lambda basic permission required for CloudWatch logging
resource "aws_iam_role_policy_attachment" "the_patient_deletion_lambda_execution_role_policy_attachment" {
  policy_arn = aws_iam_policy.the_patient_deletion_lambda-execution_policy.arn
  role       = aws_iam_role.the_patient_deletion_lambda_role.name
}

# -----------------------------------------------
# Module Data

# Data used to allow lambda to emit to cloudwatch logs
data "aws_iam_policy_document" "the_patient_deletion_lambda_execution_policy_document" {
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

data "aws_iam_policy_document" "the_patient_deletion_lambda_assume_role_policy_document" {
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

data "archive_file" "the_patient_deletion_lambda_zip" {
  output_path = local.patient_deletion_lambda_function_output_path
  type        = "zip"

  source {
    content  = file(local.patient_deletion_lambda_function_source_path)
    filename = "${local.patient_deletion_lambda_name}.py"
  }
}

# -----------------------------------------------
# Module Locals
locals {
  patient_deletion_lambda_name                 = "patient_deletion"
  patient_deletion_lambda_function_source_path = "${path.module}/lambda/${local.patient_deletion_lambda_name}.py"
  patient_deletion_lambda_function_output_path = "${path.module}/lambda/${local.patient_deletion_lambda_name}.zip"
}