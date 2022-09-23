# give executable permission with chmod +x file_name.sh

sudo apt-get install wget unzip -y
wget http://releases.hashicorp.com/terraform/1.2.7/terraform_1.2.7_linux_amd64.zip
unzip terraform_1.2.7_linux_amd64.zip

sudo mv terraform /usr/local/bin/