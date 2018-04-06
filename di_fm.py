from config import LocalConst
from xml.dom.minidom import parse
import xml.dom.minidom


class ElementNotFoundException(Exception):
    def __init__(self, element_id):
        print str(element_id)


class Channel:
    def __init__(self, channel_name, title=None, site=None, base_url=None, suffix=None,
                 small_image_url=None, large_image_url=None):
        self.name = channel_name
        self.title = title
        self.site = site
        self.baseUrl = base_url
        self.suffix = suffix
        self.small_image_url = small_image_url
        self.large_image_url = large_image_url


class DiFM:
    def __init__(self, listen_key):
        self.listenKey = listen_key
        self.channels = None


class Favourites:
    def __init__(self):
        self.DiFM = DiFM(LocalConst.LISTEN_KEY)
        self.DiFM.channels = None

    def get_channels(self):
        if self.DiFM.channels is None:
            self.DiFM.channels = self.parse_xml(LocalConst.CHANNELS_XML)
        return self.DiFM.channels

    @staticmethod
    def parse_xml(filename):
        def get_element_data(parent_element, tag):
            element = parent_element.getElementsByTagName(tag)[0]
            return element.childNodes[0].data

        def get_element_attribute(element, attribute):
            if element.hasAttribute(attribute):
                return element.getAttribute(attribute)
            return None

        def get_image_full_path(url_base, path, size):
            return "{0}{1}?size={2}".format(url_base, path, size)

        channels_dict = dict()

        dom_tree = xml.dom.minidom.parse(filename)
        root = dom_tree.documentElement
        image_url_base = get_element_attribute(root, "imageUrlBase")

        channel_classes = root.getElementsByTagName("channel_class")

        for channel_class in channel_classes:
            channel_class_site = get_element_attribute(channel_class, "site")
            channel_class_url = get_element_attribute(channel_class, "url")
            channel_class_suffix = get_element_attribute(channel_class, "suffix")

            channels = channel_class.getElementsByTagName("channel")
            for channel in channels:
                channel_name = get_element_data(channel, 'name')
                channel_title = get_element_data(channel, 'title')

                image = channel.getElementsByTagName("image")[0]  # Only one image allowed
                image_small_size = get_element_data(image, 'smallSize')
                image_large_size = get_element_data(image, 'largeSize')
                image_path = get_element_data(image, 'path')

                small_image_url = get_image_full_path(image_url_base, image_path, image_small_size)
                large_image_url = get_image_full_path(image_url_base, image_path, image_small_size)

                channel_object = Channel(channel_name=channel_name,
                                         title=channel_title,
                                         site=channel_class_site,
                                         base_url=channel_class_url,
                                         suffix=channel_class_suffix,
                                         small_image_url=small_image_url,
                                         large_image_url=large_image_url
                                         )
                channels_dict[channel_object.name] = channel_object

        return channels_dict

    def to_string(self):
        list_str = ''
        if self.DiFM.channels is None:
            raise ElementNotFoundException('No favourite channels available')

        for channel in self.DiFM.channels.keys():
            list_str += channel
            if channel == self.DiFM.channels.keys()[-2]:
                list_str += ' and '
            elif channel == self.DiFM.channels.keys()[-1]:
                break
            else:
                list_str += ', '

        return list_str
