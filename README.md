# ETC M04A 程式 (開發中，說明將隨之變動...)


# 需要的工具
- [python3.5](https://www.python.org/downloads/)
  安裝時記得要勾選 Add Python 3.5 to PATH，讓你直接在小黑窗執行 python
- [git](https://git-scm.com/download/win) (optional)
- [cmder - 更強大的小黑窗](http://cmder.net/) (optional)


# 使用方式

1. 下載專案: `git clone https://github.com/ckybonist/etc-m04a` 或 直接下載(右上角綠色button)
2. 請自行在專案根目錄創建 **data** 資料夾，並將原始資料放在其中。
3. 跑一發分析: `python3(or python) main.py`

  p.s. 執行 main.py 會跑完所有分析，但也可以單獨執行 path.py、 interchange.py、sensor.py


# 輸出
輸出檔都在 output/，其中有三個子資料夾:
- output/step1: 測站間平均時間紀錄, 由 sensor.py 輸出
- output/step2: 路段平均時間紀錄, 由 interchange.py 輸出
- output/step3: 路徑旅行時間紀錄, 由 path.py 輸出


# 程式架構

主程式:
- main.py: 執行所有分析

三個主要模組(對應到旅行時間計算的三步驟):

- sensor.py: 測站間平均時間
- interchange.py: 交流道間(路段) 平均時間
- path.py: 路徑旅行時間

其它:
- config.py: 一些全域變數
- utils.py: helper functions

# 注意事項
- 確保 data/ 內的原始資料為以下目錄結構:
  ```
  # 檢核日期/對應歷史紀錄日期/小時/TDCS_XXX.csv
    例如: 20160822/2015706/02/TDCS_M04A_20150706_020000.csv
  ```
  有時解壓縮 或 其他原因會導致目錄多了一層，像是:
  `20160822/20160502/20150706/02/TDCS_XXX.csv  # 多了一層 20160502`

  這會導致程式產生不正常的結果，甚至直接出錯。

- output/ 資料夾會由程式自動產生

- MS Excel 開 CSV 時為亂碼：
  ```
  1. 打開 Excel
  2. 點選 資料 > 從文字檔 > 選擇要開啟的檔案 > 匯入
  3. 匯入設定三步驟:
      (1) 勾選分隔符號，檔案原始格式為 65001:Unicode (UTF-8)
      (2) 分隔符號勾選 Tab鍵 及 逗點
      (3) 欄位資料格式選 一般
      (4) 完成
  ```
