"""

from pygmlparser.Parser import Parser
from pygmlparser.Graph import Graph
from pygmlparser.Edge import Edge
from pygmlparser.Node import Node
from pygmlparser.graphics.NodeGraphics import NodeGraphics
from pygmlparser.graphics.EdgeGraphics import EdgeGraphics
from pygmlparser.graphics.Point import Point




# Instantiate a parser, load a file, and parse it!
parser = Parser()
parser.loadGML('./sh_statbel_statistical_sectors_noline1.gml')
parser.parse()

print(parser)
"""
"""
import xml.etree.ElementTree as ET

tree = ET.parse('./sh_statbel_statistical_sectors.gml')
root = tree.getroot()
print(root.tag)

for child in root:
    print(child.tag, child.attrib)
"""
import pandas as pd

file = open('./sh_statbel_statistical_sectors.gml')
f = file.read()
el = f.split('<gml:featureMember>')
el.pop(0)
bxl = []

for i in range(len(el)):
    print(i)
    if "Bruxelles" in el[i]:
        dat = el[i].split('<gml:coordinates>')
        if len(dat) == 2:
            data =el[i].split('<gml:coordinates>')[1]
        elif len(dat)==3:
            data =el[i].split('<gml:coordinates>')[2]
            
            #el.pop(i)
            #break
        data_1 = data.split('</gml:coordinates>')
        coord = data_1[0]
        data_2 = data_1[1].split('\n')
        if (data_2[0]=='</gml:LinearRing></gml:outerBoundaryIs></gml:Polygon></gml:polygonMember></gml:MultiPolygon></ogr:geometryProperty>') or ('</gml:LinearRing></gml:innerBoundaryIs></gml:Polygon></gml:polygonMember></gml:MultiPolygon></ogr:geometryProperty>' == data_2[0]):        
            data_2=data_2[1:]
            if '<ogr:TX_SECTOR_DESCR_NL>' in data_2[3]:
                data_2.pop(3)
                if '<ogr:TX_MUNTY_DESCR_NL>' in data_2[6]:
                    data_2.pop(6)
                    if '<ogr:TX_MUNTY_DESCR_DE>' in data_2[7]:
                        data_2.pop(7)
                        if '<ogr:TX_MUNTY_DESCR_EN>' in data_2[7]:
                            data_2.pop(7)
                            if '<ogr:TX_ADM_DSTR_DESCR_NL>' in data_2[8]:
                                data_2.pop(8)
                                if '<ogr:TX_ADM_DSTR_DESCR_DE>' in data_2[9]:
                                    data_2.pop(9)
                                    if '<ogr:TX_ADM_DSTR_DESCR_EN>' in data_2[9]:
                                        data_2.pop(9)
                                        if '<ogr:TX_PROV_DESCR_NL>' in data_2[10]:
                                            data_2.pop(10)
                                            if '<ogr:TX_PROV_DESCR_DE>' in data_2[11]:
                                                data_2.pop(11)
                                                if '<ogr:TX_PROV_DESCR_EN>' in data_2[11]:
                                                    data_2.pop(11)
                                                    if '<ogr:TX_RGN_DESCR_NL>' in data_2[12]:
                                                        data_2.pop(12)
                                                        if '<ogr:TX_RGN_DESCR_DE>' in data_2[13]:
                                                            data_2.pop(13)
                                                            if '<ogr:TX_RGN_DESCR_EN>' in data_2[13]:
                                                                data_2.pop(13)
                                                                if '</ogr:sh_statbel_statistical_sectors>' in data_2[16]:
                                                                    data_2.pop(16)
                                                                    if '</gml:featureMember>' in data_2[16]:
                                                                        data_2.pop(16)
                                                                        if '  ' == data_2[16]:
                                                                            data_2.pop(16)
                                                                        elif '</ogr:FeatureCollection>' in data_2[16]:
                                                                            data_2.pop(16)
                                                                            if '' == data_2[16]:
                                                                                data_2.pop(16)
                                        elif '<ogr:TX_RGN_DESCR_NL>' in data_2[10]:
                                            data_2.pop(10)
                                            if '<ogr:TX_RGN_DESCR_DE>' in data_2[11]:
                                                data_2.pop(11)
                                                if '<ogr:TX_RGN_DESCR_EN>' in data_2[11]:
                                                    data_2.pop(11)
                                                    if '</ogr:sh_statbel_statistical_sectors>' in data_2[14]:
                                                        data_2.pop(14)
                                                        if '</gml:featureMember>' in data_2[14]:
                                                            data_2.pop(14)
                                                            if '  ' == data_2[14]:
                                                                data_2.pop(14)
    
        #el[i]=[coord, data_2]
        bxl.append([coord, data_2])
        #data_2 = data_1[1].split('<ogr:PKUID>')
   

for i in range(len(el)):
    if len(el[i][1])!=16 and len(el[i][1])!=14:
        print(i)

"""
if len(data_2) == 1:
    #print(i)
    el[i]=[coord, data_2]
else :
    data_3 = data_2[1].split('<ogr:OBJECTID>')
    el[i]=[coord, data_3]
#info =el[i][1].split('<ogr:PKUID>')
#el[i][1]=info[1]
#el[i][1]=[1]
"""

print(bxl[0])
print("he")

bruxelles = pd.DataFrame(columns=['Coord', 'PKUID', 'OBJECTID', 'CD_SECTOR', 'TX_SECTOR_DESCR_FR', 'CD_SUB_MUNTY', 
                                  'CD_MUNTY_REFNIS', 'TX_MUNTY_DESCR_FR', 'CD_DSTR_REFNIS', 'TX_ADM_DSTR_DESCR_FR', 
                                  'CD_RGN_REFNIS', 'TX_RGN_DESCR_FR', 'CD_NUTS1', 'CD_NUTS2', 'CD_NUTS3'])
mvs =[]
for j in range(len(bxl)):
    if len(bxl[j][1])!=14:
        mvs.append(bxl[j])
        print(bxl[j][1], "error")
        #break
    else :
        bruxelles.loc[j]=[bxl[j][0]]+bxl[j][1]
    #coord = zone[0]
    
    """
    pkuid = zone[1][0]
    'PKUID', 'OBJECTID', 'CD_SECTOR', 'TX_SECTOR_DESCR_FR', 'CD_SUB_MUNTY', 
                                  'CD_MUNTY_REFNIS', 'TX_MUNTY_DESCR_FR', 'CD_DSTR_REFNIS', 'TX_ADM_DSTR_DESCR_FR', 
                                  'CD_RGN_REFNIS', 'TX_RGN_DESCR_FR', 'CD_NUTS1', 'CD_NUTS2', 'CD_NUTS3'])
    """
bruxelles['PKUID'] = bruxelles['PKUID'].map(lambda x: str(x)[17:-12])
bruxelles['OBJECTID'] = bruxelles['OBJECTID'].map(lambda x: str(x)[20:-15])
bruxelles['CD_SECTOR'] = bruxelles['CD_SECTOR'].map(lambda x: str(x)[21:-16])
bruxelles['TX_SECTOR_DESCR_FR'] = bruxelles['TX_SECTOR_DESCR_FR'].map(lambda x: str(x)[30:-25])
bruxelles['CD_SUB_MUNTY'] = bruxelles['CD_SUB_MUNTY'].map(lambda x: str(x)[24:-19])
bruxelles['CD_MUNTY_REFNIS'] = bruxelles['CD_MUNTY_REFNIS'].map(lambda x: str(x)[27:-22])
bruxelles['TX_MUNTY_DESCR_FR'] = bruxelles['TX_MUNTY_DESCR_FR'].map(lambda x: str(x)[29:-24])
bruxelles['CD_DSTR_REFNIS'] = bruxelles['CD_DSTR_REFNIS'].map(lambda x: str(x)[26:-21])
bruxelles['TX_ADM_DSTR_DESCR_FR'] = bruxelles['TX_ADM_DSTR_DESCR_FR'].map(lambda x: str(x)[32:-27])
bruxelles['CD_RGN_REFNIS'] = bruxelles['CD_RGN_REFNIS'].map(lambda x: str(x)[25:-20])
bruxelles['TX_RGN_DESCR_FR'] = bruxelles['TX_RGN_DESCR_FR'].map(lambda x: str(x)[27:-22])
bruxelles['CD_NUTS1'] = bruxelles['CD_NUTS1'].map(lambda x: str(x)[20:-15])
bruxelles['CD_NUTS2'] = bruxelles['CD_NUTS2'].map(lambda x: str(x)[20:-15])
bruxelles['CD_NUTS3'] = bruxelles['CD_NUTS3'].map(lambda x: str(x)[20:-15])
#print(bruxelles.TX_RGN_DESCR_FR)


bruxelles.to_csv("bruxelles_parsed.csv")