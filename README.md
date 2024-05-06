# GST
[GST：a framework to automatically generate SysML diagrams from text based on deep learning]{https://github.com/HaominGuo/HaominGuo.github.io.git/files/GST.pdf}
## environments
```python
conda create -n your_env_name python=3.11.8
conda activate your_env_name
pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```
## to start

The input text of example is in *./input/Input_text.txt*, and corresponding output XMI is in ./output/import_MD.xml

The deep learning model is in *./DLmodel*
The labeled dataset is in *./DLmodel/data*
We have trained a model based on our dataset, and output it to *./DLmodel/output/best_model.pkl*. You can download our   *best_model_pkl* [here](https://drive.google.com/drive/folders/1SU0E14hhikxMLQYoEYfj_8_3KhOeqWzq).  If you want to run the program, you have to get a well-trained model(for example, our best_model.pkl) and put it into the right path.

All you have to do is to put input text in *./input/Input_text.txt*, and run the following code. Then you can get XMI file in *./output/import_MD.xml*
```python
python auto_run.py
```

If you want to train your own model on specific dataset, you have to download pre_trained model [rbt3](https://huggingface.co/hfl/rbt3/tree/main) or other pre_trained model you like, and put them in the directory *./DLmodel/rbt3/*.

## others

The pre-trained model is in *./DLmodel/rbt3*. You can change the model and train your model on your own dataset.
Train your model:

```python
cd ./DLmodel
bash train.sh
```
Maybe you have to change some parameters or code in the program before running.
