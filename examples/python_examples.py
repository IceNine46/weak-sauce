
'''
Created on Dec 29, 2015

Python modules like this one, are typically named in lower case with "_" as a logical name separator (just a convention, not required).

Since python is an object oriented program language, you can define classes.  A Class groups behavior together.  Variables defined within the class are local to the class. 
Classes contain methods, these are the same as functions but they are defined to the class.

There is an example class below.

You can also define just a standalone(not part of a class) function.

There is an example class below.

@author: Greg
'''

'''
This is an example class.  Normally the class is defined starting with an uppercase letter.
If the class is large or complex, it is best to define it in its own file of the same name, though starting with a lower case letter on the file.
Classes can be defined in a file with other functions and variables as is done in this file.

'''
class ExampleClass:
       
    '''
    The __init__ method is the class constructor.  This is true for all python classes.  You can define a set of paramters for it to take.
    The first paramter should always be "self".  This is basically the current instance of the class.
    Here we have a second parameter called name. 
    In the init method we are setting the name variable to the class variable name.
    When and instance of a class is created it is called an object.  
    '''
    def __init__(self, name):
        self.name = name
    '''
    This is a basic class method, it doesn't take any parameters, except for the self parameter.
    Methods typically start with a lower case letter.
    This method uses the class variable name and prints a message.
    Then just returns a 0 to indicate to the caller everything was ok.  A method/function does not need to return anything.
    '''
    def exampleMethod(self):
        print("Hello, %s" % self.name)
        return 0
        
        
'''
Standalone Function

This function does the same thing as the exampleMethod defined in the ExampleClass.
This time it takes the name parameter directly.
Notice we don't use self here.  Self is only for class objects.
'''
        
def exampleFunction(name):
    print("Hello, %s" % name)
    return

'''
This standalone function shows how to reference a global variable.
'''
def exampleGlobalVariableFunction():
    return
    
    
'''
In Python when you execute a file the __name__ global variable is set to __main__.
You can code the statement below, and if you execute the file directly it will do what is found within the "if" block.

'''
if __name__ == '__main__':
    
    '''Here we create a variable name.  The variable is local to this "if" block.'''
    myName = "Chris"
    '''
    Here we will create an instance of the class.  An object.  You do this by calling it with the name of the class then (<any parameters defined on the __init__ method for the class).
    In this case there is one parameter defined and that is the name variable.
    Below we have created an instance of the class and passed to its constructor the string myName.
    '''
    exampleObject = ExampleClass(myName)
    
    '''
    We now have an instance of the ExampleClass in the local variable exampleObject.
    We can use that object to access the variable and functionality of the class.
    We will now use the object to call the exampleMethod of the class.
    To call a method of a class you use the object instance <exampleObject>, a period, then the name of the method, and any parameters it requires.
    '''
    code = exampleObject.exampleMethod()
    
    if code == 0:
        print('Everything is OK.')
    else:
        print('Something went wrong.')
        
        
    '''
    Now we will call the example standalone function.
    Here we don't have to create a class instance first, we just call the function directly.
    You call a function by writing the name of the function then (<first parm, second parm, ...>).
    We can even pass in the exampleObject's name variable to the standalone function.
    '''
    exampleFunction(myName)
    exampleFunction(exampleObject.name + " From the class object.")
    
