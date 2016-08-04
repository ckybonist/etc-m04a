# ETC M04A 程式 (開發中，說明將隨之變動...)

# 必要準備
安裝 python3, TODO...


# 使用方式

請自行在專案根目錄創建 **data** 資料夾，並將原始資料放在其中。
```sh
python3 main.py
```
執行 main.py 會跑完所有分析，但也可以單獨執行 path.py, interchange.py, sensor.py


# 輸出
輸出檔都在 output/，其中有三個子資料夾:
- step1: 測站間平均時間紀錄, 由 sensor.py 輸出
- step2: 路段平均時間紀錄, 由 interchange.py 輸出
- step3: 路徑旅行時間紀錄, 由 path.py 輸出


# 程式架構

三個主要模組(對應到旅行時間計算的三步驟):

- sensor.py: 測站間平均時間
- interchange.py: 交流道間(路段) 平均時間
- path.py: 路徑旅行時間

其它:
- config.py: 一些全域變數
- utils.py: helper functions
