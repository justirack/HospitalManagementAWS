# -----------------------------------------------
# Module Resources
resource "aws_api_gateway_rest_api" "the_patient_rest_api" {
  name = local.patient_api_title
  body = data.template_file.the_patient_open_api_specification_file.rendered
}

resource "aws_api_gateway_deployment" "the_patient_rest_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.the_patient_rest_api.id

  variables = {
    version = local.patient_api_version
  }

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.the_patient_rest_api.body))
  }

  lifecycle { create_before_destroy = true }

  depends_on = [aws_api_gateway_rest_api.the_patient_rest_api]
}

resource "aws_api_gateway_gateway_response" "the_patient_rest_api_gateway_response" {
  count         = length(local.gateway_responses)
  response_type = local.gateway_responses[count.index]
  rest_api_id   = aws_api_gateway_rest_api.the_patient_rest_api.id

  response_parameters = {
    "gatewayresponse.header.Access-Control_Allow-Origin" = "'${local.patient_api_cors_domain}'"
  }

  depends_on = [
    aws_api_gateway_rest_api.the_patient_rest_api,
    aws_api_gateway_deployment.the_patient_rest_api_deployment
  ]

  lifecycle {
    ignore_changes = [response_templates, status_code]
  }
}

resource "aws_api_gateway_stage" "the_patient_rest_api_stage" {
  deployment_id = aws_api_gateway_deployment.the_patient_rest_api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.the_patient_rest_api.id
  stage_name    = local.patient_api_title

  depends_on = [
    aws_api_gateway_rest_api.the_patient_rest_api,
    aws_api_gateway_gateway_response.the_patient_rest_api_gateway_response,
    aws_api_gateway_deployment.the_patient_rest_api_deployment
  ]
}

# -----------------------------------------------
# Module Data
data "template_file" "the_patient_open_api_specification_file" {
  template = file("${path.module}/${local.patient_open_api_yml_file}")

  vars = {
    title       = local.patient_api_title
    description = local.patient_api_description
    version     = local.patient_api_version
    invoke_url  = local.patient_api_invoke_url

    # Add endpoint variables
    add_path                                          = local.patient_api_add_path
    add_description                                   = local.patient_api_add_description

    # retrieve endpoint variables
    retrieve_path                                      = local.patient_api_retrieve_path
    retrieve_description                               = local.patient_api_retrieve_description

    patient_validator_lambda_invoke_arn      = aws_lambda_function.the_patient_validator_lambda_function.invoke_arn
    patient_validator_lambda_invoke_role_arn = aws_iam_role.the_patient_validator_lambda_role.arn
  }
}

# -----------------------------------------------
# Module Locals
locals {
  patient_open_api_yml_file = "openapi-patient.yaml"
  patient_api_cors_domain   = "*"

  # General api variables
  patient_api_title       = "patient"
  patient_api_description = "The REST API that supports CRUD operations on patients in this application"
  patient_api_version     = "1.0"
  patient_api_invoke_url  = "https://${local.patient_api_title}"

  # Add endpoint variables
  patient_api_add_path        = "v1/${local.patient_api_title}/add"
  patient_api_add_description = "The endpoint that adds a patient to the database."

  # retrieve endpoint variables
  patient_api_retrieve_path        = "v1/${local.patient_api_title}/get"
  patient_api_retrieve_description = "The endpoint that gets a patient from the database"

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