#! /usr/python3

import os
import yaml
from jinja2 import Environment, FileSystemLoader
from job_bq import BQJob
from job_gcs import GCSJob

# Set up the Jinja2 environment
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

# Define the input and output directories
input_dir = 'configs'
output_dir = 'generated'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through all YAML files in the input directory and process them
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.yaml') or file.endswith('.yml'):
            # Read the YAML file
            with open(os.path.join(root, file), 'r') as stream:
                config = yaml.safe_load(stream)

            # Determine the type of job to generate based on the YAML schema
            job_type = config.get('job_type')
            if job_type == 'bq':
                job = BQJob(config)
                template_file = 'bq_dlp_scan.tf.j2'
            elif job_type == 'gcs':
                job = GCSJob(config)
                template_file = 'gcs_dlp_scan.tf.j2'
            else:
                # Skip the file if the job_type is not recognized
                print(f"Skipping {file}: unrecognized job_type {job_type}")
                continue

            # Render the Terraform template
            terraform = job.render(env.get_template(template_file))

            # Write the Terraform output to a file in the output directory
            output_file = os.path.splitext(file)[0] + '.tf'
            output_path = os.path.join(output_dir, output_file)
            with open(output_path, 'w') as f:
                f.write(terraform)

            print(f"Generated {output_path}")
