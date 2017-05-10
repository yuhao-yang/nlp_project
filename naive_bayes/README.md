# nlp_project: novel classification

Using Naive Bayes and Neural Network to classify novels. 

### Features

- Predicting novel classification based on statistical information

### Tech

Project uses a number of open source projects to work properly:

* [pybrain](https://github.com/pybrain/pybrain) - the Python Machine Learning Library
* [jieba](https://github.com/fxsjy/jieba) - the Python Chinese tokenizer library

### Installation

Project requires python package jieba (for Python 3) and pybrain.

Install the dependencies.

```sh
$ pip3 install jieba
$ pip install pybrain
```

### Running

Run run3.py to get the result of NB model (for every feature and overall):
```sh
$ python3 run3.py data/tag.txt data/title.txt data/abs.txt content.txt
```

Run nn.py to get the result of NN model:
```sh
$ python nn.py data/tag.txt.list data/tag.txt.test data/title.txt.prob data/abs.txt.prob data/content.txt.prob
```

### Development / Collaboration

Open your favorite Terminal and run these commands.

First time:
```sh
$ git clone https://github.com/yuhao-yang/nlp_project.git
```
to clone the remote branch to current directory.

Otherwise:
```sh
$ git pull origin master
```
to get the lastest version

After making some changes in local branch, check it:
```sh
$ git status
```
You should see new changes made to the directory.

Add the change:
```sh
$ git add .
```

Check it again:
```sh
$ git status
```
You should see the change in directory is ready to commit to local branch.

Add comment and commit in local branch:
```sh
$ git commit -m "Your comment message"
```

Check status again to ensure it is commited:
```sh
$ git status
```
You should see "nothing to commit".

Push to remote branch:
```sh
$ git push origin master
```

### Todos

- nerual network update (more accuracy)
- nerual network connection (with the Automation Scripts)
- training , test set reallocate