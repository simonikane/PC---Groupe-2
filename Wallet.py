import unittest
import logging
import sys, os
import datetime

# ===========================================
#               COMPONENT N° 2
#                     -
#                   WALLET
# ===========================================



################ To Do list #############################
#faire une fonction qui permet de recuperer la liste des utxos non depensés: utiliser la classe Tx
############se servir de cette fonction dans la balance afin de controler les montant non depensés
#Menu géneral ()
#fonction transaction
    ############## interface utilisatueur pour la transaction
#fonction balance
    ############## interface utilisatueur pour la balance

################end To Do list#############################




# Main menu

# Starts the application / allows the user to identify himself and choose what he wants to do
# The user enter his credentials : USERNAME and PASSWORD.
# When the user is authentified, he can choose what to do
# Enter "1" to check his account balance
# Enter "2" to make a transaction
# Enter "0" to logout

def menu_principal(Wallet):
    os.system('clear')
    print ("Hello,\n")
    Wallet.connexion()
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

def menu_balance():
    print ("Hello\n")
    print ("Do you want to consult your balance according to a specific account or all of your accounts?")
    print ("1. One specific account \n")
    print ("2. All of my accounts \n")
    account_choice = input(" >>  ")
    if account_choice == 1 :
        print ("What are the account's informations ?")
        account_account = input(" >>  ")
        #print (Wallet.balance ('''Mettre ici les arguments'''))
    elif account_choice == 2 :
        print ("Your current account balance for all of your accounts is :")
        #print (Wallet.balance ('''Mettre ici les arguments'''))
    print ("8. Back to the main menu")
    print ("9. Logout" )
    choix = input(" >>  ")
    menu(choix)
    return

#Describe the action related to transactions (creation of a transaction)

def menu_transaction():
    print ("Hello\n")
    print ("Who is the recipient of the transfer ?")
    dest = input(" >> ")
    print ("How much do you want to transfer ?")
    amount = input(" >> ")
    #print (Wallet.transaction ('''Mettre ici les arguments'''))
    print ("8. Back to the main menu")
    print ("9. Logout" )
    choice = input(" >>  ")
    menu(choice)
    return

# Back to main menu
def back():
    actions['menu_principal']()

# Exit program
def quit():
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
        for bloc in blocList:
            tx = bloc.tx1
            for utxo in tx.UTXOs:
                if publicAddress != None:
                    if utxo.dest == publicAddress:
                        balance = balance + utxo.montant
                else:
                    if utxo.dest in self.cryptoPuzzle.values():
                        balance = balance + utxo.montant
        return balance

    #Returns the list of the UTXO in the bloc
    #:param blocList => list of all the blockchain blocks
    def retrieveUTXOs(self, blocList):
        utxoList = []
        for bloc in blocList:
            tx = bloc.tx1
            for utxo in tx.UTXOs:
                utxoList.append(utxo)
        return utxoList

    #This function checks that the amount of the transaction is sufficient
    #:param listUtxoNotSpend=> list of utxos not spend
    #:param amount=> amount of the transaction
    #Return the sum of UTXOs choosen for the transactions
    def selectUtxoForTransaction(listUtxoNotSpend, amount):
        summ = 0
        UtxoChoosen = []
        for i in range(len(listUtxoNotSpend)):
            summ = summ + listUtxoNotSpend[i].montant
            if summ <= amount:
                UtxoChoosen.append(listUtxoNotSpend[i])
            else:
                break;
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
            txi = TXI(utxo.nBloc, utxo.nTx, utxo.nUtxo, sign)
            listTxi.append(txi)
        return listTxi

    #This function Creates an String (concaten the strings)
    #:param: sender_publicAdress, recipient_adress, amount => strings for contenate
    #:return result=> result from concatenation
    def concatTransactionParameters(self, sender_publicAdress, recipient_adress, amount):
        result =  ''.join([sender_publicAdress, recipient_adress, str(amount), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        print(result)
        return result

    # This function serves to initialize a transaction and help to create a signature
    #:param sender_privateAdress => indicates sender private address
    #:param recipient_adress => indicates recipient address
    #:param amount => transaction amount
    #:param blocList => List of all bloc in blockchain
    #:return listTxi=> Txi list for transaction, [utxo_recipient, utxo_sender]=> recipient Utxo and sender Utxo
    def transaction(self, sender_privateAdress, recipient_adress, amount, blocList):
        #retrieve the list of utxo
        listUtxoNotSpend = self.retrieveUTXOs(blocList)#Extraire la liste des utxo

        #Lecture des utxodispo pas encore fait ( appel de la METHODE D'ISMAIL)

        #Takes sender public address
        sender_publicAdress = self.cryptoPuzzle[sender_privateAdress]
        listUtxoChoosen, values = self.selectUtxoForTransaction(listUtxoNotSpend, amount)

        #creates an string with sender_publicAdress, recipient_adress, amount for signing
        chaineToSign = self.concatTransactionParameters(sender_publicAdress, recipient_adress, amount)
        #Sign transaction with privateKay
        sign = signature(chaineToSign, sender_privateAdress)

         # initializes txi list of the transaction
        listTxi = convertUtxoInTxi(listUtxoChoosen, sign)

        #Calculates the residual amount
        residual_amount = values - amount

        #intialializes or create utxo_recipient, utxo_sender
        utxo_recipient = UTXO(-1,-1,-1,amount, recipient_adress, -1)
        utxo_sender = UTXO(-1,-1,-1,residual_amount, sender_publicAdress, -1)

        return listTxi, [utxo_recipient, utxo_sender]


    # Return the list of UTXO not linked to a TXI
    #:param UTXO_list =>
    #:param TX_List =>
	def UTXO_not_linked_TXI(UTXO_list, TX_List):
		cpt=0
		UTXO_not_linked=[]
		for i in range(len(UTXO_list)
			for j in range(len(TX_list))
				for k in range(len(TX_list[j].UTXOs))
					if UTXO_list[i].nBloc==TX_List[j].UTXOs[k].nBloc && UTXO_list[i].nTx==TX_List[j].UTXOs[k].nTx && UTXO_list[i].nUTXO==TX_List[j].UTXOs[k].nUTXO:
						cpt=cpt+1
			if cpt==0:
				UTXO_not_linked.append(UTXO_list[i])
			cpt=0
		return UTXO_not_linked
	
		def retrieveTXIs(self, blocList)
		txiList=[]
		for bloc in blocList:
			tx=bloc.tx1
			for txi in tx.TXIs:
				txiList.append(txi)
		return txiList
	
	def UTXO_not_in_TXI(UTXO_list, TXI_list)
		utxoList=[]
		compteur=0
		for utxo in UTXO_List:
			for txi in TXI_list:
				if utxo!=txi:
					compteur=compteur+1
			utxoList.append(utxo)
		return utxoList
		



class Wallet_test(unittest.TestCase):

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

    #Checks if a UTXO is not linked to a TXI
#    def test_UTXO_not_linked_TXI(self):
#        myWallet = Wallet("id123", "AZERTYUIOP123")
#        UTXO=["a"]
#        TXI=[]
#        self.assertTrue(myWallet.UTXO_not_linked_TXI(UTXO,TXI),UTXO)
#        UTXO=["a"]
#        TXI=["a"]
#        none=[]
#        self.assertFalse(myWallet.UTXO_not_linked_TXI(UTXO,TXI),TXI)
#        self.assertTrue(myWallet.UTXO_not_linked_TXI(UTXO,TXI),none)
    
    def test_concatTransactionParameters(self):
        myWallet = Wallet("id123", "AZERTYUIOP123")
        sender_publicAdress = "SENDER"
        recipient_adress = "RECIPIENT"
        amount = 40
        self.assertTrue("SENDERRECIPIENT40" in myWallet.concatTransactionParameters(sender_publicAdress, recipient_adress, amount))
        self.assertEqual("SENDERRECIPIENT40" ,myWallet.concatTransactionParameters(sender_publicAdress, recipient_adress, amount)[:-19])



# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    #myWallet = Wallet("id123", "AZERTYUIOP123")
    #myWallet.open = False
    unittest.main()
    #menu_principal(myWallet)
