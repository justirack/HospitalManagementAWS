# -----------------------------------------------
# Module Resources
resource "aws_dynamodb_table" "the_user_table" {
  name = local.user_table_name
  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES"
  billing_mode = "PAY_PER_REQUEST"

  hash_key = "user_id"
#  range_key = "sort_key"

  # Defines the partition key as a string
  attribute {
    name = "user_id"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_iam_policy" "the_user_table_policy" {
  name_prefix = "users-table-policy"
  policy = data.aws_iam_policy_document.the_user_table_policy_document.json
}

# -----------------------------------------------
# Module Data
data "aws_iam_policy_document" "the_user_table_policy_document" {
  version = "2012-10-17"

  statement {
    effect = "Allow"

    actions = ["dynamodb:*"]
    resources = ["arn:aws:dynamodb:*"]
  }
}



# -----------------------------------------------
# Module Locals
locals {
  user_table_name = "users"
}
