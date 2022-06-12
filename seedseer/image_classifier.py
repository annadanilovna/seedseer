"""Classify and identify text in images using TensorFlow CNNs."""


import tensorflow as tf
import numpy as np

from . import config


np.set_printoptions(precision=4)


class ImageClassifier:
    """Classify and identify text in images using TensorFlow CNNs."""

    def __init__(self, load_saved_state=False):
        """Initialization."""
        self._init_datasets()
        self._init_model()

    def _load_image_dataset(self, path, split, subset, prefetch=True):
        """Load a directory of images into a Keras dataset."""
        ds = tf.keras.utils.image_dataset_from_directory(
            path,
            validation_split=split,
            subset=subset,
            seed=config.TF_SEED,
            image_size=(config.TF_IMG_WIDTH,
                        config.TF_IMG_HEIGHT),
            batch_size=config.TF_BATCH_SIZE)

        if prefetch:
            ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)

        return ds

    def _init_datasets(self):
        """Initialize training and validation datasets."""
        path = config.TRAINING_DATA_PATH
        split = config.TF_VALIDATION_SPLIT

        self._train_ds = self._load_image_dataset(path, split, "training")
        self._val_ds = self.load_image_dataset(path, split, "validation")

        self._class_names = self._train_ds.class_names

    def _init_model(self):
        """Initialize model."""
        self._model = tf.keras.Sequential([
            tf.keras.layers.Rescaling(1./255),
            # tf.keras.layers.Conv2D(32, 3, activation='relu'),
            # tf.keras.layers.MaxPooling2D(),
            # tf.keras.layers.Conv2D(32, 3, activation='relu'),
            # tf.keras.layers.MaxPooling2D(),
            # tf.keras.layers.Conv2D(32, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            # tf.keras.layers.Dense(128, activation='relu'),
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

        cpkt_path = config.TF_CHECKPOINT_PATH + "cp-{epoch:04d}.ckpt"

        # load latest weights
        latest = tf.train.latest_checkpoint(config.TF_CHECKPOINT_PATH)
        self._model.load_weights(latest)

        # Create a callback that saves the model's weights every 5 epochs
        cb = tf.keras.callbacks.ModelCheckpoint(
            filepath=cpkt_path,
            verbose=1,
            save_weights_only=True,
            save_freq=5*config.TF_BATCH_SIZE)

        self._model.fit(
            self._train_ds,
            validation_data=self._val_ds,
            epochs=100,
            callbacks=[cb]
        )

    def classify(self, ds_path=config.SEED_DATA_PATH):
        """Classify images in a directory against a trained CNN."""
        ds = self._load_image_dataset(ds_path, None, None, False)
        self._model.predict(ds)

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
