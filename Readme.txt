Python 3.6 kur, pip dahil 
pip install pandas
pip install Pillow
pip install tensorflow==1.4
pip install object_detection
pip install numpy==1.14.5

python generate_tfrecord.py csv_input=data/airplane_labels.csv output_path=data/out.record image_dir=images
# Create train data:
python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=train.record

# Create test data:
python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=test.record