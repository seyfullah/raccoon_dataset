import shutil
import os
import tempfile
import unittest
import xml_to_csv
from xml.etree import ElementTree as ET


class XMLToCSVTest(unittest.TestCase):
    def test_one_airplane_one_xml(self):
        xml_file_one = """
        <annotation verified="yes">
            <folder>images</folder>
            <filename>airplane1.png</filename>
            <path>airplane1.png</path>
            <source>
                <database>Unknown</database>
            </source>
            <size>
                <width>256</width>
                <height>256</height>
                <depth>3</depth>
            </size>
            <segmented>0</segmented>
            <object>
                <name>airplane</name>
                <pose>Unspecified</pose>
                <truncated>0</truncated>
                <difficult>0</difficult>
                <bndbox>
                    <xmin>96</xmin>
                    <ymin>96</ymin>
                    <xmax>128</xmax>
                    <ymax>128</ymax>
                </bndbox>
            </object>
        </annotation>
        """

        xml = ET.fromstring(xml_file_one)
        with tempfile.TemporaryDirectory() as tmpdirname:
            tree = ET.ElementTree(xml)
            tree.write(tmpdirname + '/test_airplane_one.xml')
            airplane_df = xml_to_csv.xml_to_csv(tmpdirname)
            self.assertEqual(airplane_df.columns.values.tolist(),
                             ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])
            self.assertEqual(airplane_df.values.tolist()[0], ['airplane1.png', 256, 256, 'airplane', 96, 96, 128, 128])

    def test_multiple_airplane_one_xml(self):
        xml_file_one = """
        <annotation verified="yes">
            <folder>images</folder>
            <filename>airplane1.png</filename>
            <path>airplane1.png</path>
            <source>
                <database>Unknown</database>
            </source>
            <size>
                <width>256</width>
                <height>256</height>
                <depth>3</depth>
            </size>
            <segmented>0</segmented>
            <object>
                <name>airplane</name>
                <pose>Unspecified</pose>
                <truncated>0</truncated>
                <difficult>0</difficult>
                <bndbox>
                    <xmin>96</xmin>
                    <ymin>96</ymin>
                    <xmax>128</xmax>
                    <ymax>128</ymax>
                </bndbox>
            </object>
            <object>
                <name>airplane</name>
                <pose>Unspecified</pose>
                <truncated>0</truncated>
                <difficult>0</difficult>
                <bndbox>
                    <xmin>32</xmin>
                    <ymin>32</ymin>
                    <xmax>64</xmax>
                    <ymax>64</ymax>
                </bndbox>
            </object>
        </annotation>
        """

        xml = ET.fromstring(xml_file_one)
        with tempfile.TemporaryDirectory() as tmpdirname:
            tree = ET.ElementTree(xml)
            tree.write(tmpdirname + '/test_airplane_one.xml')
            airplane_df = xml_to_csv.xml_to_csv(tmpdirname)
            self.assertEqual(airplane_df.columns.values.tolist(),
                             ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])
            self.assertEqual(airplane_df.values.tolist()[0], ['airplane1.png', 256, 256, 'airplane', 96, 96, 128, 128])
            self.assertEqual(airplane_df.values.tolist()[1], ['airplane1.png', 256, 256, 'airplane', 32, 32, 64, 64])

    def test_one_airplane_multiple_xml(self):
        xml_file_one = """
        <annotation verified="yes">
            <folder>images</folder>
            <filename>airplane1.png</filename>
            <path>airplane1.png</path>
            <source>
                <database>Unknown</database>
            </source>
            <size>
                <width>256</width>
                <height>256</height>
                <depth>3</depth>
            </size>
            <segmented>0</segmented>
            <object>
                <name>airplane</name>
                <pose>Unspecified</pose>
                <truncated>0</truncated>
                <difficult>0</difficult>
                <bndbox>
                    <xmin>96</xmin>
                    <ymin>96</ymin>
                    <xmax>128</xmax>
                    <ymax>128</ymax>
                </bndbox>
            </object>
        </annotation>
        """
        xml_file_two = """
        <annotation verified="yes">
           <folder>images</folder>
           <filename>airplane2.png</filename>
           <path>airplane2.png</path>
           <source>
               <database>Unknown</database>
           </source>
           <size>
               <width>256</width>
               <height>256</height>
               <depth>3</depth>
           </size>
           <segmented>0</segmented>
           <object>
               <name>airplane</name>
               <pose>Unspecified</pose>
               <truncated>0</truncated>
               <difficult>0</difficult>
               <bndbox>
                   <xmin>128</xmin>
                   <ymin>128</ymin>
                   <xmax>194</xmax>
                   <ymax>194</ymax>
               </bndbox>
           </object>
        </annotation>
        """
        xml_list = [xml_file_one, xml_file_two]
        tmpdirname = tempfile.mkdtemp()
        for index, x in enumerate(xml_list):
            xml = ET.fromstring(x)
            tree = ET.ElementTree(xml)
            tree.write(tmpdirname + '/test_airplane_{}.xml'.format(index))

        airplane_df = xml_to_csv.xml_to_csv(tmpdirname)
        self.assertEqual(airplane_df.columns.values.tolist(),
                         ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])
        self.assertEqual(airplane_df.values.tolist()[0], ['airplane1.png', 256, 256, 'airplane', 96, 96, 128, 128])
        self.assertEqual(airplane_df.values.tolist()[1], ['airplane2.png', 256, 256, 'airplane', 128, 128, 194, 194])
        shutil.rmtree(tmpdirname)
