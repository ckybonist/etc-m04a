# ETC M04A 程式 (開發中，說明將隨之變動...)

# 原始資料
請自行在專案根目錄創建 **data** 資料夾，並將原始資料放在其中。
*注意！資料夾名稱不能隨意命名*


# 程式分為以下三個部分:

## 測站間平均時間 (sensor_section)
進入 sensor_section 資料夾，並執行 travel_time.py:
```sh
python3 travel_time.py batch
         或是
./travel_time.py batch
```
*執行時，請確認當前位置是在 `sensor_section/` 裡面，否則有可能會出錯*

輸出檔會存在 `sensor_section/output`。（output 資料夾會由程式建立)

## 路段平均時間 (interchange_section)
TODO...

## 最終旅行時間
TODO...
