import re
import emoji
import unicodedata
from collections import Counter

import tensorflow_datasets as tfds
import MeCab


class NanJThreadTitleEncoder(tfds.features.text.TextEncoder):
    NUM_RESERVED_WORDS = 4  # PAD, SOS, EOS, UNK
    PAD_TOKEN_ID, PAD_TOKEN = 0, "PAD"
    SOS_TOKEN_ID, SOS_TOKEN = 1, "SOS"
    EOS_TOKEN_ID, EOS_TOKEN = 2, "EOS"
    UNK_TOKEN_ID, UNK_TOKEN = 3, "UNK"
    SPECIAL_TOKEN_MAP = {
        "彡(゚)(゚)": "NANJMIN",
        "彡(^)(^)": "NIKOJMIN",
        "（ヽ´ん`）": "KENMOUKUN",
        "(´・ω・`)": "SHOBON",
        "(*^◯^*）": "POJIHAMEKUN",
        "「": "「",  # 隣の語とくっつくのを防ぐ
        "」": "」",  # 隣の語とくっつくのを防ぐ
        "『": "「",  # 寄せる
        "』": "」",  # 寄せる
    }
    SPECIAL_TOKEN_REGEX_MAP = {
        re.compile(r"キタ━+(.+)━+\!+"): "KITA",
        re.compile("ww+"): "KUSAxN",
        re.compile("[wnm][wnm]+"): "WNMxN",
        re.compile(">>>+"): ">>>",
        re.compile(r"\!+"): "!",
        re.compile(r"\?+"): "?",
        re.compile("[0-9]+"): "NUM",
    }
    IGNORE_PHRASES = [
        "[無断転載禁止]©2ch.net",
        "\\n", "\n", "・", "、", "。", ",", ".",
        "★", "☆", "○", "●", "◎" "◯ ", "■", "□"
    ]

    _id_to_token, _token_to_id = {}, {}

    def __init__(self, mecab_dict_path, id_to_token=None, token_to_id=None):
        self.reset_state()
        self.mecab_dict_path = mecab_dict_path
        self.mecab = MeCab.Tagger(f"-d {mecab_dict_path} -Owakati")
        if id_to_token is not None and token_to_id is not None:
            self._id_to_token = id_to_token
            self._token_to_id = token_to_id

    def reset_state(self):
        self._id_to_token = {
            self.PAD_TOKEN_ID: self.PAD_TOKEN,
            self.SOS_TOKEN_ID: self.SOS_TOKEN,
            self.EOS_TOKEN_ID: self.EOS_TOKEN,
            self.UNK_TOKEN_ID: self.UNK_TOKEN,
        }
        self._token_to_id = {
            self.PAD_TOKEN: self.PAD_TOKEN_ID,
            self.SOS_TOKEN: self.SOS_TOKEN_ID,
            self.EOS_TOKEN: self.EOS_TOKEN_ID,
            self.UNK_TOKEN: self.UNK_TOKEN_ID,
        }

    def check_fit_or_load(self):
        if len(self._token_to_id) <= self.NUM_RESERVED_WORDS:
            raise RuntimeError("not fitted or loaded yet!")

    def __preprocess(self, text):
        processed = unicodedata.normalize("NFKC", text)
        processed = processed.lower()
        for phrase in self.IGNORE_PHRASES:
            processed = processed.replace(phrase, " ")
        processed = emoji.get_emoji_regexp().sub(r' ', processed)
        return processed

    def tokenize(self, text):
        processed = self.__preprocess(text)
        for phrase, token in self.SPECIAL_TOKEN_MAP.items():
            processed = processed.replace(phrase, f" {token} ")
        for regex, token in self.SPECIAL_TOKEN_REGEX_MAP.items():
            processed = regex.sub(f" {token} ", processed)
        tokens = self.mecab.parse(processed).split()
        tokens = list(filter(lambda t: len(t) > 0, tokens))
        tokens = [self.SOS_TOKEN] + tokens + [self.EOS_TOKEN] 
        return tokens

    def fit(self, tokens_list, max_vocab=20000):
        special_tokens = frozenset([
            self.PAD_TOKEN, self.SOS_TOKEN, self.EOS_TOKEN, self.UNK_TOKEN
        ])
        cnt = Counter()

        for tokens in tokens_list:
            tokens = filter(lambda t: t not in special_tokens, tokens)
            tokens = list(set(tokens))  # 1タイトルで1カウントとする
            cnt.update(tokens)

        for idx, token_freq in enumerate(cnt.most_common(n=max_vocab)):
            token, _ = token_freq
            self._id_to_token[idx + self.NUM_RESERVED_WORDS] = token
            self._token_to_id[token] = idx + self.NUM_RESERVED_WORDS

    def encode(self, s):
        """Encodes text into a list of integers."""
        self.check_fit_or_load()
        if type(s) is str:
            tokens = self.tokenize(s)
        elif type(s) is tuple:
            tokens = list(s)
        elif type(s) is list:
            tokens = s
        else:
            raise RuntimeError("Unknow type")
        return [self._token_to_id.get(t, self.UNK_TOKEN_ID) for t in tokens]

    def decode(self, ids):
        """Decodes a list of integers into text."""
        self.check_fit_or_load()
        return [self._id_to_token[i] for i in ids]

    def vocab_size(self):
        """Size of the vocabulary. Decode produces ints [1, vocab_size)."""
        self.check_fit_or_load()
        return len(self._id_to_token)

    @classmethod
    def _filename(cls, filename_prefix):
        return filename_prefix + ".nanj"
        
    def save_to_file(self, filename_prefix):
        """Store to file. Inverse of load_from_file.
        format:
            mecab_dict_path
            token0
            token1
            token2
            ...
        """
        self.check_fit_or_load()
        filename = self._filename(filename_prefix)
        with open(filename, "w") as f:
            f.write(f"{self.mecab_dict_path}\n")
            for _, token in sorted(self._id_to_token.items()):
                f.write(f"{token}\n")

    @classmethod
    def load_from_file(cls, filename_prefix):
        """Load from file. Inverse of save_to_file."""
        filename = cls._filename(filename_prefix)
        id_to_token, token_to_id = {}, {}
        with open(filename) as f:
            mecab_dict_path = f.readline().rstrip()
            for idx, line in enumerate(f):
                token = line.rstrip()
                id_to_token[idx] = token
                token_to_id[token] = idx
        return cls(mecab_dict_path, id_to_token, token_to_id)
