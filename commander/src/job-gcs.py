import yaml
from jinja2 import Environment, FileSystemLoader


class GcsDlpScanTFGenerator:
    def __init__(self, config_file, template_file, output_file):
        self.config_file = config_file
        self.template_file = template_file
        self.output_file = output_file

    def generate_tf(self):
        # Load YAML config file
        with open(self.config_file, 'r') as f:
            config = yaml.safe_load(f)

        # Load Jinja2 template
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(self.template_file)

        # Generate Terraform code
        tf_code = template.render(
            bucket_name=config['bucket_name'],
            include_regex=config['include_regex'],
            exclude_regex=config['exclude_regex'],
            custom_inspection_template_name=config['custom_inspection_template_name'],
            custom_info_types=config['custom_info_types']
        )

        # Write output to file
        with open(self.output_file, 'w') as f:
            f.write(tf_code)


if __name__ == '__main__':
    gcs_tf_generator = GcsDlpScanTFGenerator(
        config_file='gcs_config.yaml',
        template_file='gcs_template.tf.d',
        output_file='gcs_dlp_scan.tf'
    )

    gcs_tf_generator.generate_tf()
