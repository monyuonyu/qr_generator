# QR Code Generator

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](./LICENSE)

QR Code Generator Pro is an open-source Python application that allows you to **easily generate QR codes**.  
It supports both GUI and CLI modes, enabling flexible QR code creation through either an **intuitive interface** or **command line**.  
When creating QR codes, you can add text, customize font size and colors, specify error correction levels, and adjust image sizes.

---

## Table of Contents
1. [Key Features](#key-features)
2. [Directory Structure](#directory-structure)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
   - [GUI Mode](#gui-mode)
   - [CLI Mode](#cli-mode)
6. [Command Line Options](#command-line-options)
7. [License](#license)
8. [Notes](#notes)
9. [Contact & Contribution](#contact--contribution)

---

## Key Features

- **GUI Mode**
  - Easy-to-use interface built with PySide6
  - Configure text, colors, and sizes while checking the preview
  - Easily save generated images

- **CLI Mode**
  - Batch generate QR codes by specifying command line arguments
  - Support for error correction levels, sizes, and colors
  - Displays QR code information (version, data size, etc.) in results

- **Customization**
  - Add text below QR codes
  - Freely modify font size, colors, and background colors
  - Choose error correction levels (L, M, Q, H)
  - Smooth display even in high DPI environments

---

## Directory Structure

```
├── LICENSE
├── qr_generator.py     # Main QR code generation script
├── requirements.txt    # List of required packages
└── README.md          # This file
```

---

## Requirements

- Python 3.6 or later (Recommended: 3.8+)
- Works on Windows / Mac / Linux (depends on PySide6 support)

### Dependencies
- [qrcode](https://pypi.org/project/qrcode/)
- [Pillow](https://pypi.org/project/Pillow/)
- [PySide6](https://pypi.org/project/PySide6/)

---

## Installation

1. **Get the Repository**
   - Clone this repository from GitHub or download as ZIP and extract to any directory.

2. **Create Virtual Environment (Optional)**
   - If you want to isolate dependencies from other projects, create and activate a Python virtual environment (e.g., venv).

3. **Install Packages**
   - You can install all dependencies at once using `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

---

## Usage

### GUI Mode

Launch GUI mode using either of these methods:

```bash
# Run without arguments
python qr_generator.py
```
or
```bash
# Run with --gui option
python qr_generator.py --gui
```

#### Main GUI Operations

1. **Data**
   - Enter the string (URL etc.) to be encoded in the QR code.
   - A warning will display if left blank, and QR code cannot be generated.

2. **Text**
   - Enter text to display below the QR code (optional).

3. **Font Size**
   - Specify the font size for displayed text.

4. **Color Settings**
   - Select "QR Code Color" and "Background Color" via buttons.

5. **Error Correction Level**
   - Choose from `L (7%)`, `M (15%)`, `Q (25%)`, `H (30%)`.
   - `H` provides highest error correction but uses more QR code capacity.

6. **QR Code Size**
   - Specify the size of QR code dots (modules) (box_size).

7. **Preview**
   - Press "Generate QR Code" button to display result in preview screen.

8. **Save Image**
   - Press "Save Image" button to open file dialog and choose save location.

### CLI Mode

In CLI mode, **`--data` is required**, and other options can be added as needed.

#### Simple Example

```bash
python qr_generator.py --data "Hello World!"
```
- Outputs QR code image as `qrcode.png`.

#### Example with Output Path and Text

```bash
python qr_generator.py \
    --data "https://example.com" \
    --text "Sample Site" \
    --output sample_qr.png
```
- Outputs as `sample_qr.png` with "Sample Site" text below.

#### Example with Colors and Error Correction Level

```bash
python qr_generator.py \
    --data "Sample Data" \
    --qr-size 8 \
    --qr-color "#FF0000" \
    --bg-color "#FFFFFF" \
    --error-level M \
    --output colored_qr.png
```
- Generates QR code with size 8, foreground color red (`#FF0000`), background color white (`#FFFFFF`), and error correction level M(15%).

---

## Command Line Options

| Option           | Description                                                           | Default     |
| :--------------- | :-------------------------------------------------------------------- | :---------- |
| `--gui`          | Launch in GUI mode.                                                    | -           |
| `--data`         | **Required**. Specify data to encode in QR code.                       | None        |
| `--text`         | Specify text to display below.                                         | None        |
| `--output`       | Specify output file path. Outputs as `qrcode.png` if not specified.    | qrcode.png  |
| `--qr-size`      | QR code size (box_size).                                               | 10          |
| `--text-size`    | Text font size.                                                        | 20          |
| `--qr-color`     | QR code color (e.g., `black`, `#FF0000`).                             | black       |
| `--bg-color`     | Background color (e.g., `white`, `#FFFFFF`).                           | white       |
| `--error-level`  | Error correction level. Choose from `L, M, Q, H`.                      | H           |

---

## License

This project is released under the [GNU General Public License v3.0](./LICENSE).  
Please check the [LICENSE](./LICENSE) file for details.

---

## Notes

1. **About Fonts**
   - By default, prioritizes "meiryo.ttc" or "msgothic.ttc" on Windows environments.
   - Falls back to Pillow's default font if these fonts aren't found. Character corruption may occur in such cases.

2. **GUI Window Size**
   - Current implementation uses fixed window size. UI may be partially cut off depending on screen resolution.

3. **Version Compatibility**
   - Designed for Python 3.6 and later. May not work with certain dependency versions.

---

# QRコードジェネレーター（日本語）

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](./LICENSE)

QRコードジェネレーター Pro は、**QRコードを簡単に生成**できるオープンソースの Python アプリケーションです。  
GUIモードとCLIモードの両方に対応しており、**直感的な操作**または**コマンドライン**から柔軟にQRコードを作成できます。  
作成時にはテキストの追加、フォントサイズやカラー設定、エラー訂正レベルの指定、画像サイズのカスタマイズなどが可能です。

---

## 目次
1. [主な機能](#主な機能)  
2. [ディレクトリ構成](#ディレクトリ構成)  
3. [必要な環境](#必要な環境)  
4. [インストール](#インストール)  
5. [使い方](#使い方)  
   - [GUI モード](#gui-モード)  
   - [CLI モード](#cli-モード)  
6. [コマンドラインオプション一覧](#コマンドラインオプション一覧)  
7. [ライセンス](#ライセンス)  
8. [注意事項](#注意事項)  
9. [連絡先・貢献](#連絡先貢献)  

---

## 主な機能

- **GUI モード**  
  - PySide6 を利用した分かりやすい操作画面  
  - テキストや色、サイズなどをプレビューで確認しながら設定可能  
  - 生成した画像を簡単に保存

- **CLI モード**  
  - コマンドライン引数を指定するだけでQRコードを一括生成  
  - エラー訂正レベルやサイズ、色などの指定に対応  
  - 結果として QRコードに関する情報（バージョン、データサイズなど）を表示

- **カスタマイズ性**  
  - テキストをQRコード下部に追加可能  
  - フォントサイズや色、背景色を自由に変更  
  - エラー訂正レベル（L, M, Q, H）の選択  
  - 高DPI環境でも滑らかに表示

---

## ディレクトリ構成

```
├── LICENSE
├── qr_generator.py     # メインのQRコード生成スクリプト
├── requirements.txt    # 必要なパッケージ一覧
└── README.md           # このファイル
```

---

## 必要な環境

- Python 3.6 以降（推奨: 3.8 以上）
- Windows / Mac / Linux いずれのOSでも動作可能（PySide6のサポート環境に依存）

### 依存パッケージ
- [qrcode](https://pypi.org/project/qrcode/)
- [Pillow](https://pypi.org/project/Pillow/)
- [PySide6](https://pypi.org/project/PySide6/)

---

## インストール

1. **リポジトリの取得**  
   - GitHub などから本リポジトリをクローン、または ZIP としてダウンロードし、任意のディレクトリに展開してください。

2. **仮想環境の作成（任意）**  
   - 依存関係を他のプロジェクトと分離したい場合は、Python の仮想環境（venv 等）を作成し、有効化してください。

3. **パッケージのインストール**  
   - `requirements.txt` を使って依存パッケージを一括インストールできます。
     ```bash
     pip install -r requirements.txt
     ```

---

## 使い方

### GUI モード

GUI モードを起動するには、下記のいずれかの方法で実行してください。

```bash
# 引数を指定せずに実行
python qr_generator.py
```
または
```bash
# --gui オプションを付けて実行
python qr_generator.py --gui
```

#### GUI の主な操作

1. **データ**  
   - QRコードにエンコードする文字列（URLなど）を入力します。  
   - 空欄の場合は警告が表示され、QRコードを生成できません。

2. **テキスト**  
   - QRコード下部に表示するテキストを入力します（任意）。

3. **フォントサイズ**  
   - テキストを表示するフォントサイズを指定します。

4. **カラー設定**  
   - 「QRコード色」および「背景色」をボタンから選択できます。

5. **エラー訂正レベル**  
   - `L (7%)`, `M (15%)`, `Q (25%)`, `H (30%)` から選択します。  
   - `H` は誤り訂正が最も高い分、QRコードの容量を多く消費します。

6. **QRコードサイズ**  
   - QRコードのドット(モジュール)の大きさ（box_size）を指定します。

7. **プレビュー**  
   - 「QRコード生成」ボタンを押すと、プレビュー画面に生成結果が表示されます。

8. **画像の保存**  
   - 「画像を保存」ボタンを押すと、ファイルダイアログが表示され、保存先を選択できます。

### CLI モード

CLI モードでは、**必須項目として `--data`** を指定し、その他オプションを必要に応じて追加します。

#### シンプルな例

```bash
python qr_generator.py --data "Hello World!"
```
- `qrcode.png` というファイル名で QRコード画像を出力します。

#### 出力先と文字列付き例

```bash
python qr_generator.py \
    --data "https://example.com" \
    --text "サンプルサイト" \
    --output sample_qr.png
```
- `sample_qr.png` というファイル名で出力され、下部に「サンプルサイト」という文字列が付加されます。

#### カラーやエラー訂正レベルを指定する例

```bash
python qr_generator.py \
    --data "Sample Data" \
    --qr-size 8 \
    --qr-color "#FF0000" \
    --bg-color "#FFFFFF" \
    --error-level M \
    --output colored_qr.png
```
- 大きさが 8、前景色が赤 (`#FF0000`)、背景色が白 (`#FFFFFF`)、エラー訂正レベルが M(15%) の QRコードが生成されます。

---

## コマンドラインオプション一覧

| オプション          | 説明                                                                                 | デフォルト      |
| :------------------ | :----------------------------------------------------------------------------------- | :------------- |
| `--gui`             | GUIモードで起動します。                                                               | -              |
| `--data`            | **必須**。QRコードにエンコードするデータを指定します。                                | なし           |
| `--text`            | 下部に表示するテキストを指定します。                                                  | なし           |
| `--output`          | 出力ファイルパスを指定します。未指定の場合は `qrcode.png` で出力されます。             | qrcode.png     |
| `--qr-size`         | QRコードのサイズ（box_size）。                                                        | 10             |
| `--text-size`       | テキストのフォントサイズ。                                                            | 20             |
| `--qr-color`        | QRコードの色（例: `black`、`#FF0000` など）。                                         | black          |
| `--bg-color`        | 背景色（例: `white`、`#FFFFFF` など）。                                              | white          |
| `--error-level`     | エラー訂正レベル。`L, M, Q, H` のいずれか。                                           | H              |

---

## ライセンス

本プロジェクトは [GNU General Public License v3.0](./LICENSE) に基づき公開されています。  
詳細は [LICENSE](./LICENSE) ファイルをご確認ください。

---

## 注意事項

1. **フォントについて**  
   - デフォルトでは Windows環境に存在する「meiryo.ttc」または「msgothic.ttc」を優先的に使用します。  
   - これらのフォントが見つからない場合は、Pillow のデフォルトフォントにフォールバックします。その際、文字化け等が発生する可能性があります。

2. **GUIウィンドウサイズ**  
   - 現在の実装ではウィンドウサイズを固定にしています。画面解像度によっては一部UIが見切れる場合がありますのでご注意ください。

3. **バージョンの互換性**  
   - Python 3.6 以降での動作を想定しています。依存パッケージのバージョンによっては動作しない場合があります。

---
