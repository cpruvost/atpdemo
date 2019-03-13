terraform {
  backend "http" {
    address       = "${var.terraform_state_url}"
    update_method = "PUT"
  }
}