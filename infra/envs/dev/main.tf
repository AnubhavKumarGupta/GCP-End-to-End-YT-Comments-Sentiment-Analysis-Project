module "iam" {
  source     = "../../modules/iam"
  project_id = var.project_id
  region     = var.region
}

module "pubsub" {
  source     = "../../modules/pubsub"
  project_id = var.project_id
  region     = var.region
}

module "bigquery" {
  source     = "../../modules/bigquery"
  project_id = var.project_id
  region     = var.region
}

module "storage" {
  source     = "../../modules/storage"
  project_id = var.project_id
  region     = var.region
}

module "composer" {
  source       = "../../modules/composer"
  project_id   = var.project_id
  region       = var.region
  name         = "yt-pipeline-composer"
  cf_sa_email  = module.iam.cf_sa_email
}