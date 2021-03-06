# MGSum
**Code for ACL'20 paper [Multi-Granularity Interaction Network for Extractive and Abstractive Multi-Document Summarization](https://www.aclweb.org/anthology/2020.acl-main.556/) by Hanqi Jin, Tianming Wang, Xiaojun Wan. This paper is accepted by ACL'20.**

Some codes are borrowed from [fairseq](https://github.com/pytorch/fairseq).

**Requirements and Installation：**
* PyTorch version >= 1.4.0
* Python version >= 3.6

**[Download Data](https://drive.google.com/file/d/1Ac1bCFEIhG8NgGeE_3AWP864MRovmK_7/view?usp=sharing)**


**Preprocess：**
```
python process_hierarchical_sent_doc.py --source-lang src --target-lang tgt \
  --trainpref ./data/2000-300/train --validpref ./data/2000-300/valid --testpref ./data/2000-300/test \
  --destdir multi-news-2000-300-train --joined-dictionary --nwordssrc 50000 --workers 10 --task multi_loss_sent_word
```
```
python process_hierarchical_sent_doc_copy.py --source-lang src --target-lang tgt \
  --testpref ./data/2000-300/test --destdir multi-news-2000-300-copy --workers 10 \
  --srcdict multi-news-2000-300-train/dict.src.txt --tgtdict multi-news-2000-300-train/dict.tgt.txt \
  --dataset-impl raw --task multi_loss_sent_word
```

**Train:**
```
CUDA_VISIBLE_DEVICES=0,1,2,3 python train.py multi-news-2000-300-train -a hierarchical_transformer_medium \
--optimizer adam --lr 0.0001 -s src -t tgt --dropout 0.1 --max-tokens 2000   \
--share-decoder-input-output-embed   --task multi_loss_sent_word --adam-betas '(0.9, 0.98)' \
--save-dir checkpoints/hierarchical_transformer-2000-300 --share-all-embeddings  \
--lr-scheduler reduce_lr_on_plateau --lr-shrink 0.5 --criterion multi_loss_doc_sent_word \
--ddp-backend no_c10d --num-workers 2 \
--update-freq 13 --encoder-normalize-before --decoder-normalize-before --sent-weight 2
```

**Test-abstractive:**
```
CUDA_VISIBLE_DEVICES=4 python generate_for_hie.py multi-news-2000-300-copy --task multi_loss_sent_word \
--path checkpoints/hierarchical_transformer-2000-300/checkpoint_best.pt --max-len-b 400 \
--batch-size 8 --beam 5  --no-repeat-ngram-size 3 --replace-unk --raw-text --lenpen 2  
```

**Test-extractive:**
```
CUDA_VISIBLE_DEVICES=4 python generate_for_select.py multi-news-2000-300-copy --task sent_extract \
--path checkpoints/hierarchical_transformer-2000-300/checkpoint_best.pt --batch-size 1 --replace-unk \
--raw-text
```

**Citation:**
```
@inproceedings{DBLP:conf/acl/JinWW20,
  author    = {Hanqi Jin and
               Tianming Wang and
               Xiaojun Wan},
  title     = {Multi-Granularity Interaction Network for Extractive and Abstractive
               Multi-Document Summarization},
  booktitle = {Proceedings of the 58th Annual Meeting of the Association for Computational
               Linguistics, {ACL} 2020, Online, July 5-10, 2020},
  pages     = {6244--6254},
  year      = {2020},
  crossref  = {DBLP:conf/acl/2020},
  url       = {https://www.aclweb.org/anthology/2020.acl-main.556/},
  timestamp = {Wed, 24 Jun 2020 17:15:07 +0200},
  biburl    = {https://dblp.org/rec/conf/acl/JinWW20.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

