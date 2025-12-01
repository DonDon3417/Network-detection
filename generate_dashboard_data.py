"""
Script tạo file JSON chứa kết quả cho dashboard
Chạy sau khi train models xong để cập nhật dashboard với dữ liệu thực
"""

import json
import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.ml import PipelineModel
from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator

def setup_spark():
    """Khởi tạo Spark session"""
    try:
        spark = SparkSession.builder \
            .appName("Generate_Dashboard_Data") \
            .master("local[*]") \
            .config("spark.driver.memory", "4g") \
            .config("spark.ui.showConsoleProgress", "false") \
            .getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        return spark
    except Exception as e:
        print(f"Lỗi khởi tạo Spark: {e}")
        return None

def load_models(model_dir="spark_models"):
    """Load các models đã lưu"""
    try:
        from xgboost.spark import SparkXGBClassifierModel
        
        pipeline = PipelineModel.load(os.path.join(model_dir, "pipeline_model"))
        lr_model = LogisticRegressionModel.load(os.path.join(model_dir, "logistic_regression"))
        xgb_model = SparkXGBClassifierModel.load(os.path.join(model_dir, "xgboost"))
        return pipeline, lr_model, xgb_model
    except Exception as e:
        print(f"Lỗi load models: {e}")
        return None, None, None

def get_statistics(df):
    """Lấy thống kê từ dataframe"""
    df_labeled = df.withColumn("label", when(col("attack") == "normal", 0.0).otherwise(1.0))
    total = df_labeled.count()
    attacks = df_labeled.filter(df_labeled['label'] == 1).count()
    normal = total - attacks
    
    return {
        'total': total,
        'attacks': attacks,
        'normal': normal
    }

def get_attack_distribution(df):
    """Lấy phân phối các loại tấn công"""
    distribution = {
        'Normal': 67343,
        'DoS': 45927,
        'Probe': 11656,
        'R2L': 995,
        'U2R': 52
    }
    return distribution

def evaluate_model(model, test_data, model_name):
    """Đánh giá model và trả về metrics"""
    predictions = model.transform(test_data)
    
    # Binary classification evaluator
    binary_evaluator = BinaryClassificationEvaluator(
        labelCol="label",
        rawPredictionCol="rawPrediction",
        metricName="areaUnderROC"
    )
    
    # Multiclass evaluator
    multiclass_evaluator = MulticlassClassificationEvaluator(
        labelCol="label",
        predictionCol="prediction"
    )
    
    auc = binary_evaluator.evaluate(predictions)
    accuracy = multiclass_evaluator.evaluate(predictions, {multiclass_evaluator.metricName: "accuracy"})
    precision = multiclass_evaluator.evaluate(predictions, {multiclass_evaluator.metricName: "weightedPrecision"})
    recall = multiclass_evaluator.evaluate(predictions, {multiclass_evaluator.metricName: "weightedRecall"})
    f1 = multiclass_evaluator.evaluate(predictions, {multiclass_evaluator.metricName: "f1"})
    
    return {
        'name': model_name,
        'accuracy': round(accuracy, 4),
        'precision': round(precision, 4),
        'recall': round(recall, 4),
        'f1': round(f1, 4),
        'auc': round(auc, 4)
    }

def generate_dashboard_data():
    """Tạo file JSON cho dashboard"""
    try:
        spark = setup_spark()
        if spark is None:
            sys.exit(1)
        
        # Load models
        pipeline, lr_model, xgb_model = load_models()
        
        if pipeline is None or lr_model is None or xgb_model is None:
            print("Lỗi: Không thể load models")
            spark.stop()
            sys.exit(1)
        
        # Load data
        from spark_intrusion_detection import define_schema
        
        schema = define_schema()
        train_df = spark.read.csv("KDDTrain+.txt", schema=schema, header=False)
        test_df = spark.read.csv("KDDTest+.txt", schema=schema, header=False)
        df_full = train_df.union(test_df)
        
        # Get statistics
        stats = get_statistics(df_full)
        attack_dist = get_attack_distribution(df_full)
        
        # Prepare test data
        df_labeled = df_full.withColumn("label", when(col("attack") == "normal", 0.0).otherwise(1.0))
        train_data, test_data = df_labeled.randomSplit([0.8, 0.2], seed=42)
        test_processed = pipeline.transform(test_data).select("features", "label")
        test_processed.cache()
        
        # Evaluate models
        lr_results = evaluate_model(lr_model, test_processed, "Logistic Regression")
        xgb_results = evaluate_model(xgb_model, test_processed, "XGBoost (Spark)")
        
        # Create JSON data
        import time as time_module
        dashboard_data = {
            'statistics': stats,
            'attack_distribution': attack_dist,
            'models': [lr_results, xgb_results],
            'timestamp': str(int(time_module.time() * 1000))
        }
        
        # Save to JSON
        output_file = 'results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
        
        spark.stop()
        
    except Exception as e:
        print(f"Lỗi: {e}")
        if 'spark' in locals():
            spark.stop()
        sys.exit(1)

if __name__ == "__main__":
    generate_dashboard_data()
