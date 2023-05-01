import os

from scapy.all import *
from DNP3_Lib import *
import nest_asyncio
import pyshark

def generate_dnp3_data(pcapdir):
    nest_asyncio.apply()
    # Define a function to extract the function message from a DNP3 message
    def get_dnp3_function_message(pkt):
        # Check if the packet is a DNP3 message
        if pkt.haslayer(DNP3):
            # Extract the function message from the DNP3 message
            if pkt[DNP3].haslayer(DNP3ApplicationRequest):
                if(pkt[DNP3][DNP3ApplicationRequest].FUNC_CODE in applicationFunctionCode):
                    return applicationFunctionCode[pkt[DNP3][DNP3ApplicationRequest].FUNC_CODE],'req'
                return (None,None)
            elif pkt[DNP3].haslayer(DNP3ApplicationResponse):
                if(pkt[DNP3][DNP3ApplicationResponse].FUNC_CODE in applicationFunctionCode):
                    return applicationFunctionCode[pkt[DNP3][DNP3ApplicationResponse].FUNC_CODE],'res'
                return (None,None)
            else: 
                return (None,None)
        else:
            return (None,None)
    
    trainingdata = []
    input_al = set()
    output_al= set()
    pcapsList = os.listdir(pcapdir)
    
    for fname in pcapsList:
        if(fname.endswith('.pcap')):   
            pcapFile = pcapdir+'/'+fname
            
            print("Working on %s"%(pcapFile))
            # Get streams using pyshark
            print("Gathering streams.....")
            pysharkPcap = pyshark.FileCapture(pcapFile)
            streams = {}
            count = 0
            for pkt in pysharkPcap:
                if("TCP" in str(pkt.layers)):
                    if pkt.tcp.stream not in streams:
                        streams[pkt.tcp.stream]=[]
                    streams[pkt.tcp.stream].append(count)
                count += 1

            # Process dnp3 application data using scapy
            print("Identified %d TCP streams!\nIterating over s treams....."%(len(streams)))
            pcap = rdpcap(pcapFile)
            for i in streams:
                dataI = []
                dataO = []
                for pktno in streams[i]:
                    fcn_msg, pktType = get_dnp3_function_message(pcap[pktno])
                    if fcn_msg is not None:
                        if (pktType == 'req'):
                            input_al.add(fcn_msg)
                            dataI.append(fcn_msg)
                        elif (pktType == 'res'):
                            output_al.add(fcn_msg)
                            dataO.append(fcn_msg)

                if(len(dataI)==0 and len(dataO)==0):
                    continue
                if(len(dataI)==0):
                    dataI.append("MASTER_DIDNOT_REQUEST")
                    input_al.add("MASTER_DIDNOT_REQUEST")
                if(len(dataO)==0):
                    dataI.append("OUTSTATION_DIDNOT_RESPOND")
                    output_al.add("OUTSTATION_DIDNOT_RESPOND")
                # dataO.insert(0,tuple(dataI))
                trainingdata.append((tuple(dataI), dataO[-1]))
    print("Returned training data...")
    return trainingdata, list(input_al), output_al