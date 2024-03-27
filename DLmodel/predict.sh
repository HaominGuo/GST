python3 predict.py \
--max_len=150 \
--model_name_or_path="./rbt3" \
--per_gpu_eval_batch_size=500 \
--output_dir="./output" \
--fine_tunning_model="./output/best_model.pkl"