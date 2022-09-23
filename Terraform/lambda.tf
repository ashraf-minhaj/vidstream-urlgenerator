# Zip the Lamda function on the fly
data "archive_file" "source" {
  type        = "${var.archive_file_type}"
  source_dir  = "../src/"
  output_path = "../output-files/--.zip"
}

resource "aws_s3_object" "s3_bucket_obj" {
  bucket = "${var.input_bucket_name}"
  key    = "${var.bucket_key}"
  source = data.archive_file.source.output_path
}

# # upload zip to s3 and then update lamda function from s3
# resource "aws_s3_bucket_object" "s3_bucket_obj" {
#   bucket = "${var.input_bucket_name}"
#   key    = "${var.bucket_key}"
#   source = data.archive_file.source.output_path
# }

# connect this lambda with uploaded s3 zip file
# lambda needs code and iam_role
# "${aws_s3_bucket_object.file_upload.key}"
# resource - resource_name
resource "aws_lambda_function" "lambda" {
    function_name   = "${var.component_prefix}-${var.component_name}"
    s3_bucket       = aws_s3_object.s3_bucket_obj.bucket
    s3_key          = aws_s3_object.s3_bucket_obj.key
    role            = aws_iam_role.lambda_role.arn 
    handler         = "${var.component_prefix}-${var.component_name}.${var.lambda_handler}"
    runtime         = "${var.lambda_runtime}"
    timeout         = "${var.lambda_timeout}"
}


resource "aws_lambda_permission" "lambdaInvokePermission" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.lambda.arn}"
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${var.input_bucket_name}"
}

# arn:aws:s3:::vidstream-input-videos