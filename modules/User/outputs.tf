output "user_validation_lambda_function_invoke_arn"{
  value = aws_lambda_function.the_user_validation_lambda_function.invoke_arn
}

output "user_validation_lambda_role_arn" {
  value = aws_iam_role.the_user_validation_lambda_role.arn
}
