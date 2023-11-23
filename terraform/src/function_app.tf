resource "azurerm_service_plan" "service_plan" {
  name                = "${local.base_name}-service-plan"
  resource_group_name = data.azurerm_resource_group.resource_group.name
  location            = data.azurerm_resource_group.resource_group.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_storage_account" "function_app_storage" {
  name                     = replace("${local.base_name}fappstore", "-", "")
  resource_group_name      = data.azurerm_resource_group.resource_group.name
  location                 = data.azurerm_resource_group.resource_group.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_linux_function_app" "function_app" {
  name                = "${local.base_name}-function-app"
  resource_group_name = data.azurerm_resource_group.resource_group.name
  location            = data.azurerm_resource_group.resource_group.location

  storage_account_name       = azurerm_storage_account.function_app_storage.name
  storage_account_access_key = azurerm_storage_account.function_app_storage.primary_access_key
  service_plan_id            = azurerm_service_plan.service_plan.id

  site_config {
    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    AzureWebJobsFeatureFlags = "EnableWorkerIndexing"
  }
}