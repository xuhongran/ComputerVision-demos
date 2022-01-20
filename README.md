# Demos
This repository contains the source code for the demos I use for the undergraduate and graduate courses in Computer Vision. 

## Contents
1. __Images__
 - Digitization (Python script: digitization.py)
   
   <img src="01-Images/digitization.png"  width="300"/>
 - Borders (Python script: borders.py)
    ![Borders example](01-Images/borders.png)
   
2. __Edges__
 - Derivative calculation example (R script: edge_example.r)
   
    ![Derivative calculation example](02-Edges/noise_example.png ) 
    ![Derivative calculation example](02-Edges/noise_example_gaussian.png)
    <img src="02-Edges/derivative_dx_on_unsmoothed.png"  width="189"/>
    <img src="02-Edges/derivative_dx_on_smoothed.png"  width="189"/>
 
 - Hough Transform (Python script: hough.py)
 
    <img src="02-Edges/hough.png"  width="189"/>
   
3. __Geometric transformations__
 - Transformations (Python script: transformations.py)
   
    <img src="03-Geometric_transformations/transformations.png"  width="189"/>

4. __Interest points__
 - Principal Component Analysis (R script: PCA.r)
   
    <img src="04-Interest_points/PCA.png"  width="189"/>


10. __Image Classification__
 - Working with CIFAR10 dataset (CIFAR10_dataset.ipynb)

 <img src="10-ImageClassification, etc/CIFAR10-dataset/sample_training_images.png"  width="189"/>

 - k-Nearest Neighbours (NearestNeighbours.ipynb) 

 <img src="10-ImageClassification, etc/NearestNeighbour/nearest_neighbour.png"  width="189"/>

 - Linear Classifier Weights (LinearClassifier.ipynb) 

 <img src="10-ImageClassification, etc/LinearClassifier/weights_images_.png"  width="50"/>

 - Cross-Validation k-NN (CrossValidation.ipynb) 

 <img src="10-ImageClassification, etc/CrossValidation/crossvalidation_knn_.png"  width="189"/>

 - Gradient Descent (GradientDescent.ipynb)

 - Basic Neural Network (NeuralNetwork.ipynb)

 - Convolutional Autoencoder (Autoencoder.ipynb)

 <img src="10-ImageClassification, etc/ConvolutionalAutoencoder/autoencoder_loss.png"  width="189"/>
<img src="10-ImageClassification, etc/ConvolutionalAutoencoder/autoencoder_reconstruction.png"  width="189"/>

 - Convolutional Autoencoder with Linear Bottleneck (Autoencoder_w_bottleneck.ipynb)

An example of how one could combine convolutional layers and linear layers. Not recommended for use in any application.

 <img src="10-ImageClassification, etc/ConvolutionalAutoencoderWLinearBottleneck/autoencoder_loss.png"  width="189"/>
<img src="10-ImageClassification, etc/ConvolutionalAutoencoderWLinearBottleneck/autoencoder_reconstruction.png"  width="189"/>

 - Variational Autoencoders (VariationalAutoencoderCIFAR10.ipynb and VariationalAutoencoderMNIST.ipynb)
 
The VAE for CIFAR10 is using convolutional layers: 

<img src="10-ImageClassification, etc/VariationalAutoencoder/vae_reconstruction_CIFAR10.png"  width="189"/>

The VAE for MNIST is using linear layers:

<img src="10-ImageClassification, etc/VariationalAutoencoder/vae_reconstruction_MNIST.png"  width="189"/>
