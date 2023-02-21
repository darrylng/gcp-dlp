import os
import yaml

class BigQueryScanner:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def parse_config(self):
        with open(self.config_file_path, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def generate_tf(self):
        config = self.parse_config()
        columns = ", ".join(f'"{col}"' for col in config["bigquery"]["columns"])

        with open("../tempaltes/template-bq.tf.d", "r") as f:
            tf_template = f.read()

        tf_config = tf_template.format(
            template_name=config['template_name'],
            template_description=config['template_description'],
            info_type_name=config['info_type_name'],
            min_likelihood=config['min_likelihood'],
            max_findings_per_request=config['max_findings_per_request'],
            stored_info_type_name=config['stored_info_type_name'],
            stored_info_type_description=config['stored_info_type_description'],
            dictionary_words=config['dictionary_words'],
            trigger_name=config['trigger_name'],
            trigger_description=config['trigger_description'],
            bigquery_project_id=config['bigquery']['project_id'],
            bigquery_dataset_id=config['bigquery']['dataset_id'],
            bigquery_table_id=config['bigquery']['table_id'],
            columns=columns,
            frequency_minutes=config['frequency_minutes'],
            pubsub_topic=config['pubsub_topic'],
            datastore_kind=config['datastore_kind'],
            pubsub_project=config['pubsub_project']
        )

        with open(os.path.splitext(self.config_file_path)[0] + '.tf', 'w') as f:
            f.write(tf_config)
