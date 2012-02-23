"""
Usage:
python a1.py <text-file-to-test-with>

************************************************************
SFWR ENG 4C03 - Assignment 1
Authors:
Cameron Sapp		   - 0768086
Kaitlin Smith		   - 0645771
Manivanna Thevathasan - 0754015
************************************************************
"""

import re

class HexTrieNode(object):
	
	def __init__(self, parent, name, cache_entry):
		self.parent = parent
		self.name = name
		self.cache_entry = cache_entry
		self.children = {}

	def add_child(self, name, cache_entry):
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

		if self.children:
			# We shouldn't ever need to remove non-leaf nodes
			return

		del self.parent.children[self.name[-1]]
		if not self.parent.children:
			self.parent.remove()

	def search(self, address, path):
		try:
			child = self.children[address[0]]
		except (KeyError, IndexError):
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


class HexTrie(object):

	def __init__(self):
		self.root = HexTrieNode(None, "Root", None)

	def add_node(self, cache_entry):
		name = cache_entry[0]
		try:
			child = self.root.children[name[0]]
		except KeyError:
			self.root.children[name[0]] = HexTrieNode(
					self.root, name[0], cache_entry)
			return
	
		child.add_child(name[1:], cache_entry)

	def search(self, address):
		return self.root.search(address, [])

	def remove(self, address):
		node, _ = self.search(address)
		if node:
			node.remove()


class Cache(object):

	def __init__(self, switch, max_size):
		self.switch = switch
		self.max_size = max_size
		self.entries = []

	def add(self, address, port):
		
		entry = (address, port)
		
		try:
			for cacheEntry in self.entries[:]:
				#If source addresses are equal then remove 
				#the entry in the cache and HexTrie
				if entry[0] == cacheEntry[0]:
					self.entries.remove(cacheEntry)
					self.switch.trie.remove(cacheEntry[0])
		except:
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
		self.trie = HexTrie()

	def run_simulation(self, packets):
		for packet in packets:
			try:
				port, src, dst = packet
				port = int(port)
			except ValueError, e:
				print "Malformatted packet %s: %s" % (packet, e)
				continue
		
			if self.num_ports < port:
				print "Error: Packet received from port %s which is outside the scope of ports %s." %(port, self.num_ports)
				continue
			
			if not re.search('([a-fA-F0-9]{2}[:-]?){6}', src):
				print "Error: Source MAC Address is not formatted correctly."
				continue 
				
			if not re.search('([a-fA-F0-9]{2}[:-]?){6}', dst):
				print "Error: Destination MAC Address is not formatted correctly."
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
	
	if not packets:
		print "Error: No packets were specified."
	
	if cache_size <= 0:
		print "Error: Cache size must be a positive non-zero integer value."
		return
	
	Switch(num_ports, cache_size).run_simulation(packets)


if __name__ == '__main__':
	import sys
	main(sys.argv[1])

