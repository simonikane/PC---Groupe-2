# -*- coding: utf-8 -*-

class TXI():
    def __init__(self, nBloc, nTx, nUTXO, sign):
       self.nBloc = nBloc
       self.nTx = nTx
       self.nUTXO = nUTXO
       self.sign = sign


class UTXO():
    def __init__(self, nBloc, nTx, nUTXO, montant, dest, hash):
        self.nBloc = nBloc
        self.nTx = nTx
        self.nUTXO = nUTXO
        self.montant = montant
        self.dest = dest
        self.hash = hash
