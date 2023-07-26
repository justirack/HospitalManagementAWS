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
module "user_module" {
  source = "./modules/User"

  # Variables
  user-prefix = "user-"
  python-runtime = "python3.9"
  sqs_max_receive_count = 10
}
