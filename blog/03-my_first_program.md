# My First Program

In this installment, we are going to be creating what developers call a Minimum Viable Product (MVP). This is an application with the minimum amount of functionality for it to be useful. For me, in the case of the smart alarm, this is a clock that tells the time.

This functionality will allow us to get the project off the ground and we will end up with something on our bed side table that is actually reasonably useful with only a small amount of work. Firstly, we will need to create a new python project, then using Qt to create a window with a widget in the center that will display the time. We will also need to create a job that will repeatedly update the time.


## Creating a project

The first thing we need to do here is to create a project that will contain our new application. This simply involves creating a folder that you would like to store the project in and then opening that folder in VS Code.

Now to create a virtual environment. The the following command in the terminal (either from the OS or with VS Code), ensuring that you are inside the project directory:
```bash
python -m venv .venv
```

Once that has finished loading up, create a new file (file -> new file), then save and name it after the name of your project. Here is where we enter into the dangerous territory of naming convention. I have taken the approach of snake case for my python files. This means that words in the name are separated by underscores and everything is in lowercase. So for my project, this would be called pie_alarm.py. Follow whatever convention you like but just make sure you are consistent.

Now in this file, insert the following code:
```python
if __name__ == "__main__":
    print("Hello World")
```

The if statement here is some really weird python syntax that basically means that if you are running this file directly, then execute this code. We will see later that there will be a lot of files that will not be run directly but will just be included in the file that is run directly.

The code that is being run is then simply printing to the terminal the phrase "Hello World". Now we should run the file to see this in action. This can be achieved through multiple methods:
* Pressing F5
* Right clicking on the file and then choosing "Run python file in terminal"
* Going to the terminal and typing ```.venv/bin/python3 <python file>``` (or just ```python <python file>``` if not in a virtual environment) 

Nearly all of these will ask which file you want to run. Simply select the file you have just created. At the bottom some text should have come up including a line that says "Hello World". Congratulations! You have just written your first python programme.

It may be a good idea to try some python tutorials so that you can get a bit more accustomed to python as I may forget to explain some things (I will try my best). When you are ready, lets start with the alarm clock project!!!


## Displaying a window

In order to initially display a window to the user, we need to follow these very simple four steps:
* Import the QtWidget library
* create an Qt application
* create a window
* display the window
* execute the application

Lets break these down. The first step is very simple, where you add the following line to the very top of the python file. This will import the QtWidget library into the file for use (don't forget that you will have to use pip to install this library - ```.venv/bin/pip3 install PyQt5```)
```python
import PyQt5.QtWidgets
```

The second stage is create a QApplication object which is required to manage the control flow and main settings of the user interface. It is possible to pass command line arguments straight to the QApplication's constructor. In order to create the application, you need to have the following line of code:
```python
app = PyQt5.QtWidgets.QApplication(sys.argv)
```

The third stage is to create a window. While this is not strictly necessary as an instantiated Widget would create its own window, it gives a little more control over the layout application including a handy little dock for a toolbar. 

![alt text](https://doc.qt.io/qt-5/images/mainwindowlayout.png)

It also acts as a stable baseline that we can use to swap in and out widgets as and when we need them. Again, all you need to create a window is the following line of code:
```python
window = PyQt5.QtWidgets.QMainWindow()
```

Next we need to make sure that the window is visible. By default, widgets are initialised as hidden unless it or its parent is explicitly set to show. As the window will be the parent of nearly all the widgets in this application, we only need to call show here. This can be done by the following line:
```python
window.show()
```

The final step in getting our basic application started is to execute the application. All configuration of the application needs to be performed before this step as the application will not execute anything placed in the code after this until the application is shutdown. The following code executes the application:
```python
app.exec_()
```

That's it! We now have a window that will form the basis for our application. The final source code will look like this:

```python
import PyQt5.QtWidgets

if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication([])
    window = PyQt5.QtWidgets.QMainWindow()
    window.show()
    app.exec_()
```

## My First Widget

Now that we have window, we need to start populating it with Widgets that will display the information and interactions that we would like to present to the user. The first one we want to create is a widget that displays the time to the user. This can be a simple label that we will populate with the current time. We also need to add this label to the window, which we will place in the central widget. In order the create a label you can add the following lines of code (note this needs to be added before the application is executed):
```python
time_widget = PyQt5.QtWidgets.QLabel("Hello")
window.setCentralWidget(time_widget)
```

The "Hello" will populate the label with that text. However, we do not want to say hello, we want to tell the time. Fortunately, we can retrieve the time from a handy Qt function. After importing the QtCore package, we can include the following line to get the time:
```python
time = PyQt5.QtCore.QTime.currentTime()
```

However, this will give us a time object and unfortunately QLabel does not understand this. Therefore, we need to convert time into a string, which can be understood by QLabel. This can be done with the following line:
```python
time.toString("hh:mm")
```

This tells time that we want a string with the format of two digits for hours followed by a colon, and then followed by two digits for minutes. If we replace "Hello" with this line, you will see the time displayed in the window. Great but we now have two problems, the first is that the window looks dreadful and more importantly, the time does not change...

## What are StyleSheets?

The first problem we are going to attempt to solve is how bad the window looks. There are multiple ways that you can set the style of the window and its widgets, which includes setting the property directly or assigning stylesheets. I have decided to go with stylesheets as it allows you to have the definition of style for all widgets in one place and it only needs to be set once.

Stylesheets in Qt follow the same concept and format as [CSS](https://www.w3schools.com/css/) for HTML code, where you define style for specific widget types (e.g. QLabel, QMainWindow, etc.). This also includes custom QWidget classes, allowing us to really finely define the style by creating new custom QWidgets that need to have a different style to other widgets of the same type. An example of a style for a QLabel setting the text colour to white, the font size to 50, and the background colour to black is:
```css
QLabel {
  color: white;
  font-size: 50px;
  background: black;
}
```

It is also possible to set properties on the widget class that can alter which styles are applied to the widget. This can be used for example when altering the text colour, when an alarm goes from active to disabled. This can be done by using square brackets in the style definition:
```css
QLabel[active=false] {
  color: gray
}
```

For our programme so far, all we need to do is define a stylesheet for the QMainWindow and a QLabel. All I am going to do in the stylesheet for the QMainWindow is set the background to black as it works well for now with the idea of a bedside clock that will be on during the night. For the QLabel, we want to set the text colour to white, the size to about 200px and to center the alignment. This can be done with the following code:
```css
QMainWindow {
  background-color:black;
}

QLabel {
  color: white;
  font-size: 200px;
  qproperty-alignment: 'AlignCenter | AlignCenter';
}
```

The stylesheet then needs to be set on the window (which will be the parent of all other widgets). Setting the stylesheet can be achieved with the following lines of code:
```python
window.setStyleSheet(
    "QMainWindow {background-color:black;}"
    "QLabel {color: white;font-size: 200px;qproperty-alignment: 'AlignCenter | AlignCenter';}"
)
```

Now the application is starting to look a bit better. One final touch is to fix the size of the window so that it is the same size as the screen we will eventually be deploying this application to, so that we can get a better idea of sizes and spacing. The screen I have bought has a resolution of 800x480 and can be set as follows:
```python
window.setFixedSize(800, 480)
```

## Updating the time

Finally, lets deal with updating the time as a clock that is only correct once a day is not the most useful. 

It is probably a good idea at this point to break the QLabel containing the time into its own class as it now requires some logic. To define the class you simply need to insert the following code above the main function (ensuring that it is not indented):
```python
class Clock(PyQt5.QtWidgets.QLabel):
    pass
```

The first line is telling python that we want to create a new class called Clock that inherits from the QLabel class. By inheriting I mean that it gains all of the features of the QLabel class but gives us the ability to introduce or change features. The second line tells python that we don't want to make any changes to this class so it is essentially exactly the same as a QLabel. Don't worry, we will make some changes soon.

But first change time_widget to be a Clock so it looks like the code below and hopefully you will see no difference:
```python
time_widget = Clock(time.toString("hh:mm"))
```

Now lets move the logic to populate the Clock with the current time into the class. For this we will create a function in the class that will set the text as follows:
```python
class Clock(PyQt5.QtWidgets.QLabel):
    
    def set_time(self):
        time = PyQt5.QtCore.QTime.currentTime()
        self.setText(time.toString("hh:mm")
```

Here we have defined a function for the class using the def keyword. This function is called set_time, which is followed by brackets that contain what parameters need to be provided to the function. However, class functions are a little strange, where you need to insert the self keyword here but this does not need to be provided when calling the function.

The next line should look familiar. The final line is a little unusual as we are using that self word from earlier. This tells python that we are either using a variable from the class or we are calling a function within the class (for this we are doing the latter). 

You may ask at this point, where this setText function came from but this is part of the functionality we have inherited from QLabel. This function is another way of setting the text for the label.

We can now remove this logic from the main function, which should now look a little like this (again you should see no change):
```python
time_widget = Clock()
time_widget.set_time()
```

The final step is to create the functionality that will repeatedly update the time to the current time calling the function we have just created. To do this we are doing to create an init function in our class. This function is called whenever we run the Clock() command, so is good for setting up our class. We can also move the set_time function into here so functionality using this class does not have to call it: 
```python
def __init__(self, parent=None):
    super(Clock, self).__init__(parent)
    self.show_time()
```

You will notice that there are weird underscores either side of the init name. This tells python that this is a special function, which in this case is a constructor. There are a few other special functions that you can define in a class but we won't cover them just yet.

The other new thing here is the line starting with super. This is a strange way of calling the constructor of the parent class, QLabel, which is needed to make sure the class is fully set up to display text.

The last part of the constructor needed is one that will periodically call our set_time function to update it to the current time. For this we will use a QTimer function, which calls a defined function over a defined period of time. This can be configured as follows (don't forget to import PyQt5.QtCore):
```python
timer = PyQt5.QtCore.QTimer(self)
timer.timeout.connect(self.set_time)
timer.start(1000)
```

This will call our set time function every 1000 milliseconds (or every second). Now you can start the application and sit there waiting for the minute to tick up one.

And there you go. We have completed our MVP for our "alarm" clock in less than 30 lines of code. The final source code should look something like this:
```python
import PyQt5.QtWidgets
import PyQt5.QtCore

class Clock(PyQt5.QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(Clock, self).__init__(parent)
        self.set_time()

        timer = PyQt5.QtCore.QTimer(self)
        timer.timeout.connect(self.set_time)
        timer.start(1000)

    def set_time(self):
        time = PyQt5.QtCore.QTime.currentTime()
        self.setText(time.toString("hh:mm"))


if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication([])
    window = PyQt5.QtWidgets.QMainWindow()
    window.show()

    time_widget = Clock()
    window.setCentralWidget(time_widget)

    window.setStyleSheet(
        "QMainWindow {background-color:black;}"
        "QLabel {color: white;font-size: 200px;qproperty-alignment: 'AlignCenter | AlignCenter';}"
    )

    window.setFixedSize(800, 480)

    app.exec_()
```