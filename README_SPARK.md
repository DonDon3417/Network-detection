# Network Intrusion Detection - Spark Big Data

Phát hiện xâm nhập mạng sử dụng Apache Spark MLlib (CHUẨN BIG DATA).

## 📋 Yêu cầu

- Python 3.7+
- Thư viện sẽ tự động cài đặt: `pyspark`, `pyarrow`, `xgboost`

## 🚀 Cách chạy

### 1. Sử dụng run.bat (Windows) - Khuyến nghị

#### Train mới (không lưu models):
```bash
run.bat
```

#### Train và lưu models:
```bash
run.bat --save
```

#### Load models đã lưu (tiết kiệm thời gian):
```bash
run.bat --load
```

### 2. Chạy trực tiếp với Python

#### Train mới:
```bash
python spark_intrusion_detection.py
```

#### Train và lưu models:
```bash
python spark_intrusion_detection.py --save-models
```

#### Load models đã lưu:
```bash
python spark_intrusion_detection.py --load-models
```

#### Chỉ định thư mục models:
```bash
python spark_intrusion_detection.py --save-models --models-dir my_models
python spark_intrusion_detection.py --load-models --models-dir my_models
```

### 3. Import trong Jupyter Notebook

```python
# Thêm vào đầu notebook
import sys
sys.path.append(".")

# Import và chạy
from spark_intrusion_detection import create_spark_session, load_data, preprocess_data
spark = create_spark_session()
df = load_data(spark)
# ...
```

## 💾 Lưu và Load Models

### Lợi ích của việc lưu models:
- ⚡ **Tiết kiệm thời gian**: Không cần train lại (tiết kiệm ~5-10 phút)
- 💾 **Tái sử dụng**: Dùng models cho dự đoán mới
- 🔄 **Chia sẻ**: Chia sẻ models cho team

### Cấu trúc thư mục models:
```
spark_models/
├── pipeline_model/          # Pipeline tiền xử lý
│   ├── metadata/
│   └── stages/
├── logistic_regression/     # Model Logistic Regression
│   ├── data/
│   └── metadata/
└── xgboost/                 # Model XGBoost
    ├── data/
    └── metadata/
```

### Khi nào nên train lại:
- Có dữ liệu mới
- Muốn thay đổi hyperparameters
- Models hiện tại không đủ tốt

### Khi nào nên load models:
- Chỉ muốn đánh giá trên test set mới
- Demo/thuyết trình nhanh
- Dự đoán trên dữ liệu mới

## 📊 Kết quả

Chương trình sẽ xuất ra:
- Thông tin về Spark session
- Quá trình load và tiền xử lý dữ liệu
- Kết quả training (nếu train mới) hoặc evaluation (nếu load)
- Thông tin về Spark session
- Quá trình load và tiền xử lý dữ liệu
- Kết quả training (nếu train mới) hoặc evaluation (nếu load)
- Bảng so sánh 2 models:
  - Logistic Regression
  - XGBoost
- Model tốt nhất (theo Accuracy)
- Thời gian thực thi
================================================================================
LOAD MODELS ĐÃ LƯU
================================================================================
================================================================================
✓ Pipeline
✓ Logistic Regression
✓ XGBoost

✓ Đã load tất cả models từ spark_models/

================================================================================
ĐÁNH GIÁ MODELS ĐÃ LOAD
================================================================================

1. Logistic Regression...
   Accuracy: 0.9234 | F1: 0.9156 | AUC: 0.9678
2. XGBoost...
   Accuracy: 0.9876 | F1: 0.9834 | AUC: 0.9945

✓ HOÀN TẤT (SỬ DỤNG MODELS ĐÃ LƯU) TRONG 45.23s
```
## 🔧 Cấu trúc files

```
.
├── spark_intrusion_detection.py   # Script chính
├── run.bat                         # Launcher Windows
├── README_SPARK.md                 # Tài liệu này
├── KDDTrain+.txt                   # Dữ liệu train
├── KDDTest+.txt                    # Dữ liệu test
└── spark_models/                   # Thư mục models (tạo sau khi --save)
    ├── pipeline_model/
├── KDDTest+.txt                    # Dữ liệu test
└── spark_models/                   # Thư mục models (tạo sau khi --save)
    ├── pipeline_model/
    ├── logistic_regression/
    └── xgboost/
```
1. **Lần đầu chạy**: 
   ```bash
   run.bat --save
   ```
   → Train và lưu models (~8-10 phút)

2. **Các lần sau**: 
   ```bash
   run.bat --load
   ```
   → Load models có sẵn (~45 giây)

3. **Khi có dữ liệu mới**: Train lại và lưu
   ```bash
   run.bat --save
   ```

## 🎯 Ưu điểm

- ✅ **Không cần Pandas/Sklearn** - 100% Spark MLlib
- ✅ **Xử lý phân tán** - Sẵn sàng cho Big Data
- ✅ **Pipeline tự động** - StringIndexer → OneHotEncoder → VectorAssembler → StandardScaler
- ✅ **Lưu/Load nhanh** - Tiết kiệm thời gian
- ✅ **Độc lập** - Không phụ thuộc Jupyter Notebook
- ✅ **Sẵn sàng production** - Có thể deploy lên Spark Cluster

## 🆘 Troubleshooting

### Lỗi "Cannot find models directory"
→ Chạy `run.bat --save` để tạo models trước

### Lỗi memory
→ Giảm `spark.driver.memory` và `spark.executor.memory` trong `spark_intrusion_detection.py`

### Models cũ không tương thích
→ Xóa thư mục `spark_models/` và train lại
