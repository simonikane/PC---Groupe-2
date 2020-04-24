import unittest
import logging
import sys, os

# ===========================================
#               COMPONENT N° 2 
#                     -
#                   WALLET 
# ===========================================


# Main menu

# Starts the application / allows the user to identify himself and choose what he wants to do
# The user enter his credentials : USERNAME and PASSWORD.
# When the user is authentified, he can choose what to do
# Enter "1" to check his account balance
# Enter "2" to make a transaction
# Enter "0" to logout 

def menu_principal():
    os.system('clear')
    print ("Hello,\n")
   # print ("What is your id ? \n")
    #id1 = input(" >>  ")
    #print ("What is your password ? \n")
    #password = input(" >>  ")
    credentials = Wallet.askForConnexion()
    # Comment utiliser cette fonction ?
    if areCredentialsValid(credentials.loginID,credentials.password).self.open == true:
    #S'identifier en utilisant les fonctions de Iris
        print ("Veuillez choisir ce que vous souhaitez faire :\n ")
        print ("1. Consulter son solde \n")
        print ("2. Effectuer une transaction \n")
        print ("\n0. Se déconnecter")
        choix = input(" >>  ")
        menu(choix)
    else :
        print ("Credentials are invalid")
        menu_principal()
    return
    
#Execute the given choice of the user
    
def menu(choix):
    if choix.lower() == '':
        actions['menu_principal']()
    else:
        try:
            actions[choix.lower()]()
        except KeyError:
            print ("Choix ivalide, veuillez réessayer\n")
            actions['0']() #Revenir au menu principal (action qui correspond à "0")

    return

#Describes the ouput of the account balance
    
def menu_balance():
    print ("Bonjour !\n")
    print ("Vous êtes dans le menu de consultation de solde de compte.\n")
    print ("Vous avez actuellement :")
    #print (Wallet.balance ('''Mettre ici les arguments'''))
    print ("8. Revenir en arrière")
    print ("9. Quitter l'application" )
    choix = input(" >>  ")
    menu(choix)
    return

#Describe the action related to transactions (creation of a transaction)
    
def menu_transaction():
    print ("Bonjour !\n")
    print ("Vous pouvez effectuer une transaction.\n")
    print ("Qui sera le destinataire de votre paiement ?")
    #print (Wallet.transaction ('''Mettre ici les arguments'''))
    print ("8. Revenir en arrière")
    print ("9. Quitter l'application" )
    choix = input(" >>  ")
    menu(choix)
    return

# Back to main menu
def revenir():
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
    '8': revenir,
    '9': quit,
}


# ===========================================
#                WALLET FUNCTIONS   
# ===========================================
    
    
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
            self.open = True
            self.cryptoPuzzle = {} # Key : private key, value = public key
            logging.info('Test of the creation of a new wallet')

    # Collects the user's credentials
    def askForConnexion():
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


# ===========================================
#                UNIT TESTS   
# ===========================================
        
    
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




'''
# =======================
#      MAIN PROGRAM
# =======================

#Que sont ces lignes, comment gérer la configuration  ?

# Main Program
if __name__ == "__main__":
    # Launch main menu
    menuprincipal()
    
if __name__ == '__main__':
    unittest.main()
'''

