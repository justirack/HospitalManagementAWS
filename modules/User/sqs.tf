#########################################################################
# Create user Queue
#########################################################################

# ------------------------------------------------------
# Module resources
resource "aws_sqs_queue" "the_create_user_queue" {
  name                       = local.create_user_queue_name
  visibility_timeout_seconds = 60

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.the_create_user_queue_dlq.arn
    maxReceiveCount     = var.sqs_max_receive_count
  })
}

resource "aws_sqs_queue" "the_create_user_queue_dlq" {
  name = local.create_user_dlq_queue_name
}


# ------------------------------------------------------
# Module local variables
locals {
  create_user_queue_name     = "${var.user-prefix}create_user_queue"
  create_user_dlq_queue_name = "${local.create_user_queue_name}_dlq"
}

#########################################################################
# update user Queue
#########################################################################

# ------------------------------------------------------
# Module resources
resource "aws_sqs_queue" "the_update_user_queue" {
  name                       = local.update_user_queue_name
  visibility_timeout_seconds = 60

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.the_update_user_queue_dlq.arn
    maxReceiveCount     = var.sqs_max_receive_count
  })
}

resource "aws_sqs_queue" "the_update_user_queue_dlq" {
  name = local.update_user_dlq_queue_name
}


# ------------------------------------------------------
# Module local variables
locals {
  update_user_queue_name     = "${var.user-prefix}update_user_queue"
  update_user_dlq_queue_name = "${local.update_user_queue_name}_dlq"
}
