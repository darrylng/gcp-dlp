resource "google_data_loss_prevention_job_trigger" "basic" {
    parent = "projects/my-project-name"
    description = "Description"
    display_name = "Displayname"

    triggers {
        schedule {
            recurrence_period_duration = "86400s"
        }
    }

    inspect_job {
        inspect_template_name = "fake"
        actions {
            save_findings {
                output_config {
                    table {
                        project_id = "project"
                        dataset_id = "dataset"
                    }
                }
            }
        }
        storage_config {
            cloud_storage_options {
                file_set {
                    url = "gs://mybucket/directory/"
                }
            }
        }
    }
}