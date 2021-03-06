python process_hierarchical_sent_doc.py \
       --source-lang src \
       --target-lang tgt \
       --trainpref ./data/2000-300/train \
       --validpref ./data/2000-300/valid \
       --testpref ./data/2000-300/test \
       --destdir multi-news-2000-300-train \
       --joined-dictionary \
       --nwordssrc 50000 \
       --workers 10 \
       --task multi_loss_sent_word
