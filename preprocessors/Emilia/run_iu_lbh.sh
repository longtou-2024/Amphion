# longtou.2024
# At each tmuc pane, run it
# . run.sh (O)
# ./run.sh (X) <-- error

#conda activate amphion

export CUDA_VISIBLE_DEVICES=0
python main.py --config_path /home/longtou.2024/mount/longtou/saved/Emilia/config.json --input_folder_path outdir_iu

