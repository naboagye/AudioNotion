# Creating IAM role so that S3 service to assume the role and access other AWS services. 

resource "aws_iam_role" "s3_role" {
  name               = "iam_role_s3_bucket"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.an-bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.lambdafunc.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "AWSLogs/"
    filter_suffix       = ".log"
  }

  depends_on = [aws_lambda_permission.allow_bucket]
}

resource "aws_s3_bucket" "an-bucket" {
  bucket = "audio-notion-bucket"
  acl    = private

  tags = {
    Environment = "Dev"
  }
}

resource "aws_s3_bucket" "log_bucket" {
  bucket = "audio-notion-log-bucket"
}

resource "aws_s3_bucket_acl" "log_bucket_acl" {
  bucket = aws_s3_bucket.log_bucket.id
  acl    = "log-delivery-write"
}

resource "aws_s3_bucket_logging" "an-bucket" {
  bucket = aws_s3_bucket.an-bucket.id

  target_bucket = aws_s3_bucket.log_bucket.id
  target_prefix = "log/"
}
