provider "aws" {
    region = "us-east-1"
}

# Create the lambda role
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

resource "aws_iam_role" "api_lambda_flights_role" {
  name = "api_lambda_flights_role"

  assume_role_policy = "${file("../iam/iam_role.json")}"
}

# Apply the Policy Document we just created
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda_policy"
  role = aws_iam_role.api_lambda_flights_role.id
  policy = "${file("../iam/iam_policy.json")}"
}

# Create lambda function
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

module "lambda_zip" {
  source           = "github.com/ruzin/terraform_aws_lambda_python"
  output_path      = "lambda_function.zip"
  description      = ""
  source_code_path = "../src/"
  role_arn         = aws_iam_role.api_lambda_flights_role.arn
  function_name    = "api_lambda_flights"
  handler_name     = "api_lambda_flights.lambda_handler"
  runtime          = "python3.6"
  environment = {
    API_KEY = "fea7d4c61d5cff92ae5823a3016bce40"
  }
}