class MinHeap:
    def __init__(self):
        """初始化一个空的最小堆。"""
        self.heap = []

    def parent(self, index):
        """获取给定索引的父节点索引。"""
        return (index - 1) // 2

    def left_child(self, index):
        """获取给定索引的左子节点索引。"""
        return 2 * index + 1

    def right_child(self, index):
        """获取给定索引的右子节点索引。"""
        return 2 * index + 2

    def insert(self, node):
        """向堆中插入一个新节点，并调用_heapify_up来维护堆的性质。"""
        self.heap.append(node)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        """移除并返回堆中的最小元素（根节点），然后调用_heapify_down来维护堆的性质。"""
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, index):
        """从给定索引开始，通过交换节点与其父节点来维护堆的性质（最小堆）。"""
        while index != 0 and self.heap[self.parent(index)].freq > self.heap[index].freq:
            self.heap[index], self.heap[self.parent(index)] = self.heap[self.parent(index)], self.heap[index]
            index = self.parent(index)

    def _heapify_down(self, index):
        """从给定索引开始，通过交换节点与其子节点中的较小者来维护堆的性质（最小堆）。"""
        smallest = index
        left = self.left_child(index)
        right = self.right_child(index)

        if left < len(self.heap) and self.heap[left].freq < self.heap[smallest].freq:
            smallest = left

        if right < len(self.heap) and self.heap[right].freq < self.heap[smallest].freq:
            smallest = right

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def is_empty(self):
        """检查堆是否为空。"""
        return len(self.heap) == 0

    def size(self):
        """返回堆中节点的数量。"""
        return len(self.heap)

class Node:
    def __init__(self, char, freq):
        """初始化一个节点，包括字符、频率、左子节点和右子节点。"""
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        """定义节点间的比较操作，基于频率。"""
        return self.freq < other.freq
    
def build_huffman_tree(text):
    """根据给定文本构建Huffman树。"""
    # 统计字符频次
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    # 创建优先队列（最小堆）
    min_heap = MinHeap()
    for char, freq in frequency.items():
        min_heap.insert(Node(char, freq))

    # 构建Huffman树
    while min_heap.size() > 1:
        left = min_heap.extract_min()
        right = min_heap.extract_min()
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        min_heap.insert(merged)

    return min_heap.extract_min()

def generate_huffman_codes(node, prefix="", codebook={}):
    """根据Huffman树生成Huffman编码表。"""
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_encoding(text):
    """对给定文本进行Huffman编码。"""
    root = build_huffman_tree(text)
    huffman_codes = generate_huffman_codes(root)
    encoded_text = ''.join(huffman_codes[char] for char in text)
    return huffman_codes, encoded_text

def huffman_decoding(encoded_text, root):
    """对给定的Huffman编码文本进行解码。"""
    decoded_output = []
    current_node = root

    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.left is None and current_node.right is None:
            decoded_output.append(current_node.char)
            current_node = root

    return ''.join(decoded_output)

if __name__ == "__main__":
    text = input("Please enter the text to encode: ")
    huffman_codes, encoded_text = huffman_encoding(text)
    print("Huffman Codes:", huffman_codes)
    print("Encoded Text:", encoded_text)
    decoded_text = huffman_decoding(encoded_text, build_huffman_tree(text))
    print("Decoded Text:", decoded_text)