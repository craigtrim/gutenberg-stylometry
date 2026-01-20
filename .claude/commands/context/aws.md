
# AWS Context

## CLI Profiles

All AWS CLI profiles use the `dwc_*` naming convention. Available profiles:

- `dwc_lambda` - Lambda functions
- `dwc_vpc` - VPC configuration
- `dwc_apigateway` - API Gateway
- `dwc_stepfunctions` - Step Functions
- `dwc_iam` - IAM management
- `dwc_bedrock` - Bedrock AI services
- `dwc_s3` - S3 storage
- `dwc_ec2` - EC2 instances

Use these profiles with the `--profile` flag, e.g.:
```bash
aws s3 ls --profile dwc_s3
```

## S3 Buckets

### craigtrim.com
- Largely managed by project: `/Users/craigtrim/git/mville/cosc-agentic-systems`

### craigtrim-resources
- Contains resources used in this project
- Key path: `s3://craigtrim-resources/gutenberg/txt`
- Contains 60k+ Gutenberg books in text format
