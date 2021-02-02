# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# Step 1 - Building the CNN

# Initializing the CNN
classifier = Sequential()

# First convolution layer and pooling
classifier.add(Convolution2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))
# Second convolution layer and pooling
classifier.add(Convolution2D(32, (3, 3), activation='relu'))
# input_shape is going to be the pooled feature maps from the previous convolution layer
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Flattening the layers
classifier.add(Flatten())

# Adding a fully connected layer
#classifier.add(Dense(units=60, activation='relu'))
classifier.add(Dense(units=2, activation='sigmoid')) # softmax for more than 2

# Compiling the CNN
classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy']) # categorical_crossentropy for more than 2


# Step 2 - Preparing the train/test data and training the model

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory('dataset/GarbageDetection/train',
                                                 target_size=(64, 64),
                                                 batch_size=32,
                                                 color_mode='rgb',
                                                 class_mode='categorical')

test_set = test_datagen.flow_from_directory('dataset/GarbageDetection/test',
                                            target_size=(64, 64),
                                            batch_size=32,
                                            color_mode='rgb',
                                            class_mode='categorical')
classifier.fit_generator(
        training_set,
        steps_per_epoch=800, # No of images in training set
        epochs=5,
        validation_data=test_set,
        validation_steps=100)# No of images in test set


# Saving the model
model_json = classifier.to_json()
with open("GarbageDetection1.json", "w") as json_file:
    json_file.write(model_json)
classifier.save_weights('GarbageDetection1.h5')
