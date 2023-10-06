1. Set AWS credentials at ~/.aws/credentials
2. Download SSH private key at ~/.ssh/vockey.pem
3. Set the proper permissions for the key: `chmod og-rwx ~/.ssh/vockey.pem`
4. Install requirements: `sudo pip install -r requirements.txt`
5. Install vim and less: `sudo apt update && sudo apt install -y vim less`
6. Install ecommerce platform: `ansible-playbook -i inventory.aws_ec2.yml --key-file=~/.ssh/vockey.pem --user ec2-user install-ecommerce.yml`
7. Download ecommerce_data.zip from [https://drive.google.com/open?id=1TglbLwxrIOICnf8VpSRx67EMjFSfCI-F&usp=drive_fs] to the current folder.
8. Run `ansible-playbook -i inventory.aws_ec2.yml --key-file=~/.ssh/vockey.pem --user ec2-user copy-dataset-and-run-platform.yml` to copy the dataset to the instance and to run the ecommerce events generator.
9. Kafka instance can be accesed from other instances at <ecommerce_platform_private_DNS>:9092 
