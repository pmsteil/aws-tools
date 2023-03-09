# aws-setup

# This is a collection of scripts and notes for setting up a new AWS account.

The scripts are designed to be run in order, and are idempotent.

## Setup

### Prerequisites

- [ ] Install [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)


# Organizations

## Create Organization

```aws organizations create-organization --feature-set ALL```


## Create Accounts
    
    ```aws organizations create-account --email-address <email> --account-name <name> --role-name <role>```

## List Accounts

    ```aws organizations list-accounts```

## List Accounts

    ```aws organizations list-accounts```

