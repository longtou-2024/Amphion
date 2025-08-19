#task.set_accelerator_type("nvidia.com/gpu")
#task.set_accelerator_limit(2)
# set_cpu_request(cpu: str) → PipelineTask # minimum
# set_cpu_limit(cpu: str) → PipelineTask # maximum
# set_memory_request(memory: str) → PipelineTask[source]
# The minimum memory requests required. This string should be a number or a number followed by one of “E”, “Ei”, “P”, “Pi”, “T”, “Ti”, “G”, “Gi”, “M”, “Mi”, “K”, or “Ki”.
# longtou.2024

from google.protobuf import json_format
from kfp import dsl
from kfp import compiler
from kfp.client import Client
from kfp import kubernetes
from kfp.dsl import PipelineTask
from kfp.kubernetes import common

IMAGE_URL = "us-central1-docker.pkg.dev/prod-ai-project/tts/amphion:v4.0"
N_GPU = 1
N_CPU = "12"
MEM_SIZE = "100Gi"
MOUNT_PATH = "/home/longtou.2024/mount"
CONFIG_PATH = f"{MOUNT_PATH}/longtou/saved/Emilia/config.json"
WDS_PATH = "emilia_pipe"
RECIPE_NAME = "saltlux_expert"
INPUT_FOLDER_PATH = "gs://prod-ai-lab-speech-bucket/longtou/db/" + RECIPE_NAME + "/wds_v2/shard-0000{00..33}.tar"
INPUT_FOLDER_PATH2 = "gs://prod-ai-lab-speech-bucket/longtou/db/" + RECIPE_NAME + "/wds_v2/shard-0000{34..68}.tar"
GCS_URL = "gs://prod-ai-lab-speech-bucket/longtou/db/" + RECIPE_NAME + "/"
F_LOG = MOUNT_PATH + "/longtou/db/" + RECIPE_NAME +"/emilia_pipe_0.log"
F_LOG2 = MOUNT_PATH + "/longtou/db/" + RECIPE_NAME +"/emilia_pipe_1.log"
# --split_stereo
SHELL_COMMAND = f''' \
export CUDA_VISIBLE_DEVICES="0" \
&& . ./activate_python.sh \
&& python main_wds.py --config_path {CONFIG_PATH} --input_folder_path {INPUT_FOLDER_PATH} --wds_path {WDS_PATH} --gcs_url {GCS_URL} --f_log {F_LOG} --max_gpu_mem_frac 0.5 --start_shard 0 > /dev/null 2>&1 & sleep 10 && export CUDA_VISIBLE_DEVICES="0" && . ./activate_python.sh && python main_wds.py --config_path {CONFIG_PATH} --input_folder_path {INPUT_FOLDER_PATH2} --wds_path {WDS_PATH} --gcs_url {GCS_URL} --f_log {F_LOG2} --max_gpu_mem_frac 0.5 --start_shard 100
'''

def add_pod_annotation(
    task: PipelineTask,
    annotation_key: str,
    annotation_value: str,
) -> PipelineTask:
    """Pod metadata 에 annotation 을 추가하는 함수입니다.
    petethegreat(Peter Thompson)이 작성한 다음 PR 의 코드를 그대로 가져왔습니다.
    https://github.com/petethegreat/pipelines/commit/dfa93d5cedf5e558ff905767027f4eaf70652d98
    kfp 2.7.0 에는 아직 해당 기능이 포함되어 있지 않습니다.
    2.7.0 이후 해당 기능이 머지되면, 다음과 같은 방법으로 사용할 수 있을 것입니다.

    from kfp import dsl
    from kfp import kubernetes

    @dsl.component
    def comp():
        pass

    @dsl.pipeline
    def my_pipeline():
        task = comp()
        kubernetes.add_pod_annotation(
            task,
            annotation_key='run_id',
            annotation_value='123456',
        )
    """
    msg = common.get_existing_kubernetes_config_as_message(task)
    msg.pod_metadata.annotations.update({annotation_key: annotation_value})
    task.platform_config["kubernetes"] = json_format.MessageToDict(msg)

    return task

@dsl.container_component
def amphion_component(mount_path: str) -> dsl.ContainerSpec:
    command=["sh", "-c", SHELL_COMMAND, ]

    return dsl.ContainerSpec(image=IMAGE_URL,
                             command=command)
#@dsl.component
#def espnet_component(mount_path: str) -> str:
#    with open(f"./{mount_path}/longtou/log.txt","r") as fin:
#        print(fin.read())
#    return "done"


@dsl.pipeline
def amphion_pipe(
    project: str,
    location: str,
):
    pvc_mount_path = MOUNT_PATH
    task_1 = amphion_component(mount_path=pvc_mount_path)

    task_1.set_accelerator_type("nvidia.com/gpu")
    task_1.set_accelerator_limit(N_GPU)
    task_1.set_cpu_request(N_CPU)
    #task_1.set_cpu_limit(N_CPU)
    task_1.set_memory_request(MEM_SIZE)

    #kubernetes.mount_pvc(
    #    task_1,
    #    pvc_name="shm-memory-disk2",
    #    mount_path='/dev/shm',
    #)
    #######################################################
    # gcsfuse
    #######################################################
    add_pod_annotation(
        task_1,
        annotation_key="gke-gcsfuse/volumes",
        annotation_value="true",
    )

    kubernetes.mount_pvc(
        task_1,
        pvc_name="longtou-gcs-fuse-csi-static-pvc3",
        mount_path=pvc_mount_path,
    )

compiler.Compiler().compile(amphion_pipe, "amphion_pipe.yaml")

client = Client(host="https://3313888af2601658-dot-us-central1.pipelines.googleusercontent.com")
run = client.create_run_from_pipeline_package(
        "amphion_pipe.yaml",
        arguments={
            "project": "prod-ai-project",
            "location": "us-central1",
        },
)
