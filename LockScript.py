import httplib
import json
import random
import string

import Adafruit_BBIO.GPIO as GPIO
import time

from bitcoin import *

# -------------------------------------------------
# Step 1: Connect to CoinPrism API, determine owner
# -------------------------------------------------

conn = httplib.HTTPSConnection("api.coinprism.com")
conn.request("GET", "/v1/assets/AaHBiJDHdFQWzevu44WUeJkL9iEeXNvK9m/owners")     #Bitlock test token asset ID
r1 = conn.getresponse()
ownerdata = json.loads(r1.read())
conn.close()
OwnerAddr = ownerdata['owners'][0]['address']
print "Owner: "
print OwnerAddr

# --------------------------------
# Step 2: Generate Challenge Nonce
# --------------------------------

nonce = ''.join(random.SystemRandom().choice(string.uppercase + string.lowercase + string.digits) for _ in xrange(200))
print "Challenge Nonce: "
print nonce

# ----------------------------------------
# Step 3: Ask user to sign challenge nonce
# ----------------------------------------

nonceSig = raw_input("Sign Challenge Nonce: ")

# -------------------------------------------
# Step 4: Verify signature, unlock if correct
# Uses https://github.com/vbuterin/pybitcointools
# -------------------------------------------

userPubKey = compress(ecdsa_recover(nonce,nonceSig))
userAddr = pubkey_to_address(userPubKey)
CorrectSig = ecdsa_verify(nonce,nonceSig,userPubKey)
if (userAddr == OwnerAddr) & (CorrectSig == True):
    print "Unlock"
    GPIO.setup("P8_18", GPIO.OUT)
    GPIO.output("P8_18", GPIO.HIGH)
    time.sleep(2)
    GPIO.output("P8_18", GPIO.LOW)
elif (userAddr != OwnerAddr):
    print "Not Current Owner"
elif (CorrectSig == False):
    print "Signature Verification Failed"
