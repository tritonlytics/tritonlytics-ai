# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02a_verbatims-core.ipynb (unless otherwise specified).

__all__ = ['m_pre_standard_themes_saw', 'm_suf_standard_themes_saw', 'saw_standard_themes_train_config',
           'get_saw_standard_theme_train_data', 'get_saw_standard_theme_train_x', 'get_saw_standard_theme_train_dls',
           'm_pre_standard_themes_meta', 'm_suf_standard_themes_meta', 'meta_standard_themes_train_config',
           'get_meta_standard_theme_train_data', 'get_meta_standard_theme_train_x', 'get_meta_standard_theme_train_dls']

# Cell
import os, datetime
import sklearn.metrics as skm
from ..utils import *

from fastai.text.all import *
from transformers import *
from blurr.utils import *
from blurr.data.core import *
from blurr.modeling.core import *

# Cell
m_pre_standard_themes_saw = ''
m_suf_standard_themes_saw = '_multilabel_hf'

saw_standard_themes_train_config = {
    'm_suf': m_suf_standard_themes_saw,
    'm_pre': m_pre_standard_themes_saw,

    'batch_size': 8,
    'corpus_cols': ['answer_text'],
    'corpus_suf': '_ans',
    'train_data': STANDARD_THEME_SAW_PATH/'train.csv',
    'valid_data': STANDARD_THEME_SAW_PATH/'test.csv',
    'cache_data_path': STANDARD_THEME_SAW_PATH/'data_cls_standard_themes_saw.pkl',

    'opt_beta': 0.5,
    'opt_beta_average': 'weighted',
    'opt_beta_sample_weight': None,
    'opt_start': 0.08,
    'opt_end': 0.7,

    'save_model_monitor': 'precision_score',
    'save_model_comp': np.greater,
    'save_model_filename': f'{m_pre_standard_themes_saw}cls_bestmodel{m_suf_standard_themes_saw}',
    'export_filename': f'{m_pre_standard_themes_saw}export_clas{m_suf_standard_themes_saw}.pkl',

    'learner_path': STANDARD_THEME_SAW_PATH
}

# Cell
def get_saw_standard_theme_train_data(train_config={}, trg_labels=STANDARD_THEME_SAW_LABELS):
    config = {**saw_standard_themes_train_config, **train_config}

    train_df = pd.read_csv(config['train_data'])
    train_df.dropna(subset=config['corpus_cols'], inplace=True)
    train_df['labels'] = train_df[trg_labels].apply(lambda x: ' '.join(x.index[x.astype(bool)]), axis=1)
    train_df['is_valid'] = False

    if ('valid_data' in config and config['valid_data'] is not None):
        valid_df = pd.read_csv(config['valid_data'])
        valid_df.dropna(subset=config['corpus_cols'], inplace=True)
        valid_df['labels'] = valid_df[trg_labels].apply(lambda x: ' '.join(x.index[x.astype(bool)]), axis=1)
        valid_df['is_valid'] = True

        return pd.concat([train_df, valid_df])

    return train_df

# Cell
def get_saw_standard_theme_train_x(inp, corpus_cols): return ': '.join(inp[corpus_cols].values)

def get_saw_standard_theme_train_dls(df, hf_arch, hf_tokenizer, vocab=STANDARD_THEME_SAW_LABELS,
                                     train_config={}, use_cache=True):

    config = {**saw_standard_themes_train_config, **train_config}
    cache_path = config['cache_data_path'] if ('cache_data_path' in config) else None

    if (use_cache and cache_path is not None):
        if (os.path.isfile(cache_path)):
            dls = torch.load(cache_path)
            dls.bs = config['batch_size']

    blocks = (
        HF_TextBlock(hf_arch=hf_arch, hf_tokenizer=hf_tokenizer),
        MultiCategoryBlock(encoded=True, vocab=vocab)
    )

    dblock = DataBlock(blocks=blocks,
                       get_x=partial(get_saw_standard_theme_train_x, corpus_cols=config['corpus_cols']),
                       get_y=ColReader(vocab),
                       splitter=ColSplitter(col='is_valid'))

    dls = dblock.dataloaders(df, bs=config['batch_size'])
    if (cache_path is not None): torch.save(dls, config['cache_data_path'])

    return dls

# Cell
m_pre_standard_themes_meta = ''
m_suf_standard_themes_meta = '_multitask_hf'

meta_standard_themes_train_config = {
    'm_pre': m_pre_standard_themes_meta,
    'm_suf': m_suf_standard_themes_meta,

    'batch_size': 8,
    'corpus_cols': ['theme', 'answer_text'],
    'corpus_suf': '_multitask',
    'train_data': STANDARD_THEME_META_PATH/'train.csv',
    'valid_data': STANDARD_THEME_META_PATH/'test.csv',
    'cache_data_path': STANDARD_THEME_META_PATH/'data_mm_standard_themes_meta.pkl',

    'opt_beta': 0.5,
    'opt_beta_average': 'binary',
    'opt_beta_sample_weight': None,
    'opt_start': 0.08,
    'opt_end': 0.7,

    'save_model_monitor': 'valid_loss',
    'save_model_comp': np.less,
    'save_model_filename': f'{m_pre_standard_themes_meta}mm_bestmodel{m_suf_standard_themes_meta}',
    'export_filename': f'{m_pre_standard_themes_meta}export_mm{m_suf_standard_themes_meta}.pkl',

    'learner_path': STANDARD_THEME_META_PATH
}

# Cell
def get_meta_standard_theme_train_data(train_config={}):
    config = {**meta_standard_themes_train_config, **train_config}

    train_df = pd.read_csv(config['train_data'])
    train_df.dropna(subset=config['corpus_cols'], inplace=True)
    train_df['is_valid'] = False

    if ('valid_data' in config and config['valid_data'] is not None):
        valid_df = pd.read_csv(config['valid_data'])
        valid_df.dropna(subset=config['corpus_cols'], inplace=True)
        valid_df['is_valid'] = True

        return pd.concat([train_df, valid_df])

    return train_df

# Cell
def get_meta_standard_theme_train_x(inp, corpus_cols): return 'theme: ' + ' comment: '.join(inp[corpus_cols].values)

def get_meta_standard_theme_train_dls(df, hf_arch, hf_tokenizer, train_config={}, use_cache=True):

    config = {**meta_standard_themes_train_config, **train_config}
    cache_path = config['cache_data_path'] if ('cache_data_path' in config) else None

    if (use_cache and cache_path is not None):
        if (os.path.isfile(cache_path)):
            dls = torch.load(cache_path)
            dls.bs = config['batch_size']

    blocks = (
        HF_TextBlock(hf_arch=hf_arch, hf_tokenizer=hf_tokenizer),
        RegressionBlock(),
        CategoryBlock()
    )

    dblock = DataBlock(blocks=blocks,
                       get_x=partial(get_meta_standard_theme_train_x, corpus_cols=config['corpus_cols']),
                       get_y=[ColReader('avg_sentiment'), ColReader('is_example')],
                       splitter=ColSplitter(col='is_valid'),
                       n_inp=1)

    dls = dblock.dataloaders(df, bs=config['batch_size'])
    if (cache_path is not None): torch.save(dls, config['cache_data_path'])

    return dls