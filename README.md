# Double-difference measurements in global full-waveform inversions

2D Data and tools that is used in the paper:

Örsvuran, Rıdvan, Ebru Bozdağ, Ryan Modrak, Wenjie Lei, and Youyi Ruan. “Double-Difference Measurements in Global Full-Waveform Inversions.” Geophysical Journal International, 2019. https://doi.org/10.1093/gji/ggz444.

## Running 2D examples

Install required packages:

```console
$ git clone --recursive https://github.com/rdno/dd_global.git
$ cd dd_global/src
$ conda env create -f environment.yml
$ cd specfem2d
$ ./configure --with-mpi
$ make all
$ cd ../..
```

Go to an example and change the `specfem_folder` parameter in the config file.

```console
$ cd data/pair_weight_test
$ # edit pair_weight_test.yml
$ # change the following line to your specfem folder
$ # specfem_folder: ~/src/specfem2d
```

Run the example:

```console
$ conda activate sair
$ sair-run pair_weight_test.yml cc
$ # Following command plots the kernel in Figure 1.
$ sair-plot-kernel work/update_cc_1 beta_update -s -c pair_weight_test.yml -l 0.3
```

Or run them using the `run.sh` script.
