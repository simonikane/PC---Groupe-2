# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 19:41:16 2020

@author: irisj
"""
import unittest
import logging

class Wallet:
    
    def __init__(self, identifiant, mot_de_passe):
        """
        Initialisation of the portfolio
        """
        if identifiant in ("", None) or mot_de_passe in ("", None):
            raise(ValueError("ID and password must be completed"))
        else:
            self.identifiant = identifiant
            self.mot_de_passe = mot_de_passe
            self.open = True
            self.cryptoPuzzle = {} # Key : private key, value = private key
            logging.info('Test of the creation of a new wallet')
        
    def askForConnexion():
        loginId = input("Please enter your login id : ")
        password = input("Password : ")
        return loginId, password
    
    def areCredentialsValid(self, login, password, goodCdt = False):
        if(login == self.identifiant and password == self.mot_de_passe):
            self.open = True
        else:
            self.open = False
            print("Invalid credentials, plase try again")
    
    def connexion(self):
        while(self.open == False):
            loginId, password = self.askForConnexion()
            if(loginId == self.identifiant and password == self.mot_de_passe):
                self.open = True
                print("Please wait, you will be redirected to your personnal portfolio")
    
    def disconnection(self):
        self.open = False
        print("See you later ...")
        
        
    def balance(self, blocList, publicAddress = None):
        """
        This function returns the amount of cryptocurrency for one address or all the addresses of the portfolio
        :param blocList => list of all the blockchain blocks 
        :param publicAddress => if None we return the balance of all the addresses
        """
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
    
    def retrieveUTXOs(self, blocList):
        utxoList = []
        for bloc in blocList:
            tx = bloc.tx1
            for utxo in tx.UTXOs:
                utxoList.append(utxo)
        return utxoList
        

    #def transaction(self, to, amount):

class Wallet_test(unittest.TestCase):
    
    def test_Connexion_ValidCredentials(self):
        myWallet = Wallet("id123", "AZERTYUIOP123")
        myWallet.open = False
        myWallet.areCredentialsValid("id123", "AZERTYUIOP123")
        self.assertTrue(myWallet.open)
        
    def test_Connexion_InvalidCredentials(self):
        myWallet = Wallet("id123", "AZERTYUIOP123")
        myWallet.open = False
        myWallet.areCredentialsValid("id1234", "AZERTYUIOP1323")
        self.assertFalse(myWallet.open)
        myWallet.areCredentialsValid("id123", "AZERTYUIOP13234")
        self.assertFalse(myWallet.open)
        myWallet.areCredentialsValid("id1237", "AZERTYUIOP132347")
        self.assertFalse(myWallet.open)
    
    def test_Disconnexion(self):
        myWallet = Wallet("id123", "AZERTYUIOP123")
        myWallet.disconnection()
        self.assertFalse(myWallet.open)
        
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
        
    
        
if __name__ == '__main__':
    unittest.main()
