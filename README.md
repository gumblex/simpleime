# Simple IME

A Simple Pinyin IME written in Python.

## Dependency

`pip3 install DAWG`

## Setup

* Download [luna_pinyin.dict.yaml](https://github.com/rime/brise/raw/master/preset/luna_pinyin.dict.yaml) from Rime.
* Run `python3 makeindex.py`.
* Put the generated \*.dawg and pinyinlookup.py into your working directory.

## Usage

* `import simpleime`
* `loaddict(f_index='pyindex.dawg', f_essay='essay.dawg')`
* `pinyininput(sentence)`: `sentence` is the Pinyin sequence.
