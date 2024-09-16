#########################################################################
# Create patient Queue
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
# update patient Queue
#########################################################################

# ------------------------------------------------------
# Module resources
resource "aws_sqs_queue" "the_update_patient_queue" {
  name                       = local.update_patient_queue_name
  visibility_timeout_seconds = 60

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.the_update_patient_queue_dlq.arn
    maxReceiveCount     = var.sqs_max_receive_count
  })
}

resource "aws_sqs_queue" "the_update_patient_queue_dlq" {
  name = local.update_patient_dlq_queue_name
}


# ------------------------------------------------------
# Module local variables
locals {
  update_patient_queue_name     = "${var.patient-prefix}update_patient_queue"
  update_patient_dlq_queue_name = "${local.update_patient_queue_name}_dlq"
}
