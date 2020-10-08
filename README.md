# emses_inp_generator
EMSESに用いるパラメータファイル「plasma.inp」の自動生成ツール

![Main Window](images/inpgen_main.png)

## Installation
```
> pip install -r requirements.txt
```

## Usage
```
> ./inpgen.bat
```

or

```
> python src/main.py
```

## Unit Conversion
「Open Converversion」ボタンを押すと単位変換ウィンドウを開くことができます.

このウィンドウではメインウィンドウで指定したパラメータでの物理単位系とEMSES単位系の変換を行うことができます.

![Convertion Window](images/inpgen_convert.png)
