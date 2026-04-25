import argparse
import os
import sys
import json
import tempfile
import shutil
from bpe_qwen import QwenTokenizer

def load_tokenizer_from_dir(tokenizer_dir):
    vocab_path = os.path.join(tokenizer_dir, "vocab.json")
    merges_path = os.path.join(tokenizer_dir, "merges.txt")
    tokenizer_json_path = os.path.join(tokenizer_dir, "tokenizer.json")
    
    # Try looking for standard vocab.json and merges.txt
    if os.path.exists(vocab_path) and os.path.exists(merges_path):
        return QwenTokenizer(tokenizer_dir), None
        
    # If standard files aren't there, check for tokenizer.json or a combined vocab.json
    json_to_parse = None
    if os.path.exists(tokenizer_json_path):
        json_to_parse = tokenizer_json_path
    elif os.path.exists(vocab_path):
        json_to_parse = vocab_path
        
    if json_to_parse:
        try:
            with open(json_to_parse, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if "model" in data and "vocab" in data["model"] and "merges" in data["model"]:
                vocab = data["model"]["vocab"]
                merges = data["model"]["merges"]
                
                temp_dir = tempfile.mkdtemp()
                temp_vocab_path = os.path.join(temp_dir, "vocab.json")
                temp_merges_path = os.path.join(temp_dir, "merges.txt")
                
                with open(temp_vocab_path, 'w', encoding='utf-8') as f:
                    json.dump(vocab, f, ensure_ascii=False)
                    
                with open(temp_merges_path, 'w', encoding='utf-8') as f:
                    f.write("#version: 0.2\n")
                    for merge in merges:
                        if isinstance(merge, str):
                            f.write(merge + "\n")
                        elif isinstance(merge, list) and len(merge) == 2:
                            f.write(f"{merge[0]} {merge[1]}\n")
                            
                tokenizer_config_path = os.path.join(tokenizer_dir, "tokenizer_config.json")
                if os.path.exists(tokenizer_config_path):
                    shutil.copy(tokenizer_config_path, temp_dir)
                            
                return QwenTokenizer(temp_dir), temp_dir
        except Exception as e:
            print(f"Failed parsing json {json_to_parse}: {e}")
            
    print(f"Error: Could not find valid vocab.json and merges.txt, or a valid combined JSON in {tokenizer_dir}")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Tokenize strings using the bpe-qwen fast tokenizer.")
    parser.add_argument(
        "tokenizer_dir",
        type=str,
        help="Path to the directory containing vocab.json/merges.txt or a combined tokenizer.json/vocab.json"
    )
    parser.add_argument(
        "text",
        type=str,
        help="The string to tokenize, or a comma-separated list of strings if --is-list is provided."
    )
    parser.add_argument(
        "--is-list",
        action="store_true",
        help="If set, the text argument will be treated as a comma-separated list of strings."
    )

    args = parser.parse_args()

    print(f"Loading tokenizer from {args.tokenizer_dir}...")
    try:
        tokenizer, temp_dir = load_tokenizer_from_dir(args.tokenizer_dir)
    except Exception as e:
        print(f"Failed to load tokenizer: {e}")
        sys.exit(1)

    print(f"Tokenizer loaded successfully. Vocabulary size: {tokenizer.vocab_size()}")
    print("-" * 50)

    try:
        if args.is_list:
            # Split by comma and strip whitespace
            texts = [t.strip() for t in args.text.split(",")]
            for i, text in enumerate(texts):
                if not text:
                    continue
                tokens = tokenizer.encode(text)
                decoded = tokenizer.decode(tokens)
                print(f"Item {i+1}: '{text}'")
                print(f"  Tokens:  {tokens}")
                print(f"  Decoded: '{decoded}'")
                print("-" * 50)
        else:
            tokens = tokenizer.encode(args.text)
            decoded = tokenizer.decode(tokens)
            print(f"Input:   '{args.text}'")
            print(f"Tokens:  {tokens}")
            print(f"Decoded: '{decoded}'")
    finally:
        # Clean up temporary directory if we created one
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()