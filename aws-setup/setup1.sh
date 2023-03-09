#!/bin/bash

# aws-setup

# This is a collection of scripts and notes for setting up a new AWS account.

# The scripts are designed to be run in order, and are idempotent.

## Setup

### Prerequisites

# [ ] Install [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)


aws configure


# Organizations
## Create Organization

aws organizations create-organization --feature-set ALL

## Create Accounts
aws organizations create-account --email-address <email> --account-name <name> --role-name <role>```

## List Accounts

aws organizations list-accounts```


## Create IAM User

aws iam create-user --user-name <name>

## Create IAM Group

aws iam create-group --group-name <name>

## Add User to Group

aws iam add-user-to-group --user-name <name> --group-name <name>

## Create IAM Policy

aws iam create-policy --policy-name <name> --policy-document <file>

## list permission set managed policies

aws sso-admin list-managed-policies-in-permission-set


## Create Permission Sets for all templates
aws sso-admin create-permission-set --instance-arn <arn> --name <name> --description <description> --relay-state <state> --session-duration <duration> --tags <tags> --managed-policies 



## list instance arns

aws sso-admin list-instances