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

Then, generate the training data that will be used to train the TensorFlow model. With the default config and the supplied Monero word list, this will provide 3,382,080 training images.

    python -m seedseer gen [--k <job_key>]

Next, import the dataset into TensorFlow and train the model network.

    python -m seedseer train [--k <job_key>]

Finally, attempt to recover any seed words using the neural network.

    python -m seedseer recover [--k <job_key>]

The optional `job_key` (-k) parameter allows for namespacing of different simultaneous tasks.

## fonts    
Accuracy won't be very good if you don't know the font that the app/site/software uses. Look this up in the source code (if open source/free) or use a website (link below) like WhatTheFont to attempt to at least identify a close match.

For instance [Cake Wallet](https://github.com/cake-tech/cake_wallet/) uses 4 weights of Lato.

    fonts:
    - family: Lato
    fonts:
      - asset: assets/fonts/Lato-Regular.ttf
      - asset: assets/fonts/Lato-Medium.ttf
      - asset: assets/fonts/Lato-Semibold.ttf
      - asset: assets/fonts/Lato-Bold.ttf

Further digging through the source code revealed that the creation page that listed the mnemonic before taking the user to their wallet used specifically the *Lato Semibold (600 weight)*.

You can use whatever font you like, but the closer to the actual font used, the better. If you can't find the font easily, [WhatTheFont](https://www.myfonts.com/WhatTheFont/) is a good resource for determining a font from a screenshot.

## images

By default, the generated training images are greyscale with dimensions of 100px x 50px at 72 dpi. Text in black and background grey (#a0a0a0). This can all be changed in `seedseer/config.py``
