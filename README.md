# The BGP Convergence Prediction Mechanism
BGP convergence time prediction by using LSTM networks 

## Getting Started

After cloning this project, follow the instructions to test the model and get new data: 

### Prerequisites

The software tools you should install as a prerequisite to the BGP Convergence Prediction Mechanism:

* [Keras with Tensorflow backend](https://www.pyimagesearch.com/2016/11/14/installing-keras-with-tensorflow-backend/)
* [ExaBGP](https://github.com/Exa-Networks/exabgp)

### Preparing data to train and test the model

The dataset folder contains raw updates from months 6, 7, 8, 9 and 10, from 2018. 
To generate the train and test dataset files with the downloaded updates:

```console
$ cd datasets

$ python create_datasets_peers.py
```

To train the model with the generated dataset use the commands:

```console
$ cd ../bgp-convergence

$ python train_convergence-announcement.py 
```
The train dataset in composed of updates collected from month 6 (using 27 days), month 7 (using 29 days), month 8 (using 27 days), and month 9 (using 22 days). 

After training the model, a model (.json) and a weight file (.h5) is generated for each of the peers used in the train. These data can be used to test the model.

The test dataset is composed of updates collected from month 10.

To test the model with the generated model wights use the command:

```console

$ python test_convergence_predictor.py 
```
The output shows:
* The test day:
```
  ### TEST DATASET DAY 02-10 ### 
```
* The list of peers:
```
  PEER 45.61.0.85
  PEER 176.12.110.8
  PEER 178.255.145.243
  PEER 192.102.254.1
  PEER 193.0.0.56
  PEER 193.160.39.1
  PEER 195.47.235.100
  PEER 212.25.27.44
  PEER 213.200.87.254
```

* The predicted and the target Convergence Time, besides the Root Mean Squared Error (RMSE): 
```
  ...............................................................
  Predicted Convergence Time: 73
  Target Convergence Time: 58
  Event 1 - RMSE:19.765289440498126
  ...............................................................
  Predicted Convergence Time: 159
  Target Convergence Time: 213
  Event 2 - RMSE:22.535568593932833
  ...............................................................
  Predicted Convergence Time: 74
  Target Convergence Time: 57
  Event 3 - RMSE:12.36931687685298
  ...............................................................
```
The list of peers must be the same in both train_convergence-announcement.py and test_convergence_predictor.py files.

#### Getting new raw data

To download new data, first create a folder to where updates will be downloaded to:

```console
$ mkdir ~/bgp-convergence/beacon_14-08-2019
$ cd ~/bgp-convergence/beacon_14-08-2019
$ cp ../download_raw_updates/ripe/* ./
```

Open file get_ripe_files.sh and modifiy lines 3 and 7 to:
```
 updates="updates.20190814*"
 wget -A $updates -r -np -nc -l1 --no-check-certificate -e robots=off http://data.ris.ripe.net/rrc$x/2019.08/
```

Then, run the script:

```console
$ ./get_ripe_files.sh
```

The downloaded files are extracted and converted from the MRT format to txt files:
Edit the files extract_files.sh and list_files.py before run the following command:

```console
$ ./extract_files.sh
```

After the above step, the script search_prefix.sh should search and filter the beacon prefix announced at predefined schedule from beacon project. This can me modified to another prefix, at line 9 from search_prefix.sh file. The file tracklinePrefix.py should also be modified according to the number of extracted files in the folder for each rrc. Run:

Folders named bases_beacon_rrc00, bases_beacon_rrc01, bases_beacon_rrc03, etc. will be created with the filtered files. Those files will be used to calculate the convergence time and label the datasets.

To generate the files that collect the features from downloaded updates, run:

```console
$ python process_new_updates.py 
```
Finally, the generated files should be moved to the datasets folder, to train and test the model with the new data.

## Authors

* **Ricardo Bennesby** - [Scholar](https://scholar.google.com.br/citations?user=WZtAvu8AAAAJ&hl=pt-BR/)
* **Edjard Mota** - [Scholar](https://scholar.google.com.br/citations?user=7WhE5ucAAAAJ&hl=pt-BR)
* **Paulo Fonseca** - [Scholar](https://scholar.google.com.br/citations?user=e-w1zY4AAAAJ&hl=pt-BR)
* **Alexandre Passito** 
