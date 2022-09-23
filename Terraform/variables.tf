variable "aws_region" {
	default = "ap-south-1"
}

variable "aws_access_key" {
default = ""
}

variable "aws_secret_key" {
default = ""
}

variable "region" {
  
}

variable "component_prefix" {
  default = "vidstream"
}

variable "component_name" {
  default = "urlGenerator"
}

# store the zip file here
variable "input_bucket_name" {
	
}


variable "bucket_key" {
  default     = "lambda/urlgenerator.zip"
  description = "Store zip file in this bucket path"
}


variable "archive_file_type" {
  default = "zip"
}


variable "lambda_handler" {
  default = "handler"
}

variable "lambda_runtime" {
  default = "python3.9"
}

variable "lambda_timeout" {
  default = "15"
}