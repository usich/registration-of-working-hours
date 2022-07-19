import time
import xml.etree.ElementTree as ET
import FDataBase
import main
from datetime import datetime, timedelta


def create_xml():
    db = main.connect_db()
    dbase = FDataBase.FDataBase(db)
    selection = dbase.get_record_not_unloaded()

    if len(selection) == 0:
        return False

    try:
        data = ET.Element("data")
        for i in selection:
            element = ET.SubElement(data, "element")
            ET.SubElement(element, "id").text = str(i['id'])
            ET.SubElement(element, "userCode").text = str(i['userCode'])
            ET.SubElement(element, "usbCode").text = str(i['usbCode'])
            ET.SubElement(element, "timeIn").text = str(i['timeIn'])
            ET.SubElement(element, "timeOut").text = str(i['timeOut'])
        tree = ET.ElementTree(data)
        tree.write(f"outxml/temp/{datetime.now().date() - timedelta(days=1)}#regUser.xml")
    except Exception as e:
        print(e)
        return False
    return True


def upload_xml_out():
    db = main.connect_db()
    dbase = FDataBase.FDataBase(db)
    if create_xml():
        dbase.enable_unloaded_check()
    else:
        print('upload_xml_out() == ', False)

