#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Network Intrusion Detection - Spark Big Data
Phát hiện xâm nhập mạng sử dụng Apache Spark (CHUẨN BIG DATA)
"""

import os
import sys
import time
import argparse
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder, StandardScaler
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.ml import Pipeline, PipelineModel


def setup_hadoop_home():
    """Thiết lập HADOOP_HOME và PYSPARK_PYTHON cho Windows"""
    if os.name == 'nt':  # Windows
        # Thiết lập PYSPARK_PYTHON để XGBoost tìm đúng python
        python_exe = sys.executable
        os.environ['PYSPARK_PYTHON'] = python_exe
        os.environ['PYSPARK_DRIVER_PYTHON'] = python_exe
        print(f"✓ PYSPARK_PYTHON: {python_exe}")
        
        # Tìm thư mục hadoop trong project
        project_dir = Path(__file__).parent
        hadoop_dir = project_dir / "hadoop-3.3.1"
        
        if hadoop_dir.exists():
            hadoop_home = str(hadoop_dir.absolute())
            os.environ['HADOOP_HOME'] = hadoop_home
            # Thêm bin vào PATH
            bin_dir = str((hadoop_dir / "bin").absolute())
            if bin_dir not in os.environ.get('PATH', ''):
                os.environ['PATH'] = bin_dir + os.pathsep + os.environ.get('PATH', '')
            print(f"✓ HADOOP_HOME: {hadoop_home}")
        else:
            print(f"⚠ Không tìm thấy thư mục hadoop-3.3.1")
            print(f"  Chạy install_hadoop.bat để cài đặt")


def create_spark_session():
    """Khởi tạo SparkSession"""
    print("\n")
    print("=" * 80)
    print(" " * 15 + "NETWORK INTRUSION DETECTION - SPARK BIG DATA")
    print("=" * 80)
    print()
    print("=" * 80)
    print("KHỞI TẠO SPARK SESSION")
    print("=" * 80)
    
    # Thiết lập HADOOP_HOME trước khi tạo SparkSession
    setup_hadoop_home()
    
    spark = SparkSession.builder \
        .appName("Network_Intrusion_Detection_BigData") \
        .master("local[*]") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .config("spark.sql.shuffle.partitions", "200") \
        .config("spark.python.worker.reuse", "false") \
        .getOrCreate()
    
    print(f"✓ Spark Version: {spark.version}")
    print(f"✓ Spark UI: http://localhost:4040")
    print("✓ SparkSession khởi tạo thành công!")
    print()
    
    return spark


def define_schema():
    """Định nghĩa schema cho NSL-KDD dataset"""
    schema = StructType([
        StructField("duration", IntegerType(), True),
        StructField("protocol_type", StringType(), True),
        StructField("service", StringType(), True),
        StructField("flag", StringType(), True),
        StructField("src_bytes", IntegerType(), True),
        StructField("dst_bytes", IntegerType(), True),
        StructField("land", IntegerType(), True),
        StructField("wrong_fragment", IntegerType(), True),
        StructField("urgent", IntegerType(), True),
        StructField("hot", IntegerType(), True),
        StructField("num_failed_logins", IntegerType(), True),
        StructField("logged_in", IntegerType(), True),
        StructField("num_compromised", IntegerType(), True),
        StructField("root_shell", IntegerType(), True),
        StructField("su_attempted", IntegerType(), True),
        StructField("num_root", IntegerType(), True),
        StructField("num_file_creations", IntegerType(), True),
        StructField("num_shells", IntegerType(), True),
        StructField("num_access_files", IntegerType(), True),
        StructField("num_outbound_cmds", IntegerType(), True),
        StructField("is_host_login", IntegerType(), True),
        StructField("is_guest_login", IntegerType(), True),
        StructField("count", IntegerType(), True),
        StructField("srv_count", IntegerType(), True),
        StructField("serror_rate", DoubleType(), True),
        StructField("srv_serror_rate", DoubleType(), True),
        StructField("rerror_rate", DoubleType(), True),
        StructField("srv_rerror_rate", DoubleType(), True),
        StructField("same_srv_rate", DoubleType(), True),
        StructField("diff_srv_rate", DoubleType(), True),
        StructField("srv_diff_host_rate", DoubleType(), True),
        StructField("dst_host_count", IntegerType(), True),
        StructField("dst_host_srv_count", IntegerType(), True),
        StructField("dst_host_same_srv_rate", DoubleType(), True),
        StructField("dst_host_diff_srv_rate", DoubleType(), True),
        StructField("dst_host_same_src_port_rate", DoubleType(), True),
        StructField("dst_host_srv_diff_host_rate", DoubleType(), True),
        StructField("dst_host_serror_rate", DoubleType(), True),
        StructField("dst_host_srv_serror_rate", DoubleType(), True),
        StructField("dst_host_rerror_rate", DoubleType(), True),
        StructField("dst_host_srv_rerror_rate", DoubleType(), True),
        StructField("attack", StringType(), True),
        StructField("level", IntegerType(), True)
    ])
    
    return schema


def load_data(spark, data_path="./"):
    """Đọc dữ liệu với Spark"""
    print("=" * 80)
    print("ĐỌC DỮ LIỆU")
    print("=" * 80)
    
    schema = define_schema()
    
    print("Đang đọc dữ liệu với Spark...")
    start = time.time()
    
    df_train = spark.read.csv(
        data_path + "KDDTrain+.txt",
        schema=schema,
        header=False
    )
    
    df_test = spark.read.csv(
        data_path + "KDDTest+.txt",
        schema=schema,
        header=False
    )
    
    # Union 2 dataset
    df_full = df_train.union(df_test)
    
    print(f"✓ Đọc xong trong {time.time()-start:.2f}s")
    print(f"✓ Tổng số dòng: {df_full.count():,}")
    print(f"✓ Số cột: {len(df_full.columns)}")
    print()
    
    return df_full


def preprocess_data(df):
    """Tiền xử lý dữ liệu"""
    print("=" * 80)
    print("TIỀN XỬ LÝ DỮ LIỆU")
    print("=" * 80)
    
    # Tạo label
    df_labeled = df.withColumn(
        "label",
        when(col("attack") == "normal", 0.0).otherwise(1.0)
    )
    
    # Xóa duplicate
    df_clean = df_labeled.dropDuplicates()
    print(f"✓ Sau khi xóa duplicate: {df_clean.count():,} dòng")
    
    # Định nghĩa các loại cột
    categorical_cols = ["protocol_type", "service", "flag"]
    numeric_cols = [
        "duration", "src_bytes", "dst_bytes", "wrong_fragment", "urgent",
        "hot", "num_failed_logins", "num_compromised", "root_shell", "su_attempted",
        "num_root", "num_file_creations", "num_shells", "num_access_files",
        "num_outbound_cmds", "count", "srv_count", "serror_rate", "srv_serror_rate",
        "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
        "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
        "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
        "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
        "dst_host_serror_rate", "dst_host_srv_serror_rate",
        "dst_host_rerror_rate", "dst_host_srv_rerror_rate"
    ]
    
    # Xây dựng Pipeline
    stages = []
    
    # StringIndexer
    for cat_col in categorical_cols:
        indexer = StringIndexer(
            inputCol=cat_col,
            outputCol=cat_col + "_indexed",
            handleInvalid="keep"
        )
        stages.append(indexer)
    
    # OneHotEncoder
    for cat_col in categorical_cols:
        encoder = OneHotEncoder(
            inputCol=cat_col + "_indexed",
            outputCol=cat_col + "_vec"
        )
        stages.append(encoder)
    
    # VectorAssembler
    assembler_inputs = [c + "_vec" for c in categorical_cols] + numeric_cols
    assembler = VectorAssembler(
        inputCols=assembler_inputs,
        outputCol="features_raw"
    )
    stages.append(assembler)
    
    # StandardScaler
    scaler = StandardScaler(
        inputCol="features_raw",
        outputCol="features",
        withStd=True,
        withMean=False
    )
    stages.append(scaler)
    
    print(f"✓ Pipeline có {len(stages)} stages")
    print()
    
    return df_clean, Pipeline(stages=stages)


def save_models(lr_model, xgb_model, pipeline_model, models_dir="spark_models"):
    """Lưu các models đã train"""
    print("=" * 80)
    print("LƯU MODELS")
    print("=" * 80)
    
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"✓ Tạo thư mục {models_dir}/")
    
    try:
        import shutil
        
        # Lưu Pipeline
        pipeline_path = os.path.join(models_dir, "pipeline_model")
        if os.path.exists(pipeline_path):
            shutil.rmtree(pipeline_path)
        pipeline_model.save(pipeline_path)
        print(f"✓ Pipeline -> {pipeline_path}/")
        
        # Lưu Logistic Regression
        lr_path = os.path.join(models_dir, "logistic_regression")
        if os.path.exists(lr_path):
            shutil.rmtree(lr_path)
        lr_model.save(lr_path)
        print(f"✓ Logistic Regression -> {lr_path}/")
        
        # Lưu XGBoost
        if xgb_model:
            xgb_path = os.path.join(models_dir, "xgboost")
            if os.path.exists(xgb_path):
                shutil.rmtree(xgb_path)
            xgb_model.save(xgb_path)
            print(f"✓ XGBoost -> {xgb_path}/")
        
        print(f"\n✓ Đã lưu tất cả models vào {models_dir}/")
        print()
    except Exception as e:
        print(f"✗ Lỗi khi lưu models: {e}")
        print()


def load_models(models_dir="spark_models"):
    """Load các models đã lưu"""
    print("=" * 80)
    print("LOAD MODELS ĐÃ LƯU")
    print("=" * 80)
    
    try:
        from xgboost.spark import SparkXGBClassifierModel
        
        pipeline_model = PipelineModel.load(os.path.join(models_dir, "pipeline_model"))
        print(f"✓ Pipeline")
        
        lr_model = LogisticRegressionModel.load(os.path.join(models_dir, "logistic_regression"))
        print(f"✓ Logistic Regression")
        
        xgb_model = SparkXGBClassifierModel.load(os.path.join(models_dir, "xgboost"))
        print(f"✓ XGBoost")
        
        print(f"\n✓ Đã load tất cả models từ {models_dir}/")
        print()
        
        return pipeline_model, lr_model, xgb_model
    except Exception as e:
        print(f"✗ Lỗi khi load models: {e}")
        print("→ Sẽ train models mới")
        print()
        return None, None, None


def train_models(train_data, test_data):
    """Huấn luyện các mô hình"""
    results = []
    
    # Evaluators
    evaluator_auc = BinaryClassificationEvaluator(
        labelCol="label",
        rawPredictionCol="rawPrediction",
        metricName="areaUnderROC"
    )
    evaluator_acc = MulticlassClassificationEvaluator(
        labelCol="label",
        predictionCol="prediction",
        metricName="accuracy"
    )
    evaluator_f1 = MulticlassClassificationEvaluator(
        labelCol="label",
        predictionCol="prediction",
        metricName="f1"
    )
    
    # Model 1: Logistic Regression
    print("=" * 80)
    print("MÔ HÌNH 1: LOGISTIC REGRESSION")
    print("=" * 80)
    
    lr = LogisticRegression(
        featuresCol="features",
        labelCol="label",
        maxIter=100,
        regParam=0.01
    )
    
    print("Đang huấn luyện...")
    start = time.time()
    lr_model = lr.fit(train_data)
    train_time = time.time() - start
    
    lr_predictions = lr_model.transform(test_data)
    
    lr_acc = evaluator_acc.evaluate(lr_predictions)
    lr_f1 = evaluator_f1.evaluate(lr_predictions)
    lr_auc = evaluator_auc.evaluate(lr_predictions)
    
    print(f"✓ Accuracy: {lr_acc:.4f}")
    print(f"✓ F1 Score: {lr_f1:.4f}")
    print(f"✓ AUC: {lr_auc:.4f}")
    print(f"✓ Training Time: {train_time:.2f}s")
    print()
    
    results.append({
        "Model": "Logistic Regression",
        "Accuracy": lr_acc,
        "F1 Score": lr_f1,
        "AUC": lr_auc,
        "Training Time": train_time
    })
    
    # Model 2: XGBoost
    print("=" * 80)
    print("MÔ HÌNH 2: XGBOOST")
    print("=" * 80)
    
    xgb_model = None
    try:
        from xgboost.spark import SparkXGBClassifier
        
        xgb = SparkXGBClassifier(
            features_col="features",
            label_col="label",
            max_depth=6,
            learning_rate=0.1,
            n_estimators=100,
            eval_metric="auc"
        )
        
        print("Đang huấn luyện...")
        start = time.time()
        xgb_model = xgb.fit(train_data)
        train_time = time.time() - start
        
        xgb_predictions = xgb_model.transform(test_data)
        
        xgb_acc = evaluator_acc.evaluate(xgb_predictions)
        xgb_f1 = evaluator_f1.evaluate(xgb_predictions)
        xgb_auc = evaluator_auc.evaluate(xgb_predictions)
        
        print(f"✓ Accuracy: {xgb_acc:.4f}")
        print(f"✓ F1 Score: {xgb_f1:.4f}")
        print(f"✓ AUC: {xgb_auc:.4f}")
        print(f"✓ Training Time: {train_time:.2f}s")
        print()
        
        results.append({
            "Model": "XGBoost",
            "Accuracy": xgb_acc,
            "F1 Score": xgb_f1,
            "AUC": xgb_auc,
            "Training Time": train_time
        })
        
    except Exception as e:
        print(f"✗ Lỗi khi train XGBoost: {e}")
        print("→ XGBoost có thể cần cài đặt: pip install xgboost")
        print()
    
    return results, lr_model, xgb_model


def evaluate_loaded_models(pipeline_model, lr_model, xgb_model, test_data):
    """Đánh giá models đã load"""
    results = []
    
    # Evaluators
    evaluator_auc = BinaryClassificationEvaluator(
        labelCol="label",
        rawPredictionCol="rawPrediction",
        metricName="areaUnderROC"
    )
    evaluator_acc = MulticlassClassificationEvaluator(
        labelCol="label",
        predictionCol="prediction",
        metricName="accuracy"
    )
    evaluator_f1 = MulticlassClassificationEvaluator(
        labelCol="label",
        predictionCol="prediction",
        metricName="f1"
    )
    
    print("=" * 80)
    print("ĐÁNH GIÁ MODELS ĐÃ LOAD")
    print("=" * 80)
    
    # Logistic Regression
    print("\n1. Logistic Regression...")
    lr_predictions = lr_model.transform(test_data)
    lr_acc = evaluator_acc.evaluate(lr_predictions)
    lr_f1 = evaluator_f1.evaluate(lr_predictions)
    lr_auc = evaluator_auc.evaluate(lr_predictions)
    print(f"   Accuracy: {lr_acc:.4f} | F1: {lr_f1:.4f} | AUC: {lr_auc:.4f}")
    
    results.append({
        "Model": "Logistic Regression",
        "Accuracy": lr_acc,
        "F1 Score": lr_f1,
        "AUC": lr_auc,
        "Training Time": 0.0
    })
    
    # XGBoost
    if xgb_model:
        print("2. XGBoost...")
        xgb_predictions = xgb_model.transform(test_data)
        xgb_acc = evaluator_acc.evaluate(xgb_predictions)
        xgb_f1 = evaluator_f1.evaluate(xgb_predictions)
        xgb_auc = evaluator_auc.evaluate(xgb_predictions)
        print(f"   Accuracy: {xgb_acc:.4f} | F1: {xgb_f1:.4f} | AUC: {xgb_auc:.4f}")
        
        results.append({
            "Model": "XGBoost",
            "Accuracy": xgb_acc,
            "F1 Score": xgb_f1,
            "AUC": xgb_auc,
            "Training Time": 0.0
        })
    
    print()
    return results


def print_results(results):
    """In kết quả so sánh"""
    print("=" * 80)
    print(" " * 20 + "BẢNG SO SÁNH KẾT QUẢ")
    print("=" * 80)
    
    print(f"{'Model':<25} {'Accuracy':<12} {'F1 Score':<12} {'AUC':<12} {'Time (s)':<10}")
    print("-" * 80)
    
    for r in results:
        print(f"{r['Model']:<25} {r['Accuracy']:<12.4f} {r['F1 Score']:<12.4f} {r['AUC']:<12.4f} {r['Training Time']:<10.2f}")
    
    print("=" * 80)
    
    # Tìm model tốt nhất
    best_model = max(results, key=lambda x: x['Accuracy'])
    print(f"\n✓ MODEL TỐT NHẤT: {best_model['Model']}")
    print(f"  - Accuracy: {best_model['Accuracy']:.4f}")
    print(f"  - F1 Score: {best_model['F1 Score']:.4f}")
    print(f"  - Training Time: {best_model['Training Time']:.2f}s")
    print()


def main():
    """Hàm chính"""
    # Parse arguments
    parser = argparse.ArgumentParser(description='Network Intrusion Detection với Spark')
    parser.add_argument('--load-models', action='store_true', 
                        help='Load models đã lưu thay vì train mới')
    parser.add_argument('--save-models', action='store_true', 
                        help='Lưu models sau khi train')
    parser.add_argument('--models-dir', type=str, default='spark_models',
                        help='Thư mục chứa models (mặc định: spark_models)')
    args = parser.parse_args()
    
    total_start = time.time()
    
    # 1. Khởi tạo Spark
    spark = create_spark_session()
    
    # 2. Kiểm tra load models hoặc train mới
    use_loaded_models = args.load_models and os.path.exists(args.models_dir)
    
    if use_loaded_models:
        # Load models đã lưu
        loaded_pipeline, lr_model, xgb_model = load_models(args.models_dir)
        
        if loaded_pipeline and lr_model and xgb_model:
            # Đọc dữ liệu
            df = load_data(spark)
            
            # Chia train/test
            print("=" * 80)
            print("CHIA DỮ LIỆU")
            print("=" * 80)
            df_labeled = df.withColumn(
                "label",
                when(col("attack") == "normal", 0.0).otherwise(1.0)
            )
            train_data, test_data = df_labeled.randomSplit([0.8, 0.2], seed=42)
            print(f"✓ Train: {train_data.count():,} dòng")
            print(f"✓ Test: {test_data.count():,} dòng")
            print()
            
            # Áp dụng Pipeline đã load
            print("Đang áp dụng Pipeline đã load...")
            test_final = loaded_pipeline.transform(test_data).select("features", "label")
            test_final.cache()
            
            print(f"✓ Test final: {test_final.count():,} dòng")
            print()
            
            # Đánh giá models
            results = evaluate_loaded_models(loaded_pipeline, lr_model, xgb_model, test_final)
            
            # In kết quả
            print_results(results)
            
            # Thời gian tổng
            total_time = time.time() - total_start
            print("=" * 80)
            print(f"✓ HOÀN TẤT (SỬ DỤNG MODELS ĐÃ LƯU) TRONG {total_time:.2f}s")
            print("=" * 80)
            print()
        else:
            use_loaded_models = False
    
    if not use_loaded_models:
        # Train models mới
        # 2. Đọc dữ liệu
        df = load_data(spark)
        
        # 3. Tiền xử lý
        df_clean, pipeline = preprocess_data(df)
        
        # 4. Chia train/test
        print("=" * 80)
        print("CHIA DỮ LIỆU")
        print("=" * 80)
        train_data, test_data = df_clean.randomSplit([0.8, 0.2], seed=42)
        print(f"✓ Train: {train_data.count():,} dòng")
        print(f"✓ Test: {test_data.count():,} dòng")
        print()
        
        # 5. Áp dụng Pipeline và train
        print("Đang áp dụng Pipeline...")
        start = time.time()
        pipeline_model = pipeline.fit(train_data)
        print(f"✓ Fit Pipeline xong trong {time.time()-start:.2f}s")
        
        train_final = pipeline_model.transform(train_data).select("features", "label")
        test_final = pipeline_model.transform(test_data).select("features", "label")
        
        train_final.cache()
        test_final.cache()
        
        print(f"✓ Train final: {train_final.count():,} dòng")
        print(f"✓ Test final: {test_final.count():,} dòng")
        print()
        
        # Huấn luyện mô hình
        results, lr_model, xgb_model = train_models(train_final, test_final)
        
        # In kết quả
        print_results(results)
        
        # Lưu models nếu được yêu cầu
        if args.save_models:
            save_models(lr_model, xgb_model, pipeline_model, args.models_dir)
        
        # Thời gian tổng
        total_time = time.time() - total_start
        print("=" * 80)
        print(f"✓ HOÀN TẤT TOÀN BỘ QUY TRÌNH TRONG {total_time:.2f}s")
        print("=" * 80)
        print()
    
    # Dừng Spark
    spark.stop()
    print("✓ SparkSession đã đóng")
    

if __name__ == "__main__":
    main()
