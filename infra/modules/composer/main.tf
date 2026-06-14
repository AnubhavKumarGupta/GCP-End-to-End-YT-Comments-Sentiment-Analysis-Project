variable "project_id" {}
variable "name" {}
variable "cf_sa_email" {}
variable "region" {}

resource "google_composer_environment" "yt_pipeline" {
  name    = var.name
  project = var.project_id
  region  = var.region

  config {
    software_config {
      image_version = "composer-3-airflow-2.10.5-build.15"
    }

    environment_size = "ENVIRONMENT_SIZE_SMALL"
    resilience_mode  = "STANDARD_RESILIENCE"

    node_config {
      service_account = var.cf_sa_email
    }
  }
}