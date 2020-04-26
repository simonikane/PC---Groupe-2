import unittest
import logging
import sys, os
import datetime
import composant6
import bloc
from unittest.mock import MagicMock
from unittest.mock import patch


# ===========================================
#               COMPONENT N° 2
#                     -
#                   WALLET
# ===========================================



################ To Do list #############################
# TESTS
# COMPTE RENDU:
#
# Meeting composant 1 (Didi) => Ok pour qu'ils retournent la liste des blocs lorsqu'on fait appelà leur fonction
# Meeting composant 4 (Mikael) => cf captures groupe, OK pour envoyer juste la transaction (list TXI déjà signés par le composant signature, list UTXO)
# Meeting composant 6 (Lisa) => Ils avaient besoin d'une chaine en Input pour leur fonction de hashage => on a fait le taff cf fonction concatTransactionParameters

################end To Do list#############################




# Main menu

# Starts the application / allows the user to identify himself and choose what he wants to do
# The user enter his credentials : USERNAME and PASSWORD.
# When the user is authentified, he can choose what to do
# Enter "1" to check his account balance
# Enter "2" to make a transaction
# Enter "0" to logout

def menu_principal(myWallet):
    os.system('clear')
    print ("Hello,\n")
    myWallet.connexion()
    #S'identifier en utilisant les fonctions de Iris
    print ("What do you want to do ?\n")
    print ("1. Check my account balance \n")
    print ("2. Make a transaction \n")
    print ("\n9. Logout")
    choice = input(" >>  ")
    menu(choice)

#Execute the given choice of the user

def menu(choice):
    if choice.lower() == '':
        actions['menu_principal']()
    else:
        try:
            actions[choice.lower()]()
        except KeyError:
            print ("Invalid choice, please try again\n")
            actions['0']()

    return

#Describes the ouput of the account balance
def menu_balance(myWallet, blocList):
    print ("Hello\n")
    print ("Do you want to consult your balance according to a specific account or all of your accounts?")
    print ("1. One specific account \n")
    print ("2. All of my accounts \n")
    account_choice = input(" >>  ")
    if account_choice == 1 :
        print ("What are the account's informations (your private key) ?")
        account = input(" >>  ")
        print (myWallet.balance(blocList, account))
    elif account_choice == 2 :
        print ("Your current account balance for all of your accounts is :")
        print (myWallet.balance(blocList))
    print ("8. Back to the main menu")
    print ("9. Logout" )
    choix = input(" >>  ")
    menu(choix)
    return

#Describe the action related to transactions (creation of a transaction)
def menu_transaction(myWallet, blocList):
    print ("Hello\n")
    print ("Who is the recipient of the transfer (his/her public key)?")
    dest = input(" >> ")
    print ("How much do you want to transfer ?")
    amount = input(" >> ")
    print ("What are the account's informations (your private key) ?")
    account = input(" >>  ")
    myWallet.transaction(account, dest, amount, blocList)
    print("Pending Verifications... check your balance later")
    print ("8. Back to the main menu")
    print ("9. Logout" )
    choice = input(" >>  ")
    menu(choice)
    return

# Back to main menu
def back():
    actions['menu_principal']()

# Exit program
def quit(myWallet):
    myWallet.logout()
    sys.exit()

# Menu definition
# Describes all the possible functions of the program
actions = {
    '0': menu_principal,
    '1': menu_balance,
    '2': menu_transaction,
    '8': back,
    '9': quit,
}

class Wallet:
     #Initialisation of the portfolio
    #:param identifiant => the given id
    #:param password => the given password
    def __init__(self, identifiant, mot_de_passe):

        if identifiant in ("", None) or mot_de_passe in ("", None):
            raise(ValueError("ID and password must be completed"))
        else:
            self.identifiant = identifiant
            self.mot_de_passe = mot_de_passe
            self.open = False
            self.cryptoPuzzle = {} # Key : private key, value = public key
            logging.info('Test of the creation of a new wallet')
    
    
    def generatePrivatePublicKeyCouple(self):
        listkey = composant6.Signature.GenerateCouple()
        publickey = listkey[1]
        privatekey = listkey[0]
        self.cryptoPuzzle[privatekey] = publickey
    
    
    # Collects the user's credentials
    def askForConnexion(self):
        loginId = input("Please enter your login id : ")
        password = input("Password : ")
        return loginId, password

    # Check if the credentials corresponds to a profile
    #:param login => the given id
    #:param password => the given password
    #:param goodCdt => if TRUE the profile exists (id and password corresponds)
    def areCredentialsValid(self, login, password, goodCdt = False):
        if(login == self.identifiant and password == self.mot_de_passe):
            self.open = True
        else:
            self.open = False
            print("Invalid credentials, please try again")

    #Opens a session for the current user
    def connexion(self):
        while(self.open == False):
            loginId, password = self.askForConnexion()
            if(loginId == self.identifiant and password == self.mot_de_passe):
                self.open = True
                print("Please wait, you will be redirected to your personnal portfolio")

    # Logs out the user
    def logout(self):
        self.open = False
        print("See you later ...")

    #Returns the amount of cryptocurrency for one address or all the addresses of the portfolio
    #:param blocList => list of all the blockchain blocks
    #:param publicAddress => if None we return the balance of all the addresses
    def balance(self, blocList, publicAddress = None):

        balance = 0
        list_of_unspent_transaction = self.UTXO_not_in_TXI(blocList, publicAddress)
        for utxo in list_of_unspent_transaction:
            balance = balance + utxo.montant
        return balance

    

    #This function checks that the amount of the transaction is sufficient and selects the UTXOs to prepare the transaction
    #:param listUtxoNotSpend=> list of utxos not spend per address 
    #:param amount=> amount of the transaction
    #Return the sum of UTXOs choosen for the transactions
    # _______________________________________TO BE TESTED ___________________________
    def selectUtxoForTransaction(listUtxoNotSpend, amount):
        summ = 0
        UtxoChoosen = []
        for utxo in listUtxoNotSpend:
            summ = summ + utxo.montant
            if summ <= amount:
                UtxoChoosen.append(utxo)
            else:
                break;
                
        if summ < amount:
            raise(ValueError("The amount is not sufficient"))
        else:
            return UtxoChoosen,summ

    #this function creates the list of txi for the transaction
    #:param listUtxos=> liste of utxos choosen for transaction
    #:param sign=>sign of the transaction
    #return the list of TXI
    def convertUtxoInTxi(self, listUtxos, sign):
        """
        This function creates new transaction inputs with previous Utxos
        """
        listTxi = []
        for utxo in listUtxos:
            txi = bloc.TXI(utxo.nBloc, utxo.nTx, utxo.nUTXO, sign)
            listTxi.append(txi)
        return listTxi

    #This function Creates an String (concaten the strings)
    #:param: sender_publicAdress, recipient_adress, amount => strings for contenate
    #:return result=> result from concatenation
    def concatTransactionParameters(self, sender_publicAdress, recipient_adress, amount):
        result =  ''.join([sender_publicAdress, recipient_adress, str(amount), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        return result

    # This function serves to initialize a transaction and help to create a signature
    #:param sender_privateAdress => indicates sender private address
    #:param recipient_adress => indicates recipient address
    #:param amount => transaction amount
    #:param blocList => List of all bloc in blockchain
    #:return listTxi=> Txi list for transaction, [utxo_recipient, utxo_sender]=> recipient Utxo and sender Utxo
    # _______________________________________TO BE TESTED ___________________________
    def transaction(self, sender_privateAdress, recipient_adress, amount, blocList):
        #Takes sender public address
        sender_publicAdress = self.cryptoPuzzle[sender_privateAdress]
        #retrieve the list of not spent utxos
        listUtxoNotSpend = self.UTXO_not_in_TXI(blocList, sender_publicAdress) 
        listUtxoChoosen, values = self.selectUtxoForTransaction(listUtxoNotSpend, amount)

        #creates an string with sender_publicAdress, recipient_adress, amount for signing
        chaineToSign = self.concatTransactionParameters(sender_publicAdress, recipient_adress, amount)
        
        #Sign transaction with privateKay
        sign = signature(chaineToSign, sender_privateAdress)

         # initializes txi list of the transaction
        listTxi = self.convertUtxoInTxi(listUtxoChoosen, sign)

        #Calculates the residual amount
        residual_amount = values - amount
        #intialializes or create utxo_recipient, utxo_sender
        utxo_recipient = UTXO(-1,-1,-1,amount, recipient_adress, -1)
        utxo_sender = UTXO(-1,-1,-1,residual_amount, sender_publicAdress, -1)

        return listTxi, [utxo_recipient, utxo_sender]


    # _______________________________________TO BE TESTED ___________________________
    #Returns the list of the UTXO in the list of blocs
    #:param blocList => list of all the blockchain blocks
    def retrieveUTXOs(self, blocList):
        utxoList = []
        for bloc in blocList:
            tx = bloc.tx1
            for utxo in tx.UTXOs:
                utxoList.append(utxo)
        return utxoList 
    
    
    # Return the list of all TXIs
    #:param UTXO_list =>
    #:param TX_List =>
    def retrieveTXIs(self, blocList):
        txiList=[]
        for bloc in blocList:
            tx=bloc.tx1
            for txi in tx.TXIs:
                txiList.append(txi)
        return txiList
    
	
    # _______________________________________TO BE TESTED ___________________________
    # Return the list of UTXO not linked to a TXI
    #:param UTXO_list =>
    #:param TX_List =>
    def UTXO_not_in_TXI(self, blocList, publicAddress = None):
        UTXO_List=self.retrieveUTXOs(blocList)
        TXI_list=self.retrieveTXIs(blocList)
        utxo_Not_in_TXI_List=[]
        compteur=0
        
        for utxo in UTXO_List:
            if utxo.dest == publicAddress:
                for txi in TXI_list:
                    if utxo.nUTXO == txi.nUtxo:
                        compteur=compteur+1
                if compteur == 0:
                    utxo_Not_in_TXI_List.append(utxo)
                compteur=0
            if publicAddress == None:
                    if utxo.dest in self.cryptoPuzzle.values():
                        for txi in TXI_list:
                            if utxo.nUTXO == txi.nUtxo:
                                compteur=compteur+1
                        if compteur == 0:
                            utxo_Not_in_TXI_List.append(utxo)
                        compteur=0
        return utxo_Not_in_TXI_List
		

class Wallet_test(unittest.TestCase):
    
    txi1 = "Tsc 1"
    txi2 = "Tsc 2"
    txi3 = "Tsc 3"
    txi7 = "Tsc 7"
    txi8 = "Tsc 8"
    txi9 = "Tsc 9"
    txi10 = "Tsc 10"
    txi11 = "Tsc 11"
    
    utxo3 = MagicMock(nBloc = 1, ntx = 1, nUTXO = 1)
    utxo4 = MagicMock(nBloc = 2, ntx = 1, nUTXO = 2)
    utxo5 = MagicMock(nBloc = 3, ntx = 1, nUTXO = 3)

    txi4 = MagicMock(nBloc = 1, ntx = 1, nUTXO = 1, sign = "signature1")
    txi5 = MagicMock(nBloc = 2, ntx = 1, nUTXO = 2, sign = "signature1")
    txi6 = MagicMock(nBloc = 3, ntx = 1, nUTXO = 3, sign = "signature1")
    
    
    tx1 = MagicMock(TXIs = [txi1,txi2,txi3])
    tx3 = MagicMock(TXIs = [txi7,txi8,txi9])
    tx4 = MagicMock(TXIs = [txi10,txi11])
        
    bloc1 = MagicMock(tx1 = tx1)
    bloc2 = MagicMock(tx1 = tx3)
    bloc3 = MagicMock(tx1 = tx4)
        
    blocList = [bloc1, bloc2, bloc3]
    listUTXO = [utxo3, utxo4, utxo5]
    listTXI =  [txi4, txi5, txi6]
    # Checks the behavior if we enter correct credentials
    # The user should be able to access his account
    def test_Connexion_ValidCredentials(self):
        myWallet = Wallet("id123", "AZERTYUIOP123")
        myWallet.open = False
        myWallet.areCredentialsValid("id123", "AZERTYUIOP123")
        self.assertTrue(myWallet.open)

    # Checks the behavior if we enter incorrect credentials
    # The user shouldn't be able to acces his account
    def test_Connexion_InvalidCredentials(self):
        myWallet = Wallet("id123", "AZERTYUIOP123")
        myWallet.open = False
        myWallet.areCredentialsValid("id1234", "AZERTYUIOP1323")
        self.assertFalse(myWallet.open)
        myWallet.areCredentialsValid("id123", "AZERTYUIOP13234")
        self.assertFalse(myWallet.open)
        myWallet.areCredentialsValid("id1237", "AZERTYUIOP132347")
        self.assertFalse(myWallet.open)

    #Checks if the function closes the user's session
    def test_Logout(self):
        myWallet = Wallet("id123", "AZERTYUIOP123")
        myWallet.logout()
        self.assertFalse(myWallet.open)

    #Checks if the function is able to create a wallet only if there are correct inputs
    def test_NewWallet(self):
        with self.assertRaises(ValueError):
            Wallet("", "")
        with self.assertRaises(ValueError):
            Wallet('', '')
        with self.assertRaises(ValueError):
            Wallet(None, None)
        with self.assertRaises(ValueError):
            Wallet("Test", None)
        with self.assertRaises(ValueError):
            Wallet(None, "Test")
        wallet = Wallet("id123", "AZERTYUIOP123")
        self.assertEqual([wallet.identifiant, wallet.mot_de_passe], ["id123", "AZERTYUIOP123"])

    
    def test_ConcatTransactionParameters(self):
        myWallet = Wallet("id123", "AZERTYUIOP123")
        sender_publicAdress = "SENDER"
        recipient_adress = "RECIPIENT"
        amount = 40
        self.assertTrue("SENDERRECIPIENT40" in myWallet.concatTransactionParameters(sender_publicAdress, recipient_adress, amount))
        self.assertEqual("SENDERRECIPIENT40" ,myWallet.concatTransactionParameters(sender_publicAdress, recipient_adress, amount)[:-19])

    def test_RetrieveTXIs(self):
        myWallet = Wallet("id123", "AZERTYUIOP123")
        testList = myWallet.retrieveTXIs(Wallet_test.blocList)
        
        expectedlst = [Wallet_test.txi1,Wallet_test.txi2,Wallet_test.txi3,Wallet_test.txi7,Wallet_test.txi8,Wallet_test.txi9,Wallet_test.txi10,Wallet_test.txi11]
        
        self.assertEqual(testList, expectedlst)

        
    def test_balance(self):
        myWallet = Wallet("id123", "AZERTYUIOP123")
        utxo1 = MagicMock(montant = 30)
        utxo2 = MagicMock(montant = 5)
        utxo3 = MagicMock(montant = 20)
        myWallet.UTXO_not_in_TXI = MagicMock(return_value = [utxo1,utxo2,utxo3])
        b = myWallet.balance([],None)
        self.assertEqual(b, 55)
        myWallet.UTXO_not_in_TXI = MagicMock(return_value = [])
        b = myWallet.balance([],None)
        self.assertEqual(b, 0)
        
        
    def test_generatePrivatePublicKeyCouple(self):
        myWallet = Wallet("id123", "AZERTYUIOP123")
        with patch("composant6.Signature") as mock:
            mock.GenerateCouple.return_value = ["privatek", "publick"]
            myWallet.generatePrivatePublicKeyCouple()
        self.assertEqual(myWallet.cryptoPuzzle["privatek"], "publick")
        
       
        
        
        
        
        
        
        
    def side_effectF(nBloc, nTx, nUTXO, sign):
        for txi in Wallet_test.listTXI:
            if(nBloc == txi.nBloc and nTx ==txi.nTx and nUTXO == txi.nUTXO and sign == txi.sign):
                print(txi)
                return txi
        return None
    
#    def test_convertUtxoInTxi(self):
#        myWallet = Wallet("id123", "AZERTYUIOP123")
#        with patch("bloc.TXI") as mock:
#            mock.TXI = MagicMock(side_effect = Wallet_test.side_effectF)
#            listTxitest = myWallet.convertUtxoInTxi(Wallet_test.listUTXO, "signature1")
#            print("----")
#            print(listTxitest)
#            print("----")
#            print(Wallet_test.listTXI)
#            print("----")
#        self.assertEqual(listTxitest[0], Wallet_test.listTXI[0])
#        with patch("bloc.TXI") as mock:
#            mock.TXI = MagicMock(side_effect = Wallet_test.side_effectF)
#            listTxitest = myWallet.convertUtxoInTxi(Wallet_test.listUTXO, "signature2")
#        self.assertNotEqual(listTxitest[0], Wallet_test.listTXI[0])
        
        
# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    #myWallet = Wallet("id123", "AZERTYUIOP123")
    #myWallet.open = False
    unittest.main()
    #menu_principal(myWallet)
