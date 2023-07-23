# -----------------------------------------------
# Module Resources
resource "aws_api_gateway_rest_api" "the_user_rest_api" {
  name = local.user_api_title
  body = data.template_file.the_user_open_api_specification_file.rendered
}

resource "aws_api_gateway_deployment" "the_user_rest_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.the_user_rest_api.id

  variables = {
    version = local.user_api_version
  }

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.the_user_rest_api.body))
  }

  lifecycle { create_before_destroy = true }

  depends_on = [aws_api_gateway_rest_api.the_user_rest_api]
}

resource "aws_api_gateway_gateway_response" "the_user_rest_api_gateway_response" {
  count         = length(local.gateway_responses)
  response_type = local.gateway_responses[count.index]
  rest_api_id   = aws_api_gateway_rest_api.the_user_rest_api.id

  response_parameters = {
    "gatewayresponse.header.Access-Control_Allow-Origin" = "'${local.user_api_cors_domain}'"
  }

  depends_on = [
    aws_api_gateway_rest_api.the_user_rest_api,
    aws_api_gateway_deployment.the_user_rest_api_deployment
  ]

  lifecycle {
    ignore_changes = [response_templates, status_code]
  }
}

resource "aws_api_gateway_stage" "the_user_rest_api_stage" {
  deployment_id = aws_api_gateway_deployment.the_user_rest_api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.the_user_rest_api.id
  stage_name    = local.user_api_title

  depends_on = [
    aws_api_gateway_rest_api.the_user_rest_api,
    aws_api_gateway_gateway_response.the_user_rest_api_gateway_response,
    aws_api_gateway_deployment.the_user_rest_api_deployment
  ]
}

# -----------------------------------------------
# Module Data
data "template_file" "the_user_open_api_specification_file" {
  template = file("${path.module}/${local.user_open_api_yml_file}")

  vars = {
    title       = local.user_api_title
    description = local.user_api_description
    version     = local.user_api_version
    invoke_url  = local.user_api_invoke_url

    # Add endpoint variables
    add_path        = local.user_api_add_path
    add_description = local.user_api_add_description

    # retrieve endpoint variables
    retrieve_path        = local.user_api_retrieve_path
    retrieve_description = local.user_api_retrieve_description

    # Update endpoint variables
    update_path        = local.user_api_update_path
    update_description = local.user_api_update_description

    # Delete endpoint variables
    delete_path        = local.user_api_delete_path
    delete_description = local.user_api_delete_description

    user_validation_lambda_invoke_arn      = aws_lambda_function.the_user_validation_lambda_function.invoke_arn
    user_validation_lambda_invoke_role_arn = aws_iam_role.the_user_validation_lambda_role.arn
  }
}

# -----------------------------------------------
# Module Locals
locals {
  user_open_api_yml_file = "openapi-user.yaml"
  user_api_cors_domain   = "*"

  # General api variables
  user_api_title       = "user"
  user_api_description = "The REST API that supports CRUD operations on users in this application"
  user_api_version     = "1.0"
  user_api_invoke_url  = "https://${local.user_api_title}"

  # Add endpoint variables
  user_api_add_path        = "v1/${local.user_api_title}/add"
  user_api_add_description = "The endpoint that adds a user to the database."

  # retrieve endpoint variables
  user_api_retrieve_path        = "v1/${local.user_api_title}/get"
  user_api_retrieve_description = "The endpoint that gets a user from the database"

  # Update endpoint variables
  user_api_update_path        = "v1/${local.user_api_title}/update"
  user_api_update_description = "The endpoint that updates an existing users information."

  # Delete endpoint variables
  user_api_delete_path        = "v1/${local.user_api_title}/delete"
  user_api_delete_description = "The endpoint that deletes a users information"

  gateway_responses = [
    "ACCESS_DENIED",
    "API_CONFIGURATION_ERROR",
    "AUTHORIZER_FAILURE",
    "AUTHORIZER_CONFIGURATION_ERROR",
    "BAD_REQUEST_PARAMETERS",
    "BAD_REQUEST_BODY",
    "DEFAULT_4XX",
    "DEFAULT_5XX",
    "EXPIRED_TOKEN",
    "INVALID_SIGNATURE",
    "INTEGRATION_FAILURE",
    "INTEGRATION_TIMEOUT",
    "INVALID_API_KEY",
    "MISSING_AUTHENTICATION_TOKEN",
    "QUOTA_EXCEEDED",
    "REQUEST_TOO_LARGE",
    "RESOURCE_NOT_FOUND",
    "THROTTLED",
    "UNAUTHORIZED",
    "UNSUPPORTED_MEDIA_TYPE"
  ]
}