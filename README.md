# seedseer

seedseer generates training data based on a wallets wordlist with various amounts of blur, and then feeds that to a neural network that can then be used to attempt to decipher blurry wallet photos.

It's extremely helpful to know the font used by the wallet software. For instance [Cake Wallet](https://github.com/cake-tech/cake_wallet/) uses 4 weights of Lato.

    fonts:
    - family: Lato
    fonts:
      - asset: assets/fonts/Lato-Regular.ttf
      - asset: assets/fonts/Lato-Medium.ttf
      - asset: assets/fonts/Lato-Semibold.ttf
      - asset: assets/fonts/Lato-Bold.ttf

## install

    git clone ...
    cd seedeer
    pipenv install

# usage

    pipenv shell
    python -m seedseer --help

    seedseer v1.0
    usage: python -m seedseer [action] [params]

    action            : gen, train, or recover
