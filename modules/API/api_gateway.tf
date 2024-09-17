# -----------------------------------------------
# Module Resources
resource "aws_api_gateway_rest_api" "the_user_rest_api" {
  name = local.api_title
  body = data.template_file.the_user_open_api_specification_file.rendered
}

resource "aws_api_gateway_deployment" "the_user_rest_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.the_user_rest_api.id

  variables = {
    version = local.api_version
  }

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.the_user_rest_api.body))
  }

  lifecycle { create_before_destroy = true }

  depends_on = [aws_api_gateway_rest_api.the_user_rest_api]
}

resource "aws_api_gateway_gateway_response" "the_user_rest_api_gateway_response" {
  count = length(local.gateway_responses)
  response_type = local.gateway_responses[count.index]
  rest_api_id   = aws_api_gateway_rest_api.the_user_rest_api.id

  response_parameters = {
    "gatewayresponse.header.Access-Control-Allow-Origin" = "'${local.user_api_cors_domain}'"
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
  stage_name    = local.api_title

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
    title       = local.api_title
    description = local.api_description
    version     = local.api_version
    invoke_url = local.api_invoke_url

    # Add endpoint variables
    add_user_path = local.add_user_path
    add_user_description = local.add_user_description

    # retrieve endpoint variables
    retrieve_user_path = local.retrieve_user_path
    retrieve_user_description = local.retrieve_user_description

    # Update endpoint variables
    update_user_path = local.update_user_path
    update_user_description = local.update_user_description

    # Delete endpoint variables
    delete_user_path = local.delete_user_path
    delete_user_description = local.delete_user_description

    # Options endpoint variables
    options_user_path = local.options_user_path
    options_user_description = local.options_user_description

    # User validation lambda information
    user_validation_lambda_invoke_arn = var.user_validation_lambda_function_invoke_arn
    user_validation_lambda_invoke_role_arn = var.user_validation_lambda_role_arn


    # Book endpoint variables
    book_appointment_path = local.book_appointment_path
    book_appointment_description = local.book_appointment_description

    # Retrieve endpoint variables
    retrieve_appointment_path = local.retrieve_appointment_path
    retrieve_appointment_description = local.retrieve_appointment_description

    # Update endpoint variables
    update_appointment_path = local.update_appointment_path
    update_appointment_description = local.update_appointment_description

    # Cancel endpoint variables
    cancel_appointment_path = local.cancel_appointment_path
    cancel_appointment_description = local.cancel_appointment_description

    # Appointment validation lambda information
    appointment_validation_lambda_invoke_arn      = var.appointment_validation_lambda_function_invoke_arn
    appointment_validation_lambda_invoke_role_arn = var.appointment_validation_lambda_role_arn
  }
}

# -----------------------------------------------
# Module Locals
locals {
  user_open_api_yml_file = "openapi-hospital_management.yaml"
  user_api_cors_domain = "*"

  # General api variables
  api_title            = "HospitalManagement"
  user_api_path        = "user"
  appointment_api_path = "appointment"
  api_description      = "The REST API that supports CRUD operations for this application"
  api_version          = "1.0"
  api_path_version     = "v1"
  api_invoke_url       = "https://${local.api_title}"

  # User API variables
  # Add endpoint user variables
  add_user_path = "${local.api_path_version}/${local.user_api_path}/add"
  add_user_description = "The endpoint that adds a user to the database."

  # retrieve user endpoint variables
  retrieve_user_path = "${local.api_path_version}/${local.user_api_path}/get"
  retrieve_user_description = "The endpoint that gets a user from the database"

  # Update user endpoint variables
  update_user_path = "${local.api_path_version}/${local.user_api_path}/update"
  update_user_description = "The endpoint that updates an existing users information."

  # Delete user endpoint variables
  delete_user_path = "${local.api_path_version}/${local.user_api_path}/delete"
  delete_user_description = "The endpoint that deletes a users information"

  # Options endpoint variables
  options_user_path        = "${local.api_path_version}/${local.user_api_path}/options"
  options_user_description = "An options endpoint for the user API"


  # Appointment API variables
  # Book endpoint variables
  book_appointment_path = "${local.api_path_version}/${local.appointment_api_path}/book"
  book_appointment_description = "The endpoint that books an appointment"

  # Retrieve endpoint variables
  retrieve_appointment_path = "${local.api_path_version}/${local.appointment_api_path}/get"
  retrieve_appointment_description = "The endpoint that retrieves a list of appointments"

  # Update endpoint variables
  update_appointment_path = "${local.api_path_version}/${local.appointment_api_path}/update"
  update_appointment_description = "The endpoint that updates an appointment"

  # Cancel endpoint variables
  cancel_appointment_path        = "${local.api_path_version}/${local.appointment_api_path}/cancel"
  cancel_appointment_description = "The endpoint that cancels an appointment"

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