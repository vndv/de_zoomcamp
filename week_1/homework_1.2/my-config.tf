terraform {
   required_providers {
     yandex = {
       source = "yandex-cloud/yandex"
     }
   }
 }

  variable "token" {
     type = string
 }

 variable "cloud-id" {
     type = string
 }

  variable "folder-id" {
     type = string
 }
  
 provider "yandex" {
   token  =  var.token
   cloud_id  = var.cloud-id
   folder_id = var.folder-id
   zone      = "ru-central1-a"
 }


 
resource "yandex_iam_service_account" "sa" {
  name = "dtc"
}

// Assigning roles to the service account
resource "yandex_resourcemanager_folder_iam_member" "sa-editor" {
  folder_id = var.folder-id
  role      = "storage.editor"
  member    = "serviceAccount:${yandex_iam_service_account.sa.id}"
}

// Creating a static access key
resource "yandex_iam_service_account_static_access_key" "sa-static-key" {
  service_account_id = yandex_iam_service_account.sa.id
  description        = "static access key for object storage"
}

// Creating a bucket using the key
resource "yandex_storage_bucket" "test" {
  access_key = yandex_iam_service_account_static_access_key.sa-static-key.access_key
  secret_key = yandex_iam_service_account_static_access_key.sa-static-key.secret_key
  bucket     = "de-zoomcamp"
}