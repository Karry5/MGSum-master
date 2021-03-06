python process_hierarchical_sent_doc_copy.py \
       --source-lang src \
       --target-lang tgt \
       --testpref ./data/2000-300/test \
       --destdir multi-news-2000-300-copy \
       --workers 10 \
       --srcdict multi-news-2000-300-train/dict.src.txt \
       --tgtdict multi-news-2000-300-train/dict.tgt.txt \
       --dataset-impl raw \
       --task multi_loss_sent_word