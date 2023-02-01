
"""
Convert Arabic Number to Roman Number.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลขอราบิก เป็นตัวเลขโรมัน
โดยที่ค่าที่รับต้องมีค่ามากกว่า 0 จนถึง 1000

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""

def convertNumberToRomman(input) :
    
    # Chart of Roman Number
    romanNumberChart = {    
                            1: "I",
                            5: "V",
                            10: "X",
                            50: "L",
                            100: "C",
                            500: "D",
                            1000: "M"
                        }
    
    try:

        # try converting to integer
        input = int(input)

        # Request Minimum of input number for convert to Roman Symbols is 0 and Maximum is 1000.
        if input > 0 and input <= 1000 :
            # Variables checker use for check what is maximum of Roman Symbols that we will use. ( will be a number that can be divided evenly )
            checker = 1
            # If value of input more than checker, this loop will working and will stop when else. ( ex. if input is 1 digit checker will be 1 and input is 2 digit checker will be 10 )
            while input >= checker:
                checker *= 10

            checker /= 10
            # put the String together by result +=
            result = ""

            # start loop if input not equal 0
            while input:
                # lastNum will keep digit by digit of input start with first digit untill last digit.
                lastNum = int(input / checker)

                ### below this it is condition to check mapping each digit with Roman Symbols. ###

                if lastNum <= 3: 
                    
                    result += (romanNumberChart[checker] * lastNum)
                
                elif lastNum == 4: 
                    
                    result += (romanNumberChart[checker] + romanNumberChart[checker * 5])
                
                elif 5 <= lastNum <= 8: 
                    
                    result += (romanNumberChart[checker * 5] + (romanNumberChart[checker] * (lastNum - 5)))
                
                elif lastNum == 9: 
                    
                    result += (romanNumberChart[checker] + romanNumberChart[checker * 10])
        
                input = int(input % checker)
                
                checker /= 10
                
            return 'Your Roman Value is : ' + result
        
        else :
            
            return 'Please input value between 1 to 1000'
    
    except ValueError:

        return 'Please put the value to Integer'


#########################################

        #### Main Function ####

#########################################

numInput = input('The numberic for convert to Roman value is : ')

print(convertNumberToRomman(numInput))
