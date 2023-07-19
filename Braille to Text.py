'''

Team Name : eg-Tactile
Module : Braille To Text & Character
Version Number : 2.0

'''

#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import pyttsx3
import os
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#File System Fucntions 
def Create_File():
  Speech(Speech_Object,"Please Enter File Name After Finish press Space Button")
  Read_File_Name(switch_Space)
  Speech(Speech_Object,File_Name[0])
  open(File_Name[0],'w+')
  Speech(Speech_Object,"File successfully created")
  
def Rename_File():
  Speech(Speech_Object,"Please enter the old file name")
  Read_File_Name(switch_Space)
  old_file_name = File_Name[0]
  Speech(Speech_Object,"Please enter the new file names")
  File_Name[0] = ''
  Read_File_Name(switch_Space)
  new_file_name = File_Name[0]
  os.rename(old_file_name, new_file_name)
  Speech(Speech_Object,"File successfully renamed")

def Delete_File():
  Speech(Speech_Object,"Please Enter File Name After Finish press Space Button")
  Read_File_Name(switch_Space)
  os.remove(File_Name[0])   
  Speech(Speech_Object,"File successfully Deleted")
  
#Require pip install pyttsx3
def Init_Speech_object():
  Object = pyttsx3.init()
  Object.setProperty('rate',190)
  return Object

def Speech(Object,data):
  Object.say(data)
  Object.runAndWait()

def Text_To_Speech_File(Path,Object):
   with open(Path,'r') as File:
    F= File.readlines()
    for i in F:
      Speech(Object,i)

def Text_CheckKey(dic, key,Word,Text_To_Speech_Object):
  if key in dic.keys():
    print(dic[key])
    Word[0] += dic[key]
  else:
    print("Not present")
    Speech(Text_To_Speech_Object,"Wrong Character Please Write character again")

def Character_CheckKey(dic, key,Character_To_Speech_Object):
    if key in dic.keys():
      print(dic[key])
      Speech(Character_To_Speech_Object,dic[key])
    else:
      print("Not present")
      Speech(Character_To_Speech_Object,"Wrong Character Please Write character again")

def Init_Buttons(Buttons_Pins,Pins_Count):
  for i in range (Pins_Count):
    GPIO.setup(Buttons_Pins[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def CheckButtons(Buttons_Pressed,Buttons_Weight,Buttons_Pins,Calc_Sign):
  for i in range(6):
    if(GPIO.input(Buttons_Pins[i]) == 1) and (Buttons_Pressed[i] == False):
      Calc_Sign[0] += Buttons_Weight[i]
      Buttons_Pressed[i] = True

def CheckMode(Button,Mode_List,Mode_Counter,Speech_Object):
    if GPIO.input(Button)==1:
     Mode_Counter[0] +=1
     if(Mode_Counter[0]==Capital):
      Mode_List[0] = 'C'
      Speech(Speech_Object,"Capital Mode")
     elif(Mode_Counter[0]==Letter):
      Mode_List[0] = 'L'
      Speech(Speech_Object,"Letter Mode")
     elif(Mode_Counter[0]==Number):
      Mode_List[0] = 'N'
      Speech(Speech_Object,"Number Mode")
      Mode_Counter[0] = 0   # Return again to Capital_Mode

def CheckSpace(Button,Word,Path):
    if GPIO.input(Button)==1:
     print(Word[0])
     with open(Path,'w+') as File:
      File.write(Word[0])
      File.write(" ")
     Word[0] = ' '

def CheckBackSpace(Button,Word):
    if GPIO.input(Button) == 1:
     String = [sub[: -1] for sub in Word]
     Word[0] = String[0]
     print(Word[0])
     
def RecordCharacter(Button,Calc_Sign,Buttons_Pressed,Mode_List,Word,Text_To_Speech_Object):
    if GPIO.input(Button)==1:
     if Mode_List[0] == 'C' and Calc_Sign[0] > 0:
      Text_CheckKey(Braille_Sign_Capital,Calc_Sign[0],Word,Text_To_Speech_Object)
     elif Mode_List[0] == 'L' and Calc_Sign[0] > 0:
      Text_CheckKey(Braille_Sign_Letter,Calc_Sign[0],Word,Text_To_Speech_Object)
     elif Mode_List[0] == 'N' and Calc_Sign[0] > 0:
      Text_CheckKey(Braille_Sign_Number,Calc_Sign[0],Word,Text_To_Speech_Object)
     for i in range(6):
      Buttons_Pressed[i] = False
     Calc_Sign[0]= 0

def Show(Button,Calc_Sign,Buttons_Pressed,Mode_List,Character_To_Speech_Object):
    if GPIO.input(Button)==1:
     if Mode_List[0] == 'C' and Calc_Sign[0] > 0:
      Character_CheckKey(Braille_Sign_Capital,Calc_Sign[0],Character_To_Speech_Object)
     elif Mode_List[0] == 'L' and Calc_Sign[0] > 0:
      Character_CheckKey(Braille_Sign_Letter,Calc_Sign[0],Character_To_Speech_Object)
     elif Mode_List[0] == 'N' and Calc_Sign[0] > 0:
      Character_CheckKey(Braille_Sign_Number,Calc_Sign[0],Character_To_Speech_Object)
     for i in range(6):
      Buttons_Pressed[i] = False
     Calc_Sign[0]= 0
    
def Get_Input(Braille_Sign_Number,Mode_Choice,Buttons_Pressed,Buttons_Weight,Buttons_Pins,Calc_choice):
    while GPIO.input(switch_Show) == 0:
     for i in range(6):
      if(GPIO.input(Buttons_Pins[i]) == 1) and (Buttons_Pressed[i] == False):
       Calc_choice[0] += Buttons_Weight[i]
       Buttons_Pressed[i] = True
    
    if Braille_Sign_Number[Calc_choice[0]] == '1':
      Mode_Choice[0] = '1'
    elif Braille_Sign_Number[Calc_choice[0]] == '2':
      Mode_Choice[0] = '2'
    elif Braille_Sign_Number[Calc_choice[0]] == '3':
      Mode_Choice[0] = '3'
    elif Braille_Sign_Number[Calc_choice[0]] == '4':
      Mode_Choice[0] = '4'
    elif Braille_Sign_Number[Calc_choice[0]] == '5':
      Mode_Choice[0] = '5' 
    elif Braille_Sign_Number[Calc_choice[0]] == '6':
      Mode_Choice[0] = '6'
    else:
      Mode_Choice[0] = '0'
    
    Calc_choice[0] = 0
    for i in range(6):
      Buttons_Pressed[i] = False
    
def Read_File_Name(switch_Space):
    while GPIO.input(switch_Space) == 0:
      CheckMode(switch_Mode,Mode_List,Mode_Counter,Speech_Object)
      CheckButtons(Buttons_Pressed,Buttons_Weight,Buttons_Pins,Calc_Sign)
      RecordCharacter(switch_Show,Calc_Sign,Buttons_Pressed,Mode_List,File_Name,Speech_Object)
      CheckBackSpace(switch_BackSpace,File_Name)
      time.sleep(0.122)
    
def CheckExit(switch_Space,switch_BackSpace):
    if GPIO.input(switch_Space) == 1 and GPIO.input(switch_BackSpace) == 1:
      for i in range(len(Mode_Choices_List)):
        Mode_Choices_List[i] = False
   
def menu(Speech_Object):
    Speech(Speech_Object,"To Learn Braille Press 1")
    Speech(Speech_Object,"To Write to File Press 2")
    Speech(Speech_Object,"To hear File Press 3")
    Speech(Speech_Object,"To File system options press 4")
    Get_Input(Braille_Sign_Number, Mode_Choices_List, Buttons_Pressed, Buttons_Weight, Buttons_Pins, Calc_Choice)
    if Mode_Choices_List[0] == '1' or Mode_Choices_List[0] == '2' or Mode_Choices_List[0] == '3' :
      return
    while Mode_Choices_List[0] == '4':
      Speech(Speech_Object,"To Create File Press 1")
      Speech(Speech_Object,"To Rename File Press 2")
      Speech(Speech_Object,"To Delete File Press 3")
      Speech(Speech_Object,"To Return Back Press 4")
      Get_Input(Braille_Sign_Number, Mode_Choices_List, Buttons_Pressed, Buttons_Weight, Buttons_Pins, Calc_Choice)
      if Mode_Choices_List[0] == '1':
        Mode_Choices_List[0] = '4'
        break
      elif Mode_Choices_List[0] == '2':
        Mode_Choices_List[0] = '5'
        break
      elif Mode_Choices_List[0] == '3':
        Mode_Choices_List[0] = '6'
        break
      elif Mode_Choices_List[0] == '4':
        Mode_Choices_List[0] = '0'
        break
      else:
        Speech(Speech_Object,"Wrong Choice")
        continue

#String To Hold Characters
Word = ['']
File_Name =['Default_File']
address = ''

#Define Used Variables
Calc_Sign = [0]
Calc_Choice = [0]


#Define Modes
Mode_Counter = [0] 
Number= 3
Letter= 2
Capital= 1


switch_Mode= 40
switch_Show = 36
switch_Space = 12
switch_BackSpace = 15


#Define Button_Pressed & Buttons Weights List
Buttons_Pressed = [False,False,False,False,False,False]
Buttons_Weight = [32,8,2,16,4,1]
Buttons_Pins = [18,31,22,32,29,33,40,36,12,15]
Mode_List = ['N']
Mode_Choices_List = ['0']

#Define Used Dictionary That Hold Characters
Braille_Sign_Capital={
  32:'A',
  40:'B',
  48:'C',
  52:'D',
  36:'E',
  56:'F',
  60:'G',
  44:'H',
  24:'I',
  28:'J',
  34:'K',
  42:'L',
  50:'M',
  54:'N',
  38:'O',
  58:'P',
  62:'Q',
  46:'R',
  26:'S',
  30:'T',
  35:'U',
  43:'V',
  29:'W',
  51:'X',
  55:'Y',
  39:'Z',
  11:'?',
  13:'.',
  8 :',',
  10:';',
  12:':',
  18:'/',
  14:'!',
  22:'@',
  23:'#'  
}
Braille_Sign_Letter={
  32:'a',
  40:'b',
  48:'c',
  52:'d',
  36:'e',
  56:'f',
  60:'g',
  44:'h',
  24:'i',
  28:'j',
  34:'k',
  42:'l',
  50:'m',
  54:'n',
  38:'o',
  58:'p',
  62:'q',
  46:'r',
  26:'s',
  30:'t',
  35:'u',
  43:'v',
  29:'w',
  51:'x',
  55:'y',
  39:'z',
  11:'?',
  13:'.',
  8 :',',
  10:';',
  12:':',
  18:'/',
  14:'!',
  22:'@',
  23:'#'  
}
Braille_Sign_Number={
  32:'1',
  40:'2',
  48:'3',
  52:'4',
  36:'5',
  56:'6',
  60:'7',
  44:'8',
  24:'9',
  28:'0',
  11:'?',
  13:'.',
  8 :',',
  6 :'*',
  10:';',
  12:'-',
  18:'/',
  14:'+',
  22:'@',
  23:'#'  
}

#Create Text To Speech Object 
Speech_Object = Init_Speech_object()

#Enable Buttons To Ouput PullDown
Init_Buttons(Buttons_Pins,len(Buttons_Pins))
Speech(Speech_Object,"Welcome to EG Tactile Writing mode")

while 1:
    
    #Menu of EG-Tactile Writing System
    menu(Speech_Object)

    while Mode_Choices_List[0] == '1':
      CheckMode(switch_Mode,Mode_List,Mode_Counter,Speech_Object)
      CheckButtons(Buttons_Pressed,Buttons_Weight,Buttons_Pins,Calc_Sign)
      Show(switch_Show,Calc_Sign,Buttons_Pressed,Mode_List,Speech_Object)
      CheckExit(switch_Space,switch_BackSpace)
      time.sleep(0.122)

    while Mode_Choices_List[0] == '2':
      CheckMode(switch_Mode,Mode_List,Mode_Counter,Speech_Object)
      CheckButtons(Buttons_Pressed,Buttons_Weight,Buttons_Pins,Calc_Sign)
      RecordCharacter(switch_Show,Calc_Sign,Buttons_Pressed,Mode_List,Word,Speech_Object)
      CheckSpace(switch_Space,Word,File_Name[0])
      CheckBackSpace(switch_BackSpace,Word)
      CheckExit(switch_Space,switch_BackSpace)
      time.sleep(0.122)
    
    if Mode_Choices_List[0] == '3':
      File_Name[0] = ''
      Speech(Speech_Object,"Please Enter File Name After Finish press Space Button")
      Read_File_Name(switch_Space)
      Speech(Speech_Object,File_Name[0])
      Speech(Speech_Object,"Content of File is")
      Text_To_Speech_File(File_Name[0],Speech_Object)
      Speech(Speech_Object,"End of File Content")

    elif Mode_Choices_List[0] == '4':
      File_Name[0] = ''
      Create_File()

    elif Mode_Choices_List[0] == '5':
      File_Name[0] = ''
      Rename_File()

    elif Mode_Choices_List[0] == '6':
      File_Name[0] = ''
      Delete_File()


      
    




  

