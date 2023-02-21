# Configure Data Loss Prevention templates to be used for masking PII/PCI data
locals {
  dlp_location        = "projects/${var.project_id}/locations/${var.region}"
  dlp_inspection_name = "${var.data_masking_template_name}-identification${var.ws_env_suffix}"
  dlp_name_exclusions = [
    "bazel",
    "jaeger",
    "kafka",
    "kube",
    "jose",
  ]
  dlp_email_exclusion_iam = ".+@.+.iam.gserviceaccount.com$"
  dlp_email_exclusion_anz = ".+@anz.com$"
}

# This template is applied to identify the sensitive data
resource "google_data_loss_prevention_inspect_template" "inspection" {
  display_name = local.dlp_inspection_name
  parent       = local.dlp_location
  description  = "Identification template for PCI/PII data"

  inspect_config {
    info_types {
      name = "CREDIT_CARD_NUMBER"
    }

    info_types {
      name = "AUSTRALIA_TAX_FILE_NUMBER"
    }

    info_types {
      name = "EMAIL_ADDRESS"
    }

    info_types {
      name = "PHONE_NUMBER"
    }

    info_types {
      name = "STREET_ADDRESS"
    }

    info_types {
      name = "PERSON_NAME"
    }

    info_types {
      name = "AUTH_TOKEN"
    }

    info_types {
      name = "GCP_CREDENTIALS"
    }

    info_types {
      name = "JSON_WEB_TOKEN"
    }

    info_types {
      name = "AUSTRALIA_DRIVERS_LICENSE_NUMBER"
    }

    info_types {
      name = "AUSTRALIA_MEDICARE_NUMBER"
    }

    info_types {
      name = "AUSTRALIA_PASSPORT"
    }

    rule_set {
      info_types {
        name = "PERSON_NAME"
      }

      rules {
        exclusion_rule {
          dictionary {
            word_list {
              words = local.dlp_name_exclusions
            }
          }
          matching_type = "MATCHING_TYPE_PARTIAL_MATCH"
        }
      }
    }

    rule_set {
      info_types {
        name = "EMAIL_ADDRESS"
      }
      rules {
        exclusion_rule {
          regex {
            pattern = local.dlp_email_exclusion_iam
          }
          matching_type = "MATCHING_TYPE_FULL_MATCH"
        }
      }
    }

    rule_set {
      info_types {
        name = "EMAIL_ADDRESS"
      }
      rules {
        exclusion_rule {
          regex {
            pattern = local.dlp_email_exclusion_anz
          }
          matching_type = "MATCHING_TYPE_FULL_MATCH"
        }
      }
    }
    min_likelihood = var.data_masking_match_likelihood
    # content_options = ["CONTENT_TEXT"]
  }
}