terraform {
  backend "http" {
    address = "https://objectstorage.eu-frankfurt-1.oraclecloud.com/p/avJQClo6ZzbMBxkSBNfvXhkYdE8kSy2IEipcDViiBmI/n/oraseemeafrtech1/b/AtpDemo/o/terraform.tfstate"
    update_method = "PUT"
  }
}