
"""
Convert inputber to Thai Text.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลข เป็นตัวหนังสือภาษาไทย
โดยที่ค่าที่รับต้องมีค่ามากกว่าหรือเท่ากับ 0 และน้อยกว่า 10 ล้าน

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""

###### print numberic to Thai Languages ######
def int_to_th(input):
    
    # List of value that we will use to convert number to Thai Languages.
    d = { 0 : 'ศูนย์', 1 : 'หนึ่ง', 2 : 'สอง', 3 : 'สาม', 4 : 'สี่', 5 : 'ห้า',
          6 : 'หก', 7 : 'เจ็ด', 8 : 'แปด', 9 : 'เก้า', 10 : 'สิบ',
          11 : 'สิบเอ็ด', 12 : 'สิบสอง', 13 : 'สิบสาม', 14 : 'สิบสี่',15 : 'สิบห้า',
          16 : 'สิบหก', 17 : 'สิบเจ็ด', 18 : 'สิบแปด',19 : 'สิบเก้า', 20 : 'ยี่สิบ',
          30 : 'สามสิบ', 40 : 'สี่สิบ', 50 : 'ห้าสิบ', 60 : 'หกสิบ',
          70 : 'เจ็ดสิบ', 80 : 'แปดสิบ', 90 : 'เก้าสิบ' }
    
    
    rounding = 'เอ็ด'
    
    k = 1000
    tt = k*10
    ht = tt*10
    m = ht*10
    tm = m*10

    try:

        # try converting to integer
        input = int(input)
    
        # continue if input greater than or equal 0
        assert(input >= 0)

        if (input < 20):
            return d[input]

        elif (input < 100):
            if input % 10 == 0: return d[input]
            elif input % 10 == 1: return d[input-1] + rounding
            else: return d[input // 10 * 10] + d[input % 10]

        elif (input < k):
            if input % 100 == 0: return d[input // 100] + 'ร้อย'
            elif input % 100 == 1: return d[input-1 // 100] + 'ร้อย' + rounding
            else: return d[input // 100] + 'ร้อย' + int_to_th(input % 100)

        elif (input < tt):
            if input % k == 0: return int_to_th(input // k) + 'พัน'
            elif input % k == 1: return d[input-1 // k] + 'พัน' + rounding
            else: return int_to_th(input // k) + 'พัน' + int_to_th(input % k)

        elif (input < ht):
            if (input % tt) == 0: return int_to_th(input // m) + 'หมื่น'
            elif input % tt == 1: return d[input-1 // tt] + 'หมื่น' + rounding
            else: return int_to_th(input // tt) + 'หมื่น' + int_to_th(input % tt)
            
        elif (input < m):
            if (input % ht) == 0: return int_to_th(input // m) + 'แสน'
            elif input % ht == 1: return d[input-1 // ht] + 'แสน' + rounding
            else: return int_to_th(input // ht) + 'แสน' + int_to_th(input % ht)
            
        elif (input < tm):
            if (input % m) == 0: return int_to_th(input // m) + 'ล้าน'
            elif input % k == 1: return d[input-1 // k] + 'ล้าน' + rounding
            else: return int_to_th(input // m) + 'ล้าน' + int_to_th(input % m)

        raise AssertionError('Please input the number between 0 to 9,999,999')
    
    except ValueError:

        return 'Please put the value to Integer'
    

#########################################

        #### Main Function ####

#########################################

inputInput = input('โปรดใส่ตัวเลขที่ต้องการจะแปลงเป็นภาษาไทย : ')

print('ตัวเลขของคุณ คือ : ' + int_to_th(inputInput))
