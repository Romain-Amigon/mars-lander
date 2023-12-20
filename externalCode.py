import AG
X=AG.pop(1)
i=-1



#To run your python code, you must construct a class Program with a constructor and a function runTurn
class Program:	

	#The constructor takes in an argument land, which is a list of [x, y] of every ground point
	def __init__(self, land):
		self.land = land

	#The function runTurn takes in an argument with the seven integers read at each game turn
	#It must return a vector of two integers [angle, power], printing these values will do nothing
	def runTurn(self, inputValues,p,i):
		x, y, xVelocity, yVelocity, fuel, rotate, power = inputValues
		
        
        
		return p[i]