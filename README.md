# seedseer

attempt to recover a mnemonic seed from a blurry photo.

seedseer generates training data based on a wallet's wordlist, feeds the data int a neural network that then attempts to decipher the seed words in a mnemonic from a blurry photo.

## install

    git clone ...
    cd seedeer
    pipenv install

# usage

An image of each of the mnemonic seed words should go in `SEED_DATA_PATH` (by default `res/seed_data`). The word list for the cryptocurrency/wallet by default should be put in `res/word_list.txt`. Any fonts can be put in `res/`. These parameters can all be adjusted in the config. **Take care not to accidentally commit your seed words!**

The first step is to review the `seedseer/config.py`. Adjust parameters according to your requirements.

Then, generate the training data and import into Tensorflow. With the default config and the supplied Monero word list, this will provide 260,160 images to train the system with. On a 11th generation i5, this took ~480s and takes 1.1gb of storage.

    python -m seedseer gen
    python -m seedseer tfimport

Next, train the neural network.

    python -m seedseer train

Finally, attempt to recover any seed words using the neural network.

    python -m seedseer recover

## fonts    
It's extremely helpful to know the font used by the wallet software. For instance [Cake Wallet](https://github.com/cake-tech/cake_wallet/) uses 4 weights of Lato.

    fonts:
    - family: Lato
    fonts:
      - asset: assets/fonts/Lato-Regular.ttf
      - asset: assets/fonts/Lato-Medium.ttf
      - asset: assets/fonts/Lato-Semibold.ttf
      - asset: assets/fonts/Lato-Bold.ttf

Further digging through the source code revealed that the creation page that listed the mnemonic before taking the user to their wallet used the Lato Semibold (600 weight).

You can use whatever font you like, but the closer to the actual font used, the better. If you can't find the font easily, [WhatTheFont](https://www.myfonts.com/WhatTheFont/) is a good resource for determining a font from a screenshot.

## images

The test data that is generated is 100px x 50px at 72 DPI. Images are grayscale with the text in black and background grey (#a0a0a0) to match the images from the Cake Wallet I had. You can change these as necessary in /config.py`
