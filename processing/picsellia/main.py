from picsellia import Client
from picsellia.sdk.dataset import DatasetVersion
from utils.data_augmentation import simple_rotation
import os

api_token = os.environ["api_token"]

if "host" not in os.environ:
    host = "https://app.picsellia.com"
else:
    host = os.environ["host"]
job_id = os.environ["job_id"]

client = Client(
    api_token=api_token,
    host=host
)

job = client.get_job_by_id(job_id)

context = job.sync()["datasetversionprocessingjob"]
input_dataset_version_id = context["input_dataset_version_id"]
output_dataset_version = context["output_dataset_version_id"]
parameters = context["parameters"]

input_dataset_version: DatasetVersion = client.get_dataset_version_by_id(
    input_dataset_version_id
)

input_dataset_version.download("data")

file_list = [os.path.join("data", path) for path in os.listdir("data")]

target_path = "rotated_data"
simple_rotation(file_list, target_path=target_path)

new_file_list = [os.path.join(target_path, path) for path in os.listdir(target_path)]

datalake = client.get_datalake()
data_list = datalake.upload_data(new_file_list)

output_dataset: DatasetVersion = client.get_dataset_version_by_id(
    output_dataset_version
)

output_dataset.add_data(data_list, tags=["augmented", "processing"])