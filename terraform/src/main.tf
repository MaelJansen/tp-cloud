terraform {
  required_version = "~> 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.78.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "nomprenom-resource-group"
    storage_account_name = "nomprenomterraformstorage"
    container_name       = "states"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  # Ici nous sommes supposés définir des paramètres du provider Azure
  features {}

  use_cli         = true
  subscription_id = "0ff4bd81-58b2-4bfd-b35d-57b8d3f03d8c"
  tenant_id       = "7c8bac59-e815-4c8d-b01b-bd61e2dad846"
}

locals {
  base_name = "nomprenom"
}

data "azurerm_client_config" "current" {}

data "azurerm_resource_group" "resource_group" {
  name = "${local.base_name}-resource-group"
}