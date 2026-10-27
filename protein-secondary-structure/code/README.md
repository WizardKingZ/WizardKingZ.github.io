# Protein Secondary Structure Prediction

Reference implementation for the convolutional–recurrent Q8 sequence model described in the accompanying research report.

## Files

- `main.py` — training, recorded validation runs, model export, and prediction export
- `model.py` — network classes and model construction
- `data_prep.py` — tokenization, encoding, padding, and target preparation
- `util.py` — n-gram conversion, masked accuracy, and prediction decoding

## Environment note

The code uses the Keras API available when the model was developed. Current TensorFlow/Keras releases may require import and optimizer-argument updates. The source is provided as a reference implementation rather than a pinned, production-ready package.

## Data

The training and test datasets are not included in this download. The scripts expect `dataset/train.csv` and `dataset/test.csv` with the columns shown in `main.py`.
