# dslr

### Installing dependencies

(Optional) Run `python -m venv venv` then `source venv/bin/activate` in order to activate the virtual environment.

Run `pip install -r requirements.txt` to install all dependencies.

## Data Visualization

### Describe

Run `python describe.py [file to describe]`.

### Histogram

Run `python histogram.py [file to make a histogram for]`.

### Scatter plot

Run `python scatter_plot.py [file to make a scatter plot for]`.

### Pair plot

Run `python pair_plot.py [file to make a pair plot for]`.

## Logistic Regression

### Training

Run `python logreg_train.py [file to train from]`.

You may specify a destination file for the weights with the `--destination` or `-d` option. By default, they will be written to `weights.lgr`.

### Predicting

Run `python logreg_predict.py [file to predict from] [weights file]`.

You may specify a destination file for the predictions with the `--destination` or `-d` option. By default, they will be written to `houses.csv`.