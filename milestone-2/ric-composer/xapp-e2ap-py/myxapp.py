#
#                  Politecnico di Milano
#
#         Student: Caravano Andrea
#            A.Y.: 2023/2024
#
#   Last modified: 05/09/2024
#
#     Description: Mobile Radio Networks/Wireless Networks: OpenRAN Project (Milestone 2)
#

import src.e2ap_xapp as e2ap_xapp
#from ran_messages_pb2 import *
from time import sleep
from ricxappframe.e2ap.asn1 import IndicationMsg

import sys
sys.path.append("oai-oran-protolib/builds/")
from ran_messages_pb2 import *

# for the CSV file and timestamp
import csv
import time




def xappLogic():

    # instanciate xapp
    connector = e2ap_xapp.e2apXapp()

    # get gnbs connected to RIC
    gnb_id_list = connector.get_gnb_id_list()
    print("{} gNB connected to RIC, listing:".format(len(gnb_id_list)))
    for gnb_id in gnb_id_list:
        print(gnb_id)
    print("---------")

    if (len(gnb_id_list) >= 1):
        gnb = gnb_id_list[0]
        report_request_buffer = e2sm_report_request_buffer()
    else:
        return

    # read loop
    sleep_time = 0.5

    with open('mrn-project.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        while True:
            print("Sending report request")
            connector.send_e2ap_control_request(report_request_buffer,gnb)
            print("Sleeping {}s...".format(sleep_time))
            sleep(sleep_time)
            messgs = connector.get_queued_rx_message()
            if len(messgs) == 0:
                print("no messages received")
                print("____")
            else:
                print("{} messages received while waiting, printing:".format(len(messgs)))
                for msg in messgs:
                    if msg["message type"] == connector.RIC_IND_RMR_ID:
                        print("RIC Indication received from gNB {}, decoding E2SM payload".format(msg["meid"]))
                        indm = IndicationMsg()
                        indm.decode(msg["payload"])
                        resp = RAN_indication_response()
                        resp.ParseFromString(indm.indication_message)
                        print(resp)
                        print("___")
                        print("Saving the response with its timestamp...")
                        ts = time.time()
                        writer.writerow([ts, resp])
                        print("___")
                    else:
                        print("Unrecognized E2AP message received from gNB {}".format(msg["meid"]))

def e2sm_report_request_buffer():
    master_mess = RAN_message()
    master_mess.msg_type = RAN_message_type.INDICATION_REQUEST
    inner_mess = RAN_indication_request()
    inner_mess.target_params.extend([RAN_parameter.GNB_ID, RAN_parameter.UE_LIST, RAN_parameter.CELL_LOAD])
    master_mess.ran_indication_request.CopyFrom(inner_mess)
    buf = master_mess.SerializeToString()
    return buf

if __name__ == "__main__":
    xappLogic()
