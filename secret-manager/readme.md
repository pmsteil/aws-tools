# readme.md


## instructions for the python version
> works
```bash
python3 -m venv venv
source venv/bin/activate
pip install boto3
python3 secret-get.py 
```


## instructions for the javascript version
> never got this to work... 

```bash
npm install @aws-sdk/client-secrets-manager
node secret-get.js
```

## instructions for the ruby version
> Works!
```bash
gem install aws-sdk-secretsmanager
ruby secret-get.rb
```

## instructions for the go version
> Works!
```bash
go mod init secret-get
go get github.com/aws/aws-sdk-go-v2
go get github.com/aws/aws-sdk-go-v2/config
github.com/aws/aws-sdk-go-v2/service/secretsmanager
go run secret-get.go
```