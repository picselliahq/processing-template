from picsellia import Client
from picsellia.sdk.dataset import DatasetVersion
from utils.data_augmentation import simple_rotation
import os

api_token = os.environ["api_token"]
organization_id = os.environ["organization_id"]
job_id = os.environ["job_id"]

client = Client(
    api_token=api_token,
    organization_id=organization_id
)

job = client.get_job_by_id(job_id)

context = job.sync()["dataset_version_processing_job"]
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
data_list = datalake.upload_data(new_file_list, tags=["augmented", "processing"])
try:
    output_dataset: DatasetVersion = client.get_dataset_version_by_id(
        output_dataset_version
    )
except:
    dataset = client.get_dataset_by_id(input_dataset_version.origin_id)
    new_name = input_dataset_version.version + "-rotated"
    output_dataset: DatasetVersion = dataset.create_version(version=new_name, type=input_dataset_version.type)

output_dataset.add_data(data_list)
