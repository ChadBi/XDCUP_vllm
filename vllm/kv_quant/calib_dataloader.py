# Copyright (c) OpenMMLab. All rights reserved.
import numpy as np
import torch


def set_seed(seed):
    np.random.seed(seed)
    torch.random.manual_seed(seed)


def get_wikitext2(tokenizer, nsamples, seed, seqlen, path=None):
    """Load Wikitext-2 train and test datasets and tokenize.
    Args:
        tokenizer: Tokenizer to encode text.
        nsamples: Number of samples to take from train set.
        seed: Random seed for sampling.
        seqlen: Maximum sequence length.
    Returns:
        train_loader: List of sampled and tokenized training examples.
        test_enc: Full tokenized Wikitext-2 test set.
    """
    from datasets import load_dataset
    traindata = load_dataset(path if path else 'wikitext',
                             'wikitext-2-raw-v1',
                             split='train')
    testdata = load_dataset(path if path else 'wikitext',
                            'wikitext-2-raw-v1',
                            split='test')

    trainenc = tokenizer('\n\n'.join(traindata['text']), return_tensors='pt')
    testenc = tokenizer('\n\n'.join(testdata['text']), return_tensors='pt')

    import random
    random.seed(seed)
    trainloader = []
    for _ in range(nsamples):
        i = random.randint(0, trainenc.input_ids.shape[1] - seqlen)
        j = i + seqlen
        inp = trainenc.input_ids[:, i:j]
        tar = inp.clone()
        tar[:, :-1] = -100
        trainloader.append((inp, tar))
    return trainloader, testenc


def get_ptb(tokenizer, nsamples, seed, seqlen):
    """Load PTB train and validation datasets and tokenize.
    Args:
        tokenizer: Tokenizer to encode text.
        nsamples: Number of samples to take from train set.
        seed: Random seed for sampling.
        seqlen: Maximum sequence length.
    Returns:
        train_loader: List of sampled and tokenized training examples.
        test_enc: Full tokenized PTB validation set.
    """
    from datasets import load_dataset
    traindata = load_dataset('ptb_text_only', 'penn_treebank', split='train')
    valdata = load_dataset('ptb_text_only',
                           'penn_treebank',
                           split='validation')

    trainenc = tokenizer('\n\n'.join(traindata['sentence']),
                         return_tensors='pt')
    testenc = tokenizer('\n\n'.join(valdata['sentence']), return_tensors='pt')

    import random
    random.seed(seed)
    trainloader = []
    for _ in range(nsamples):
        i = random.randint(0, trainenc.input_ids.shape[1] - seqlen)
        j = i + seqlen
        inp = trainenc.input_ids[:, i:j]
        tar = inp.clone()
        tar[:, :-1] = -100
        trainloader.append((inp, tar))
    return trainloader, testenc


def get_c4(tokenizer, nsamples, seed, seqlen, path=None):
    """Load C4 train and validation datasets and tokenize.
    Args:
        tokenizer: Tokenizer to encode text.
        nsamples: Number of samples to take from train set.
        seed: Random seed for sampling.
        seqlen: Maximum sequence length.
    Returns:
        train_loader: List of sampled and tokenized training examples.
        test_enc: Full tokenized PTB validation set.
    """
    from datasets import load_dataset
    traindata = load_dataset(
        path if path else 'allenai/c4',
        'allenai--c4',
        data_files={'train': 'en/c4-train.00000-of-01024.json.gz'},
        split='train',
        use_auth_token=False)
    valdata = load_dataset(
        path if path else 'allenai/c4',
        'allenai--c4',
        data_files={'validation': 'en/c4-validation.00000-of-00008.json.gz'},
        split='validation',
        use_auth_token=False)

    import random
    random.seed(seed)
    trainloader = []
    for _ in range(nsamples):
        while True:
            i = random.randint(0, len(traindata) - 1)
            trainenc = tokenizer(traindata[i]['text'], return_tensors='pt')
            if trainenc.input_ids.shape[1] >= seqlen:
                break
        i = random.randint(0, trainenc.input_ids.shape[1] - seqlen)
        j = i + seqlen
        inp = trainenc.input_ids[:, i:j]
        tar = inp.clone()
        tar[:, :-1] = -100
        trainloader.append((inp, tar))

    valenc = []
    for _ in range(256):
        while True:
            i = random.randint(0, len(valdata) - 1)
            tmp = tokenizer(valdata[i]['text'], return_tensors='pt')
            if tmp.input_ids.shape[1] >= seqlen:
                break
        i = random.randint(0, tmp.input_ids.shape[1] - seqlen)
        j = i + seqlen
        valenc.append(tmp.input_ids[:, i:j])
    valenc = torch.hstack(valenc)

    class TokenizerWrapper:

        def __init__(self, input_ids):
            self.input_ids = input_ids

    valenc = TokenizerWrapper(valenc)

    return trainloader, valenc


def get_ptb_new(tokenizer, nsamples, seed, seqlen):
    """Load PTB New train and validation datasets and tokenize.
    Args:
        tokenizer: Tokenizer to encode text.
        nsamples: Number of samples to take from train set.
        seed: Random seed for sampling.
        seqlen: Maximum sequence length.
    Returns:
        train_loader: List of sampled and tokenized training examples.
        test_enc: Full tokenized PTB validation set.
    """
    from datasets import load_dataset
    traindata = load_dataset('ptb_text_only', 'penn_treebank', split='train')
    testdata = load_dataset('ptb_text_only', 'penn_treebank', split='test')

    trainenc = tokenizer(' '.join(traindata['sentence']), return_tensors='pt')
    testenc = tokenizer(' '.join(testdata['sentence']), return_tensors='pt')

    import random
    random.seed(seed)
    trainloader = []
    for _ in range(nsamples):
        i = random.randint(0, trainenc.input_ids.shape[1] - seqlen)
        j = i + seqlen
        inp = trainenc.input_ids[:, i:j]
        tar = inp.clone()
        tar[:, :-1] = -100
        trainloader.append((inp, tar))
    return trainloader, testenc


def get_c4_new(tokenizer, nsamples, seed, seqlen):
    """Load C4 New train and validation datasets and tokenize.
    Args:
        tokenizer: Tokenizer to encode text.
        nsamples: Number of samples to take from train set.
        seed: Random seed for sampling.
        seqlen: Maximum sequence length.
    Returns:
        train_loader: List of sampled and tokenized training examples.
        test_enc: Full tokenized PTB validation set.
    """
    from datasets import load_dataset
    traindata = load_dataset(
        'allenai/c4',
        'allenai--c4',
        data_files={'train': 'en/c4-train.00000-of-01024.json.gz'},
        split='train')
    valdata = load_dataset(
        'allenai/c4',
        'allenai--c4',
        data_files={'validation': 'en/c4-validation.00000-of-00008.json.gz'},
        split='validation')

    import random
    random.seed(seed)
    trainloader = []
    for _ in range(nsamples):
        while True:
            i = random.randint(0, len(traindata) - 1)
            trainenc = tokenizer(traindata[i]['text'], return_tensors='pt')
            if trainenc.input_ids.shape[1] >= seqlen:
                break
        i = random.randint(0, trainenc.input_ids.shape[1] - seqlen)
        j = i + seqlen
        inp = trainenc.input_ids[:, i:j]
        tar = inp.clone()
        tar[:, :-1] = -100
        trainloader.append((inp, tar))

    valenc = tokenizer(' '.join(valdata[:1100]['text']), return_tensors='pt')
    valenc = valenc.input_ids[:, :(256 * seqlen)]

    class TokenizerWrapper:

        def __init__(self, input_ids):
            self.input_ids = input_ids

    valenc = TokenizerWrapper(valenc)

    return trainloader, valenc


def get_pileval(tokenizer, nsamples, seed, path, seqlen=512):
    """Load pileval train dataset and tokenize.
    Args:
        tokenizer: Tokenizer to encode text.
        nsamples: Number of samples to take from train set.
        seed: Random seed for sampling.
        seqlen: Maximum sequence length.
    Returns:
        train_loader: List of sampled and tokenized training examples.
        test_enc: Full tokenized PTB validation set.
    """
    from datasets import load_dataset
    from datasets.builder import DatasetGenerationError
    try:
        dataset = load_dataset('json', data_files=path, split='train')
    except DatasetGenerationError as err:
        raise InterruptedError('There have been some issues when generating '
                               'the dataset, you could try to download it '
                               'locally first, and replace the `data_files`'
                               'with local addresses or use other datasets '
                               '(c4, wiki, ptb).') from err
    dataset = dataset.shuffle(seed=seed)
    samples = []
    n_run = 0
    for data in dataset:
        line = data['text']
        line = line.strip()
        line_encoded = tokenizer.encode(line)
        if len(line_encoded) > 512:
            continue
        sample = torch.tensor([line_encoded])
        if sample.numel() == 0:
            continue
        samples.append(sample)
        n_run += 1
        if n_run == nsamples:
            break
    # now concatenate all samples and split according to block size
    cat_samples = torch.cat(samples, dim=1)
    n_split = cat_samples.shape[1] // seqlen
    print(f' * Split into {n_split} blocks')
    return [
        cat_samples[:, i * seqlen:(i + 1) * seqlen] for i in range(n_split)
    ], None


def get_sharegpt(tokenizer, nsamples, seed, path, seqlen=2048):
    """Load ShareGPT dataset and tokenize for calibration.
    Args:
        tokenizer: Tokenizer to encode text.
        nsamples: Number of samples to take.
        seed: Random seed for sampling.
        path: Path to ShareGPT JSON dataset.
        seqlen: Maximum sequence length.
    Returns:
        samples: List of tokenized training examples.
    """
    from datasets import load_dataset
    from datasets.builder import DatasetGenerationError
    import numpy as np
    import torch

    try:
        dataset = load_dataset('json', data_files=path, split='train')
    except DatasetGenerationError as err:
        raise InterruptedError('Failed to load ShareGPT dataset. '
                               'Ensure the path is correct and the format is valid.') from err

    # 随机打乱数据集
    np.random.seed(seed)
    indices = np.random.permutation(len(dataset))
    samples = []
    n_collected = 0

    for idx in indices:
        # 获取对话样本
        conv = dataset[int(idx)]['conversations']

        # 拼接对话（USER: ...\nASSISTANT: ... 格式）
        text = ""
        for turn in conv:
            role = "USER: " if turn['from'] == 'human' else "ASSISTANT: "
            text += role + turn['value'].strip() + "\n"

        # 编码并截断
        encoded = tokenizer.encode(
            text,
            truncation=True,
            max_length=seqlen,
            padding='max_length'
        )

        # 转换为张量 (1, seqlen)
        sample = torch.tensor([encoded])

        # 确保最终形状为 (1, seqlen)
        if sample.shape[1] != seqlen:
            # 如果仍有异常长度（如特殊 token 导致），跳过该样本
            continue

        samples.append(sample)
        n_collected += 1

        if n_collected == nsamples:
            break

    print(f" * Collected {len(samples)} ShareGPT samples for calibration")
    return samples, None  # 返回样本列表和 None（无测试数据）

def get_calib_loaders(name,
                      tokenizer,
                      nsamples=128,
                      seed=0,
                      seqlen=2048,
                      path=None):
    """Get calibration data loaders for a dataset.
    Args:
      name: Dataset name ('wikitext2', 'ptb', 'c4', etc).
      tokenizer: Tokenizer to encode text.
      nsamples: Number of samples to take from train set.
      seed: Random seed for sampling.
      seqlen: Maximum sequence length.
    Returns:
      train_loader: List of sampled and tokenized training examples.
      test_data: Full tokenized validation set.
    """
    if 'wikitext2' in name:
        return get_wikitext2(tokenizer, nsamples, seed, seqlen, path)
    if 'ptb' in name:
        if 'new' in name:
            return get_ptb_new(tokenizer, nsamples, seed, seqlen)
        return get_ptb(tokenizer, nsamples, seed, seqlen)
    if 'c4' in name:
        if 'new' in name:
            return get_c4_new(tokenizer, nsamples, seed, seqlen)
        return get_c4(tokenizer, nsamples, seed, seqlen, path)

    if 'pileval' in name:
        if path is None:
            path = 'https://the-eye.eu/public/AI/pile/val.jsonl.zst'
        return get_pileval(tokenizer, nsamples, seed, path, seqlen)
    if 'sharegpt' in name.lower():
        return get_sharegpt(tokenizer, nsamples, seed, path, seqlen)