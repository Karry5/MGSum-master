CUDA_VISIBLE_DEVICES=5 python generate_for_select.py multi-news-2000-300-copy \
                       --task sent_extract \
                       --path checkpoints/hierarchical_transformer-2000-300-maxtoken-2600-freq-40-cu05/checkpoint_best.pt \
                       --batch-size 1 \
                       --replace-unk \
                       --raw-text > test_extractive.out
