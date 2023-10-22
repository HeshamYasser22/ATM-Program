DataBase = open('DataBase.txt' , 'a+')
Data = {}
def LoadData():
    global Data
    #Go to First Line of Txt File
    DataBase.seek(0)
    for i in DataBase.read().split('\n'):
        if i != '':
            i = i.split(':')
            Data[i[0]] = i[1].strip (',').split(',')
            Data[i[0]][2] = int (i[1].split(',')[2])

def StoreData():
    global Data
    #Go to First Line of Txt File
    DataBase.seek(0)
    #Empty the Txt file Before Writing
    DataBase.truncate(0)
    for i in Data :
        DataBase.write(str(i).strip('\''))
        DataBase.write((":"))
        for j in Data[i]:
            DataBase.write(str(j).strip('\''))
            DataBase.write((","))
        DataBase.write(("\n"))
    DataBase.flush()


def CheckUser(User):
    global Data
    #Check if Account Number is in DataBase
    if User in Data:
        #If Found Return The Account Number
        return User
    else:
        #else Return 0
        return 0

def PassCheck (User , Password):
    #Check if The Password of The Entered Account Number if Right
    if Data[User][1] == Password:
        #If Right Return 1
        return 1
    else :
        #else Return 0
        return 0

def main():
    global Data
    #Super Loop (It's An ATM So it's Running All TIME)
    while (1):
        #Ask to Enter Account Number
        User = input ("Enter Account Number : ")
        #Check The Account Number
        Result = CheckUser(User)
        #If Account Number is Found :
        if (Result != 0):
            #Check if The Account is Not Suspended
            if Data[Result][3] != '1':
                #initialize Number Of Trials with 0
                Tries = 0
                #While Number of Tries Does't Exceed The Limited Number
                while Tries < 3:
                    #Ask To Enter Password
                    Password = input ("Enter Account Password : ")
                    #Check The Password
                    PassResult = PassCheck(Result , Password)
                    #If Password Is Right:
                    if PassResult == 1:
                        #Print A message Saying Welcome + Name of User
                        print ("Welcome " + Data[Result][0])
                        break
                    else :
                        #Print A message Saying Wrong Password
                        print ("Wrong Password!")
                        #Increment Number of Tries With 1
                        Tries += 1
                #If Number Of Tries Exceed The Limited Number:
                if Tries >=3:
                    #Print A message Saying Account Suspended
                    print ("Account Suspended!")
                    #Suspend The Account In Data Base
                    Data[Result][3] = 1
                    StoreData()
                else :
                    OpenAccount(Result)
            #If Tring To Enter Locked Account:
            else:
                print ("This Account is locked, Please go to the Branch")
        else:
            print ("Wrong Account Number!")

def OpenAccount(AccountNumber):
    #initialize Quit var with 0
    Quit = 0
    #Loop While Quit not Equal 'Q'
    while (Quit != 'Q'):
        #Print The Availabe Options
        print("Cash             ->       To Cash Withdraw")
        print("Balance          ->       To Balance Inquiry")
        print("Password Change  ->       To Change Password")
        print("Fawry            ->       For Fawry Service")
        print("Exit             ->       To Exit Account")
        #Ask The User To Enter Choice of Options
        Choice = input("Your Choice : ").lower().title()
        if Choice == 'Cash':
            Cash(AccountNumber)
        elif Choice == 'Balance':
            Balance(AccountNumber)
        elif Choice == 'Password Change':
            PasswordChange(AccountNumber)
        elif Choice == 'Fawry':
            Fawry(AccountNumber)
        elif Choice == 'Exit':
            Quit = 'Q'
        else :
            print ("Wrong Input !")

def Cash (AccountNumber):
    global Data
    #initialize Quit var with 0
    Quit = 0
    #Loop While Quit not Equal 'Q'
    while Quit != 'Q':
        #Ask to Enter Amount of Cash
        Cashout = input("Enter Desired Amount of Cash : ")
        #Check if Enters Cash is Digits Only
        if Cashout.isdigit():
            Cashout = int (Cashout)
            #Check if Entered Cash is Multiples of 100
            if Cashout%100 ==0:
                #Check if Cash in Account is Enough
                if Cashout <= Data[AccountNumber][2]:
                    ATM_Actuator_Out(Cashout)
                    #Update Cash in Account with the New Value
                    Data[AccountNumber][2] -= Cashout
                    StoreData()
                    print ("Thank You")
                    Quit = 'Q'
                else :
                    print ("No Sufficient Balance!")
                    Quit = 'Q'
            else :
                print ('Not Allowed Value!')
        else :
            print ('Wrong Input!')

def ATM_Actuator_Out(Cash):
    #An Empty Function Cause No Hardware
    pass

def Balance(AccountNumber):
    global Data
    #Print Name And Balance of The User
    print ('Name : ' + Data[AccountNumber][0])
    print ('Balance = ' , Data[AccountNumber][2])

def PasswordChange(AccountNumber):
    global Data
    #Initialize Quit var with 0
    Quit = 0
    #Loop While Quit != 'Q'
    while Quit != 'Q':
        #Ask The User To Enter The New Password
        Password = input ("Enter New Password : ")
        #Ask The User To Reenter The New Password
        PasswordConfirm = input ('Enter New Password Again : ')
        #Check if The New Password and The Confirmation is Equal and The lenght of Password is 4 Digits
        if Password == PasswordConfirm and len(Password) ==4 and Password.isdigit():
            #Update The Password in DataBase
            Data[AccountNumber][1] = Password
            print ("Password Changed Succesfully")
            StoreData()
            Quit = 'Q'
        else:
            print ('Wrong Input ,Please Try Again!')

def Fawry(AccountNumber):
    global Data
    #Print List of Operations
    RechargeList = ['Orange' , 'Etisalat' , 'Vodafone' , 'We']
    print ("Orange          ->          For Orange Recharge")
    print ('Etisalat        ->          For Etisalat Recharge')
    print ('Vodafone        ->          For Vodafone Recharge')
    print ('We              ->          For We Recharge')
    #Ask to Enter Choice
    Choice = input('Enter Choice : ').lower().capitalize()
    #if The Choice is Available:
    if Choice in RechargeList:
        #Ask to Enter Phone Number and Amount of Charge
        Phone = input("Enter Phone Number : ")
        Charge = input ('Enter Amount of Charge : ')
        #Check if Charge Amout and Phone Number is Right
        if Charge.isdigit() and Phone.isdigit():
            Charge = int(Charge)
            #Check if The Balance in Account is Enough
            if Charge <= Data[AccountNumber][2]:
                #Update The Balance With New Value And Store in DataBase
                Data[AccountNumber][2] -= Charge
                StoreData()
                print ("Succesful Operation")
            else:
                print ("Not Enough Balance!")
        else:
            print ("Wrong Entry!")


if __name__ == "__main__":
    LoadData()
    main()
