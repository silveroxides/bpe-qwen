# bpe-qwen (High-Performance BPE Tokenizer)

[![CI](https://github.com/silveroxides/bpe-qwen/actions/workflows/build_release.yml/badge.svg)](https://github.com/silveroxides/bpe-qwen/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Rust](https://img.shields.io/badge/rust-stable-brightgreen.svg)](https://www.rust-lang.org/)

A blazing-fast BPE tokenizer for Qwen, Llama 3, Mistral, and other byte-level BPE models. Built with Rust and the [rust-gems BPE crate](https://github.com/github/rust-gems/tree/main/crates/bpe). This fork adds support for Python 3.13 and dynamic architecture detection.

## 🚀 Key Improvements in this Fork

- **Python 3.13 Support**: Full compatibility and optimized builds for the latest Python release.
- **Dynamic Architecture Support**: Automatically extracts pre-tokenization regex patterns from `tokenizer.json`. This allows the same engine to work blazingly fast with **Qwen2.5**, **Meta-Llama-3**, **Mistral**, and more.
- **Improved CLI Utility**: A dedicated `tokenize_cli.py` script for rapid testing and debugging of tokenizer files.
- **Stable ABI Builds**: CI/CD pipeline configured with forward compatibility for future Python versions.

## ✨ Features

- 🏎️ **Linear-time tokenization** using an optimized Rust backtracking implementation.
- 🎯 **Optimized Qwen Path**: Automatically uses a zero-allocation, indices-based fast path when Qwen-style patterns are detected.
- 🐍 **Seamless Integration**: Drop-in replacement for HuggingFace `PreTrainedTokenizerFast`.
- 📦 **Multi-Format Loader**: Supports both the traditional `vocab.json`/`merges.txt` pair and the modern unified `tokenizer.json`.
- ⚡ **SIMD Accelerated**: Fast ASCII detection using SSE2/NEON intrinsics.

## 📊 Benchmark Results

Benchmarked on a mixed dataset of code, prose, and technical documentation (approx. 500 texts, 1.3M characters).

| Tokenizer Implementation | Throughput (Chars/sec) | Speedup vs HF |
| :--- | :--- | :--- |
| **bpe-qwen (Rust)** | **47.36 M** | **13.8x** |
| SentencePiece (C++) | 10.51 M | 3.1x |
| Transformers (HF) | 3.44 M | 1.0x |

*System: Windows 11, Python 3.13. Results may vary by architecture.*

## 🛠️ Installation

### From Source (Recommended for Performance)
Building from source ensures the compiler can utilize your specific CPU features (SIMD, etc.).

```bash
# Clone the repository including the required Rust submodules
git clone --recursive https://github.com/silveroxides/bpe-qwen.git
cd bpe-qwen

# Install using pip (triggers Rust compilation)
pip install .
```

## 📖 Usage

### Python API
You can use `bpe_qwen` directly or as a drop-in replacement via the `AutoLinearTokenizer` wrapper.

```python
from bpe_qwen import AutoLinearTokenizer

# Load any byte-level BPE model (e.g., Llama-3 or Qwen2.5)
tokenizer = AutoLinearTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")

# Standard HuggingFace interface
text = "Rust is blazingly fast!"
outputs = tokenizer(text, return_tensors="pt")
print(outputs["input_ids"])

# Round-trip decoding
decoded = tokenizer.decode(outputs["input_ids"][0])
```

### Command Line Interface
Use the included CLI tool to quickly verify tokenizer outputs without writing code:

```bash
# Tokenize a single string
python tokenize_cli.py path/to/model_dir "Your prompt here"

# Tokenize a list of strings
python tokenize_cli.py path/to/model_dir "prompt one, prompt two" --is-list
```

## 🏗️ Development

To build the project in-place for development and run the included benchmarks:

```bash
# Build in release mode
maturin develop --release

# Run internal benchmarks
python benchmark_tokenizers.py
```

## 📜 License & Acknowledgments

- **Original Implementation**: [Sweep AI](https://sweep.dev)
- **Core Engine**: [rust-gems BPE crate](https://github.com/github/rust-gems)
- **Fork Maintainer**: [silveroxides](https://github.com/silveroxides)

This project is licensed under the MIT License.
