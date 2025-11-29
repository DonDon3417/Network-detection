# Network Intrusion Detection System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Spark](https://img.shields.io/badge/Apache%20Spark-4.0.1-orange)
![XGBoost](https://img.shields.io/badge/XGBoost-Latest-green)

Hệ thống phát hiện xâm nhập mạng sử dụng Apache Spark và Machine Learning với dataset NSL-KDD.

---

## 🎯 Tính năng

- ✅ Xử lý Big Data với Apache Spark (phân tán)
- ✅ 2 mô hình ML: Logistic Regression + XGBoost
- ✅ Pipeline tự động: StringIndexer → OneHotEncoder → VectorAssembler → StandardScaler
- ✅ Save/Load models để tiết kiệm thời gian training
- ✅ Dataset: NSL-KDD (125,973 train + 22,544 test records)
- ✅ Metrics đầy đủ: Accuracy, Precision, Recall, F1, AUC

---

## 📊 Kết quả

| Model | Accuracy | F1 Score | AUC | Training Time |
|-------|----------|----------|-----|---------------|
| **Logistic Regression** | 95.18% | 95.18% | 98.86% | ~30s |
| **XGBoost** | 98.74% | 98.74% | 99.92% | ~150s |

---

## 🚀 Quick Start

### 1. Clone repository

```bash
git clone https://github.com/DonDon3417/Network-detection.git
cd Network-detection
```

### 2. Tải dữ liệu

Tải NSL-KDD dataset từ: https://www.unb.ca/cic/datasets/nsl.html

- `KDDTrain+.txt` (125,973 records)
- `KDDTest+.txt` (22,544 records)

Đặt vào thư mục project.

### 3. Cài đặt Python 3.11

Tải Python 3.11.9: https://www.python.org/downloads/release/python-3119/

### 4. Setup môi trường

```bash
# Windows
setup_python311.bat

# Cài Hadoop winutils (Windows only)
install_hadoop.bat
```

### 5. Chạy

```bash
# Train và lưu models (lần đầu)
run.bat --save

# Load models đã lưu (lần sau - nhanh hơn)
run.bat --load

# Hoặc train không lưu
run.bat
```

---

## 📁 Cấu trúc Project

```
Network-detection/
├── 📄 README.md                        # File này
├── 📄 README_SPARK.md                  # Chi tiết Spark
├── 📄 requirements.txt                 # Python dependencies
├── 📄 .gitignore                       # Git ignore rules
│
├── 🐍 spark_intrusion_detection.py    # Main Spark script
├── 📓 Phát_hiện_xâm_nhập.ipynb        # EDA & Pandas/Sklearn
│
├── 🦇 run.bat                          # Run script
├── 🦇 setup_python311.bat              # Setup Python 3.11
├── 🦇 install_hadoop.bat               # Install Hadoop winutils
│
├── 📊 KDDTrain+.txt                    # Training data (not in Git)
└── 📊 KDDTest+.txt                     # Test data (not in Git)
```

---

## 💻 Yêu cầu hệ thống

### Phần cứng (khuyến nghị)
- **RAM**: 8GB+ (16GB tốt hơn)
- **CPU**: 4 cores+
- **Disk**: 2GB free space

### Phần mềm
- **OS**: Windows 10/11, Linux, macOS
- **Python**: 3.11.9
- **Java**: JDK 8 hoặc 11 (cho Spark)

---

## 📚 Dependencies

```
pyspark==4.0.1
xgboost
pyarrow>=11.0.0
pandas
numpy
scikit-learn
matplotlib
seaborn
```

Cài đặt:
```bash
pip install -r requirements.txt
```

---

## 🔧 Cách sử dụng

### Mode 1: Train và lưu models

```bash
run.bat --save
```

**Output:**
- Train 2 models (Logistic Regression + XGBoost)
- Lưu vào `spark_models/`
- Hiển thị bảng so sánh

**Thời gian:** ~8-10 phút

### Mode 2: Load models đã lưu

```bash
run.bat --load
```

**Output:**
- Load models từ `spark_models/`
- Evaluate trên test set
- Hiển thị metrics

**Thời gian:** ~45 giây

### Mode 3: Train không lưu

```bash
run.bat
```

Train và evaluate, không lưu models.

---

## 📊 Dataset: NSL-KDD

### Mô tả
- **Source**: Canadian Institute for Cybersecurity
- **Type**: Network intrusion detection
- **Format**: Text files với 43 features
- **Classes**: Normal (0) vs Attack (1)

### Dataset split
- **Train**: 125,973 records
- **Test**: 22,544 records

---

## 🐛 Troubleshooting

### Lỗi: "HADOOP_HOME is not set"
**Giải pháp:**
```bash
install_hadoop.bat
```

### Lỗi: "ModuleNotFoundError: No module named 'pyspark'"
**Giải pháp:**
```bash
pip install pyspark xgboost pyarrow
```

### Lỗi: "Python worker exited unexpectedly"
**Nguyên nhân:** Python version không tương thích

**Giải pháp:** Dùng Python 3.11 (không dùng 3.12)
```bash
setup_python311.bat
```

### Lỗi: "Java gateway process exited"
**Giải pháp:** Cài Java JDK 8 hoặc 11
- Download: https://adoptium.net/

---

## 📖 Tài liệu

- [Apache Spark ML Guide](https://spark.apache.org/docs/latest/ml-guide.html)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [NSL-KDD Dataset](https://www.unb.ca/cic/datasets/nsl.html)

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**DonDon3417**

🔗 GitHub: https://github.com/DonDon3417
