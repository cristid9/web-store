## @package herlpers
#
#  This package will contains helpers for using the database

def And(expr):
	newExpr = list(expr)
	newExpr[0] = "AND " + newExpr[0]
	return tuple(newExpr)



##
#
#
def equals(op1, op2):
	return (str(op1) + " = %(" + str(op1) + ")s", {str(op1): str(op2)})	

##
#
#
def notEquals(op1, op2):
	return (str(op1) + " != %(" + str(op1) + ")s", {str(op1): str(op2)})	

##
#
#
def lessThan(op1, op2):
	return (str(op1) + " < %(" + str(op1) + ")s", {str(op1): str(op2)})
	
##
#
#
def lessOrEquals(op1, op2):
	return (str(op1) + " <= %(" + str(op1) + ")s", {str(op1): str(op2)})

##
#
#
def greaterThan(op1, op2):
	return (str(op1) + " > %(" + str(op1) + ")s", {str(op1): str(op2)})

##
#
#
def greaterOrEquals(op1, op2):
	return (str(op1) + " >= %(" + str(op1) + ")s", {str(op1): str(op2)})
