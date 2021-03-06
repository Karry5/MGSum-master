CUDA_VISIBLE_DEVICES=4 python generate_for_hie.py multi-news-2000-300-copy \
                       --task multi_loss_sent_word \
                       --path checkpoints/hierarchical_transformer-2000-300-maxtoken-2600-freq-40-cu05/checkpoint_best.pt \
                       --max-len-b 400 \
                       --batch-size 1 \
                       --beam 5  \
                       --no-repeat-ngram-size 3 \
                       --replace-unk \
                       --raw-text \
                       --lenpen 2 > test_abstractive_1.out
