#!/usr/bin/env python

import imaplib
import email
import re

# VARS
server = "DOPLNIT"
uzivatel = "DOPLNIT"
heslo = "DOPLNIT"
slozkaKeStazeniOD = "INBOX"


# PRIHLASENI K IMAP SERVERU
M = imaplib.IMAP4_SSL(server)
try:
    M.login(uzivatel,heslo)
except imaplib.IMAP4.error:
    print ("... neprihlaseno k IMAP serveru (asi user/pass) !")
    exit()
else:
    print ("... Prihlasen k IMAP serveru\n")

# UKAZ VSECHNY SCHRANKY
err, schranky = M.list()
if err == 'OK':
    print ("Schranky :")
    for f in schranky:
        print("\t", f)

# VYBER SLOZKU
err, poradiSchranky = M.select(slozkaKeStazeniOD)
if err != 'OK':
    print ("... schranka neexistuje")
    exit()

# PROJDI SLOZKU
err,cislaZprav = M.search(None,"ALL")
if err != 'OK':
    print("... schranka neobsahuje zadnou zpravu")
    exit()

# ZISKEJ UID ZPRAV VE VYBRANEM ADRESARI
err, uidZpravSeznam = M.uid('search', None, 'ALL')
if err != 'OK':
    print("... nelze ziskat uid zprav")
    exit()
uidZpravSplit = uidZpravSeznam[0].split()

# SBER ODESILATELU
odesilatele = []
for uidZpravy in uidZpravSplit:
    err, hlavickaEmailu = M.uid('fetch', uidZpravy, "(RFC822)")
    poleVHlavicce = email.message_from_bytes(hlavickaEmailu[0][1]).get('From', "")
    emailAdresa = re.findall(r'[\w\.-]+@[\w\.-]+', poleVHlavicce)
    odesilatele.extend(emailAdresa)

print("\nDeduplikovani odesilatele :")
for r in set(odesilatele):
    print("\t",r)

M.logout()
