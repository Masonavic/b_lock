# b_Lock: Cryptocurrency Access Token

## Motivation

Smart property is an emergent idea in which physical objects have their access control (and thus ownership) based on a cryptocurrency token. One of the prime benefits of bitcoin, namely that of a trustless, decentralized and secure ledger system for assigning ownership, could be applied to physical devices such as computers, cars, and perhaps even houses. In addition, programmable forms of ownership such as multi-signature transaction control, smart contracts and smart loans could fundamentally alter the nature of how we interact with the things we own.

While some ideas for how to implement smart property schemes have been advanced, to date a proof-of-concept device that can be used to link ownership of a blockchain-based token to a physical actuator (e.g. a lock) has not been developed. The B_Lock aims to bridge this gap, with the ultimate aim being to provide a cheap, robust and secure device to provide a simple high/low voltage output in response to cryptographic verification of the device’s ownership status on the blockchain.

## Software Overview

In many ways the B_Lock concept is identical to other smart locks that are being developed, with one crucial difference: while other products have their access control ultimately contingent on the device manufacturer, access to the B_Lock will be exclusively controlled by the blockchain.

The pseudo-code algorithm for operation of the B_Lock is described below.

<table>
  <tr>
    <td>Step</td>
    <td>Description</td>
    <td>Methodology</td>
    <td>Dependencies</td>
  </tr>
  <tr>
    <td>1</td>
    <td>Determine current ownership</td>
    <td>Query CoinPrism API</td>
    <td>Network hardware, HTTPS/SSL</td>
  </tr>
  <tr>
    <td>2</td>
    <td>Create random challenge nonce</td>
    <td>Hardware random number functions</td>
    <td>Hardware random number functions</td>
  </tr>
  <tr>
    <td>3</td>
    <td>Send challenge nonce to user</td>
    <td>Bluetooth/Ethernet/Wifi</td>
    <td>LAN Interface</td>
  </tr>
  <tr>
    <td>4</td>
    <td>User signs and returns nonce</td>
    <td>Bluetooth/Ethernet/Wifi</td>
    <td>LAN Interface</td>
  </tr>
  <tr>
    <td>5</td>
    <td>Device verifies signature</td>
    <td>EDSCA signature verification</td>
    <td>Bitcoin library</td>
  </tr>
  <tr>
    <td>6</td>
    <td>If signature verifies, unlock device</td>
    <td>Relay/solenoid/etc</td>
    <td>Lock hardware</td>
  </tr>
</table>


### 1. Ownership Determination

Part 1 is essential, and is what differentiates the B_Lock from any other lock (smart or "dumb") that has a *single* owner. Like any cryptocurrency token the B_Lock’s ownership token is trade-able, thus necessitating the need to check ownership on each use. The code checks the CoinPrism API to determine the current owner address for its token ID. Network access is necessary for this step, as well as SSL libraries to prevent "man in the middle" attacks from changing the owner address.

### 2. Challenge Nonce

The challenge nonce needs to be randomly generated every time the device is run to prevent replay attacks. In the Python implementation this is done with software-based random number generation, however, ultimately hardware-based random data generation is preferred.

### 3. 4. User Communication

Currently the script is run within the Cloud9 IDE supplied by the BeagleBone firmware. In the future, the script will communicate with the user via BlueTooth, through which it will also bridge and internet connection for the ownership determination in step 1.

### Signature Verification (5)

Vitalik Buterin's [Pybitcointools](https://github.com/vbuterin/pybitcointools) is used to verify signatures.

### Unlocking/Locking Sequence (6)

Code is implemented to momentarily open and close the relay of the Beaglebone Relay Cape (see below).

## Hardware Implementation

### Computing Platform

The physical implementation of the B_Lock prototype was chosen to be the [BeagleBoard Black](http://beagleboard.org/BLACK). In order to reduce the potential attack surface as much as possible, the simplest hardware & software implementation to accomplish the needs of the device is prioritized. Thus, the BeagleBone black was chosen as something of a middle ground between the Arduino, which is (apparently) incapable of some of the network and cryptographic functions necessary for the device and the Raspberry Pi that was (perhaps) overpowered for what was necessary.

However, in the future, a more Arduino-like device for purpose-built computation is more desirable from a security standpoint than full-fledged general-purpose computers such as the BeagleBone and Pi. 

### Locking Device

The [BeagleBoard Black relay cape](http://www.logicsupply.com/cbb-relay/) is used to gate the voltage applied to a [solenoid](http://www.amazon.com/gp/product/B005FOTJF8). The entire device is placed inside a sealed plastic enclosure. This is not meant to be a hardened secure device but merely a proof-of-concept.

### Network Access

Multiple means of network access are possible with the device. The goal for the prototype device is to enable Bluetooth network access through a nearby smartphone or computer. The B_Lock will then bridge a connection to the internet through the device, and use this connection for Step 1.

## Blockchain Token

At present, the simplest functioning system for implementing a tradable blockchain-based ownership token is the Colored Coins project, particularly the Open Assets specification. Thus, in the proposed design, the only piece of stored data that differs between devices is the "Asset ID" corresponding to the each device’s specific ownership token. The Asset ID is the only piece of information necessary to determine the device’s current ownership status. In the version 1 implementation, the device queries the CoinPrism API to determine the address holding its current ownership token. A more secure implementation might instead verify block header progression, at the expense of speed. 

## Software

A simple script was written in Python utilizing SSL/HTTPS and bitcoin libraries to perform the initial ownership check and signature verification respectively. Messages signed by bitcoin private keys the ECDSA algorithm. Some specialized mathematics are necessary to first extract the public key from the signed message in order to verify the signature. However, this functionality is contained in certain bitcoin libraries. 

The software implementation is intentionally meant to be simple for two reasons: First, at present this is primarily intended as a proof of concept device. Second, as alluded to before, a low-complexity purpose-built device is prioritized so as to minimize the attack surface associated with general-purpose computing platforms.
