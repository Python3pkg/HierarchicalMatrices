from utils import admissible


class BlockClusterTree(object):
    def __init__(self, left_clustertree, right_clustertree, admissible_function=admissible, level=0):
        self.sons = []
        self.left_clustertree = left_clustertree
        self.right_clustertree = right_clustertree
        self.admissible = admissible_function
        self.level = level
        for left_son in self.left_clustertree.sons:
            for right_son in self.right_clustertree.sons:
                if not self.admissible(left_son, right_son):
                    self.sons.append(BlockClusterTree(left_son, right_son, self.admissible, self.level + 1))

    def __repr__(self):
        optional_string = " with children {0!s}".format(self.sons) if self.sons else ""
        return "<BlockClusterTree at level {0}{1}>".format(str(self.level), optional_string)

    def __eq__(self, other):
        """Test for equality"""
        return (self.left_clustertree == other.left_clustertree
                and self.right_clustertree == other.right_clustertree
                and self.sons == other.sons
                and self.admissible == other.admissible
                and self.level == other.level
                )

    def depth(self, root_level=None):
        if root_level is None:
            root_level = self.level
        if not self.sons:
            return self.level - root_level
        else:
            return max([son.depth(root_level) for son in self.sons])

    def to_list(self):
        return [self, [son.to_list() for son in self.sons]]

    def draw(self):
        import matplotlib.pyplot as plt
        # set x coordinates for patch
        x = [self.left_clustertree.get_index(0), self.left_clustertree.get_index(0),
             self.left_clustertree.get_index(-1) + 1, self.left_clustertree.get_index(-1) + 1]
        # set y coordinates for patch
        y = [self.right_clustertree.get_index(0), self.right_clustertree.get_index(-1) + 1,
             self.right_clustertree.get_index(-1) + 1, self.right_clustertree.get_index(0)]
        color = 'g' if self.admissible(self.left_clustertree, self.right_clustertree) else 'r'
        plt.fill(x, y, color)

    def plot(self):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        self._plot()
        plt.show()

    def _plot(self):
        if self.sons:
            for son in self.sons:
                son._plot()
        else:
            self.draw()

    def export(self, form='xml', out_file='bct_out'):
        """Export obj in specified format.

                implemented: xml, dot, bin
                """

        def _to_xml(lst, out_string=''):
            if len(lst[1]):
                value_string = str(lst[0])
                display_string = str(len(lst[1]))
            else:
                value_string = str(lst[0])
                display_string = str(lst[0])
            out_string += '<node value="{0}">{1}\n'.format(value_string, display_string)
            if len(lst) > 1 and type(lst[1]) is list:
                for item in lst[1]:
                    out_string = _to_xml(item, out_string)
            out_string += "</node>\n"
            return out_string

        def _to_dot(lst, out_string=''):
            if len(lst) > 1 and type(lst[1]) is list:
                for item in lst[1]:
                    if type(item) is list:
                        value_string = str(lst[0])
                        item_string = str(item[0])
                        label_string = len(lst[0])
                        out_string += '''"{0}" -- "{1}";
                                "{0}"[label="{2}",color="#cccccc",style="filled",shape="box"];\n'''.format(
                            value_string, item_string, label_string)
                        out_string = _to_dot(item, out_string)
                    else:
                        value_string = str(lst[0])
                        item_string = item
                        label_string = len(eval(value_string.replace('|', ',')))
                        out_string += '''"{0}" -- "{1}";
                                "{0}"[label="{2}",color="#cccccc",style="filled",shape="box"];
                                "{1}"[color="#cccccc",style="filled",shape="box"];\n'''.format(value_string,
                                                                                               item_string,
                                                                                               label_string)
            return out_string

        if form == 'xml':
            export_list = self.to_list()
            head = '<?xml version="1.0" encoding="utf-8"?>\n'
            output = _to_xml(export_list)
            output = head + output
            with open(out_file, "w") as out:
                out.write(output)
        elif form == 'dot':
            export_list = self.to_list()
            head = 'graph {\n'
            output = _to_dot(export_list)
            tail = '}'
            output = head + output + tail
            with open(out_file, "w") as out:
                out.write(output)
        elif form == 'bin':
            import pickle
            file_handle = open(out_file, "wb")
            pickle.dump(self, file_handle, protocol=-1)
            file_handle.close()
        else:
            raise NotImplementedError()
