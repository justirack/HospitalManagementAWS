#########################################################################
# Create Patient Queue
#########################################################################

# ------------------------------------------------------
# Module resources
resource "aws_sqs_queue" "the_create_patient_queue" {
  name                       = local.create_patient_queue_name
  visibility_timeout_seconds = 60

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.the_create_patient_queue_dlq.arn
    maxReceiveCount     = var.sqs_max_receive_count
  })
}

resource "aws_sqs_queue" "the_create_patient_queue_dlq" {
  name = local.create_patient_dlq_queue_name
}


# ------------------------------------------------------
# Module local variables
locals {
  create_patient_queue_name     = "${var.patient-prefix}create_patient_queue"
  create_patient_dlq_queue_name = "${local.create_patient_queue_name}_dlq"
}

#########################################################################
# Retrieve Patient Queue
#########################################################################

# ------------------------------------------------------
# Module resources
resource "aws_sqs_queue" "the_retrieve_patient_queue" {
  name                       = local.retrieve_patient_queue_name
  visibility_timeout_seconds = 60

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.the_retrieve_patient_queue_dlq.arn
    maxReceiveCount     = var.sqs_max_receive_count
  })
}

resource "aws_sqs_queue" "the_retrieve_patient_queue_dlq" {
  name = local.retrieve_patient_dlq_queue_name
}


# ------------------------------------------------------
# Module local variables
locals {
  retrieve_patient_queue_name     = "${var.patient-prefix}retrieve_patient_queue"
  retrieve_patient_dlq_queue_name = "${local.retrieve_patient_queue_name}_dlq"
}
