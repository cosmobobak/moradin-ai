from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, Conv3D, Flatten, Dense, SimpleRNN, MaxPooling3D, Dropout, BatchNormalization, Input, concatenate
from tensorflow import keras
from os import name
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

BATCH_SIZE = 64


class NetMaker:
    def __init__(self) -> None:
        inputLayer = Input(
            shape=(2, 3, 3), batch_size=BATCH_SIZE, name="Input")
        #################################################################
        ##################### CONVOLUTIONAL BLOCK #######################
        #################################################################
        x = Conv2D(64, kernel_size=(1), strides=(1, 1), padding="same",
                   data_format='channels_last', name="FrontConv")(inputLayer)
        a = BatchNormalization(axis=-1, center=False,
                               scale=False, epsilon=1e-5, name="FrontNorm")(x)
        #################################################################
        ##################### RESIDUAL BLOCK ############################
        #################################################################
        x = Conv2D(64, kernel_size=(1), strides=(1, 1), padding="same",
                   data_format='channels_last', name="ResConv1")(x)
        b = BatchNormalization(axis=-1, center=False,
                               scale=False, epsilon=1e-5, name="ResNorm1")(x)
        x = concatenate([a, b])
        #################################################################
        ##################### RESIDUAL BLOCK ############################
        #################################################################
        x = Conv2D(64, kernel_size=(1), strides=(1, 1), padding="same",
                   data_format='channels_last', name="ResConv2")(x)
        c = BatchNormalization(axis=-1, center=False,
                               scale=False, epsilon=1e-5, name="ResNorm2")(x)
        x = concatenate([b, c])
        #################################################################
        ##################### RESIDUAL BLOCK ############################
        #################################################################
        x = Conv2D(64, kernel_size=(1), strides=(1, 1), padding="same",
                   data_format='channels_last', name="ResConv3")(x)
        d = BatchNormalization(axis=-1, center=False,
                               scale=False, epsilon=1e-5, name="ResNorm3")(x)
        x = concatenate([c, d])
        #################################################################
        ##################### RESIDUAL BLOCK ############################
        #################################################################
        x = Conv2D(64, kernel_size=(1), strides=(1, 1), padding="same",
                   data_format='channels_last', name="ResConv4")(x)
        e = BatchNormalization(axis=-1, center=False,
                               scale=False, epsilon=1e-5, name="ResNorm4")(x)
        x = concatenate([d, e])
        #################################################################
        ##################### RESIDUAL BLOCK ############################
        #################################################################
        x = Conv2D(64, kernel_size=(1), strides=(1, 1), padding="same",
                   data_format='channels_last', name="ResConv5")(x)
        f = BatchNormalization(axis=-1, center=False,
                               scale=False, epsilon=1e-5, name="ResNorm5")(x)
        x = concatenate([e, f])
        #################################################################
        ##################### FULLY CONNECTED OUT #######################
        #################################################################
        x = Flatten()(x)
        x = Dense(256, activation="relu", name="Dense1")(x)
        outputLayer = Dense(1, name="eval", activation="tanh")(x)

        self.evalModel = Model(inputs=inputLayer, outputs=outputLayer)

        self.evalModel.compile(
            optimizer=keras.optimizers.Adam(),
            loss=keras.losses.MeanSquaredError(),
            metrics=[],
        )

        self.evalModel.summary()

    def __call__(self) -> Model:
        return self.evalModel
