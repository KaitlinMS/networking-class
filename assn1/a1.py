"""
Usage:
python a1.py <text-file-to-test-with>

TODO add docs - design decisions and stuff
"""

class HexTrieNode(object):
    
    def __init__(self, parent, name, cache_entry):
        self.parent = parent
        self.name = name
        self.cache_entry = cache_entry
        self.children = {}

    def add_child(self, name, cache_entry):
        # TODO case where child is already added

        if not self.children:
            # I'm a leaf. Create a new child with my cache entry's info before
            # adding the one I'm supposed to add.
            cache_entry_initial = self.cache_entry[0][len(self.name)]
            self.children[cache_entry_initial] = HexTrieNode(
                    self, self.name + cache_entry_initial, self.cache_entry)
            self.cache_entry = None
        try:
            child = self.children[name[0]]
        except KeyError:
            self.children[name[0]] = HexTrieNode(
                    self, self.name + name[0], cache_entry)
            return

        child.add_child(name[1:], cache_entry)

    def remove(self):
        """
        Nodes remove themselves from the trie. This way, we can just get a
        node from its cache entry, call this method and the trie will
        fix itself
        """
        if not self.parent:
            return

        del self.parent.children[self.name[-1]]
        if not self.parent.children:
            self.parent.remove()

    def search(self, address, path):
        try:
            child = self.children[address[0]]
        except KeyError:
            if not self.cache_entry:
                # I'm not a leaf, but I have no path to the address
                # through my children. Search failed.
                return None, None

            if not self.cache_entry[0][len(self.name):] == address:
                # I'm a leaf, but my cache entry doesn't match the
                # search address. Search failed.
                return None, None

            path.append(self.name)
            return self, path

        path.append(self.name)
        return child.search(address[1:], path)


class RootHexTrieNode(HexTrieNode):

    def __init__(self):
        HexTrieNode.__init__(self, None, "Root", None)

    def add_child(self):
        raise NotImplementedError(
                "Not implemented for root node. Use add_node instead.")

    def add_node(self, cache_entry):
        name = cache_entry[0]
        try:
            child = self.children[name[0]]
        except KeyError:
            self.children[name[0]] = HexTrieNode(
                    self, name[0], cache_entry)
            return

        child.add_child(name[1:], cache_entry)

    def search(self, address):
        return HexTrieNode.search(self, address, [])

    def remove(self, address):
        node, _ = self.search(address)
        if node:
            node.remove()


class Cache(object):
    #XXX all cache stuff is untested

    def __init__(self, switch, max_size):
        self.switch = switch
        self.max_size = max_size
        self.entries = []

    def add(self, address, port):
        entry = (address, port)

        # If the entry is already in the cache, remove it
        # so we can say it's been recently used
        try:
            self.entries.remove(entry)
        except ValueError:
            pass
        self.entries.append(entry)

        if len(self.entries) > self.max_size:
            self.remove(0)
        return entry

    def remove(self, index):
        removed_entry = self.entries.pop(index)
        self.switch.trie.remove(removed_entry[0])


class Switch(object):

    def __init__(self, num_ports, cache_size):
        self.num_ports = num_ports
        self.cache = Cache(self, cache_size)
        self.trie = RootHexTrieNode()

    def run_simulation(self, packets):
        for packet in packets:
            try:
                port, src, dst = packet
                port = int(port)
            except ValueError, e:
                print "Malformatted packet %s: %s" % (packet, e)
                continue

            cache_entry = self.cache.add(src.replace(':', ''), port)
            self.trie.add_node(cache_entry)

            node, path = self.trie.search(dst.replace(':', ''))

            if node:
                dst_port = node.cache_entry[1]
                print "%s %s port %d" % (dst, ' --> '.join(path), dst_port)
            else:
                print '%s all ports except %d' % (dst, port)


def main(filepath):
    try:
        fd = open(filepath)
    except IOError, e:
        print "Error opening file:", e
        return

    try:
        num_ports = int(fd.readline())
        cache_size = int(fd.readline())
        packets = [line.split() for line in fd]
    except Exception, e:
        print "Bad file:", e
        return
    finally:
        fd.close()

    Switch(num_ports, cache_size).run_simulation(packets)


if __name__ == '__main__':
    import sys
    main(sys.argv[1])

