# Train RNN to recognize to Learn DNP3 ICS Protocol (PCAP Data)
The whole point of this repository is to learn states of SCADA Systems's DNP3 Protocol. This ICS Communication Protocol data can be found in multiple packet capture files (pcap) dumps all over the internet.

- Code for the RNN in this taken from [Extracting-FSM-From-RNNs](https://github.com/DES-Lab/Extracting-FSM-From-RNNs) and [Train-RNN-on-Regural-Langauges repositories](https://github.com/emuskardin/Train-RNN-on-Regural-Langauges/tree/master) and modified 
to work for our problem.
- This repository contains minimal code which can be used to train RNN (plain, GRU, LSTM) to recognize regular languages.
- It also provides a method of extracting regular languages form trained RNNs using active automata learning (AALpy).
- It also contains code to extrtact TCP streams from PCAP and extract DNP3 function codes from the sequence of packets. These function codes are then transformed and inputted to RNN.

## Install 
I will update the `requirements.txt` to have an accurate list of all required libraries in the future. The mail ones are `AALpy, Scapy, Pyshark, Tshark, pytorch, numpy, crcmod` just off the top of my mind.

To visualize finite state machines, ensure that Graphviz is installed on your system. Also install tshark for pyshark to work.

## Run Training & Create a Finite State Machine Model
To run the training, simply configure to your wishes and run the `RNN_Driver.py` script.

## Acknowledgement
- Thanks to **Renuka Konka** & **Monika Solanki** for their contribution and for being awesome teammates. This is a team effort.
- This work wouldn't be possible if not for the ideas, constant support and critisism of Prof. [Dr. Habeeb Olufowobi](https://dipupo.github.io/) & [Uchenna Ezeobi](https://scholar.google.com/citations?user=tj9rDt0AAAAJ&hl=en)
- Thanks to [nrodofile](https://github.com/nrodofile) for this awesome [ScapyDNP3_lib](https://github.com/nrodofile/ScapyDNP3_lib)
- Sample PCAPs are from the repository [ICS-Security-Tools](https://github.com/ITI/ICS-Security-Tools/blob/master/protocols/README.md)

PS. `generate_dnp3_data.py` still needs some work which when finished can generate pcaps with random dnp3 messages.