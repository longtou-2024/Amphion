#!/usr/bin/env bash

#--input_folder_path "gs://prod-ai-lab-speech-bucket/longtou/db/speechlabs/wds_v2/shard-000000.tar" \
python main_wds_lite.py \
    --config_path "/home/longtou.2024/mount/longtou/saved/Emilia/config.json" \
    --input_folder_path "gs://prod-ai-lab-speech-bucket/longtou/tmp/diquest_child/wds_v2/shard-000000.tar" \
    --wds_path emilia_pipe_lite \
    --gcs_url "gs://prod-ai-lab-speech-bucket/longtou/tmp/diquest_child/" \
    --f_log "emilia_pipe.log"
