# Getting Started

## Hardware

I have ordered the main parts of the smart alarm: 
* Raspberry Pi - 3 Model B+: I bought the [starter kit](https://www.amazon.co.uk/gp/product/B07GKQRRKL/ref=ppx_yo_dt_b_asin_title_o04_s01?ie=UTF8&psc=1) because I am lazy but realistically you just need the [Raspberry Pi](https://www.amazon.co.uk/Raspberry-Pi-Model-64-Bit-Processor/dp/B07BDR5PDW/ref=sr_1_3?crid=34XPA0PDJAFV&keywords=raspberry+pi+3+b%2B&qid=1563700951&s=computers&sprefix=raspberry%2Ccomputers%2C136&sr=1-3), a [power supply](https://thepihut.com/products/official-raspberry-pi-universal-power-supply) and an [SD card](https://www.amazon.co.uk/gp/product/B073JWXGNT/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1)
* [UPERFECT 7](https://www.amazon.co.uk/gp/product/B07L8CM5M8/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1) inch capacitive touch screen. This seemed like a pretty decent screen and for most purposes it is, but it leaks a lot of light from the screen with is not great at night (**DO NOT BUY!**)

The RPI fitted nicely on the back of the screen and after connecting the HDMI and USB cable from the RPI to the touch specific power supply, it worked pretty much out of the box. I installed a on-screen keyboard but there was not really much space, so I decided just to attach a physical keyboard. Once this was up and running, it was just a matter of starting to build the alarm software to get an idea of how it will all work.

## Python

I decided to develop from my laptop and then later deploy the code to the RPI, so the next few steps are just about setting up a python environment on my laptop. Everything I will be doing is from the perspective of a linux environment so may not necessarily work in Windows and MAC.

One of the best Python editors is probably PyCharm as it is targeted solely for Python and is made by JetBrains who make a whole range of great IDE’s. I don’t actually use this as I program in a number of languages and don’t really want an editor for each language but if you are starting out, I would definitely recommend PyCharm. A good getting started guide can be found [here](https://www.jetbrains.com/help/pycharm/quick-start-guide.html).

For this series, I am going to be using VS Code as this is what I use for everything else but I will try to include links to guides on how to do it in PyCharm. A really good starter guide here python in VS Code can be found [here](https://code.visualstudio.com/docs/python/python-tutorial).

Once you have an IDE, it is a good idea to set up a few tools that will provide endless help while coding. If you are using PyCharm, this all likely comes out the box. With VS Code you just need to install the Python extension, which provides most of this functionality. These are: 
* [Linting](https://www.pylint.org/) - analyses your code as you go identifying errors
* [Autocomplete](https://code.visualstudio.com/docs/languages/python#_autocomplete-and-intellisense) - tries to guess what you want to type before you’ve typed it
* [Formatting](https://github.com/psf/black) - makes you code automatically look tidy
* [Debugging](https://realpython.com/python-debugging-pdb/) - allows you to run code line by line to debug any problems
* [Testing](https://docs.python-guide.org/writing/tests/) - helps with writing and running tests to make sure your code is working properly

You will also probably want to set up a virtual environment. This is a python concept where you development environment is isolated off away from the rest of the operating system. This means you can install/change/remove packages without worrying about what it might break on your computer. It also makes the project a bit easier to deploy as you can include the prerequisites for installing the program in a requirements.txt file and pip will handle the rest. The starter guide linked above will cover how to do this.

## User Interface

One of the most important aspects of the alarm clock will be the user interface. This is how most of the information will be conveyed to the user and how the user will use and configure the alarm. Building user interfaces from scratch is quite a large task but luckily there are a number of frameworks that do most of the heavy lifting for us.

This can include [HTML and CSS]() for a web application, [gtk]() or what I will use in this project, [Qt](). As with each of these, Qt provides a whole range of standard user interface objects which it calls Widgets. These can then be arranged on the screen and functionality wired up to create the overall alarm interface. 

TODO: SHOW SOME IMAGES OF QT USER INTERFACES AND WIDGETS

In order to use Qt, we need to install the PyQt5 library so that it can be included in the project. This can be achieved with a useful python utility called pip. Installing Qt is as simple as running:
```python
pip install PyQt5
```

