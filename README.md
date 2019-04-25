# food-picker
Food Picker is a CLI tool for quickly finding the best restaurants near a given location. During my weekly work travels, I found myself searching Yelp daily for new restaurants. This CLI tool is the first step in my automation of this process.

[![Build Status](https://travis-ci.com/cnw004/food-picker.svg?branch=master)](https://travis-ci.com/cnw004/food-picker)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

### Screen shot of CLI results
![fp in action!](https://github.com/cnw004/food-picker/blob/images/imgs/output.png)

### Setup
This CLI tool leverages the Yelp Fusion API. In order for the CLI tool to make requests, you must obtain an authorization key from Yelp. Go to [this webpage](https://www.yelp.com/developers/documentation/v3/authentication) and follow the instructions to obtain your key. 

Once you have a key, create a file in the root directory called `CONFIG.cfg` and fill it with the following contents (where <your_key> is the key you get from Yelp):
```
[api-access]
key = <your_key>
```

### Build
**Make sure to complete the setup step before building**
Begin by cloning this repository to your local machine
`git clone git@github.com:cnw004/food-picker.git`
Move into the root direcctory and run the `setup.py` script:
`python setup.py build`
This will create a binary in a folder called env in the root of food-picker and all necessary dependencies. First, move the binary to a directory in your PATH (ex `mv env/bin/fp /usr/local/bin`). You can now run the CLI tool by typing `fp`

### Features
Currently, food-picker only has one command: `fp find ADDR` which will find restaurants nearby. This command supports multiple option flags to tailor your results. Type `fp find --help` to see these options.
I plan to add more features in the future.