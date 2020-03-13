#CNN (v1)
#tensorFlowImages
import numpy as np, os,random,string
from tqdm import tqdm #used to track progress
from tensorflow.keras.layers import Conv2D, Dense, Input, MaxPooling2D, Activation, Flatten, Dropout
from tensorflow.keras.models import Model,load_model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.activations import elu
from PIL import Image
os.chdir(os.path.dirname(os.path.realpath(__file__)))
def getTrainData():
    charlist=list(string.ascii_uppercase+string.digits)
    #Gets a list of all possible characters
    traindir=os.listdir("charImages/train")
    testdir=os.listdir("charImages/valid")
    #List all the training and validation data
    data,labels,validdata,validlabels=[],[],[],[]
    for i in tqdm(traindir,ascii=True,desc="Train: "):
        try:
             im=Image.open("charImages/train/"+i)
             data.append(np.asarray(im))
             #Opens each image and adds it to the data list
             labels.append(charlist.index(i[0]))
             #Get the first character of the filename and
             #uses the list to convert it to a number (as tensorflow
             #can't read strings) then adds it to the labels list
        except:
             pass
    for i in tqdm(testdir,ascii=True,desc="Validation: "):
        try:
             im=Image.open("charImages/valid/"+i)
             validdata.append(np.asarray(im))
             validlabels.append(charlist.index(i[0]))
        except:
             pass
        #Adds the validation images and labels to the validation lists
    c = list(zip(data, labels))
    random.shuffle(c)
    data, labels = zip(*c)
    #Shuffle the data and labels by the same amount
    data,labels=np.asarray(data,dtype=np.float32),np.asarray(labels)
    data=data/255.0
    #Convert the image data to the correct form for the neural network
    c = list(zip(validdata, validlabels))
    random.shuffle(c)
    validdata, validlabels = zip(*c)
    #Shuffle the data and labels by the same amount
    validdata,validlabels=np.asarray(validdata,dtype=np.float32),np.asarray(validlabels)
    validdata=validdata/255.0
    #Convert the image data to the correct form for the neural network
    data = data.reshape((data.shape[0], data.shape[1], data.shape[2], 1))
    validdata = validdata.reshape((validdata.shape[0], validdata.shape[1], validdata.shape[2], 1))
    #Rehsape the data to be acceptable for the network
    return data,labels,validdata,validlabels
def trainModel():
    earlystop = EarlyStopping(monitor='val_loss', patience=3,verbose=1, mode='auto')
    #Callback EarlyStopping will stop the training if the validation loss doesn't appear
    #to be changing, this is to prevent overfitting
    model=cnn(True)
    #Gets the model with the flag training as True
    data,labels,validdata,validlabels=getTrainData()
    #Gets all the training data
    model.fit(data, labels,
    epochs=5,batch_size=256,
    validation_data=(validdata,validlabels),
    shuffle="batch",
    steps_per_epoch=None,
    verbose=1,use_multiprocessing=True,callbacks=[earlystop]
    )
    #Train the model with 5 epochs, batch size of 256, data shuffling
    #multiprocessing and the early stopping callback
    model.save_weights("default_weights.h5")
    #Save the model's weights to the default_weights.h5 file
def cnn(training):
    inputs=Input(shape=(30,30,1))
    #Create a layer for the inputs

    conv1=Conv2D(128, (3,3), padding="valid",strides=1, activation="relu", kernel_initializer="he_uniform")(inputs)
    #Create a 2D convolutional layer with a depth of 128 and a 3x3 kernel, activation is relu

    conv2=Conv2D(128, (3,3), padding="same",strides=1, activation="relu", kernel_initializer="he_uniform")(conv1)
    pool2=MaxPooling2D(pool_size=(2, 2),strides=2,padding="same")(conv2)
    #Add a pooling layer with pool size 2x2 and 2 strides

    conv3=Conv2D(256, (3,3), padding="same",strides=1, activation="relu", kernel_initializer="he_uniform")(pool2)

    conv4=Conv2D(256, (3,3), padding="same",strides=1, activation="relu", kernel_initializer="he_uniform")(conv3)
    pool4=MaxPooling2D(pool_size=(2, 2),strides=2,padding="same")(conv4)

    conv5=Conv2D(512, (3,3), padding="same",strides=1, activation="relu", kernel_initializer="he_uniform")(pool4)

    conv6=Conv2D(512, (3,3), padding="same",strides=1, activation="relu", kernel_initializer="he_uniform")(conv5)
    pool6=MaxPooling2D(pool_size=(2, 2),strides=2,padding="same")(conv6)

    flatten=Flatten()(pool6)
    #Flatten the convolutional layers

    dense1=Dense(2048,kernel_initializer="he_uniform", activation="relu")(flatten)
    #Add a dense layer with 2048 neurons and relu activation

    if training:
        dropout1=Dropout(0.5)(dense1)

        dense2=Dense(2048,kernel_initializer="he_uniform", activation="relu")(dropout1)
        dropout2=Dropout(0.5)(dense2)
        #If the model is training, use 0.5 dropout

        outputs=Dense(36,activation="softmax")(dropout2)
    else:
        dense2=Dense(2048,kernel_initializer="he_uniform", activation="relu")(dense1)
        #If it is not training, do not use dropout

        outputs=Dense(36,activation="softmax")(dense2)
        #Create an output layer with 36 neurons, one for each character
        #This uses softmax, which is useful for getting a maximum

    model=Model(inputs=inputs,outputs=outputs)
    #Set the model as end-to-end with the inputs and outputs
    model.compile(optimizer="Adam",loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    #Compile the model with the adam optimiser and sparse_categorical_crossentropy loss
    return model

def getPredict(filename,image):
    image=image.reshape((image.shape[0], image.shape[1], image.shape[2], 1))
    #Reshape the images to be suitable for the network
    charlist=list(string.ascii_uppercase+string.digits)
    model=cnn(False)
    #Get the model with the training flag as false
    model.load_weights("default_weights.h5")
    #Load the weights
    predicts=model.predict(image,verbose=0)
    results=np.argmax(predicts,axis=1)
    endstr="".join([charlist[i] for i in results])
    #Get the predictions and join them into a string for the word
    return endstr
