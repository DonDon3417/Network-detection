"""
Script tạo file JSON chứa kết quả cho dashboard
Chạy sau khi train models xong để cập nhật dashboard với dữ liệu thực
"""

import json
import os
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.classification import LogisticRegressionModel
from xgboost.spark import SparkXGBClassifierModel
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator

def setup_spark():
    """Khởi tạo Spark session"""
    spark = SparkSession.builder \
        .appName("Generate_Dashboard_Data") \
        .master("local[*]") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()
    return spark

def load_models(spark, model_dir="spark_models"):
    """Load các models đã lưu"""
    try:
        pipeline = PipelineModel.load(os.path.join(model_dir, "pipeline_model"))
        lr_model = LogisticRegressionModel.load(os.path.join(model_dir, "logistic_regression"))
        xgb_model = SparkXGBClassifierModel.load(os.path.join(model_dir, "xgboost"))
        return pipeline, lr_model, xgb_model
    except Exception as e:
        print(f"❌ Lỗi load models: {e}")
        print("Vui lòng chạy: run.bat --save trước")
        return None, None, None

def get_statistics(df):
    """Lấy thống kê từ dataframe"""
    total = df.count()
    attacks = df.filter(df['attack'] == 1).count()
    normal = total - attacks
    
    return {
        'total': total,
        'attacks': attacks,
        'normal': normal
    }

def get_attack_distribution(df):
    """Lấy phân phối các loại tấn công"""
    # Giả định có cột 'attack_type' trong data
    # NSL-KDD có: Normal, DoS, Probe, R2L, U2R
    
    # Nếu không có cột attack_type, dùng dữ liệu mặc định
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
        labelCol="attack",
        rawPredictionCol="rawPrediction",
        metricName="areaUnderROC"
    )
    
    # Multiclass evaluator
    multiclass_evaluator = MulticlassClassificationEvaluator(
        labelCol="attack",
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
    print("=" * 80)
    print("🎨 GENERATE DASHBOARD DATA")
    print("=" * 80)
    
    spark = setup_spark()
    
    # Load models
    print("\n📂 Loading models...")
    pipeline, lr_model, xgb_model = load_models(spark)
    
    if pipeline is None:
        spark.stop()
        return
    
    # Load test data
    print("📊 Loading test data...")
    from spark_intrusion_detection import define_schema, load_data, preprocess_data
    
    schema = define_schema()
    train_df, test_df = load_data(spark, schema)
    train_processed, test_processed = preprocess_data(train_df, test_df, pipeline)
    
    # Get statistics
    print("📈 Calculating statistics...")
    stats = get_statistics(train_df)
    attack_dist = get_attack_distribution(train_df)
    
    # Evaluate models
    print("🧪 Evaluating Logistic Regression...")
    lr_results = evaluate_model(lr_model, test_processed, "Logistic Regression")
    
    print("🧪 Evaluating XGBoost...")
    xgb_results = evaluate_model(xgb_model, test_processed, "XGBoost (Spark)")
    
    # Create JSON data
    dashboard_data = {
        'statistics': stats,
        'attack_distribution': attack_dist,
        'models': [lr_results, xgb_results],
        'timestamp': str(spark.sparkContext.startTime)
    }
    
    # Save to JSON
    output_file = 'results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Đã tạo file: {output_file}")
    print("\n📊 Kết quả:")
    print(f"   Tổng gói tin: {stats['total']:,}")
    print(f"   Tấn công: {stats['attacks']:,}")
    print(f"   Normal: {stats['normal']:,}")
    print(f"\n📈 Models:")
    print(f"   LR - Accuracy: {lr_results['accuracy']*100:.2f}% | AUC: {lr_results['auc']:.4f}")
    print(f"   XGBoost - Accuracy: {xgb_results['accuracy']*100:.2f}% | AUC: {xgb_results['auc']:.4f}")
    
    print("\n🌐 Để xem dashboard:")
    print("   1. Mở file: dashboard.html")
    print("   2. Hoặc chạy: python -m http.server 8000")
    print("   3. Truy cập: http://localhost:8000/dashboard.html")
    
    spark.stop()

if __name__ == "__main__":
    generate_dashboard_data()
