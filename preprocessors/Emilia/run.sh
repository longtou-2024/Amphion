# longtou.2024
# At each tmuc pane, run it
# . run.sh (O)
# ./run.sh (X) <-- error

conda activate amphion

export CUDA_VISIBLE_DEVICES=$1
python main.py --config_path config${1}.json
