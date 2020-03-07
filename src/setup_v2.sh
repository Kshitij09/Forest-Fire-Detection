#!/bin/bash
if [ ! -e /content/models ]; then
        mkdir -p /root/.torch/models
        mkdir -p /root/.fastai/data
        ln -s /root/.torch/models /content
        ln -s /root/.fastai/data /content
        rm -rf /content/sample_data/
fi
echo Installing dependencies
pip install -q feather-format kornia pyarrow wandb nbdev fastprogress fastcore --upgrade
echo Installing fastai2
pip install git+https://github.com/fastai/fastai2.git --upgrade
echo Done.
