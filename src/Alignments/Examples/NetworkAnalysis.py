import Alignments.UserActivities.Plots as Plt
import Alignments.UserActivities.Clustering as Cls
import Alignments.Settings as St
from os import listdir
from Alignments.Utility import normalise_path as nrm
from os.path import join, isdir, isfile
import codecs


linkset_1 = "http://risis.eu/linkset/clustered_exactStrSim_N167245093"
linkset_2 = "http://risis.eu/linkset/clustered_exactStrSim_N1245679810818748702"
linkset_3 = "http://risis.eu/linkset/clustered_test"
resources_list = ["<http://risis.eu/orgref_20170703/resource/1389122>",
                  "<http://risis.eu/cordisH2020/resource/participant_993809912>",
                  "<http://www.grid.ac/institutes/grid.1034.6>"]

# print disambiguate_network(linkset_1, resources_list)
# Cls.cluster_d_test(linkset_4, network_size=3,  directory="C:\Users\Al\Videos\LinkMetric",
#                    greater_equal=True, limit=50000)

linkset = "http://risis.eu/linkset/clustered_exactStrSim_N1245679810818748702"
org = "http://risis.eu/orgreg_20170718/resource/organization"
uni = "http://risis.eu/orgreg_20170718/ontology/class/University"
ds = "http://risis.eu/dataset/orgreg_20170718"
# resources_matched(alignment=linkset, dataset=ds, resource_type=uni, matched=True)

# THE INITIAL DATASET IS grid_20170712
grid_GRAPH = "http://risis.eu/dataset/grid_20170712"
grid_org_type = "http://xmlns.com/foaf/0.1/Organization"
grid_cluster_PROPS = ["<http://www.grid.ac/ontology/hasAddress>/<http://www.grid.ac/ontology/countryCode>",
                      "<http://www.grid.ac/ontology/hasAddress>/<http://www.grid.ac/ontology/countryName>"]
grid_link_org_props = ["http://www.w3.org/2000/01/rdf-schema#label", "http://www.w3.org/2004/02/skos/core#prefLabel",
                       "http://www.w3.org/2004/02/skos/core#altLabel",
                       "http://xmlns.com/foaf/0.1/homepage",
                       "<http://www.grid.ac/ontology/hasAddress>/<http://www.w3.org/2003/01/geo/wgs84_pos#lat>",
                       "<http://www.grid.ac/ontology/hasAddress>/<http://www.w3.org/2003/01/geo/wgs84_pos#long>"]
grid_main_dict = {St.graph: grid_GRAPH,
                  St.data: [{St.entity_datatype: grid_org_type, St.properties: grid_link_org_props}]}

# [ETER] DATASET TO ADD
eter_GRAPH = "http://risis.eu/dataset/eter_2014"
eter_cluster_PROPS = ["http://risis.eu/eter_2014/ontology/predicate/Country_Code"]
eter_org_type = "http://risis.eu/eter_2014/ontology/class/University"
eter_link_org_props = ["http://risis.eu/eter_2014/ontology/predicate/Institution_Name",
                       "<http://risis.eu/eter_2014/ontology/predicate/English_Institution_Name>",
                       "http://risis.eu/eter_2014/ontology/predicate/Name_of_foreign_institution",
                       "http://risis.eu/eter_2014/ontology/predicate/Institutional_website",
                       "http://risis.eu/eter_2014/ontology/predicate/Geographic_coordinates__longitude",
                       "http://risis.eu/eter_2014/ontology/predicate/Geographic_coordinates__latitude"]
eter_main_dict = {St.graph: eter_GRAPH,
                  St.data: [{St.entity_datatype: eter_org_type, St.properties: eter_link_org_props}]}

# [ORGREG] DATASET TO ADD
orgreg_GRAPH = "http://risis.eu/dataset/orgreg_20170718"
orgreg_cluster_PROPS = ["<http://risis.eu/orgreg_20170718/ontology/predicate/locationOf>"
                        "/<http://risis.eu/orgreg_20170718/ontology/predicate/Country_of_location>",
                        "http://risis.eu/orgreg_20170718/ontology/predicate/Country_of_establishment"]
orgreg_org_type = "http://risis.eu/orgreg_20170718/resource/organization"
orgreg_link_org_props = ["http://risis.eu/orgreg_20170718/ontology/predicate/Name_of_entity",
                         "http://risis.eu/orgreg_20170718/ontology/predicate/English_name_of_entity",
                         "http://risis.eu/orgreg_20170718/ontology/predicate/Entity_current_name_English",
                         "http://risis.eu/orgreg_20170718/ontology/predicate/Website_of_entity",
                         "<http://risis.eu/orgreg_20170718/ontology/predicate/locationOf>"
                         "/<http://risis.eu/orgreg_20170718/ontology/predicate/Geographical_coordinates__latitude>",
                         "<http://risis.eu/orgreg_20170718/ontology/predicate/locationOf>"
                         "/<http://risis.eu/orgreg_20170718/ontology/predicate/Geographical_coordinates__longitude>"]

orgreg_main_dict = {St.graph: orgreg_GRAPH,
                    St.data: [{St.entity_datatype: orgreg_org_type, St.properties: orgreg_link_org_props}]}

targets = [
    grid_main_dict,
    orgreg_main_dict,
    eter_main_dict
]


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    COMPUTING AN ALIGNMENT STATISTICS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# OUTPUT FALSE RETURNS THE MATRIX WHILE OUTPUT TRUE RETURNS THE DISPLAY MATRIX IN A TABLE FORMAT
stats = Cls.resource_stat(alignment=linkset, dataset=ds, resource_type=org, output=True, activated=False)
# for stat in stats:
#     for key, value in stat.items():
#         print "{:21} : {}".format(key, value)

# Cls.disambiguate_network_2(["<http://www.grid.ac/institutes/grid.474119.e>",
#                             "<http://risis.eu/orgreg_20170718/resource/HR1016>",
#                             "<http://www.grid.ac/institutes/grid.4808.4>"], targets, output=True)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    PLOT THE LINK NETWORK
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
size = 7
ls_4 = "http://risis.eu/lens/union_Grid_20170712_Eter_2014_Orgreg_20170718_N1655042445"
ls_5 = "http://risis.eu/lens/union_Eter_2014_Orgreg_20170718_Grid_20170712_N2030153069"
ls_1k = "http://risis.eu/lens/union_Eter_2014_Orgreg_20170718_Grid_20170712_P1640316176"
directory = "C:\Users\Al\Videos\LinkMetric"

# for i in range(3, 50):
#
#     size = i
#
#     Plt.cluster_d_test(ls_4, network_size=size,  targets=targets,
#                        directory=directory, greater_equal=False, limit=70000, activated=True)
#
#     Plt.cluster_d_test(ls_5, network_size=size,  targets=targets,
#                        directory=directory, greater_equal=False, limit=70000, activated=True)
#
#     Plt.cluster_d_test(ls_1k, network_size=size,  targets=targets,
#                        directory=directory, greater_equal=False, limit=70000, activated=True)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    ANALYSING THE LINKED NETWORK FILES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# t50 = "C:\Users\Al\Videos\LinkMetric\7_Analysis_20171215\union_Eter_2014_Orgreg_20170718_Grid_20170712_N2030153069"
# t100 = "C:\Users\Al\Videos\LinkMetric\7_Analysis_20171215\union_Grid_20170712_Eter_2014_Orgreg_20170718_N1655042445"
# t1000 = "C:\Users\Al\Videos\LinkMetric\7_Analysis_20171215\union_Eter_2014_Orgreg_20170718_Grid_20170712_P1640316176"
t50 = "C:\Users\Al\Videos\LinkMetric\\3_Analysis_20171225\union_Eter_2014_Orgreg_20170718_Grid_20170712_N2030153069"
t100 = "C:\Users\Al\Videos\LinkMetric\\3_Analysis_20171225\union_Grid_20170712_Eter_2014_Orgreg_20170718_N1655042445"
t1000 = "C:\Users\Al\Videos\LinkMetric\\3_Analysis_20171225\union_Eter_2014_Orgreg_20170718_Grid_20170712_P1640316176"


def folder_check(file_1, file_2):

    folders_1 = [f for f in listdir(nrm(file_1)) if isdir(join(nrm(file_1), f))]
    folders_2 = [f for f in listdir(nrm(file_2)) if isdir(join(nrm(file_2), f))]
    print "\nPATH 1: {}".format(len(folders_1))
    print "PATH : {}".format(len(folders_2))
    set_1 = set(folders_1)
    set_2 = set(folders_2)

    diff = set_1 - set_2
    print "\nDIFF(FOLDER_1 [{}] - FOLDER_2 [{}]) [{}]".format( len(folders_1) -1,  len(folders_2) -1, len(diff))
    for item in diff:
        print "\t{}".format(item)

    # diff = set_2 - set_1
    # print "\nDIFF(FOLDER_2 - FOLDER_1) [{}]".format(len(diff))
    # for item in diff:
    #     print "\t{}".format(item)
    #
    # diff = set_1.intersection(set_2)
    # print "\nINTERSECTION(FOLDER_1 - FOLDER_2) [{}]".format(len(diff))
    # for item in diff:
    #     print "\t{}".format(item)
    # print len(diff)



import io
directory = "C:\Users\Al\Videos\LinkMetric"

# wr = codecs.open("C:\Users\Al\Videos\LinkMetric\\"
#                  "7_Analysis_20171220\union_Eter_2014_Orgreg_20170718_Grid_20170712_N2030153069\\"
#                  "7_N2141339763\cluster_N2141339763_20171220.txt", "rb")
# text = wr.read()
# print text.__contains__("<http://www.grid.ac/institutes/grid.457417.4>")
# wr.close()
# print "DOE!"

# main folder
#   Sub-Folders
#       target folders
#           Target file
#               Comparison

def track(directory, resource):
    print "\nMAIN DIRECTORY {}".format(directory)
    # LOOK FOR MAIN FOLDERS IN MAIN DIRECTORY
    main_folders = [f for f in listdir(nrm(directory)) if isdir(join(nrm(directory), f))]

    # GO THROUGH EACH MAIN FOLDER
    for main_folder in main_folders:
        main_path = join(directory, main_folder)
        # print "\tMAIN-FOLDER: {}".format(main_folder)
        # FOREACH MAIN FOLDER GAT THE SUB-FOLDER
        sub_folders = [f for f in listdir(nrm(main_path)) if isdir(join(nrm(main_path), f))]

        for sub_folder in sub_folders:
            sub_path = join(main_path, sub_folder)
            # print "\t\tSUB-FOLDER: {}".format(sub_folder)

            # TARGET FOLDERS
            target_folder = [f for f in listdir(nrm(sub_path)) if isdir(join(nrm(sub_path), f))]
            for target in target_folder:
                i_folder = "{}".format(join(main_path, sub_path, target))
                # print "\t\t\tTARGET-FOLDER: {}".format(target)
                i_file = [f for f in listdir(nrm(i_folder)) if isfile(join(nrm(i_folder), f))]


                for target_file in i_file:
                    if target_file.lower().endswith(".txt"):
                        target_path = join(main_path, sub_path, target, target_file)
                        wr = codecs.open(target_path, "rb")
                        text = wr.read()
                        wr.close()

                        result = text.__contains__(resource)
                        if result is True:
                            print "\n\tMAIN-FOLDER: {}".format(main_folder)
                            print "\t\tSUB-FOLDER: {}".format(sub_folder)
                            print "\t\t\tTARGET-FOLDER: {}".format(target)
                            print "\t\t\t\tTARGET FILE: {}".format(target_file)
                            print "\tPATH: {}".format(join(main_path, sub_path, target))
                            print "\t\t\t\t{}".format(result)



track_3 = "<http://risis.eu/eter_2014/resource/HU0023>"
track_5 = "<http://www.grid.ac/institutes/grid.469502.c>"
# track(directory, "<http://risis.eu/eter_2014/resource/FR0088>")
# track(directory, "<http://www.grid.ac/institutes/grid.452199.2>")

folder_check(t50, t100)
folder_check(t50, t1000)
track(directory, track_3)
print "DONE!!!"