wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

bash Miniconda3-latest-Linux-x86_64.sh

conda create -n insight python=3.6

conda activate insight

conda install -c anaconda zeromq

conda install -c conda-forge opencv
