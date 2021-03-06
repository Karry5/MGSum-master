# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree. An additional grant of patent rights
# can be found in the PATENTS file in the same directory.

import math
import torch.nn.functional as F
import torch

from fairseq import utils

from . import FairseqCriterion, register_criterion


@register_criterion('word_sent_loss')
class WordSentLossCriterion(FairseqCriterion):

    def __init__(self, args, task):
        super().__init__(args, task)

    def forward(self, model, sample, reduce=True):
        """Compute the loss for the given sample.

        Returns a tuple with three elements:
        1) the loss
        2) the sample size, which is used as the denominator for the gradient
        3) logging outputs to display while training
        """
        net_output, sentence_decoder_out = model(**sample['net_input'])
        loss, _ = self.compute_loss(model, net_output, sample, reduce=reduce)
        sentence_loss, _ = self.compute_sentence_loss(model, sentence_decoder_out, sample, reduce=reduce)
        sample_size = sample['target'].size(0) if self.args.sentence_avg else sample['ntokens']
        logging_output = {
            'loss': utils.item(loss.data) if reduce else loss.data,
            'sent_loss': utils.item(sentence_loss.data) if reduce else sentence_loss.data,
            'doc_loss': 0,
            'ntokens': sample['ntokens'],
            'nsentences': sample['target'].size(0),
            'sample_size': sample_size,
            'sentence_size': sample['net_input']['doc_block_mask'].sum().item(),
            'doc_size': sample['doc_target_lengths'].sum().item(),
        }
        return loss, sentence_loss, sample_size, logging_output

    def compute_loss(self, model, net_output, sample, reduce=True):
        lprobs = model.get_normalized_probs(net_output, log_probs=True, sample=sample)
        lprobs = lprobs.view(-1, lprobs.size(-1))
        target = model.get_targets(sample, net_output).view(-1)
        loss = F.nll_loss(lprobs, target, size_average=False, ignore_index=self.padding_idx,
                          reduce=reduce)
        return loss, loss

    def compute_sentence_loss(self, model, net_output, sample, reduce=True):
        lprobs = model.sentence_decoder.get_normalized_probs(net_output, log_probs=True, sample=sample)
        lprobs = lprobs.view(-1, lprobs.size(-1))
        target = sample['sentence_target'].view(-1, 1)
        non_pad_mask = target.ne(6)
        nll_loss = F.nll_loss(lprobs, target.view(-1), size_average=False, ignore_index=6, reduce=reduce)
        smooth_loss = -lprobs.sum(dim=-1, keepdim=True)[non_pad_mask]
        if reduce:
            nll_loss = nll_loss.sum()
            smooth_loss = smooth_loss.sum()
        eps_i = 0.1 / lprobs.size(-1)
        loss = (1. - 0.1) * nll_loss + eps_i * smooth_loss
        return loss, nll_loss

    @staticmethod
    def aggregate_logging_outputs(logging_outputs):
        """Aggregate logging outputs from data parallel training."""
        loss_sum = sum(log.get('loss', 0) for log in logging_outputs)
        sent_loss_sum = sum(log.get('sent_loss', 0) for log in logging_outputs)
        doc_loss_sum = sum(log.get('doc_loss', 0) for log in logging_outputs)
        ntokens = sum(log.get('ntokens', 0) for log in logging_outputs)
        nsentences = sum(log.get('nsentences', 0) for log in logging_outputs)
        sample_size = sum(log.get('sample_size', 0) for log in logging_outputs)
        doc_size = sum(log.get('doc_size', 0) for log in logging_outputs)
        sentence_size = sum(log.get('sentence_size', 0) for log in logging_outputs)
        agg_output = {
            'loss': loss_sum / sample_size / math.log(2),
            'sent_loss': sent_loss_sum / sentence_size / math.log(2),
            'doc_loss': doc_loss_sum / doc_size / math.log(2),
            'ntokens': ntokens,
            'nsentences': nsentences,
            'sample_size': sample_size,
        }
        if sample_size != ntokens:
            agg_output['nll_loss'] = loss_sum / ntokens / math.log(2)
        return agg_output

