# bpe-qwen (silveroxides fork)

A blazing-fast BPE tokenizer for Qwen and other LLM models, built with Rust and the [rust-gems BPE crate](https://github.com/github/rust-gems/tree/main/crates/bpe). Achieves **6x-18x faster** tokenization compared to HuggingFace tokenizers.

## Features

- 🚀 **Linear-time tokenization** based on the rust-gems BPE crate.
- 🎯 **Dynamic Architecture Support**: Automatically extracts pre-tokenization regex from `tokenizer.json`, supporting Qwen2, Llama 3, Mistral, and more.
- 🐍 **Python bindings** via PyO3 for seamless integration.
- 📦 **Multi-format support**: Loads from standard `vocab.json`/`merges.txt` or combined `tokenizer.json`.
- ⚡ **Extremely fast**: Built with SIMD ASCII detection and optimized Rust backtracking.
- ✅ **100% accuracy verified** against HuggingFace baselines.

## Installation

### From PyPI
```bash
pip install bpe-qwen
```

### From Source (this fork)
Requires the Rust toolchain and Python 3.10+.

```bash
# Clone with submodules (CRITICAL)
git clone --recursive https://github.com/silveroxides/bpe-qwen.git
cd bpe-qwen

# Install
pip install .
```

## Usage

### Using the CLI tool
We provide a convenient CLI tool for quick tokenization:
```bash
python tokenize_cli.py /path/to/tokenizer_dir "Hello, world!"
```

### Quick Start in Python
Use `bpe-qwen` as a drop-in replacement for HuggingFace tokenizers:

```python
from bpe_qwen import AutoLinearTokenizer

# This automatically uses the fast Rust bpe-qwen under the hood
tokenizer = AutoLinearTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")

# Use it exactly like a HuggingFace tokenizer
outputs = tokenizer("Hello, world!", return_tensors="pt")
print(outputs["input_ids"])
```

## Benchmark Results

Performance comparison on various text samples:

| Tokenizer | Encoding Speed | Speedup vs HF |
|-----------|----------------|---------------|
| **bpe-qwen (Rust)** | **47.3M chars/sec** | **~14x** |
| SentencePiece | 10.5M chars/sec | ~3x |
| Transformers (HF) | 3.4M chars/sec | 1.0x |

## Development

### Building and Testing
```bash
# Build in-place for development
maturin develop --release

# Run benchmarks
python benchmark_tokenizers.py
```

## Limitations
- Optimized for Byte-level BPE architectures.

## Acknowledgments
- Original project by [Sweep AI](https://sweep.dev).
- Built on top of the [rust-gems BPE crate](https://github.com/github/rust-gems).
