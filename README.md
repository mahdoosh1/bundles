# Bundles
A Python library for managing translation files, also known as bundles.

## Overview
This library provides a simple and efficient way to manage translation files. It allows you to easily load, access, and manage translations for multiple languages.

## Features
* Support for multiple languages and translations
* Easy to use and integrate into existing projects
* Simple and efficient way to manage translation files

## Installation
To install the library, simply copy the `bundles.py` file into your project directory.

## Usage
Here is an example of how to use the library:
```python
from bundles import Bundles

current_language = "English"
bundles_path = "./bundles/"
identifier = "welcome_message"

bundles = Bundles(bundles_path)

print(bundles.get_translation(current_language,identifier))
```

## Classes
The library includes the following public classes:

* Bundle: A class representing a single bundle.
* Bundles: A class representing a collection of bundles.
* Language: A class representing a single language.
* Languages: A class representing a collection of languages.

Difference of Bundles and Langauges classes are:
* Bundles class uses methods `get_translation` and `get_language`
* Languages class has language name set to its attributes

## Contributing
Contributions are welcome! If you have any suggestions or improvements, please submit a pull request.
Please star this project; thats a contribution!

## License
This library is licensed under the MIT License. See the LICENSE file for details. 