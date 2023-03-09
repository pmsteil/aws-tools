

# current instance type: m1.small 1.7 gb ram, 1 vcpu, ??? gb storage - $31.68/month
# new instance type: t4g.micro 1 gb ram, 2 vcpu, ?? gb storage - $2.63/month
PROD-SQL-EXPRESS=i-05101d64

# current instance type: t1.micro - .6 gb ram, 1 vcpu, 160 ?? storage $14.40/month
PROD-ONESOURCE-FTP=i-a25dc0d8


# current instance type: t2.small - 2 gb ram, 1 vcpu, ?? storage $31.68/month $16.56/month
# (fb.infranet,iiproject,onesource/SMTP)
WWW_PROD_CF8_WIN32=i-0d9207e67263ffc5d

# aws ec2 modify-instance-type --instance-id $PROD-SQL-EXPRESS --instance-type t4g.micro
aws ec2 modify-instance-type --instance-id $WWW_PROD_CF8_WIN32 --instance-type t3.small
# aws ec2 modify-instance-type --instance-id <instance-id> --instance-type t3.small
