# -*- coding: utf-8 -*-
# coding=utf-8

from Alignments.ToRDF.RDF import *
from Alignments.Utility import win_bat as bat
from kitchen.text.converters import to_bytes, to_unicode


__name__ = """CSV"""
entity_type_prefix = u"entity"


class CSV(RDF):

    def no_id(self, database, is_trig, file_to_convert, separator, entity_type, rdftype):

        database = database.replace(" ", "_")

        """
            param database: name of the dataset
            param is_trig: A boolean value indicating the format of the RDF file that will be generated.
            param file_to_convert: Represents the oath of the CSV file that that is to be converted.
            param separator: A character specifying the character used for value separation.
            param entity_type: The name of the entity type starting by a capital character.

            Note: This conversion uses the number of the row as subject identifier. This is used when it
            is hard to isolate an entity withing the csv file or no column qualifies as identifier.
        """

        bom = ''
        _file = ""
        print
        self.errorCount = 0
        self.rdftype = rdftype
        self.inputPath = file_to_convert  # -> string   The out file path
        self.pvFormat = u""  # -> string   Representing RDF triple format to use for formatting Predicate_Value
        self.risisOntNeutral = "riClass:Neutral"  # Prefix for Neutrality
        self.lastColumn = 0  # -> int      The last attribute index
        self.longestHeader = 0  # -> int      The number of characters in the longest attribute
        self.data_prefix = entity_type.lower().replace(' ', '_')
        '''Replace unwanted characters -> #;:.-(–)—[']`=’/”{“}^@*+!~\,%'''
        self.pattern = '[?&#;:%!~+`=’*.(\-)–\\—@\['',\\]`{^}“/”]'

        try:
            # Open the file to convert
            # _file = codecs.open(self.inputPath, 'rb', encoding="utf-8")
            _file = open(self.inputPath, 'rb')

        except Exception as exception:
            print "\n", exception
            exit(1)

        """ About BYTE ORDER MARK (BOM) """
        self.first_line = to_bytes(_file.readline())
        if self.first_line.startswith(to_bytes(codecs.BOM_UTF8)):
            for i in range(len(to_bytes(codecs.BOM_UTF8))):
                bom += self.first_line[i]
            self.first_line = self.first_line.replace(bom, '')
            print u"[" + os.path.basename(self.inputPath) + u"]", u"contains BOM."

        # get the first line
        self.first_line = self.first_line.strip(u'\r\n')
        print "\n\tThis is the header: ", self.first_line

        # Get the attribute headers
        # -> Array  about the list of attributes in the csv file
        self.csvHeader = self.extractor(self.first_line, separator)
        self.csvHeaderLabel = self.extractor(self.first_line, separator)

        """ 2. Get the last column ID. This allows to stop the loop before the end
                whenever the identification column happens to be the last column"""
        self.lastColumn = len(self.csvHeader) - 1
        # This is no longer the case because we now keep the column used as reference
        # if self.subjectID == self.lastColumn:
        #     self.lastColumn -= 1

        """ 3. Get the attribute headers and make them URI ready"""
        for i in range(0, len(self.csvHeader)):

            # '''Replace unwanted characters -> #;:.-(–)—[']`=’/”{“}^@*+!~\,%'''
            # pattern = '[?&#;:%!~+`=’*.(\-)–\\—@\['',\\]`{^}“/”]'
            self.csvHeader[i] = self.csvHeader[i].replace(' ', '_')
            self.csvHeader[i] = re.sub(self.pattern, u"", self.csvHeader[i].replace('&', "_and_"))

            '''For every attribute composed of more than 1 word and separated by space,
            start the first word with lower case followed by the underscore character'''

            # print self.csvHeader
            new_header = ""
            header_split = self.csvHeader[i].split()
            if header_split is not None and len(header_split) > 0:
                new_header = header_split[0].lower()

            for j in range(1, len(header_split)):
                new_header += u"_" + header_split[j]
                self.csvHeader[i] = new_header
            # print header_split

            '''Get the size (number of characters) of the longest attribute'''
            if self.longestHeader < len(self.csvHeader[i]):
                self.longestHeader = len(self.csvHeader[i])

        """ 4. Set the RDF triple formatter """
        sub_position = 6
        # vocab: takes 6 slots
        pre_position = sub_position + self.longestHeader
        self.pvFormat = u"{0:>" + u"{0}".format(
            str(sub_position)) + u"} {1:" + u"{0}".format(str(pre_position)) + u"} {2}"

        schema = self.get_schema(entity_type=entity_type, field_metadata=self.fieldMetadata)
        # print schema
        RDF.__init__(self, input_path=self.inputPath, database=database, entity_type=entity_type,
                     is_trig=is_trig, namespace=self.get_namespace(database), schema=schema)

        n = 0
        """ Opening the named-graph """
        self.open_trig(dataset_prefix)

        """ Writing the rdf instances of the dataset """
        while True:

            n += 1
            line = to_unicode(_file.readline(), "utf-8")

            if not line:

                """ Closing the named-graph by closing the turtle writer """
                if self.isClosed is not True:
                    self.close_writer()

                print '\nNo more line... Process ended at line > ' + str(n)
                print 'Done with converting [' + file_to_convert + '] to RDF!!!'
                _file.close()

                # WRITE THE BAT FILE
                print self.dirName
                self.bat_file = bat(self.dirName, self.database)
                break

            # if n <= 5:
            #     # print line
            #     pass
            # if n == 6:
            #     self.turtleWriter.close()
            #     break

            """ Proceed with the conversion """
            self.write_triples_2(to_unicode(line), separator, row_number=n, field_metadata=self.fieldMetadata)

    def __init__(self, database, is_trig, file_to_convert, separator, entity_type,
                 rdftype=None, subject_id=None, field_metadata=None):
        print rdftype
        print subject_id
        """
            param database: name of the dataset
            param is_trig: A boolean value indicating the format of the RDF file that will be generated.
            param file_to_convert: Represents the oath of the CSV file that that is to be converted.
            param separator: A character specifying the character used for value separation.
            param subject_id: The index of the column identified to be used as the subject in the RDF file.
            param entity_type: The name of the entity type starting by a capital character.
        """
        self.fieldMetadata = field_metadata
        if subject_id is None:
            self.no_id(database, is_trig, file_to_convert, separator, entity_type, rdftype)
            return

        bom = ''
        _file = ""

        self.errorCount = 0
        self.rdftype = rdftype
        self.subjectID = subject_id         # -> int      The index of the attribute to use as identification
        self.inputPath = file_to_convert    # -> string   The out file path
        self.pvFormat = u""  # -> string   Representing RDF triple format to use for formatting Predicate_Value
        self.risisOntNeutral = "riClass:Neutral"  # Prefix for Neutrality
        self.lastColumn = 0  # -> int      The last attribute index
        self.longestHeader = 0  # -> int      The number of characters in the longest attribute
        self.data_prefix = entity_type.lower().replace(' ', '_')

        '''Replace unwanted characters -> #;:.-(–)—[']`=’/”{“}^@*+!~\,%'''
        self.pattern = '[?&#;:%!~+`=’*.(\-)–\\—@\['',\\]`{^}“/”]'

        try:
            # Open the file to convert
            # _file = codecs.open(self.inputPath, 'rb', encoding="utf-8")
            _file = open(self.inputPath, 'rb')

        except Exception as exception:
            print "\n", exception
            exit(1)

        """ About BYTE ORDER MARK (BOM) """
        self.first_line = _file.readline().strip()
        if self.first_line.startswith(to_bytes(codecs.BOM_UTF8)):
            for i in range(len(to_bytes(codecs.BOM_UTF8))):
                bom += self.first_line[i]
            self.first_line = self.first_line.replace(bom, '')
            print u"[" + os.path.basename(self.inputPath) + u"]", u"contains BOM."

        # get the first line
        # self.first_line = self.first_line.strip(u'\r\n')
        print "\n\tThis is the header: ", self.first_line

        # Get the attribute headers
        # -> Array  about the list of attributes in the csv file
        self.csvHeader = self.extractor(self.first_line, separator)
        self.csvHeaderLabel = self.extractor(self.first_line, separator)

        """ 2. Get the last column ID. This allows to stop the loop before the end
                whenever the identification column happens to be the last column"""
        self.lastColumn = len(self.csvHeader) - 1
        # This is no longer the case because we now keep the column used as reference
        # if self.subjectID == self.lastColumn:
        #     self.lastColumn -= 1

        """ 3. Get the attribute headers and make them URI ready"""
        for i in range(0, len(self.csvHeader)):

            self.csvHeader[i] = self.csvHeader[i].replace(' ', '_')
            self.csvHeader[i] = re.sub(self.pattern, u"", self.csvHeader[i].replace('&', "_and_"))

            '''For every attribute composed of more than 1 word and separated by space,
            stat the first word with lower case followed by the underscore character'''

            # print self.csvHeader
            new_header = ""
            header_split = self.csvHeader[i].split()
            if header_split is not None and len(header_split) > 0:
                new_header = header_split[0].lower()
            for j in range(1, len(header_split)):
                new_header += u"_" + header_split[j]
                self.csvHeader[i] = new_header
            # print header_split

            '''Get the size (number of characters) of the longest attribute'''
            if self.longestHeader < len(self.csvHeader[i]):
                self.longestHeader = len(self.csvHeader[i])

        """ 4. Set the RDF triple formatter """
        sub_position = 6
        # vocab: takes 6 slots
        pre_position = sub_position + self.longestHeader
        self.pvFormat = u"{0:>" + u"{0}".format(
            str(sub_position)) + u"} {1:" + u"{0}".format(str(pre_position)) + u"} {2}"

        schema = self.get_schema(entity_type=entity_type, field_metadata=self.fieldMetadata)
        # print schema
        RDF.__init__(self, input_path=self.inputPath, database=database, entity_type=entity_type,
                     is_trig=is_trig, namespace=self.get_namespace(database), schema=schema)

        n = 0
        """ Opening the named-graph
        """
        self.open_trig(dataset_prefix)

        """ Writing the rdf instances of the dataset
        """
        while True:
            n += 1
            line = to_unicode(_file.readline())

            if not line:

                # WRITE THE BAT FILE
                print self.dirName
                self.bat_file = bat(self.dirName, self.database)

                """ Closing the named-graph by closing the turtle writer.
                    CAN POSSIBLY THROUGH AND EXCEPTION BY RDFLIB AFTER CHECKING THE FILE
                """
                if self.isClosed is not True:
                    self.close_writer()

                print '\nNo more line... Process ended at line > ' + str(n)
                print 'Done with converting [' + file_to_convert + '] to RDF!!!'
                _file.close()

                break

            # if n <= 5:
            #     # print line
            #     pass
            # if n == 6:
            #     self.turtleWriter.close()
            #     break

            """ Proceed with the conversion """
            self.write_triples(to_unicode(line), separator, self.fieldMetadata)

    @staticmethod
    def extractor(record, separator):
        td = '"'
        attributes = []
        temp = ""

        # print record
        i = 0
        while i < len(record):

            if record[i] == td:
                j = i + 1
                while j < len(record):
                    if record[j] != td:
                        temp += record[j]
                    elif j + 1 < len(record) and record[j + 1] != separator:
                        if record[j] != td:
                            temp += record[j]
                    elif j + 1 < len(record) and record[j + 1] == separator:
                        j += 2
                        break
                    j += 1

                attributes.append(temp)
                temp = ""
                i = j

            else:
                while i < len(record):

                    # Enqueue if you encounter the separator
                    if record[i] == separator:
                        attributes.append(temp)
                        # print "> separator " + temp
                        temp = ""

                    # Append if the current character is not a separator
                    if record[i] != separator:
                        temp += record[i]
                        # print "> temp " + temp

                    # Not an interesting case. Just get oit :-)
                    else:
                        i += 1
                        break

                    # Increment the iterator
                    i += 1

        # Append the last attribute
        if temp != "":
            attributes.append(temp)

        # print "EXTRACTOR RETURNED: {}".format(attributes)
        return attributes

    @staticmethod
    def get_namespace(database):
        """ This function outputs the static hardcoded namespace required for the OrgRef dataset """
        name_space = cStringIO.StringIO()
        name_space.write("\t### Name Space #########################################################################\n")
        name_space.write("\t@base <http://risis.eu/> .\n")
        name_space.write("\t@prefix dataset: <dataset/> .\n")
        name_space.write("\t@prefix schema: <ontology/> .\n")
        name_space.write("\t@prefix entity: <{0}/ontology/class/> .\n".format(database))
        name_space.write("\t@prefix vocab: <{0}/ontology/predicate/> .\n".format(database))
        name_space.write("\t@prefix data: <{0}/resource/> .\n".format(database))

        name_space.write("\t@prefix riClass: <risis/ontology/class/> .\n")

        name_space.write("\t@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
        name_space.write("\t@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
        name_space.write("\t@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")
        name_space.write("\t@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")
        name_space.write("\t########################################################################################\n")
        content = name_space.getvalue()
        name_space.close()
        return content

    @staticmethod
    def view_file(file_path, size=10):
        bom = ''
        # _file = ""
        # first_line = ""
        # text = ""
        bldr = cStringIO.StringIO()
        try:
            # Open the file to convert
            # _file = codecs.open(self.inputPath, 'rb', encoding="utf-8")
            _file = open(file_path, 'rb')

        except Exception as exception:
            # print "\n", exception
            message = "NO DATASET FILE UPLOADED\n\n\n\n\n\n\t\t" + str(exception)
            return {"header": "NO DATASET FILE UPLOADED",  "sample": message}

        """ About BYTE ORDER MARK (BOM) """
        first_line = to_bytes(_file.readline())

        if first_line.startswith(to_bytes(codecs.BOM_UTF8)):
            for i in range(len(to_bytes(codecs.BOM_UTF8))):
                bom += first_line[i]
            first_line = first_line.replace(bom, '')
            print u"[" + os.path.basename(file_path) + u"]", u"contains BOM."

        # get the first line
        first_line = first_line.strip(u'\r\n')
        bldr.write(first_line + "\n")

        for i in range(0, size):
            bldr.write(_file.readline())
        text = bldr.getvalue()
        bldr.close()
        _file.close()

        # print text
        return {"header": first_line, "sample": text}

    @staticmethod
    def view_data(file_path, limit=1000):
        # file = ""
        # sample = ""
        builder = cStringIO.StringIO()
        _file = open(file_path, 'rb')
        for i in range(0, limit):
            builder.write(_file.readline())
        builder.write("\n...")
        sample = builder.getvalue()
        _file.close()
        builder.close()
        return sample

    def view_converted_data(self, limit=1000):
        # file = ""
        # sample = ""
        builder = cStringIO.StringIO()
        _file = open(self.outputPath, 'rb')
        for i in range(0, limit):
            builder.write(_file.readline())
        builder.write("\n...")
        sample = builder.getvalue()
        _file.close()
        builder.close()
        return sample

    def view_converted_schema(self, limit=1000):
        # file = ""
        # sample = ""
        builder = cStringIO.StringIO()
        _file = open(self.outputMetaPath, 'rb')
        for i in range(0, limit):
            builder.write(_file.readline())
        builder.write("\n...")
        sample = builder.getvalue()
        _file.close()
        builder.close()
        return sample

    def write_record_values(self, record, field_metadata=None):
        """ This function takes as an argument a csv record as
        an array witch represents a csv line in the dataset """

        array_sep = None
        if field_metadata is not None:
            array_sep = field_metadata["array_sep"]

        if len(record) != len(self.csvHeader):
            return ""

        # ITERATE THROUGH THE HEADER
        for i in range(0, len(self.csvHeader)):

            # GETTING PROPERTY VALUES
            cur_value = record[i].strip()
            # print str(i) + " " + self.csvHeader[i] + "\t" + cur_value

            # GETTING THE SEPARATOR FOR THAT HEADER
            curr_sep = None
            if array_sep is not None:
                curr_sep = array_sep[i]

            # SPLITTING THE RECORD USING curr_sep
            # IN CASE THE VALUE HAS A SPECIFIC FORMAT
            if curr_sep is not None and len(curr_sep) > 0:
                values = cur_value.split(curr_sep)

                for value in values:
                    if self.rdftype is None or i not in self.rdftype:
                        # print "NOT WORKING IN MORE"
                        self.write_predicate_value(i, value)
                    elif i in self.rdftype:
                        # print "WORKING IN MORE"
                        self.write_rdftype_value(i, value)

            else:
                if self.rdftype is None or i not in self.rdftype:
                    # print "NOT WORKING " + str(self.rdftype)
                    self.write_predicate_value(i, cur_value)
                elif i in self.rdftype:
                    # print "WORKING"
                    self.write_rdftype_value(i, cur_value)

    def get_schema(self, entity_type, field_metadata=None):
        """ This function gets the set of attribute header as the NEUTRAL implicit Orgref RDF schema """
        schema = cStringIO.StringIO()
        schema.write('\n')

        schema.write("\t### Classes #####################################################\n")
        schema.write("\t#################################################################\n\n")

        if entity_type is not None and entity_type != "":
            schema.write("\t### [  ]\n")
            schema.write(u"\t{0}:{1}\n".format(entity_type_prefix, entity_type))
            schema.write(self.pvFormat.format("", 'rdf:type', "rdfs:Class, owl:Class ;\n"))
            schema.write(self.pvFormat.format(b"", b"rdfs:label", self.triple_value(entity_type) + u" .\n"))

        schema.write("\n\n\t### Properties ##################################################\n")
        schema.write("\t#################################################################\n\n")

        # """Create the named graph"""
        # if is_trig is True:
        #     schema.write("### [ About the schema of " + str(database) + " ]\n")
        #     schema.write(schema_prefix + database.strip().replace(" ", "_") + "\n")
        #     schema.write(u"{\n")

        description = None
        if field_metadata is not None:
            description = field_metadata["description"]

        curr_description = None
        for i in range(0, len(self.csvHeader)):
            if description is not None:
                curr_description = description[i]

            schema.write(b"\t### [ " +
                         str(i + 1) + b" ] About the attribute: \"" + to_bytes(self.csvHeader[i]) + b"\" \n")
            schema.write(b"\t" +
                         to_bytes(vocabulary_prefix) + to_bytes(self.csvHeader[i]).strip().replace(b" ", b"_") + b"\n")
            schema.write(self.pvFormat.format(b"", b"rdf:type", self.risisOntNeutral + u" ,\n"))
            schema.write(self.pvFormat.format(b"", b"", b"rdf:Property" + u" ;\n"))

            # WRITING GIVEN COMMENT
            if curr_description is not None and len(curr_description) > 0:
                schema.write(
                    self.pvFormat.format(b"", b"rdfs:comment", self.triple_value(curr_description) + u" ;\n"))

            # WRITING GIVEN COMMENT
            if self.rdftype is not None and i in self.rdftype:
                schema.write(
                    self.pvFormat.format(b"", b"rdfs:comment", self.triple_value(
                        "This property was not used to describe the data as it has "
                        "been redefined as an RDF property ") + u" ;\n"))

            schema.write(self.pvFormat.format(b"", b"rdfs:label", self.triple_value(self.csvHeaderLabel[i]) + u" .\n"))
            if i != len(self.csvHeader) - 1:
                schema.write(b"\n")

        # """Close the named graph"""
        # if is_trig is True:
        #     schema.write("}\n")

        return schema.getvalue()

    def write_triples(self, line, separator, field_metadata=None):

        # print line

        # Replace unwanted characters -> \r\n
        # line = line.rstrip(u'\r\n')
        record = self.extractor(line, separator)

        if len(record) != len(self.csvHeader):
            self.errorCount += 1
            print "{:5} Record encoding error. Header: {} columns while Record: {} columns".format(
                self.errorCount, len(self.csvHeader), len(record))
            print "\t\t{:8}".format(record)
            return ""

        size = len(record) - 1
        record[size] = record[size].rstrip(u'\r\n')
        # print str(record[size]).__contains__(u'\r\n')
        # print record
        subject_resource = record[self.subjectID].strip()

        if subject_resource is not None:
            subject_resource = subject_resource.strip()

        if subject_resource != "":
            self.refreshCount += 1
        if self.refreshCount > self.fileSplitSize:
            self.refreshCount = 0
            self.refresh()

        # Write the subject
        self.instanceCount += 1
        self.write_line("\t### [ " + str(self.instanceCount) + " ]")
        # self.write_line(u"\t{0}:".format(self.data_prefix) + subject_resource.replace(" ", "_"))
        self.write_line(u"\t{0}:".format(self.data_prefix) + self.check_for_uri(subject_resource))

        if self.entityType is not None and self.entityType != "":
            self.write_line(self.pvFormat.format("", 'rdf:type', u"{0}:{1} ;".format(
                entity_type_prefix, self.entityType)))

        # Write the values
        self.write_record_values(record, field_metadata)
        # print record

    def write_triples_2(self, line, separator, row_number, field_metadata=None):

        # print line
        # line = line.strip(b'\r\n')

        record = self.extractor(line, separator)
        size = len(record) - 1
        record[size] = record[size].rstrip(u'\r\n')
        # print str(record[size]).__contains__(u'\r\n')
        # print record
        subject_resource = "R{0}".format(row_number)

        if subject_resource is not None:
            subject_resource = subject_resource.strip()

        if subject_resource != "":
            self.refreshCount += 1
        if self.refreshCount > self.fileSplitSize:
            self.refreshCount = 0
            self.refresh()

        # Write the subject
        self.instanceCount += 1
        self.write_line("\t### [ " + str(self.instanceCount) + " ]")

        # self.write_line(u"\t{0}:".format(self.data_prefix) + subject_resource.strip().replace(" ", "_"))
        self.write_line(u"\t{0}:".format(self.data_prefix) + self.check_for_uri(subject_resource))

        if self.entityType is not None and self.entityType != "":
            self.write_line(self.pvFormat.format("", 'rdf:type', u"{0}:{1} ;".format(
                entity_type_prefix, self.entityType)))

        # Write the values
        self.write_record_values(record, field_metadata)
        # print record

    def write_predicate_value(self, index, value):

        val = value.strip()
        # The last column has a value so, end the triple with a dot
        if index == self.lastColumn and val != "":
            self.write_line(
                self.pvFormat.format(
                    "", vocabulary_prefix + self.csvHeader[index], self.triple_value(val)) + " .")
            self.write_line("")

        # The last column does not have a value => No triple but end of the subject.
        elif index == self.lastColumn and val == "":
            self.write_line("{0:>6}".format("."))
            self.write_line("")

        # Normal RDF business
        elif val != b"":
            # print("\n" + "[" + str(i) + "]" + self.csvHeader[i] + ": " + cur_value)
            self.write_line(self.pvFormat.format(u"", u"{0}{1}".format(
                vocabulary_prefix, self.csvHeader[index]), self.triple_value(val)) + u" ;")

    def write_rdftype_value(self, index, value):

        val = str(value.replace(' ', '_')).strip()
        val = re.sub(self.pattern, u"", val.replace('&', "_and_"))
        # The last column has a value so, end the triple with a dot
        if index == self.lastColumn and val != "":
            self.write_line(self.pvFormat.format(u"", u"rdf:type", u"{}:{}".format(self.data_prefix, val)) + u" .")
            self.write_line("")

        # The last column does not have a value => No triple but end of the subject.
        elif index == self.lastColumn and val == "":
            self.write_line("{0:>6}".format("."))
            self.write_line("")

        # Normal RDF business
        elif val != b"":
            # print("\n" + "[" + str(i) + "]" + self.csvHeader[i] + ": " + cur_value)
            self.write_line(
                self.pvFormat.format(u"", u"rdf:type", u"{}:{}".format(self.data_prefix, to_unicode(val))) + u" ;")

# print CSV.extractor("""\"Name","Country","State?","Level",
# "Wikipedia","Wikidata","VIAF","ISNI","GRID","Website","ID\"""", ",")

# CSV.view_file("C:\Users\Al\PycharmProjects\Linkset\Data_uploaded\orgref.csv")
