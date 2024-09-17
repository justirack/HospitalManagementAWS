terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-west-2"
}


# --------------------------------------------------
# :: Module calls
module "user" {
  source = "./modules/User"

  # Variables
  user-prefix           = "user-"
  python-runtime        = "python3.9"
  sqs_max_receive_count = 10
}

module "appointment" {
  source = "./modules/Appointment"


  python-runtime        = "python3.9"
  sqs_max_receive_count = 10
  appointment-prefix    = "appointment-"
}

module "API" {
  source = "./modules/API"

  # Variables
  user_validation_lambda_function_invoke_arn = module.user.user_validation_lambda_function_invoke_arn
  user_validation_lambda_role_arn            = module.user.user_validation_lambda_role_arn

  appointment_validation_lambda_function_invoke_arn = module.appointment.appointment_validation_lambda_function_invoke_arn
  appointment_validation_lambda_role_arn            = module.appointment.appointment_validation_lambda_role_arn
}