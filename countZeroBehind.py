"""เขียนโปรแกรมหาจำนวนเลข 0 ที่อยู่ติดกันหลังสุดของค่า factorial ด้วย Python โดยห้ามใช้ math.factorial เช่น 7! = 5040 มีเลข 0 ต่อท้าย 1 ตัว, 10! = 3628800 มีเลข 0 ต่อท้าย 2 ตัว"""

def findZeroBehind(input: str):
    
    zeros = 0
    max_index = len(input) - 1
    
    for index,value in enumerate(input):

        iterator = max_index - index
        
        checkZeros = input[iterator]

        if checkZeros == '0':
            
            zeros += 1
            
        else:
            
            return 'The zeros behind equal : ' + str(zeros) + ' digits'
        
    return zeros

def check_int(s):
    
    if s[0] in ('-', '+'):
        
        return s[1:].isdigit()
    
    return s.isdigit()

#########################################

        #### Main Function ####

#########################################

numInput = input('Numbers for counting the zeros behind : ')

if check_int(numInput) :

    print(findZeroBehind(numInput))
    
else :
    
    print('Please put the value to Integer')