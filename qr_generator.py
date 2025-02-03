import sys
from pathlib import Path
import qrcode
from PIL import Image, ImageDraw, ImageFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QMessageBox,
    QColorDialog, QSpinBox, QComboBox
)
from PySide6.QtGui import QPixmap, QImage, QColor
from PySide6.QtCore import Qt
import argparse

class ColorButton(QPushButton):
    def __init__(self, color=QColor('black'), parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.color = color
        self.update_color(color)

    def update_color(self, color):
        self.color = color
        self.setStyleSheet(
            f'QPushButton {{ background-color: {color.name()}; '
            'border: 2px solid #CCCCCC; border-radius: 5px; }}'
            'QPushButton:hover { border: 2px solid #999999; }'
        )

class QRCodeGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.qr_image = None
        self.last_save_directory = str(Path.home())
        
    def initUI(self):
        self.setWindowTitle('QRコードジェネレーター Pro')
        self.setFixedSize(400, 650)  # ウィンドウの高さを増やす
        
        # メインウィジェット
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # データ入力
        data_layout = QHBoxLayout()
        data_label = QLabel('データ:')
        self.data_input = QLineEdit()
        data_layout.addWidget(data_label)
        data_layout.addWidget(self.data_input)
        layout.addLayout(data_layout)

        # テキスト入力
        text_layout = QHBoxLayout()
        text_label = QLabel('テキスト:')
        self.text_input = QLineEdit()
        text_layout.addWidget(text_label)
        text_layout.addWidget(self.text_input)
        layout.addLayout(text_layout)

        # フォントサイズ
        font_layout = QHBoxLayout()
        font_label = QLabel('フォントサイズ:')
        self.font_size_input = QSpinBox()
        self.font_size_input.setRange(8, 72)
        self.font_size_input.setValue(20)
        self.font_size_input.setFixedWidth(80)
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_size_input)
        font_layout.addStretch()
        layout.addLayout(font_layout)

        # カラー設定
        color_layout = QHBoxLayout()
        qr_color_label = QLabel('QRコード色:')
        self.qr_color_button = ColorButton(QColor('black'))
        self.qr_color_button.clicked.connect(lambda: self.choose_color('qr'))
        bg_color_label = QLabel('背景色:')
        self.bg_color_button = ColorButton(QColor('white'))
        self.bg_color_button.clicked.connect(lambda: self.choose_color('bg'))
        
        color_layout.addWidget(qr_color_label)
        color_layout.addWidget(self.qr_color_button)
        color_layout.addSpacing(20)
        color_layout.addWidget(bg_color_label)
        color_layout.addWidget(self.bg_color_button)
        color_layout.addStretch()
        layout.addLayout(color_layout)

        # エラー訂正レベル
        error_layout = QHBoxLayout()
        error_label = QLabel('エラー訂正レベル:')
        self.error_level = QComboBox()
        self.error_level.addItems(['L (7%)', 'M (15%)', 'Q (25%)', 'H (30%)'])
        self.error_level.setCurrentText('H (30%)')
        self.error_level.setFixedWidth(100)
        error_layout.addWidget(error_label)
        error_layout.addWidget(self.error_level)
        error_layout.addStretch()
        layout.addLayout(error_layout)

        # QRコードサイズ
        size_layout = QHBoxLayout()
        size_label = QLabel('QRコードサイズ:')
        self.size_input = QSpinBox()
        self.size_input.setRange(1, 20)
        self.size_input.setValue(10)
        self.size_input.setFixedWidth(80)
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_input)
        size_layout.addStretch()
        layout.addLayout(size_layout)

        # 生成ボタン
        self.generate_button = QPushButton('QRコード生成')
        self.generate_button.setFixedHeight(40)
        self.generate_button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        self.generate_button.clicked.connect(self.generate_qr_code)
        layout.addWidget(self.generate_button)

        # プレビューエリアのコンテナ
        preview_container = QWidget()
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setSpacing(10)

        # プレビュー表示のサイズを調整
        preview_width = 360  # マージンを考慮した幅
        preview_height = 300  # 適度な高さ
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(preview_width, preview_height)
        self.image_label.setStyleSheet('''
            QLabel {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
            }
        ''')
        preview_layout.addWidget(self.image_label)

        # 保存ボタン
        self.save_button = QPushButton('画像を保存')
        self.save_button.setFixedHeight(40)
        self.save_button.setFixedWidth(preview_width)  # プレビューと同じ幅に設定
        self.save_button.setStyleSheet('''
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
            }
        ''')
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)
        preview_layout.addWidget(self.save_button)

        # プレビューコンテナをメインレイアウトに追加
        layout.addWidget(preview_container)

    def choose_color(self, target):
        color = QColorDialog.getColor()
        if color.isValid():
            if target == 'qr':
                self.qr_color_button.update_color(color)
            else:
                self.bg_color_button.update_color(color)

    def generate_qr_code(self):
        data = self.data_input.text().strip()
        text = self.text_input.text().strip()

        if not data:
            QMessageBox.warning(self, '入力エラー', 'QRコードにエンコードするデータを入力してください。')
            return

        # エラー訂正レベルの設定
        error_levels = {'L (7%)': 'L', 'M (15%)': 'M', 'Q (25%)': 'Q', 'H (30%)': 'H'}
        error_level = error_levels[self.error_level.currentText()]

        # QRコードの生成
        qr = qrcode.QRCode(
            version=None,  # 自動バージョン選択
            error_correction=getattr(qrcode.constants, f'ERROR_CORRECT_{error_level}'),
            box_size=self.size_input.value(),
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        qr_img = qr.make_image(
            fill_color=self.qr_color_button.color.name(),
            back_color=self.bg_color_button.color.name()
        ).convert("RGBA")

        # テキストの追加
        if text:
            try:
                font = ImageFont.truetype("meiryo.ttc", self.font_size_input.value())
            except IOError:
                try:
                    font = ImageFont.truetype("msgothic.ttc", self.font_size_input.value())
                except IOError:
                    font = ImageFont.load_default()
                    QMessageBox.warning(self, 'フォントエラー', 'システムフォントが見つかりません。デフォルトフォントを使用します。')

            # テキストサイズの計算
            temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
            temp_draw = ImageDraw.Draw(temp_img)
            bbox = temp_draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # 新しい画像サイズの計算（パディングを調整）
            padding = 20  # パディングを50から20に減少
            new_width = max(qr_img.width, text_width) + padding * 2
            new_height = qr_img.height + text_height + padding * 2  # パディングを3から2に減少

            # 新しい画像の作成
            new_img = Image.new("RGBA", (new_width, new_height), self.bg_color_button.color.name())
            
            # QRコードの貼り付け（上部）
            qr_x = (new_width - qr_img.width) // 2
            qr_y = padding
            new_img.paste(qr_img, (qr_x, qr_y))

            # テキストの描画（下部、余白を調整）
            draw = ImageDraw.Draw(new_img)
            text_x = (new_width - text_width) // 2
            text_y = qr_img.height + padding  # パディングを2からそのままに変更
            draw.text((text_x, text_y), text, font=font, fill=self.qr_color_button.color.name())
            
            self.qr_image = new_img
        else:
            self.qr_image = qr_img

        # プレビューの表示
        self.update_preview()
        self.save_button.setEnabled(True)

    def update_preview(self):
        if self.qr_image:
            # RGBA画像をQPixmapに変換
            data = self.qr_image.convert("RGB").tobytes("raw", "RGB")
            qimage = QImage(
                data,
                self.qr_image.width,
                self.qr_image.height,
                self.qr_image.width * 3,  # bytes per line
                QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(qimage)
            
            # ラベルのサイズを取得
            label_size = self.image_label.size()
            
            # アスペクト比を保持しながら、ラベルに合わせてリサイズ
            scaled_pixmap = pixmap.scaled(
                label_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            # 中央に配置
            self.image_label.setPixmap(scaled_pixmap)

    def save_image(self):
        if not self.qr_image:
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存先を選択",
            str(Path(self.last_save_directory) / "qrcode.png"),
            "PNG画像 (*.png);;JPEG画像 (*.jpg *.jpeg);;全てのファイル (*)",
            options=options
        )
        
        if file_path:
            try:
                self.last_save_directory = str(Path(file_path).parent)
                self.qr_image.save(file_path)
                QMessageBox.information(self, '保存完了', f'画像を保存しました: {file_path}')
            except Exception as e:
                QMessageBox.warning(self, '保存エラー', f'画像の保存に失敗しました: {str(e)}')

def generate_qr_from_cli(data, text=None, output=None, qr_size=10, text_size=20,
                   qr_color="black", bg_color="white", error_level="H"):
    """コマンドライン用のQRコード生成関数"""
    # QRコードの生成
    qr = qrcode.QRCode(
        version=None,  # 自動バージョン選択
        error_correction=getattr(qrcode.constants, f'ERROR_CORRECT_{error_level}'),
        box_size=qr_size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # 使用されたバージョンとデータ容量を表示
    print(f"QRコード情報:")
    print(f"- 使用バージョン: {qr.version} ({(qr.version * 4 + 17)}x{(qr.version * 4 + 17)}モジュール)")
    print(f"- エラー訂正レベル: {error_level}")
    print(f"- データサイズ: {len(data)} 文字")
    
    qr_img = qr.make_image(fill_color=qr_color, back_color=bg_color).convert("RGBA")

    # テキストの追加
    if text:
        try:
            font = ImageFont.truetype("meiryo.ttc", text_size)
        except IOError:
            try:
                font = ImageFont.truetype("msgothic.ttc", text_size)
            except IOError:
                font = ImageFont.load_default()
                print("警告: システムフォントが見つかりません。デフォルトフォントを使用します。")

        # テキストサイズの計算
        temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        bbox = temp_draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # 新しい画像サイズの計算
        padding = 20
        new_width = max(qr_img.width, text_width) + padding * 2
        new_height = qr_img.height + text_height + padding * 2

        # 新しい画像の作成
        new_img = Image.new("RGBA", (new_width, new_height), bg_color)
        
        # QRコードの貼り付け
        qr_x = (new_width - qr_img.width) // 2
        qr_y = padding
        new_img.paste(qr_img, (qr_x, qr_y))

        # テキストの描画
        draw = ImageDraw.Draw(new_img)
        text_x = (new_width - text_width) // 2
        text_y = qr_img.height + padding
        draw.text((text_x, text_y), text, font=font, fill=qr_color)
        
        qr_img = new_img

    # 出力パスの設定
    if not output:
        output = "qrcode.png"
    
    # 画像の保存
    qr_img.save(output)
    print(f"\nQRコードを保存しました: {output}")

if __name__ == '__main__':
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='QRコードジェネレーター')
    parser.add_argument('--gui', action='store_true', help='GUIモードで起動')
    parser.add_argument('--data', help='QRコードに埋め込むデータ')
    parser.add_argument('--text', help='QRコードの下に表示するテキスト')
    parser.add_argument('--output', help='出力ファイルパス')
    parser.add_argument('--qr-size', type=int, default=10, help='QRコードのサイズ (デフォルト: 10)')
    parser.add_argument('--text-size', type=int, default=20, help='テキストのフォントサイズ (デフォルト: 20)')
    parser.add_argument('--qr-color', default="black", help='QRコードの色 (例: black, #FF0000)')
    parser.add_argument('--bg-color', default="white", help='背景色 (例: white, #FFFFFF)')
    parser.add_argument('--error-level', choices=['L', 'M', 'Q', 'H'], default='H',
                      help='エラー訂正レベル (L: 7%, M: 15%, Q: 25%, H: 30%)')
    args = parser.parse_args()

    if args.gui or len(sys.argv) == 1:
        # GUIモードの起動
        app = QApplication(sys.argv)
        window = QRCodeGenerator()
        window.show()
        sys.exit(app.exec())
    else:
        # CLIモードでの実行
        if not args.data:
            parser.error("--dataは必須です")
        
        generate_qr_from_cli(
            data=args.data,
            text=args.text,
            output=args.output,
            qr_size=args.qr_size,
            text_size=args.text_size,
            qr_color=args.qr_color,
            bg_color=args.bg_color,
            error_level=args.error_level
        )

