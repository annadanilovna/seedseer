"""Import data into TF."""

import logging
import os

import tensorflow as tf
import numpy as np

from . import config


np.set_printoptions(precision=4)


class TensorFlowModel:
    """Handle import of tensorflow dataset training data."""

    def __init__(self):
        """Initialization."""
        self._autotune = tf.data.AUTOTUNE
        cpkt_model_fit = f"{config.TF_CHECKPOINT_PATH}/{config.TF_DS_INIT_CP}"
        self._cpkt_model_fit = cpkt_model_fit

        self._init_datasets()
        self._init_model()

    def _init_datasets(self):
        """
        Initialize training and validation datasets.
        """
        self._train_ds = tf.keras.utils.image_dataset_from_directory(
            config.TRAINING_DATA_PATH,
            validation_split=config.TF_VALIDATION_SPLIT,
            subset="training",
            seed=config.TF_SEED,
            image_size=(config.TF_IMG_WIDTH,
                        config.TF_IMG_HEIGHT),
            batch_size=config.TF_BATCH_SIZE)

        self._val_ds = tf.keras.utils.image_dataset_from_directory(
            config.TRAINING_DATA_PATH,
            validation_split=config.TF_VALIDATION_SPLIT,
            subset="validation",
            seed=config.TF_SEED,
            image_size=(config.TF_IMG_WIDTH,
                        config.TF_IMG_HEIGHT),
            batch_size=config.TF_BATCH_SIZE)

        self._class_names = self._train_ds.class_names
        num_classes = len(self._class_names)

        logging.info(f"Class names ({num_classes}): {str(self._class_names)}")

        self._train_ds.cache().prefetch(buffer_size=self._autotune)
        self._val_ds.cache().prefetch(buffer_size=self._autotune)

    def _init_model(self):
        """Initialize model."""
        self._model = tf.keras.Sequential([
            tf.keras.layers.Rescaling(1./255),
            tf.keras.layers.Conv2D(32, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(32, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(32, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(len(self._class_names))
        ])

        self._model.compile(
            optimizer='adam',
            loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )

    def train(self):
        """Train model. Pull from checkpoint if possible, otherwise run
        new fit."""
        cpkt_path = self._cpkt_model_fit
        if os.path.isfile(cpkt_path):
            self._model.load_weights(self._cpkt_model_fit)
        else:
            cb = tf.keras.callbacks.ModelCheckpoint(filepath=cpkt_path,
                                                    save_weights_only=True,
                                                    verbose=1)
            self._model.fit(
                self._train_ds,
                validation_data=self._val_ds,
                epochs=3,
                callbacks=[cb]
            )

    def summary(self):
        """Print model summary."""
        self._model.summary()

    def save(self):
        """Save model."""
        self._model.save(f"{config.TF_MODEL_PATH}/{config.TF_MODEL_FILE}")

    def load(self):
        """Load from file."""
        fn = f"{config.TF_MODEL_PATH}/{config.TF_MODEL_FILE}"
        self._model = tf.keras.models.load_model(fn)

    @staticmethod
    def process_path(file_path):
        """Process file path."""
        label = tf.strings.split(file_path, os.sep)[-2]
        return tf.io.read_file(file_path), label