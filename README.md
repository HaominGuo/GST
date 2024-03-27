# GST
GST：a framework to automatically generate SysML diagrams from text based on deep learning
## environments
```python
conda create -n your_env_name python=3.11.8
conda activate your_env_name
pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```
## to start
The input text of example is in the directory ./input, and corresponding output XMI is in the directory ./output

The deep learning model is in ./DLmodel
The labeled dataset is in ./DLmodel/data
We have trained a model based on our dataset, and output it to ./DLmodel/output/best_model.pkl

All you have to do is to put input in ./input/, and run the following code. Then you can get XMI file in ./output/
```python
python auto_run.py
```

## others
The pre-trained model is in ./DLmodel/rbt3. You can change the model and train your model on your own dataset.
Train your model:

```python
cd ./DLmodel
bash train.sh
```
Maybe you have to change some parameters or code in the program before running