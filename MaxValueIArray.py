"""เขียนโปรแกรมหา index ของตัวเลขที่มีค่ามากที่สุดใน Array ด้วยภาษา python เช่น [1,2,1,3,5,6,4] ลำดับที่มีค่ามากที่สุด คือ index = 5 โดยไม่ให้ใช้ฟังก์ชั่นที่มีอยู่แล้ว ให้ใช้แค่ลูปกับการเช็คเงื่อนไข"""

def findMaxValue(inputArray: list) :
    
    """ 
    These 2 lines as below should work more efficiently than condition checks. if only need maximum or minimum of index value.
    
    InputArray.sort()
        
    return InputArray[len(InputArray)-1]
    
    """
    
    maxIndexValue = inputArray[0]
    
    index = 0
    
    for i in range(1,len(inputArray)):
        
        if int(inputArray[i]) > int(maxIndexValue) :
            
            maxIndexValue = inputArray[i]
            
            index = i
    
    return 'Maximum number [ position : ' + str(index + 1) +' ] [ value : ' + str(maxIndexValue) + ' ]'

def check_int(s):
    
    if s[0] in ('-', '+'):
        
        return s[1:].isdigit()
    
    return s.isdigit()

#########################################

        #### Main Function ####

#########################################

sizeOfList = input('Please input size of your list : ')
indexList = []

if check_int(sizeOfList) and int(sizeOfList) > 0 :
    
    size = int(sizeOfList)
    
    if size <= 10 :

        for i in range(size) :

            InputList = input('Please input list number :[ ' + str(i+1) + ' ] = ')
            
            if check_int(InputList) and int(InputList) < 1000001 :
            
                indexList.append(InputList)
            
            elif int(InputList) > 1000000 :
                
                print('Please put the value between 1 to 1,000,000')
                break
            
            else :
                
                print('Please put the value to Integer')
                break
            
        print(findMaxValue(indexList))

    else:
        
        print('Maximum of list size limit as 10 indexs')

elif int(sizeOfList) <= 0 :
    
    print('Please put the value greater than \'0\'')

else: 
    
    print('Please put the value to Integer')
    
